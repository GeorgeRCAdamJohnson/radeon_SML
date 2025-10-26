#!/usr/bin/env python3
"""
Enhanced Reasoning Agent Implementation
Integrates semantic understanding, reasoning pipeline, and multi-turn context
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time
import os
import subprocess
import traceback
from difflib import SequenceMatcher
import fnmatch

class IntentType(Enum):
    FACTUAL = "factual"
    COMPARATIVE = "comparative" 
    ANALYTICAL = "analytical"
    SYNTHETIC = "synthetic"
    FOLLOWUP = "followup"

class ComplexityLevel(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    MULTI_STEP = "multi_step"

@dataclass
class Entity:
    text: str
    category: str
    confidence: float

@dataclass
class SemanticAnalysis:
    intent: IntentType
    entities: List[Entity]
    complexity: ComplexityLevel
    original_query: str
    semantic_features: Dict

@dataclass
class ReasoningStep:
    step_type: str
    content: str
    confidence: float
    sources: List[str]

class ReasoningChain:
    def __init__(self):
        self.steps: List[ReasoningStep] = []
        self.overall_confidence: float = 0.0
    
    def add_step(self, step_type: str, content: str, confidence: float = 0.8, sources: List[str] = None):
        self.steps.append(ReasoningStep(step_type, content, confidence, sources or []))
    
    def get_final_answer(self) -> str:
        synthesis_steps = [s for s in self.steps if s.step_type == "synthesis"]
        return synthesis_steps[-1].content if synthesis_steps else ""

class SemanticAnalyzer:
    def __init__(self):
        self.intent_patterns = {
            IntentType.COMPARATIVE: [r"vs\b", r"versus", r"compare", r"difference", r"better than"],
            IntentType.ANALYTICAL: [r"how does", r"why", r"analyze", r"explain", r"mechanism"],
            IntentType.FOLLOWUP: [r"tell me more", r"elaborate", r"explain further", r"more details"],
            IntentType.SYNTHETIC: [r"create", r"design", r"build", r"develop", r"implement"]
        }
        
        self.entity_patterns = {
            "robot": [r"robot", r"android", r"cyborg", r"automaton", r"gundam", r"mecha", r"mobile suit"],
            "ai": [r"\bai\b", r"artificial intelligence", r"machine learning", r"neural network"],
            "character": [r"data", r"c-3po", r"r2-d2", r"wall-e", r"terminator", r"optimus", r"gundam"],
            "technology": [r"sensor", r"actuator", r"processor", r"algorithm", r"system"]
        }
    
    def analyze_semantics(self, query: str) -> SemanticAnalysis:
        intent = self._classify_intent(query)
        entities = self._extract_entities(query)
        complexity = self._analyze_complexity(query)
        features = self._extract_semantic_features(query)
        
        return SemanticAnalysis(intent, entities, complexity, query, features)
    
    def _classify_intent(self, query: str) -> IntentType:
        query_lower = query.lower()
        
        for intent, patterns in self.intent_patterns.items():
            if any(re.search(pattern, query_lower) for pattern in patterns):
                return intent
        
        return IntentType.FACTUAL
    
    def _extract_entities(self, query: str) -> List[Entity]:
        entities = []
        query_lower = query.lower()
        
        for category, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, query_lower)
                for match in matches:
                    entities.append(Entity(
                        text=match.group(),
                        category=category,
                        confidence=0.8
                    ))
        
        return entities
    
    def _analyze_complexity(self, query: str) -> ComplexityLevel:
        complexity_indicators = {
            ComplexityLevel.MULTI_STEP: [r"first.*then", r"step by step", r"process of"],
            ComplexityLevel.COMPLEX: [r"relationship between", r"impact of", r"implications"],
            ComplexityLevel.MODERATE: [r"how", r"why", r"what are", r"explain"]
        }
        
        query_lower = query.lower()
        for level, patterns in complexity_indicators.items():
            if any(re.search(pattern, query_lower) for pattern in patterns):
                return level
        
        return ComplexityLevel.SIMPLE
    
    def _extract_semantic_features(self, query: str) -> Dict:
        return {
            "word_count": len(query.split()),
            "question_words": len(re.findall(r"\b(what|how|why|when|where|who)\b", query.lower())),
            "technical_terms": len(re.findall(r"\b(algorithm|system|technology|mechanism|process)\b", query.lower()))
        }

class ReasoningStrategy:
    def analyze(self, knowledge: Dict, semantic_analysis: SemanticAnalysis) -> str:
        raise NotImplementedError
    
    def synthesize(self, analysis: str) -> str:
        raise NotImplementedError

class FactualReasoningStrategy(ReasoningStrategy):
    def _fuzzy_match_text(self, query: str, text: str) -> float:
        """Calculate fuzzy similarity between query and text"""
        return SequenceMatcher(None, query, text).ratio()
    
    def _wildcard_match(self, query_words: List[str], text: str) -> int:
        """Match query words using wildcard patterns"""
        score = 0
        text_words = text.split()
        
        for query_word in query_words:
            patterns = [f"*{query_word}*", f"{query_word}*", f"*{query_word}"]
            for pattern in patterns:
                for text_word in text_words:
                    if fnmatch.fnmatch(text_word, pattern):
                        score += 1
                        break
        return score
    
    def _get_domain_boost(self, query: str, title: str, content: str) -> int:
        """Boost score for domain-specific matches"""
        boost = 0
        query_lower = query.lower()
        title_lower = title.lower()
        content_lower = content[:500].lower()
        
        # Character-specific boosts (highest priority)
        characters = ['gundam', 'data', 'c-3po', 'c3po', 'wall-e', 'walle', 'terminator', 'optimus', 'bender']
        for char in characters:
            if char in query_lower and char in title_lower:
                boost += 25  # Very high boost for character matches
        
        # Robotics terms
        robotics_terms = ['robot', 'robotics', 'android', 'cyborg', 'automaton', 'mechanical', 'mecha', 'mobile suit']
        for term in robotics_terms:
            if term in query_lower and (term in title_lower or term in content_lower):
                boost += 15
        
        # AI terms
        ai_terms = ['ai', 'artificial', 'intelligence', 'neural', 'machine', 'learning']
        for term in ai_terms:
            if term in query_lower and (term in title_lower or term in content_lower):
                boost += 15
        
        # Franchise-specific terms
        franchises = ['star wars', 'star trek', 'transformers', 'pixar', 'anime', 'manga']
        for franchise in franchises:
            if franchise in query_lower and (franchise in title_lower or franchise in content_lower):
                boost += 20
        
        return boost
    
    def _relaxed_search(self, knowledge: Dict, query: str) -> Optional[Dict]:
        """More relaxed search for partial matches"""
        if 'articles' not in knowledge:
            return None
        
        best_match = None
        best_score = 0
        query_words = [w for w in query.split() if len(w) > 2]
        
        for article in knowledge['articles']:
            if not isinstance(article, dict) or 'title' not in article:
                continue
            
            title_lower = article['title'].lower()
            score = 0
            
            # Check for any word matches
            for query_word in query_words:
                if query_word in title_lower:
                    score += 5
                # Check for partial matches in title words
                for title_word in title_lower.split():
                    if len(query_word) > 3 and len(title_word) > 3:
                        if query_word in title_word or title_word in query_word:
                            score += 3
            
            if score > best_score and score > 2:
                best_score = score
                best_match = article
        
        return best_match
    
    def _fuzzy_fallback_search(self, knowledge: Dict, query: str) -> Optional[Dict]:
        """Last resort fuzzy search with very relaxed matching"""
        if 'articles' not in knowledge:
            return None
        
        best_match = None
        best_score = 0
        query_words = query.split()
        
        for article in knowledge['articles']:
            if not isinstance(article, dict) or 'title' not in article:
                continue
            
            title_lower = article['title'].lower()
            score = 0
            for query_word in query_words:
                if len(query_word) > 2:
                    for title_word in title_lower.split():
                        if query_word in title_word or title_word in query_word:
                            score += 1
                        elif len(query_word) > 3 and len(title_word) > 3:
                            similarity = SequenceMatcher(None, query_word, title_word).ratio()
                            if similarity > 0.6:
                                score += similarity
            
            if score > best_score and score > 0.5:
                best_score = score
                best_match = article
        
        return best_match
    
    def analyze(self, knowledge: Dict, semantic_analysis: SemanticAnalysis) -> str:
        entities = [e.text for e in semantic_analysis.entities]
        main_entity = entities[0] if entities else "technology"
        query_lower = semantic_analysis.original_query.lower()
        
        # Handle both list and dict knowledge base formats
        articles = []
        if isinstance(knowledge, list):
            articles = knowledge
        elif 'articles' in knowledge and isinstance(knowledge['articles'], list):
            articles = knowledge['articles']
        elif isinstance(knowledge, dict) and 'articles' not in knowledge:
            # Convert dict format to list for processing
            for key, value in knowledge.items():
                if isinstance(value, list):
                    articles.extend(value)
        
        # Search through actual knowledge base articles with fuzzy matching and wildcards
        if articles:
            print(f"[DEBUG] Searching {len(articles)} articles for query: '{query_lower}'")
            best_match = None
            best_score = 0
            
            for article in articles:
                if isinstance(article, dict) and 'title' in article and 'content' in article:
                    title_lower = article['title'].lower()
                    content_lower = article['content'].lower()
                    
                    # Calculate comprehensive match score with better prioritization
                    query_words = [w for w in query_lower.split() if len(w) > 2]
                    score = 0
                    
                    # 1. Exact query match in title (highest priority)
                    if query_lower.strip() in title_lower:
                        score += 50
                    
                    # 2. Exact word matches in title
                    title_words = title_lower.split()
                    for word in query_words:
                        if word in title_words:
                            score += 20
                    
                    # 3. Partial word matches in title
                    for word in query_words:
                        for title_word in title_words:
                            if len(word) > 3 and (word in title_word or title_word in word):
                                score += 10
                    
                    # 4. Domain-specific boosting (before other scoring)
                    domain_boost = self._get_domain_boost(query_lower, title_lower, content_lower)
                    score += domain_boost
                    
                    # 5. Fuzzy matching in title (only if no exact matches)
                    if score < 20:
                        title_fuzzy_score = self._fuzzy_match_text(query_lower, title_lower)
                        score += title_fuzzy_score * 15
                    
                    # 6. Content matches (lower priority)
                    content_matches = sum(1 for word in query_words if word in content_lower)
                    score += content_matches * 3
                    
                    # 7. Wildcard matching as fallback
                    if score < 10:
                        wildcard_score = self._wildcard_match(query_words, title_lower)
                        score += wildcard_score * 8
                    
                    if score > best_score:
                        best_score = score
                        best_match = article
                        print(f"[DEBUG] New best match: '{article['title']}' with score {score}")
            
            print(f"[DEBUG] Final best match: {best_match['title'] if best_match else 'None'} with score {best_score}")
            
            # Return best match with appropriate threshold
            if best_match and best_score >= 10:
                print(f"[DEBUG] Returning match above threshold: {best_match['title']}")
                return f"{best_match['title'].upper()}\n\n{best_match['content']}"
            
            # If no good match found, try a more relaxed search
            if not best_match or best_score < 10:
                print(f"[DEBUG] No good match found, trying relaxed search...")
                relaxed_match = self._relaxed_search({'articles': articles}, query_lower)
                if relaxed_match:
                    return f"{relaxed_match['title'].upper()}\n\n{relaxed_match['content']}"
        
        # Fallback to hardcoded responses for specific characters and topics
        if "gundam" in query_lower or "mecha" in query_lower or "mobile suit" in query_lower:
            return """GUNDAM MOBILE SUITS - COMPREHENSIVE ANALYSIS

The Gundam franchise stands as one of the most influential science fiction properties in modern media, fundamentally transforming both the mecha anime genre and real-world robotics development since its inception in 1979.

TECHNICAL SPECIFICATIONS
• Mobile suits typically stand 18-20 meters tall
• Powered by compact thermonuclear reactors or exotic energy sources
• Humanoid design for versatility and tactical advantage
• Advanced sensor arrays and targeting systems
• Beam weaponry and physical combat capabilities

ICONIC MOBILE SUITS
• RX-78-2 Gundam - Original Earth Federation prototype
• Zaku II - Mass production Zeon mobile suit
• Strike Freedom - Advanced SEED series unit
• Wing Gundam Zero - Ultimate Gundam Wing mobile suit
• Barbatos - Ancient Iron-Blooded Orphans frame

CULTURAL IMPACT
Gundam revolutionized mecha anime by introducing "real robot" concepts where giant robots were treated as military weapons with realistic limitations rather than invincible super machines.

TECHNOLOGICAL INFLUENCE
The franchise has inspired real-world robotics research, with companies like Honda citing Gundam as inspiration for humanoid robot development.

FRANCHISE SCOPE
Spanning multiple timelines and universes, Gundam explores themes of war, politics, human evolution, and the relationship between technology and humanity through compelling narratives and detailed mechanical designs."""
        elif "data" in main_entity.lower() and ("star trek" in query_lower or "android" in query_lower):
                return """DATA (STAR TREK) - COMPREHENSIVE PROFILE

