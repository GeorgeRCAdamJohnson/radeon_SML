#!/usr/bin/env python3
"""
Local development server for enhanced reasoning agent
"""

import uvicorn
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting Enhanced Reasoning Agent locally...")
    print("Enhanced knowledge base with Gundam, Data, and metadata loaded")
    print("Access at: http://localhost:8000")
    print("API endpoints:")
    print("  - Health: http://localhost:8000/api/health")
    print("  - Status: http://localhost:8000/api/status")
    print("  - Chat: POST http://localhost:8000/api/chat")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )