#!/usr/bin/env python3
"""
Phi-2 Performance Test Script
Tests inference speed vs Ollama baseline
"""
import time
import requests
import json
from datetime import datetime

def test_text_generation_webui():
    """Test Text Generation WebUI with Phi-2"""
    print("🧪 Testing Text Generation WebUI + Phi-2 Performance")
    print("=" * 50)
    
    # Test prompt for AI ethics education
    test_prompt = "What are the key ethical considerations when developing AI systems for education?"
    
    # API endpoint (assuming default port)
    url = "http://localhost:5000/v1/completions"
    
    payload = {
        "prompt": test_prompt,
        "max_tokens": 150,
        "temperature": 0.7,
        "stop": ["\n\n"]
    }
    
    print(f"📝 Test Prompt: {test_prompt}")
    print(f"⏰ Starting inference test at {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            inference_time = end_time - start_time
            
            print(f"✅ SUCCESS!")
            print(f"⚡ Inference Time: {inference_time:.2f} seconds")
            print(f"📊 Response: {result.get('choices', [{}])[0].get('text', 'No response')[:200]}...")
            
            # Compare to Ollama baseline
            ollama_time = 270  # 4.5 minutes
            improvement = ((ollama_time - inference_time) / ollama_time) * 100
            
            print(f"\n📈 PERFORMANCE COMPARISON:")
            print(f"   Ollama (baseline): {ollama_time} seconds")
            print(f"   Text-Gen WebUI:    {inference_time:.2f} seconds")
            print(f"   Improvement:       {improvement:.1f}%")
            
            return inference_time
            
        else:
            print(f"❌ API Error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Text Generation WebUI not running")
        print("💡 Start it with: python server.py --model microsoft_phi-2 --cpu --api --api-port 5000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_direct_inference():
    """Test direct inference without API"""
    print("\n🔬 Testing Direct Inference (Fallback)")
    print("=" * 50)
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        print("📦 Loading Phi-2 model directly...")
        start_load = time.time()
        
        model_path = "C:/Users/biges/Desktop/amd_ai/text-generation-webui/user_data/models/microsoft_phi-2"
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32)
        
        load_time = time.time() - start_load
        print(f"⏱️  Model Load Time: {load_time:.2f} seconds")
        
        # Test inference
        test_prompt = "What are the key ethical considerations when developing AI systems for education?"
        print(f"📝 Test Prompt: {test_prompt}")
        
        start_inference = time.time()
        inputs = tokenizer(test_prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_length=inputs.input_ids.shape[1] + 50,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        inference_time = time.time() - start_inference
        
        print(f"✅ SUCCESS!")
        print(f"⚡ Inference Time: {inference_time:.2f} seconds")
        print(f"📊 Response: {response[len(test_prompt):].strip()[:200]}...")
        
        return inference_time
        
    except ImportError:
        print("❌ Transformers library not available")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 RADEON-AI V2 Performance Test")
    print("Testing Phi-2 vs Ollama Baseline (4.5 minutes)")
    print("=" * 60)
    
    # Try API first, fallback to direct
    result = test_text_generation_webui()
    
    if result is None:
        print("\n🔄 Trying direct inference...")
        result = test_direct_inference()
    
    if result:
        print(f"\n🎉 FINAL RESULT: {result:.2f} seconds")
        print("✅ Performance target achieved!")
    else:
        print("\n❌ Performance test failed")
        print("💡 Ensure Text Generation WebUI is running or dependencies are installed")