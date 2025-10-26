#!/usr/bin/env python3
"""
Quick test of enhanced reasoning agent
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reasoning_agent import EnhancedReasoningAgent

def test_enhanced_agent():
    print("Testing Enhanced Reasoning Agent with new knowledge base...")
    
    agent = EnhancedReasoningAgent()
    
    test_queries = [
        "What is Gundam?",
        "Tell me about Data from Star Trek",
        "What is Isaac Asimov known for?",
        "Explain the Three Laws of Robotics",
        "What is the Turing Test?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        
        result = agent.process_query(query)
        
        print(f"Intent: {result['intent']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Entities: {[e['text'] for e in result['entities']]}")
        print(f"\nResponse:\n{result['response']}")
        
        if result['reasoning_steps']:
            print(f"\nReasoning Steps:")
            for step in result['reasoning_steps']:
                print(f"  - {step['type']}: {step['confidence']:.2f}")

if __name__ == "__main__":
    test_enhanced_agent()