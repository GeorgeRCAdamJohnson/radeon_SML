import requests
import json

def test_api():
    base_url = "https://radeon-ai-960026900565.us-central1.run.app"
    
    print("=== TESTING RADEON AI API ===\n")
    
    # Test health endpoint
    print("1. Testing /api/health...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test status endpoint
    print("2. Testing /api/status...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   System: {data.get('system_name')}")
            print(f"   Articles: {data.get('knowledge_stats', {}).get('total_articles')}")
            print(f"   Words: {data.get('knowledge_stats', {}).get('total_words')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test chat endpoint
    print("3. Testing /api/chat...")
    try:
        chat_data = {
            "message": "What is Data from Star Trek?",
            "format": "summary",
            "session_id": "test-session"
        }
        response = requests.post(f"{base_url}/api/chat", 
                               json=chat_data, 
                               timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response length: {len(data.get('response', ''))}")
            print(f"   Confidence: {data.get('confidence')}")
            print(f"   Sources: {data.get('sources')}")
            print(f"   First 200 chars: {data.get('response', '')[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_api()