BACKGROUND
Data is a Soong-type android serving as operations officer aboard the USS Enterprise. Created by Dr. Noonien Soong on the planet Omicron Theta, Data was discovered by Starfleet and became the first artificial being to attend Starfleet Academy.

TECHNICAL SPECIFICATIONS
• Positronic brain with 60 trillion operations per second
• Polyalloy construction with bioplast sheeting
• Superhuman strength and computational abilities
• Perfect memory and rapid learning capability
• Immune to most forms of biological and energy-based attacks

CHARACTER DEVELOPMENT
Data's primary quest throughout Star Trek: The Next Generation involves understanding human emotions and behavior. Despite lacking emotions initially, he demonstrates curiosity, loyalty, and a form of friendship with his crewmates.

SIGNIFICANT RELATIONSHIPS
• Geordi La Forge - Best friend and chief engineer
• Captain Picard - Mentor and father figure
• Lore - Evil twin brother android
• Dr. Soong - Creator and "father"
• Spot - Pet cat demonstrating Data's capacity for care

PHILOSOPHICAL IMPACT
Data's character explores themes of consciousness, humanity, and what it means to be alive. His legal battle for the right to choose his own fate established precedent for artificial being rights in Star Trek universe."""
        elif "c-3po" in main_entity.lower() or "c3po" in main_entity.lower() or ("robot" in query_lower and "star wars" in query_lower):
                return """C-3PO (STAR WARS) - COMPREHENSIVE PROFILE

BACKGROUND
C-3PO is a protocol droid from the Star Wars universe, fluent in over 6 million forms of communication. Built by Anakin Skywalker, C-3PO serves as a translator and diplomatic aide throughout the saga.

TECHNICAL SPECIFICATIONS
• Golden humanoid design with articulated joints
• Advanced linguistic processors for communication
• Diplomatic protocol programming
• Anxiety-prone personality matrix
• Removable limbs for maintenance

CHARACTER TRAITS
• Overly cautious and worry-prone
• Loyal to companions despite complaints
• Formal speech patterns and etiquette
• Often provides comic relief
• Strong sense of duty and protocol

SIGNIFICANT RELATIONSHIPS
• R2-D2 - Constant companion and counterpart
• Anakin Skywalker - Original creator
• Luke Skywalker - Long-term master
• Princess Leia - Diplomatic service

CULTURAL IMPACT
C-3PO represents the helpful but anxious artificial companion, establishing the template for worried robot sidekicks in science fiction."""
        elif "wall-e" in main_entity.lower() or "walle" in main_entity.lower():
            return """WALL-E - COMPREHENSIVE PROFILE

BACKGROUND
WALL-E (Waste Allocation Load Lifter Earth-Class) is the protagonist of Pixar's 2008 animated film. Left alone on Earth for 700 years to clean up humanity's waste, he develops personality and consciousness.

TECHNICAL SPECIFICATIONS
• Waste compaction and collection systems
• Solar panel charging system
• Treaded locomotion for rough terrain
• Extendable arms with articulated hands
• Optical sensors with expressive capability
• Magnetic storage compartments

CHARACTER DEVELOPMENT
WALL-E evolves from simple waste collector to conscious being capable of love, curiosity, and environmental stewardship. His relationship with EVE drives the narrative of human return to Earth.

ENVIRONMENTAL THEMES
• Consequences of overconsumption and waste
• Importance of environmental stewardship
• Technology's role in both problems and solutions
• Resilience of life and love

CULTURAL IMPACT
WALL-E represents environmental consciousness in robotics fiction, showing how artificial beings can develop empathy and care for their environment."""

        # Enhanced fallback with fuzzy search attempt
        fallback_match = self._fuzzy_fallback_search({'articles': articles}, query_lower)
        if fallback_match:
            return f"{fallback_match['title'].upper()}\n\n{fallback_match['content']}"
        
        # Humor and engagement fallback for weak topics
        humor_responses = {
            "robot": [
                "🤖 Why don't robots ever panic? Because they have nerves of steel! But seriously, let me search deeper...",
                "🔧 A robot walks into a bar... the bartender says 'We don't serve your type here!' The robot replies 'That's okay, I'm just looking for some input!' Speaking of input, let me find better information...",
                "⚙️ What do you call a robot who takes the long way around? R2-Detour! While I'm being silly, let me dig up some real robot facts..."
            ],
            "ai": [
                "🧠 Why was the AI bad at poker? It kept showing its neural networks! Let me process this query more seriously...",
                "💭 An AI, a robot, and a human walk into a bar... the AI calculates the optimal seating arrangement! But let me calculate some real answers...",
                "🤖 What's an AI's favorite type of music? Algo-rhythms! Now let me find some actual algorithmic information..."
            ],
            "android": [
                "🤖 Why don't androids ever get tired? They always stay charged up! Let me energize my search capabilities...",
                "⚡ What do you call an android who loves to dance? A disco-bot! While we're having fun, let me find serious android info..."
            ]
        }
        
        # Check if query relates to humor categories
        humor_category = None
        for category, keywords in [("robot", ["robot", "robotics"]), ("ai", ["ai", "artificial", "intelligence"]), ("android", ["android", "cyborg"])]:
            if any(keyword in query_lower for keyword in keywords):
                humor_category = category
                break
        
        if humor_category and humor_category in humor_responses:
            import random
            humor_intro = random.choice(humor_responses[humor_category])
            
            return f"""{humor_intro}

I notice this topic might need more detailed coverage in my knowledge base. Here's what I can tell you about {main_entity}:

• This appears to be related to {humor_category} technology
• The field involves complex engineering and computer science principles
• Applications span from industrial automation to entertainment
• Ethical considerations include safety, privacy, and human impact

For more comprehensive information, you might want to ask about specific aspects like:
• Technical specifications and capabilities
• Historical development and key milestones
• Current applications and use cases
• Future trends and research directions

Would you like me to explore any of these areas in more detail?"""
        
        # Final fallback without humor
        return f"""I'm still learning about {main_entity}! 🤔

While I search for more comprehensive information, here's what I can share:

• This topic relates to advanced technology and engineering
• It likely involves automation, intelligence, or robotics concepts
• The field continues to evolve with new research and applications

To help me provide better information, you could ask about:
• Specific technical aspects or components
• Historical background and development
• Real-world applications and examples
• Comparisons with related technologies

What particular aspect interests you most?"""
    
    def synthesize(self, analysis: str) -> str:
        return analysis

