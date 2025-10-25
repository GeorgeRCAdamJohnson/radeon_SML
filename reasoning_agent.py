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
            "robot": [r"robot", r"android", r"cyborg", r"automaton"],
            "ai": [r"\bai\b", r"artificial intelligence", r"machine learning", r"neural network"],
            "character": [r"data", r"c-3po", r"r2-d2", r"wall-e", r"terminator", r"optimus"],
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
    def analyze(self, knowledge: Dict, semantic_analysis: SemanticAnalysis) -> str:
        entities = [e.text for e in semantic_analysis.entities]
        main_entity = entities[0] if entities else "technology"
        
        if any("robot" in e.lower() for e in entities):
            return """ROBOTICS - COMPREHENSIVE FIELD ANALYSIS

FIELD DEFINITION
Robotics is an interdisciplinary engineering field that integrates mechanical engineering, electrical engineering, computer science, and artificial intelligence to design, construct, and operate autonomous machines capable of performing tasks traditionally requiring human intervention.

CORE TECHNOLOGIES
• Mechanical Systems: Actuators, joints, linkages, and structural components
• Control Systems: Feedback loops, sensors, and real-time processing
• Artificial Intelligence: Machine learning, computer vision, and decision-making
• Power Systems: Batteries, fuel cells, and energy management
• Communication: Wireless protocols, networking, and human-machine interfaces
• Materials Science: Lightweight composites, smart materials, and durability

MAJOR APPLICATION DOMAINS
• Industrial Automation: Manufacturing, assembly, and quality control systems
• Medical Robotics: Surgical assistance, rehabilitation, and prosthetic devices
• Service Robotics: Cleaning, security, and personal assistance applications
• Exploration Robotics: Space missions, deep-sea research, and hazardous environments
• Military Applications: Reconnaissance, bomb disposal, and combat support
• Agricultural Systems: Precision farming, harvesting, and crop monitoring

EMERGING TRENDS
• Collaborative robots (cobots) working alongside humans
• Swarm robotics for coordinated multi-robot systems
• Soft robotics using flexible materials and bio-inspired designs
• Autonomous vehicles and delivery systems
• Brain-computer interfaces for direct neural control
• Quantum sensors for enhanced perception capabilities

CHALLENGES AND LIMITATIONS
• Safety and reliability in human-robot interaction
• Ethical considerations in autonomous decision-making
• Cost-effectiveness for widespread adoption
• Technical complexity in unstructured environments
• Regulatory frameworks for autonomous systems"""
        elif any("ai" in e.lower() for e in entities):
            return """ARTIFICIAL INTELLIGENCE - COMPREHENSIVE ANALYSIS

FIELD OVERVIEW
Artificial Intelligence encompasses computational systems designed to perform tasks that typically require human intelligence, including learning, reasoning, perception, and decision-making. AI systems can analyze data, recognize patterns, and make predictions or recommendations based on their training and algorithms.

CORE TECHNOLOGIES
• Machine Learning: Algorithms that improve performance through experience and data
• Deep Learning: Multi-layered neural networks for complex pattern recognition
• Natural Language Processing: Understanding and generating human language
• Computer Vision: Image and video analysis for object recognition and scene understanding
• Expert Systems: Knowledge-based systems for specialized domain expertise
• Reinforcement Learning: Learning through trial and error with reward feedback

APPLICATION DOMAINS
• Healthcare: Diagnostic imaging, drug discovery, and personalized treatment
• Finance: Fraud detection, algorithmic trading, and risk assessment
• Transportation: Autonomous vehicles and traffic optimization
• Manufacturing: Predictive maintenance and quality control
• Entertainment: Content recommendation and procedural generation
• Communication: Language translation and virtual assistants

CURRENT CAPABILITIES
• Image recognition surpassing human accuracy in specific domains
• Natural language understanding for conversational interfaces
• Game-playing systems achieving superhuman performance
• Predictive analytics for business intelligence and forecasting
• Automated decision-making in structured environments
• Pattern recognition in complex datasets

LIMITATIONS AND CHALLENGES
• Lack of general intelligence and common sense reasoning
• Bias and fairness issues in training data and algorithms
• Explainability and transparency in decision-making processes
• Energy consumption and computational requirements
• Ethical considerations in autonomous systems
• Safety and reliability in critical applications"""
        elif any("android" in e.lower() for e in entities):
            return """ANDROIDS - COMPREHENSIVE ANALYSIS

DEFINITION AND CHARACTERISTICS
Androids are humanoid robots designed to closely resemble humans in appearance, behavior, and interaction patterns. Unlike traditional robots, androids prioritize human-like aesthetics and social capabilities over purely functional design.

TECHNICAL COMPONENTS
• Artificial skin and facial features for realistic appearance
• Advanced actuators for natural movement and gestures
• Speech synthesis and natural language processing
• Computer vision for facial recognition and social cues
• Machine learning algorithms for personality adaptation
• Sensory systems mimicking human touch, sight, and hearing

CURRENT APPLICATIONS
• Hospitality industry for customer service and reception
• Healthcare as patient companions and therapy assistants
• Education for language learning and special needs support
• Entertainment in theme parks and interactive experiences
• Research platforms for studying human-robot interaction
• Elder care providing companionship and basic assistance

DEVELOPMENT CHALLENGES
• Uncanny valley effect causing discomfort in human observers
• Complex manufacturing requiring precision engineering
• High costs limiting widespread adoption
• Ethical concerns about human replacement and deception
• Technical limitations in natural conversation and emotion recognition

FUTURE PROSPECTS
Android technology continues advancing toward more convincing human simulation, with potential applications in personal assistance, social companionship, and specialized service roles."""
        else:
            return f"Comprehensive analysis of {main_entity} covering technical foundations, applications, and impact."
    
    def synthesize(self, analysis: str) -> str:
        return analysis

