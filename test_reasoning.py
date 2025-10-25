import requests

def test_reasoning_agent():
    base_url = "https://radeon-ai-960026900565.us-central1.run.app"
    
    # Test with a specific question that should trigger detailed response
    chat_data = {
        "message": "Tell me about Data from Star Trek in detail",
        "format": "detailed", 
        "session_id": "test-reasoning"
    }
    
    response = requests.post(f"{base_url}/api/chat", json=chat_data, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        response_text = data.get('response', '')
        
        print(f"Response length: {len(response_text)}")
        print(f"Confidence: {data.get('confidence')}")
        print(f"Sources: {data.get('sources')}")
        print(f"Reasoning steps: {len(data.get('reasoning_steps', []))}")
        print(f"Entities: {data.get('entities_detected', [])}")
        print(f"Intent: {data.get('intent')}")
        print(f"Complexity: {data.get('complexity_level')}")
        print("\nFirst 300 characters:")
        print(response_text[:300])
        
        # Check if it's using reasoning agent or fallback
        if "DATA (STAR TREK)" in response_text.upper():
            print("\n✅ Using enhanced reasoning agent")
        elif len(response_text) < 200:
            print("\n❌ Using fallback responses")
        else:
            print("\n❓ Unclear which system is responding")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    test_reasoning_agent()