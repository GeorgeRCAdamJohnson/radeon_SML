#!/usr/bin/env python3
"""
Simple Natural Language Demo Server
Demonstrates the enhanced conversational AI without complexity
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import time
import uuid
from natural_language_discovery import DiscoveryEngine

app = FastAPI(title="Radeon AI - Natural Language Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    format: str = "detailed"
    session_id: str = "demo-session"

# Initialize discovery engine
discovery_engine = DiscoveryEngine()

# Simple knowledge base for demo
DEMO_RESPONSES = {
    "artificial intelligence": "Artificial Intelligence (AI) is like giving computers the ability to think and learn, similar to how humans do! It's a branch of computer science that creates smart machines capable of performing tasks that typically require human intelligence - like recognizing speech, making decisions, solving problems, and learning from experience.",
    
    "machine learning": "Machine Learning is a subset of AI where computers learn patterns from data without being explicitly programmed for every scenario. Think of it like teaching a child to recognize animals - instead of describing every feature, you show them lots of pictures until they can identify animals on their own!",
    
    "robotics": "Robotics combines engineering, computer science, and AI to create machines (robots) that can sense their environment, make decisions, and perform physical tasks. From manufacturing robots in factories to rovers exploring Mars, robotics is everywhere!",
    
    "ai ethics": "AI Ethics deals with ensuring artificial intelligence is developed and used responsibly. It addresses important questions like: Will AI replace jobs? How do we prevent bias? Should AI make life-or-death decisions? It's about making sure AI benefits everyone fairly.",
    
    "neural networks": "Neural Networks are computer systems inspired by how our brains work! They have interconnected nodes (like brain neurons) that process information and learn patterns. They're the backbone of modern AI applications like image recognition and language translation."
}

def find_best_response(query: str) -> str:
    """Find the best matching response from our knowledge base"""
    query_lower = query.lower()
    
    # Look for key topics
    for topic, response in DEMO_RESPONSES.items():
        if topic in query_lower:
            return response
    
    # Default educational response
    if any(word in query_lower for word in ["what", "how", "why", "explain"]):
        return f"That's a great question about {query}! While I'm still learning about this specific topic, I'd love to help you explore related concepts. Try asking about artificial intelligence, machine learning, robotics, or AI ethics - these are areas where I have lots of knowledge to share!"
    
    return f"Hello! I'm your AI learning companion, ready to help you explore the fascinating world of technology! Try asking me about artificial intelligence, robotics, machine learning, or AI ethics."

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Enhanced chat endpoint with natural language processing"""
    
    query = request.message
    session_id = request.session_id
    
    # Process with natural language discovery
    natural_data = discovery_engine.process_natural_query(query, session_id)
    
    # Get base response
    base_response = find_best_response(natural_data["enhanced_query"])
    
    # Enhance response with natural language features
    enhanced_response = discovery_engine.enhance_response_with_discovery(base_response, natural_data)
    
    # Build comprehensive response
    return {
        "id": str(uuid.uuid4()),
        "response": enhanced_response,
        "timestamp": time.time(),
        "confidence": 0.85,
        "processing_time": 0.5,
        "from_cache": False,
        "safety_blocked": False,
        
        # Natural Language Features
        "conversation_style": natural_data["conversation_style"],
        "user_level": natural_data["user_level"],
        "related_topics": natural_data["discovery_topics"],
        "follow_up_suggestions": natural_data["follow_up_questions"],
        
        # Enhanced metadata
        "natural_language_processing": {
            "original_query": query,
            "enhanced_query": natural_data["enhanced_query"],
            "response_intro": natural_data["response_intro"],
            "discovery_enabled": True,
            "session_context": natural_data["session_context"]
        }
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy", 
        "natural_language": "active",
        "discovery_engine": "enabled"
    }

@app.get("/api/status")
async def status():
    return {
        "system_name": "Radeon AI - Natural Language Demo",
        "version": "3.0.0-preview",
        "features": {
            "natural_language_processing": True,
            "conversation_adaptation": True,
            "smart_discovery": True,
            "learning_level_detection": True,
            "follow_up_suggestions": True
        },
        "demo_topics": list(DEMO_RESPONSES.keys())
    }

# Add static file serving for the enhanced frontend
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/")
    async def read_index():
        return FileResponse('static/index.html')

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Natural Language Demo Server...")
    print(f"📍 Available at: http://localhost:{port}")
    print(f"✨ Features: Conversational AI, Smart Discovery, Adaptive Learning")
    uvicorn.run(app, host="0.0.0.0", port=port)