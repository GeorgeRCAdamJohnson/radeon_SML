#!/usr/bin/env python3
"""
Debug script to test knowledge base search
"""

import json
import os
from reasoning_agent import EnhancedReasoningAgent

def main():
    print("=== DEBUGGING KNOWLEDGE BASE SEARCH ===")
    
    # Initialize agent
    agent = EnhancedReasoningAgent()
    
    # Check knowledge base structure
    print(f"Knowledge base type: {type(agent.knowledge_base)}")
    
    if isinstance(agent.knowledge_base, list):
        print(f"Knowledge base is a list with {len(agent.knowledge_base)} articles")
        if len(agent.knowledge_base) > 0:
            first_article = agent.knowledge_base[0]
            print(f"First article keys: {list(first_article.keys()) if isinstance(first_article, dict) else 'Not a dict'}")
            if isinstance(first_article, dict) and 'title' in first_article:
                print(f"First article title: {first_article['title']}")
    elif isinstance(agent.knowledge_base, dict):
        print(f"Knowledge base is a dict with keys: {list(agent.knowledge_base.keys())}")
        if 'articles' in agent.knowledge_base:
            articles = agent.knowledge_base['articles']
            print(f"Articles list has {len(articles)} items")
    
    # Test search for "gundam"
    print("\n=== TESTING GUNDAM SEARCH ===")
    result = agent.process_query("gundam")
    
    print(f"Response length: {len(result['response'])}")
    print(f"First 200 chars: {result['response'][:200]}")
    print(f"Reasoning steps: {len(result['reasoning_steps'])}")
    for step in result['reasoning_steps']:
        print(f"  - {step['type']}: {step['content'][:100]}...")
    
    # Test direct search in knowledge base
    print("\n=== DIRECT SEARCH TEST ===")
    if isinstance(agent.knowledge_base, list):
        articles = agent.knowledge_base
    elif 'articles' in agent.knowledge_base:
        articles = agent.knowledge_base['articles']
    else:
        articles = []
    
    gundam_matches = []
    for i, article in enumerate(articles):
        if isinstance(article, dict) and 'title' in article:
            title_lower = article['title'].lower()
            if 'gundam' in title_lower or 'mecha' in title_lower or 'mobile suit' in title_lower:
                gundam_matches.append((i, article['title']))
    
    print(f"Found {len(gundam_matches)} potential Gundam matches:")
    for i, title in gundam_matches[:5]:  # Show first 5
        print(f"  [{i}] {title}")

if __name__ == "__main__":
    main()