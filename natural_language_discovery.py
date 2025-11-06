#!/usr/bin/env python3
"""
Natural Language Discovery Engine
Makes the AI more conversational, intuitive, and discoverable for students
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ConversationStyle(Enum):
    CASUAL = "casual"          # "Hey, let me explain..."
    EDUCATIONAL = "educational"  # "Let's explore this together..."
    ENTHUSIASTIC = "enthusiastic"  # "That's a great question!"
    SUPPORTIVE = "supportive"   # "I understand this can be confusing..."

class LearningLevel(Enum):
    BEGINNER = "beginner"       # High school / early college
    INTERMEDIATE = "intermediate"  # College / some background
    ADVANCED = "advanced"       # Graduate / professional

@dataclass
class ConversationContext:
    user_level: LearningLevel = LearningLevel.BEGINNER
    conversation_style: ConversationStyle = ConversationStyle.EDUCATIONAL
    topics_discussed: List[str] = None
    follow_up_count: int = 0
    confusion_indicators: int = 0

class NaturalLanguageProcessor:
    """Enhanced NLP for more natural, discoverable conversations"""
    
    def __init__(self):
        self.greeting_patterns = [
            r"^(hi|hello|hey|sup|what's up)",
            r"(good morning|good afternoon|good evening)",
            r"^(yo|hiya)"
        ]
        
        self.confusion_patterns = [
            r"(i don't understand|confused|what do you mean|huh|what)",
            r"(can you explain|clarify|make it simpler|break it down)",
            r"(i'm lost|too complex|over my head)"
        ]
        
        self.enthusiasm_patterns = [
            r"(that's cool|awesome|amazing|wow|interesting)",
            r"(tell me more|want to know more|fascinating)",
            r"(love this|really cool|impressive)"
        ]
        
        self.casual_patterns = [
            r"(what's|what is|whats)",
            r"(how do|how does|how can)",
            r"(why do|why does|why is)",
            r"(can you|could you|would you)"
        ]
        
        # Natural question starters that should be handled conversationally
        self.question_starters = {
            "what": "What's a great question! Let me break this down for you...",
            "how": "That's exactly what I love helping with! Here's how...",
            "why": "Excellent question! The reason is...",
            "when": "Good timing question! Let me explain when...",
            "where": "Great spatial thinking! Here's where...",
            "who": "Interesting! Let me tell you about who..."
        }
        
        # Topic discovery helpers
        self.topic_bridges = {
            "robotics": ["automation", "AI", "programming", "sensors", "actuators", "ethics"],
            "ai": ["machine learning", "neural networks", "algorithms", "robotics", "ethics"],
            "ethics": ["philosophy", "responsibility", "bias", "fairness", "society", "AI"]
        }
        
    def make_conversational(self, query: str, context: ConversationContext) -> Tuple[str, ConversationContext]:
        """Transform query and context to be more conversational"""
        
        # Detect conversation style
        if any(re.search(pattern, query.lower()) for pattern in self.greeting_patterns):
            context.conversation_style = ConversationStyle.CASUAL
            
        if any(re.search(pattern, query.lower()) for pattern in self.confusion_patterns):
            context.confusion_indicators += 1
            context.conversation_style = ConversationStyle.SUPPORTIVE
            
        if any(re.search(pattern, query.lower()) for pattern in self.enthusiasm_patterns):
            context.conversation_style = ConversationStyle.ENTHUSIASTIC
        
        # Enhance the query for better processing
        enhanced_query = self._enhance_query_for_search(query, context)
        
        return enhanced_query, context
    
    def _enhance_query_for_search(self, query: str, context: ConversationContext) -> str:
        """Enhance queries for better search and understanding"""
        
        # Handle casual questions more naturally
        query_lower = query.lower().strip()
        
        # Expand common abbreviations and casual language
        expansions = {
            "what's": "what is",
            "how's": "how is", 
            "where's": "where is",
            "ai": "artificial intelligence",
            "ml": "machine learning",
            "bot": "robot",
            "tech": "technology"
        }
        
        for abbrev, expansion in expansions.items():
            query_lower = re.sub(r'\b' + abbrev + r'\b', expansion, query_lower)
        
        # Add context from previous topics
        if context.topics_discussed:
            # Don't modify the query, but this helps with search context
            pass
            
        return query_lower
    
    def generate_natural_response_intro(self, query: str, context: ConversationContext) -> str:
        """Generate natural, conversational response introductions"""
        
        query_lower = query.lower().strip()
        
        # Handle greetings
        if any(re.search(pattern, query_lower) for pattern in self.greeting_patterns):
            return "Hey there! I'm here to help you explore robotics and AI ethics. What would you like to learn about today?"
        
        # Handle confusion
        if context.confusion_indicators > 0:
            return "No worries! Let me explain this more clearly. "
        
        # Question-based responses
        for starter, intro in self.question_starters.items():
            if query_lower.startswith(starter):
                return intro
        
        # Default based on conversation style
        if context.conversation_style == ConversationStyle.ENTHUSIASTIC:
            return "That's a fantastic question! "
        elif context.conversation_style == ConversationStyle.SUPPORTIVE:
            return "I understand this can be tricky. Let me help clarify... "
        elif context.conversation_style == ConversationStyle.CASUAL:
            return "Sure thing! "
        else:
            return "Great question! "
    
    def suggest_discovery_topics(self, current_query: str, context: ConversationContext) -> List[str]:
        """Suggest related topics for natural discovery"""
        
        suggestions = []
        query_lower = current_query.lower()
        
        # Find main topic
        main_topic = None
        for topic in self.topic_bridges.keys():
            if topic in query_lower:
                main_topic = topic
                break
        
        if main_topic:
            # Add related topics
            related = self.topic_bridges[main_topic]
            suggestions.extend([f"Learn about {topic}" for topic in related[:3]])
        
        # Add conversation-style suggestions
        if "robot" in query_lower:
            suggestions.extend([
                "How do robots actually work?",
                "What are some cool robot examples?",
                "Are there ethical concerns with robots?"
            ])
        elif "ethics" in query_lower:
            suggestions.extend([
                "Why do we need AI ethics?",
                "What are some ethical dilemmas in robotics?",
                "How can we make AI more fair?"
            ])
        elif "ai" in query_lower or "artificial intelligence" in query_lower:
            suggestions.extend([
                "How does AI learn?",
                "What can AI do in robots?",
                "What are AI's limitations?"
            ])
        
        return suggestions[:4]  # Limit to 4 suggestions
    
    def generate_follow_up_questions(self, query: str, response_content: str) -> List[str]:
        """Generate natural follow-up questions"""
        
        follow_ups = []
        query_lower = query.lower()
        
        # Pattern-based follow-ups
        if "what is" in query_lower:
            follow_ups.append("How does this actually work in practice?")
            follow_ups.append("Can you give me some real examples?")
        elif "how" in query_lower:
            follow_ups.append("What are some challenges with this approach?")
            follow_ups.append("Where is this technology heading?")
        elif "why" in query_lower:
            follow_ups.append("What are the implications of this?")
            follow_ups.append("How does this affect society?")
        
        # Topic-specific follow-ups
        if any(word in query_lower for word in ["robot", "robotics"]):
            follow_ups.extend([
                "What types of robots are most common today?",
                "How do robots impact jobs and society?",
                "What's the future of robotics?"
            ])
        
        if any(word in query_lower for word in ["ai", "artificial intelligence"]):
            follow_ups.extend([
                "How is AI different from traditional programming?",
                "What are the biggest challenges in AI?",
                "How can we ensure AI is used ethically?"
            ])
        
        if "ethics" in query_lower:
            follow_ups.extend([
                "What are some controversial ethical issues?",
                "How do we balance innovation with responsibility?",
                "Who decides what's ethical in technology?"
            ])
        
        return follow_ups[:3]  # Limit to 3 follow-ups
    
    def detect_learning_level(self, query: str, context: ConversationContext) -> LearningLevel:
        """Detect user's learning level from their questions"""
        
        query_lower = query.lower()
        
        # Beginner indicators
        beginner_indicators = [
            "what is", "basic", "simple", "for dummies", "explain like",
            "i'm new to", "just starting", "don't know much"
        ]
        
        # Advanced indicators  
        advanced_indicators = [
            "algorithm", "implementation", "optimization", "research",
            "theoretical", "mathematical", "technical details", "architecture"
        ]
        
        if any(indicator in query_lower for indicator in advanced_indicators):
            return LearningLevel.ADVANCED
        elif any(indicator in query_lower for indicator in beginner_indicators):
            return LearningLevel.BEGINNER
        else:
            return LearningLevel.INTERMEDIATE
    
    def adjust_response_complexity(self, response: str, level: LearningLevel) -> str:
        """Adjust response complexity based on user level"""
        
        if level == LearningLevel.BEGINNER:
            # Add friendly explanations
            response = self._add_beginner_context(response)
        elif level == LearningLevel.ADVANCED:
            # Keep technical depth
            pass
        
        return response
    
    def _add_beginner_context(self, response: str) -> str:
        """Add beginner-friendly context and explanations"""
        
        # Add simple definitions for technical terms
        technical_terms = {
            "algorithm": "algorithm (a set of rules or instructions for solving a problem)",
            "neural network": "neural network (a computer system inspired by how our brain works)",
            "machine learning": "machine learning (teaching computers to learn patterns from data)",
            "sensors": "sensors (devices that detect things like light, sound, or touch)",
            "actuators": "actuators (parts that make things move, like motors)"
        }
        
        for term, definition in technical_terms.items():
            response = re.sub(r'\b' + term + r'\b', definition, response, flags=re.IGNORECASE)
        
        return response