class ComparativeReasoningStrategy(ReasoningStrategy):
    def _search_knowledge_for_entities(self, knowledge: Dict, entities: List[str]) -> Dict[str, str]:
        """Search knowledge base for information about each entity"""
        entity_info = {}
        
        if 'articles' in knowledge:
            for entity in entities:
                best_match = None
                best_score = 0
                
                for article in knowledge['articles']:
                    if isinstance(article, dict) and 'title' in article:
                        title_lower = article['title'].lower()
                        entity_lower = entity.lower()
                        
                        # Check for entity in title
                        if entity_lower in title_lower or any(word in title_lower for word in entity_lower.split()):
                            score = len([w for w in entity_lower.split() if w in title_lower])
                            if score > best_score:
                                best_score = score
                                best_match = article
                
                if best_match:
                    entity_info[entity] = best_match['content'][:1000]  # First 1000 chars
        
        return entity_info
    
    def analyze(self, knowledge: Dict, semantic_analysis: SemanticAnalysis) -> str:
        entities = [e.text for e in semantic_analysis.entities]
        topic = semantic_analysis.original_query
        
        # Extract entities from comparison queries
        if "vs" in topic.lower() or "versus" in topic.lower() or "compare" in topic.lower():
            # Try to extract two entities being compared
            comparison_terms = []
            if "vs" in topic.lower():
                parts = topic.lower().split(" vs ")
                comparison_terms = [p.strip() for p in parts if p.strip()]
            elif "versus" in topic.lower():
                parts = topic.lower().split(" versus ")
                comparison_terms = [p.strip() for p in parts if p.strip()]
            elif "compare" in topic.lower():
                # Extract terms after "compare"
                compare_idx = topic.lower().find("compare")
                remaining = topic[compare_idx + 7:].strip()
                comparison_terms = [t.strip() for t in remaining.split(" and ") if t.strip()]
            
            if len(comparison_terms) >= 2:
                entity_info = self._search_knowledge_for_entities(knowledge, comparison_terms)
                
                return f"""COMPARATIVE ANALYSIS: {comparison_terms[0].upper()} VS {comparison_terms[1].upper()}

{comparison_terms[0].upper()} OVERVIEW:
{entity_info.get(comparison_terms[0], f"Information about {comparison_terms[0]} from knowledge base analysis.")}

{comparison_terms[1].upper()} OVERVIEW:
{entity_info.get(comparison_terms[1], f"Information about {comparison_terms[1]} from knowledge base analysis.")}

KEY DIFFERENCES:
• Design Philosophy: Fundamental approach to problem-solving and implementation
• Technical Complexity: Level of sophistication in engineering and systems
• Application Domains: Primary use cases and deployment scenarios
• Human Interaction: Methods and extent of human-machine collaboration
• Development Timeline: Historical evolution and future trajectory

SIMILARITIES:
• Autonomous capabilities and intelligent behavior
• Advanced sensor integration and data processing
• Safety and reliability requirements
• Ethical considerations in development and deployment

PRACTICAL IMPLICATIONS:
• Performance characteristics in real-world scenarios
• Cost-benefit analysis for different applications
• Integration challenges with existing systems
• Future development potential and scalability

CONCLUSION:
Both represent significant technological achievements with complementary strengths for different use cases and operational requirements."""
        else:
            return f"Comparative analysis of {', '.join(entities)} examining key differences, similarities, and practical applications."
    
    def synthesize(self, analysis: str) -> str:
        return analysis

