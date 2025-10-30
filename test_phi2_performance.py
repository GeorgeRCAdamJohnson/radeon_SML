import time
import requests
import json

def test_phi2_inference():
    url = "http://127.0.0.1:5000/v1/completions"
    
    payload = {
        "model": "microsoft_phi-2",
        "prompt": "What is artificial intelligence?",
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    print("Testing Phi-2 inference speed...")
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        end_time = time.time()
        
        if response.status_code == 200:
            inference_time = end_time - start_time
            print(f"✅ Success: {inference_time:.2f} seconds")
            result = response.json()
            print(f"Response: {result.get('choices', [{}])[0].get('text', 'No text')}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is Text Generation WebUI running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_phi2_inference()