class DiscoveryEngine:
    """Helps users discover content in natural, intuitive ways"""
    
    def __init__(self):
        self.nlp = NaturalLanguageProcessor()
        self.conversation_contexts = {}  # session_id -> ConversationContext
    
    def process_natural_query(self, query: str, session_id: str = "default") -> Dict:
        """Process a query with natural language understanding and discovery"""
        
        # Get or create conversation context
        if session_id not in self.conversation_contexts:
            self.conversation_contexts[session_id] = ConversationContext()
        
        context = self.conversation_contexts[session_id]
        
        # Make query more conversational
        enhanced_query, updated_context = self.nlp.make_conversational(query, context)
        self.conversation_contexts[session_id] = updated_context
        
        # Detect user level
        user_level = self.nlp.detect_learning_level(query, context)
        updated_context.user_level = user_level
        
        # Generate natural response intro
        response_intro = self.nlp.generate_natural_response_intro(query, context)
        
        # Generate discovery suggestions
        discovery_topics = self.nlp.suggest_discovery_topics(query, context)
        
        # Generate follow-ups
        follow_ups = self.nlp.generate_follow_up_questions(query, "")  # We'll fill response later
        
        return {
            "enhanced_query": enhanced_query,
            "response_intro": response_intro,
            "user_level": user_level.value,
            "conversation_style": context.conversation_style.value,
            "discovery_topics": discovery_topics,
            "follow_up_questions": follow_ups,
            "session_context": {
                "topics_discussed": context.topics_discussed or [],
                "follow_up_count": context.follow_up_count,
                "confusion_indicators": context.confusion_indicators
            }
        }
    
    def enhance_response_with_discovery(self, base_response: str, natural_data: Dict) -> str:
        """Enhance a base response with natural language and discovery elements"""
        
        # Start with natural intro
        enhanced_response = natural_data["response_intro"]
        
        # Adjust complexity based on user level
        level = LearningLevel(natural_data["user_level"])
        adjusted_response = self.nlp.adjust_response_complexity(base_response, level)
        
        # Combine intro with response
        enhanced_response += adjusted_response
        
        # Add discovery elements
        if natural_data["discovery_topics"]:
            enhanced_response += "\n\n🔍 **You might also like to explore:**\n"
            for topic in natural_data["discovery_topics"][:3]:
                enhanced_response += f"• {topic}\n"
        
        return enhanced_response