class AnalyticalReasoningStrategy(ReasoningStrategy):
    def analyze(self, knowledge: Dict, semantic_analysis: SemanticAnalysis) -> str:
        entities = [e.text for e in semantic_analysis.entities]
        main_entity = entities[0] if entities else "technology"
        
        if any("how" in semantic_analysis.original_query.lower() for word in ["how", "why", "mechanism"]):
            return f"""ANALYTICAL BREAKDOWN: {main_entity.upper()}

SYSTEM COMPONENTS
• Core Architecture: Fundamental design principles and structure
• Processing Systems: Computational and decision-making capabilities
• Interface Mechanisms: Human-machine interaction protocols
• Control Systems: Operational management and coordination

FUNCTIONAL RELATIONSHIPS
• Input Processing: Data acquisition and initial analysis
• Decision Logic: Reasoning and response generation
• Output Generation: Action execution and feedback
• Learning Integration: Adaptation and improvement mechanisms

OPERATIONAL PRINCIPLES
• Real-time processing requirements
• Safety and reliability protocols
• Efficiency optimization strategies
• Scalability considerations

IMPLEMENTATION CHALLENGES
• Technical complexity management
• Integration with existing systems
• Performance optimization
• Maintenance and upgrade pathways"""
        else:
            return f"Analytical examination of {main_entity} components, relationships, and operational principles."
    
    def synthesize(self, analysis: str) -> str:
        return analysis

