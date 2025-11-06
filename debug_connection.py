import requests
import json

def test_endpoints():
    base_url = "https://radeon-ai-960026900565.us-central1.run.app"
    
    print("Testing endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"✅ /api/health: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ /api/health: {e}")
    
    # Test chat endpoint
    try:
        response = requests.post(f"{base_url}/api/chat", 
                               json={"message": "test", "format": "standard", "session_id": "test"},
                               timeout=10)
        print(f"✅ /api/chat: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response length: {len(data.get('response', ''))}")
    except Exception as e:
        print(f"❌ /api/chat: {e}")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"✅ /: {response.status_code}")
        print(f"   Content length: {len(response.text)}")
    except Exception as e:
        print(f"❌ /: {e}")

if __name__ == "__main__":
    test_endpoints()