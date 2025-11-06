#!/usr/bin/env python3
"""
Test Natural Language Discovery Features
Quick test of the enhanced conversational AI
"""

import requests
import json
import time

def test_natural_language_api():
    """Test the enhanced API with natural language queries"""
    
    base_url = "http://localhost:8000"
    
    # Test queries with different styles
    test_queries = [
        "Hi! What is artificial intelligence?",
        "How do robots work?",
        "I'm confused about AI ethics - can you explain?", 
        "That's cool! Tell me more about machine learning",
        "What's the difference between AI and robotics?",
        "Why should I care about robot ethics?"
    ]
    
    print("🤖 Testing Natural Language Discovery Engine")
    print("=" * 50)
    
    session_id = f"test-session-{int(time.time())}"
    
    for i, query in enumerate(test_queries):
        print(f"\n📝 Query {i+1}: '{query}'")
        
        try:
            response = requests.post(f"{base_url}/api/chat", json={
                "message": query,
                "format": "detailed", 
                "session_id": session_id
            })
            
            if response.status_code == 200:
                data = response.json()
                
                # Show natural language processing results
                nl_data = data.get('natural_language_processing', {})
                print(f"🧠 Original: {nl_data.get('original_query', 'N/A')}")
                print(f"✨ Enhanced: {nl_data.get('enhanced_query', 'N/A')}")
                print(f"🎭 Style: {data.get('conversation_style', 'N/A')}")
                print(f"📚 Level: {data.get('user_level', 'N/A')}")
                
                # Show response intro
                print(f"💬 Intro: {nl_data.get('response_intro', 'N/A')}")
                
                # Show discovery features
                discovery_topics = data.get('related_topics', [])
                follow_ups = data.get('follow_up_suggestions', [])
                
                print(f"🔍 Discovery Topics: {', '.join(discovery_topics[:3])}")
                print(f"❓ Follow-ups: {', '.join(follow_ups[:2])}")
                
                # Show confidence and processing
                print(f"🎯 Confidence: {data.get('confidence', 0):.2f}")
                print(f"⚡ Processing: {data.get('processing_time', 0):.2f}s")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Small delay between requests
        time.sleep(1)

def test_discovery_suggestions():
    """Test the topic discovery functionality"""
    
    print("\n🔍 Testing Discovery Suggestions")
    print("=" * 30)
    
    # Test different topic areas
    topics = ["robotics", "ai ethics", "machine learning", "automation"]
    
    for topic in topics:
        query = f"Tell me about {topic}"
        print(f"\n📋 Testing topic: {topic}")
        
        try:
            response = requests.post("http://localhost:8000/api/chat", json={
                "message": query,
                "format": "detailed"
            })
            
            if response.status_code == 200:
                data = response.json()
                discovery = data.get('related_topics', [])
                follow_ups = data.get('follow_up_suggestions', [])
                
                print(f"   🎯 Discovered: {discovery}")
                print(f"   💭 Follow-ups: {follow_ups}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Natural Language Discovery Tests...")
    time.sleep(2)  # Give server time to fully start
    
    test_natural_language_api()
    test_discovery_suggestions()
    
    print("\n✅ Testing Complete!")
    print("\n💡 Try the enhanced interface at: http://localhost:8000")
    print("   - More conversational responses")
    print("   - Smart topic discovery") 
    print("   - Natural follow-up questions")
    print("   - Adaptive learning levels")