#!/usr/bin/env python3
"""
Demo: Natural Language Discovery Features
Shows how the enhanced AI feels more conversational and discoverable
"""

from natural_language_discovery import DiscoveryEngine, LearningLevel, ConversationStyle

def demo_natural_language_processing():
    """Demonstrate the natural language processing capabilities"""
    
    print("🤖 Natural Language Discovery Demo")
    print("=" * 50)
    
    discovery_engine = DiscoveryEngine()
    
    # Test different types of queries
    test_queries = [
        "Hi! What is artificial intelligence?",
        "I'm confused about machine learning",
        "That's amazing! Tell me more about robotics",
        "How do robots actually work?",
        "Why should I care about AI ethics?",
        "what's the difference between ai and ml?"
    ]
    
    for i, query in enumerate(test_queries):
        print(f"\n📝 Query {i+1}: '{query}'")
        print("-" * 40)
        
        # Process with natural language discovery
        result = discovery_engine.process_natural_query(query, f"demo-session")
        
        # Show the processing results
        print(f"🔤 Original Query: {query}")
        print(f"✨ Enhanced Query: {result['enhanced_query']}")
        print(f"🎭 Conversation Style: {result['conversation_style']}")
        print(f"📚 Detected Level: {result['user_level']}")
        print(f"💬 Response Intro: {result['response_intro']}")
        
        # Show discovery features
        print(f"\n🔍 Discovery Topics:")
        for topic in result['discovery_topics']:
            print(f"   • {topic}")
            
        print(f"\n❓ Follow-up Questions:")
        for question in result['follow_up_questions']:
            print(f"   • {question}")
        
        # Show session context
        context = result['session_context']
        print(f"\n📊 Session Context:")
        print(f"   Topics Discussed: {len(context['topics_discussed'])}")
        print(f"   Follow-ups: {context['follow_up_count']}")
        print(f"   Confusion Indicators: {context['confusion_indicators']}")

def demo_conversation_adaptation():
    """Show how responses adapt to conversation style and user level"""
    
    print(f"\n\n🎭 Conversation Style Adaptation Demo")
    print("=" * 50)
    
    discovery_engine = DiscoveryEngine()
    
    # Test same question with different styles
    base_query = "What is machine learning?"
    
    test_scenarios = [
        ("Beginner Student", "I'm new to this - what is machine learning?"),
        ("Confused Student", "I don't understand machine learning at all"),
        ("Enthusiastic Student", "Machine learning sounds awesome! What is it?"),
        ("Advanced Student", "Explain the theoretical foundations of machine learning algorithms")
    ]
    
    for scenario_name, query in test_scenarios:
        print(f"\n📚 Scenario: {scenario_name}")
        print(f"💭 Query: '{query}'")
        
        result = discovery_engine.process_natural_query(query, f"scenario-{scenario_name}")
        
        print(f"   🎭 Style: {result['conversation_style']}")
        print(f"   📊 Level: {result['user_level']}")
        print(f"   💬 Intro: {result['response_intro']}")
        
        # Show how discovery topics adapt
        print(f"   🔍 Suggested Topics: {', '.join(result['discovery_topics'][:3])}")

def demo_discovery_suggestions():
    """Show how the system suggests related topics for exploration"""
    
    print(f"\n\n🔍 Smart Discovery Demo")
    print("=" * 30)
    
    discovery_engine = DiscoveryEngine()
    
    topic_queries = [
        "Tell me about robotics",
        "What is AI ethics?", 
        "How does automation work?",
        "Explain neural networks"
    ]
    
    for query in topic_queries:
        print(f"\n🎯 Topic: {query}")
        result = discovery_engine.process_natural_query(query, "discovery-demo")
        
        print(f"   💡 Discoveries: {result['discovery_topics']}")
        print(f"   ❓ Follow-ups: {result['follow_up_questions']}")

if __name__ == "__main__":
    print("🚀 Starting Natural Language Discovery Demonstrations...")
    print("This shows how the AI becomes more conversational and discoverable!\n")
    
    # Run all demos
    demo_natural_language_processing()
    demo_conversation_adaptation()
    demo_discovery_suggestions()
    
    print(f"\n\n✅ Demo Complete!")
    print(f"\n💡 Key Improvements:")
    print(f"   🗣️  More conversational and natural responses")
    print(f"   🎭  Adapts to user's conversation style and confusion level")
    print(f"   📚  Detects learning level (beginner/intermediate/advanced)")
    print(f"   🔍  Smart topic discovery and related content suggestions")
    print(f"   ❓  Intelligent follow-up questions for deeper learning")
    print(f"   📊  Session memory for better context understanding")
    print(f"\n🎯 This makes the AI feel more like a helpful tutor than a search engine!")