class ComparativeReasoningStrategy(ReasoningStrategy):
    def analyze(self, knowledge: Dict, semantic_analysis: SemanticAnalysis) -> str:
        entities = [e.text for e in semantic_analysis.entities]
        topic = semantic_analysis.original_query
        
        if "vs" in topic.lower() or "versus" in topic.lower():
            return f"""COMPARATIVE ANALYSIS: {topic.upper()}

Comprehensive comparison examining fundamental differences, similarities, and evolutionary relationships between these domains, analyzing both fictional representations and real-world technological developments.

KEY DIFFERENCES
• Design Philosophy: Functional vs aesthetic priorities
• Technical Complexity: Specialized vs general-purpose systems
• Human Interaction: Task-focused vs social integration
• Development Timeline: Current technology vs future concepts

SIMILARITIES
• Autonomous operation capabilities
• Advanced sensor and processing systems
• Human-machine interface requirements
• Ethical and safety considerations

APPLICATION CONTEXTS
• Industrial and commercial deployment
• Research and development platforms
• Entertainment and media representation
• Future technological integration

CONCLUSION
Both domains represent significant technological achievements with distinct advantages for different applications and use cases."""
        else:
            return f"Comparative analysis of {', '.join(entities)} examining key differences and similarities."
    
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
        chain.add_step("knowledge_retrieval", f"Retrieved {len(relevant_knowledge)} relevant sources", 0.9)
        
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
        relevant_knowledge = {}
        for entity in semantic_analysis.entities:
            # Check for specific character data
            entity_lower = entity.text.lower()
            if entity_lower in knowledge_base.get("character_data", {}):
                relevant_knowledge[entity.text] = knowledge_base["character_data"][entity_lower]
            elif entity.category in knowledge_base:
                relevant_knowledge[entity.text] = knowledge_base[entity.category]
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
                            print(f"⚠️ Unrecognized robotics data format in {robotics_file}: {type(robotics_data)}")
                        print(f"✅ Loaded robotics knowledge from {robotics_file} (type={type(robotics_data).__name__})")
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
                            print(f"⚠️ Unrecognized ethics data format in {ethics_file}: {type(ethics_data)}")
                        print(f"✅ Loaded ethics knowledge from {ethics_file} (type={type(ethics_data).__name__})")
                    break
                    
            if knowledge_data:
                return knowledge_data
                
        except Exception as e:
            print(f"❌ Could not load external knowledge base: {e}")
            # Dump diagnostics to help debug KB loading in containers/CI
            try:
                self._dump_kb_diagnostics(robotics_files, ethics_files, exception_info=traceback.format_exc())
            except Exception:
                print("⚠️ Failed to write KB diagnostics")
        
        print("⚠️ Using fallback knowledge base")
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
            print(f"✅ Wrote KB fallback diagnostics to {out_path}")
        except Exception as e:
            print(f"❌ Failed to write diagnostics file: {e}")
    
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
        
        return {
            "response": reasoning_chain.get_final_answer(),
            "reasoning_steps": [{"type": s.step_type, "content": s.content, "confidence": s.confidence} for s in reasoning_chain.steps],
            "confidence": reasoning_chain.overall_confidence,
            "intent": semantic_analysis.intent.value,
            "complexity": semantic_analysis.complexity.value,
            "entities": [{"text": e.text, "category": e.category} for e in semantic_analysis.entities],
            "enhanced_prompt": enhanced_prompt,
            "session_context": len(context.conversation_history)
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