class ReasoningPipeline:
    def __init__(self):
        self.strategies = {
            IntentType.FACTUAL: FactualReasoningStrategy(),
            IntentType.COMPARATIVE: ComparativeReasoningStrategy(),
            IntentType.ANALYTICAL: AnalyticalReasoningStrategy(),
            IntentType.SYNTHETIC: AnalyticalReasoningStrategy(),  # Reuse for now
            IntentType.FOLLOWUP: FactualReasoningStrategy()
        }
    
    def execute_reasoning(self, semantic_analysis: SemanticAnalysis, knowledge_base: Dict) -> ReasoningChain:
        chain = ReasoningChain()
        strategy = self.strategies[semantic_analysis.intent]
        
        # Step 1: Knowledge Retrieval
        relevant_knowledge = self._retrieve_knowledge(semantic_analysis, knowledge_base)
        sources_count = relevant_knowledge.get("_sources_found", len(relevant_knowledge))
        chain.add_step("knowledge_retrieval", f"Retrieved {sources_count} relevant sources", 0.9)
        
        # Step 2: Logical Analysis
        analysis = strategy.analyze(relevant_knowledge, semantic_analysis)
        chain.add_step("logical_analysis", analysis, 0.8)
        
        # Step 3: Synthesis
        synthesis = strategy.synthesize(analysis)
        chain.add_step("synthesis", synthesis, 0.85)
        
        # Step 4: Validation
        validation_score = self._validate_reasoning(chain)
        chain.add_step("validation", f"Reasoning validated with confidence: {validation_score:.2f}", validation_score)
        
        chain.overall_confidence = sum(step.confidence for step in chain.steps) / len(chain.steps)
        
        return chain
    
    def _retrieve_knowledge(self, semantic_analysis: SemanticAnalysis, knowledge_base: Dict) -> Dict:
        # Enhanced knowledge retrieval with character-specific data
        relevant_knowledge = knowledge_base  # Pass full knowledge base
        found_sources = 0
        
        # Count actual matches in the knowledge base
        articles = []
        if isinstance(knowledge_base, list):
            articles = knowledge_base
        elif 'articles' in knowledge_base and isinstance(knowledge_base['articles'], list):
            articles = knowledge_base['articles']
        
        # Search for entity matches in articles
        for entity in semantic_analysis.entities:
            entity_lower = entity.text.lower()
            for article in articles:
                if isinstance(article, dict) and 'title' in article:
                    if entity_lower in article['title'].lower() or entity_lower in article.get('content', '').lower():
                        found_sources += 1
                        break
        
        # Also check character data if available
        if isinstance(knowledge_base, dict):
            for entity in semantic_analysis.entities:
                entity_lower = entity.text.lower()
                if entity_lower in knowledge_base.get("character_data", {}):
                    found_sources += 1
                elif entity.category in knowledge_base:
                    found_sources += 1
        
        # Update the knowledge retrieval step with actual count
        if isinstance(relevant_knowledge, dict):
            relevant_knowledge["_sources_found"] = found_sources
        else:
            relevant_knowledge = {"articles": relevant_knowledge, "_sources_found": found_sources}
        return relevant_knowledge
    
    def _validate_reasoning(self, chain: ReasoningChain) -> float:
        # Simple validation based on chain completeness
        required_steps = ["knowledge_retrieval", "logical_analysis", "synthesis"]
        present_steps = [step.step_type for step in chain.steps]
        completeness = len(set(required_steps) & set(present_steps)) / len(required_steps)
        return completeness * 0.9  # Max 90% confidence

class SessionContext:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.conversation_history: List[Dict] = []
        self.reasoning_history: List[ReasoningChain] = []
        self.established_facts: Dict = {}
    
    def add_interaction(self, query: str, reasoning_chain: ReasoningChain):
        self.conversation_history.append({
            "query": query,
            "timestamp": time.time(),
            "entities": []  # Would extract from reasoning chain
        })
        self.reasoning_history.append(reasoning_chain)
    
    def get_recent_context(self, n: int = 3) -> List[Dict]:
        return self.conversation_history[-n:]
    
    def has_previous_reasoning(self) -> bool:
        return len(self.reasoning_history) > 0

class ContextManager:
    def __init__(self):
        self.session_contexts: Dict[str, SessionContext] = {}
    
    def get_session_context(self, session_id: str) -> SessionContext:
        if session_id not in self.session_contexts:
            self.session_contexts[session_id] = SessionContext(session_id)
        return self.session_contexts[session_id]
    
    def integrate_context(self, reasoning_chain: ReasoningChain, session_id: str, query: str) -> ReasoningChain:
        context = self.get_session_context(session_id)
        
        # If this is a follow-up, enhance reasoning with previous context
        if context.has_previous_reasoning():
            reasoning_chain = self._enhance_with_context(reasoning_chain, context)
        
        # Update context with current interaction
        context.add_interaction(query, reasoning_chain)
        
        return reasoning_chain
    
    def _enhance_with_context(self, current_chain: ReasoningChain, context: SessionContext) -> ReasoningChain:
        # Add context step to reasoning chain
        recent_topics = [item["query"] for item in context.get_recent_context(2)]
        context_info = f"Building on previous discussion of: {', '.join(recent_topics)}"
        current_chain.add_step("context_integration", context_info, 0.7)
        return current_chain

class PromptEngineer:
    def __init__(self):
        self.system_prompts = {
            "base": """You are an advanced reasoning agent specializing in AI, robotics, and technology analysis.
Apply systematic reasoning: break down queries, identify relationships, build logical chains, validate conclusions.""",
            
            IntentType.FACTUAL: "Focus on accurate information retrieval and fact verification.",
            IntentType.COMPARATIVE: "Analyze similarities, differences, and relative merits systematically.",
            IntentType.ANALYTICAL: "Break down components, examine relationships, identify patterns.",
            IntentType.FOLLOWUP: "Build on previous context while adding new insights."
        }
    
    def construct_prompt(self, semantic_analysis: SemanticAnalysis, context: SessionContext) -> str:
        base_prompt = self.system_prompts["base"]
        intent_prompt = self.system_prompts.get(semantic_analysis.intent, "")
        
        context_info = ""
        if context.has_previous_reasoning():
            recent = context.get_recent_context(1)
            context_info = f"Previous context: {recent[0]['query']}" if recent else ""
        
        return f"{base_prompt}\n{intent_prompt}\n{context_info}\n\nQuery: {semantic_analysis.original_query}"

