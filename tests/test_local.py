#!/usr/bin/env python3
import requests
import json

# Test the server directly
url = "http://localhost:8000/api/chat"
data = {
    "message": "gundam",
    "format": "detailed",
    "session_id": "test-session"
}

try:
    response = requests.post(url, json=data)
    if response.ok:
        result = response.json()
        print(f"Response length: {len(result['response'])}")
        print(f"First 200 chars: {result['response'][:200]}...")
    else:
        print(f"Error: {response.status_code}")
except Exception as e:
    print(f"Connection error: {e}")