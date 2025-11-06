#!/usr/bin/env python3
"""Quick script to test what's actually deployed"""

import requests
import hashlib

def get_deployed_frontend():
    """Get the deployed frontend HTML"""
    try:
        response = requests.get('https://radeon-ai-960026900565.us-central1.run.app/')
        return response.text
    except Exception as e:
        return f"Error: {e}"

def get_local_frontend():
    """Get local frontend HTML"""
    try:
        with open('src/react/deploy/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

def compare_files():
    deployed = get_deployed_frontend()
    local = get_local_frontend()
    
    deployed_hash = hashlib.md5(deployed.encode()).hexdigest()
    local_hash = hashlib.md5(local.encode()).hexdigest()
    
    print(f"Deployed hash: {deployed_hash}")
    print(f"Local hash:    {local_hash}")
    print(f"Match: {deployed_hash == local_hash}")
    
    # Check for fallback comments
    if "// try {" in deployed:
        print("✅ Deployed version has commented fallbacks")
    else:
        print("❌ Deployed version still has active fallbacks")

if __name__ == "__main__":
    compare_files()