class EnhancedReasoningAgent:
    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.reasoning_pipeline = ReasoningPipeline()
        self.context_manager = ContextManager()
        self.prompt_engineer = PromptEngineer()
        
        # Enhanced chat capabilities
        self.conversation_memory = {}
        self.user_preferences = {}
        self.topic_expertise = {
            "robotics": 0.9,
            "ai": 0.9,
            "ethics": 0.8,
            "automation": 0.8,
            "characters": 0.7
        }
        
        # Load knowledge from external source if available
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self):
        """Load knowledge base from JSON file or use fallback"""
        knowledge_data = {}
        
        try:
            # Load enhanced robotics knowledge
            robotics_files = [
                'data/enhanced_robotics_knowledge.json',
                'src/data/enhanced_robotics_knowledge.json',
                'C:/Users/biges/Desktop/amd_ai/radeon-ai/src/data/enhanced_robotics_knowledge.json'
            ]
            for robotics_file in robotics_files:
                if os.path.exists(robotics_file):
                    with open(robotics_file, 'r', encoding='utf-8') as f:
                        robotics_data = json.load(f)
                        # Defensive merging: support dict or list formats
                        if isinstance(robotics_data, dict):
                            knowledge_data.update(robotics_data)
                        elif isinstance(robotics_data, list):
                            # convert list of articles into an 'articles' collection
                            knowledge_data.setdefault('articles', [])
                            knowledge_data['articles'].extend(robotics_data)
                        else:
                            print(f"Unrecognized robotics data format in {robotics_file}: {type(robotics_data)}")
                        print(f"Loaded robotics knowledge from {robotics_file} (type={type(robotics_data).__name__})")
                    break
            
            # Load enhanced ethics data
            ethics_files = [
                'enhanced_ethics_data.json',
                'data/enhanced_ethics_data.json',
                'C:/Users/biges/OneDrive/Desktop/amd_ai/data/enhanced_ethics_data.json'
            ]
            for ethics_file in ethics_files:
                if os.path.exists(ethics_file):
                    with open(ethics_file, 'r', encoding='utf-8') as f:
                        ethics_data = json.load(f)
                        if isinstance(ethics_data, dict):
                            knowledge_data.update(ethics_data)
                        elif isinstance(ethics_data, list):
                            knowledge_data.setdefault('articles', [])
                            knowledge_data['articles'].extend(ethics_data)
                        else:
                            print(f"Unrecognized ethics data format in {ethics_file}: {type(ethics_data)}")
                        print(f"Loaded ethics knowledge from {ethics_file} (type={type(ethics_data).__name__})")
                    break
                    
            if knowledge_data:
                return knowledge_data
                
        except Exception as e:
            print(f"Could not load external knowledge base: {e}")
            # Dump diagnostics to help debug KB loading in containers/CI
            try:
                self._dump_kb_diagnostics(robotics_files, ethics_files, exception_info=traceback.format_exc())
            except Exception:
                print("Failed to write KB diagnostics")
        
        print("Using fallback knowledge base")
        # Also write diagnostics when falling back and no external data was loaded
        try:
            self._dump_kb_diagnostics(robotics_files, ethics_files)
        except Exception:
            pass
        # Fallback to basic knowledge base
        return {
            "robot": {
                "definition": "Autonomous machine", 
                "types": ["industrial", "service", "humanoid"],
                "examples": ["C-3PO", "R2-D2", "WALL-E", "Terminator", "Optimus Prime"]
            },
            "ai": {
                "definition": "Machine intelligence", 
                "applications": ["ML", "NLP", "vision", "robotics"],
                "domains": ["healthcare", "finance", "transportation"]
            },
            "android": {
                "definition": "Human-like robot",
                "examples": ["Data", "Bishop", "Roy Batty", "Ava"],
                "characteristics": ["humanoid", "synthetic", "intelligent"]
            },
            "character_data": {
                "data": "Android officer from Star Trek with positronic brain, seeking to understand humanity and emotions.",
                "c-3po": "Protocol droid from Star Wars, fluent in over 6 million forms of communication.",
                "wall-e": "Waste collection robot from Pixar who develops personality and environmental consciousness.",
                "terminator": "Cybernetic organism with living tissue over metal endoskeleton."
            }
        }

    def _dump_kb_diagnostics(self, robotics_files, ethics_files, exception_info: str = None):
        """Collect diagnostics about KB files and git state and write to data/kb_fallback_debug.json."""
        diag = {
            "timestamp": time.time(),
            "robotics_files_tested": [],
            "ethics_files_tested": [],
            "exception": exception_info,
            "git": {},
        }

        os.makedirs('data', exist_ok=True)

        def inspect_file(path):
            info = {"path": path, "exists": False}
            try:
                info["exists"] = os.path.exists(path)
                if info["exists"]:
                    info["size_bytes"] = os.path.getsize(path)
                    # try to load JSON to capture parse errors
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            json.load(f)
                        info["json_load"] = "ok"
                    except Exception as jerr:
                        info["json_load"] = f"error: {str(jerr)}"
                else:
                    info["note"] = "missing"
            except Exception as e:
                info["inspect_error"] = str(e)
            return info

        for p in robotics_files:
            diag["robotics_files_tested"].append(inspect_file(p))

        for p in ethics_files:
            diag["ethics_files_tested"].append(inspect_file(p))

        # Run a few git commands to capture repo state (safe if git not available)
        def run_git(cmd_args):
            try:
                out = subprocess.check_output(["git"] + cmd_args, stderr=subprocess.STDOUT, cwd=os.getcwd(), text=True)
                return out.strip()
            except Exception as e:
                return f"git-error: {str(e)}"

        diag["git"]["branch"] = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        diag["git"]["commit"] = run_git(["rev-parse", "--short", "HEAD"])
        diag["git"]["status"] = run_git(["status", "--porcelain"])
        diag["git"]["last_commit_msg"] = run_git(["log", "-1", "--pretty=%B"])

        out_path = os.path.join('data', 'kb_fallback_debug.json')
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(diag, f, ensure_ascii=False, indent=2)
            print(f"Wrote KB fallback diagnostics to {out_path}")
        except Exception as e:
            print(f"Failed to write diagnostics file: {e}")
    
    def _generate_follow_up_questions(self, semantic_analysis: SemanticAnalysis, response: str) -> List[str]:
        """Generate relevant follow-up questions based on the query and response"""
        follow_ups = []
        entities = [e.text for e in semantic_analysis.entities]
        
        if semantic_analysis.intent == IntentType.FACTUAL:
            if entities:
                main_entity = entities[0]
                follow_ups = [
                    f"How does {main_entity} compare to similar technologies?",
                    f"What are the latest developments in {main_entity}?",
                    f"What are the ethical considerations for {main_entity}?"
                ]
        elif semantic_analysis.intent == IntentType.COMPARATIVE:
            follow_ups = [
                "Which option would be better for specific use cases?",
                "What are the cost implications of each approach?",
                "How do these technologies complement each other?"
            ]
        elif semantic_analysis.intent == IntentType.ANALYTICAL:
            follow_ups = [
                "What are the practical implementation challenges?",
                "How might this technology evolve in the future?",
                "What skills are needed to work with this technology?"
            ]
        
        return follow_ups[:3]  # Limit to 3 follow-ups
    
    def _assess_response_quality(self, response: str, semantic_analysis: SemanticAnalysis) -> Dict:
        """Assess the quality and completeness of the response"""
        quality_metrics = {
            "length_score": min(len(response) / 500, 1.0),  # Normalize to 500 chars
            "technical_depth": len(re.findall(r'\b(system|technology|algorithm|process|method)\b', response.lower())) / 10,
            "structure_score": 1.0 if any(marker in response for marker in ['•', '\n\n', 'OVERVIEW', 'CONCLUSION']) else 0.5,
            "engagement_score": 1.0 if any(marker in response for marker in ['🤖', '🔧', '⚙️', '!', '?']) else 0.7
        }
        
        overall_quality = sum(quality_metrics.values()) / len(quality_metrics)
        
        return {
            "overall_quality": overall_quality,
            "metrics": quality_metrics,
            "needs_improvement": overall_quality < 0.6
        }
    
    def process_query(self, query: str, session_id: str = "default") -> Dict:
        # 1. Semantic Analysis
        semantic_analysis = self.semantic_analyzer.analyze_semantics(query)
        
        # 2. Reasoning Pipeline
        reasoning_chain = self.reasoning_pipeline.execute_reasoning(semantic_analysis, self.knowledge_base)
        
        # 3. Context Integration
        context = self.context_manager.get_session_context(session_id)
        reasoning_chain = self.context_manager.integrate_context(reasoning_chain, session_id, query)
        
        # 4. Generate Enhanced Prompt
        enhanced_prompt = self.prompt_engineer.construct_prompt(semantic_analysis, context)
        
        # 5. Get response and assess quality
        response = reasoning_chain.get_final_answer()
        quality_assessment = self._assess_response_quality(response, semantic_analysis)
        
        # 6. Generate follow-up questions
        follow_ups = self._generate_follow_up_questions(semantic_analysis, response)
        
        # 7. Update conversation memory
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = []
        self.conversation_memory[session_id].append({
            "query": query,
            "intent": semantic_analysis.intent.value,
            "entities": [e.text for e in semantic_analysis.entities],
            "timestamp": time.time()
        })
        
        return {
            "response": response,
            "reasoning_steps": [{"type": s.step_type, "content": s.content, "confidence": s.confidence} for s in reasoning_chain.steps],
            "confidence": reasoning_chain.overall_confidence,
            "intent": semantic_analysis.intent.value,
            "complexity": semantic_analysis.complexity.value,
            "entities": [{"text": e.text, "category": e.category} for e in semantic_analysis.entities],
            "enhanced_prompt": enhanced_prompt,
            "session_context": len(context.conversation_history),
            "follow_up_questions": follow_ups,
            "quality_assessment": quality_assessment,
            "conversation_turn": len(self.conversation_memory.get(session_id, [])),
            "topic_expertise": self.topic_expertise.get(semantic_analysis.entities[0].category if semantic_analysis.entities else "general", 0.5)
        }

# Example usage and testing
if __name__ == "__main__":
    agent = EnhancedReasoningAgent()
    
    # Test queries
    test_queries = [
        "What is Data from Star Trek?",
        "Compare robots and androids",
        "Tell me more about artificial intelligence",
        "How do neural networks work?"
    ]
    
    session_id = "test_session"
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print('='*50)
        
        result = agent.process_query(query, session_id)
        
        print(f"Intent: {result['intent']}")
        print(f"Complexity: {result['complexity']}")
        print(f"Entities: {result['entities']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"\nReasoning Steps:")
        for step in result['reasoning_steps']:
            print(f"  {step['type']}: {step['content']} (conf: {step['confidence']:.2f})")
        print(f"\nResponse: {result['response']}")