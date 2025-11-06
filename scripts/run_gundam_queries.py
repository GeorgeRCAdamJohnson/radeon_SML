#!/usr/bin/env python3
"""Run the EnhancedReasoningAgent for several Gundam query formats and save outputs."""
import json
import os
import sys
import time

# Ensure repo root is on sys.path so local modules like reasoning_agent can be imported
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from reasoning_agent import EnhancedReasoningAgent


def main():
    agent = EnhancedReasoningAgent()

    prompts = {
        "detailed": "Provide a detailed analysis of the Gundam franchise, covering history, technology, and cultural impact.",
        "essay": "Write an essay about Gundam: themes, evolution, and its influence on robotics and society.",
        "standard": "Give a standard informational overview of Gundam (what it is and key facts).",
        "summary": "Give a concise summary of Gundam in 3-4 sentences.",
        "list": "Provide a list of notable Gundam mobile suits and brief one-line descriptions."
    }

    results = []
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    for fmt, prompt in prompts.items():
        session_id = f"gundam_{fmt}_{int(time.time())}"
        print(f"Running format: {fmt} -> '{prompt}'")
        try:
            res = agent.process_query(prompt, session_id=session_id)
        except Exception as e:
            res = {"error": str(e)}

        entry = {
            "format": fmt,
            "prompt": prompt,
            "timestamp": time.time(),
            "session_id": session_id,
            "result": res
        }
        results.append(entry)

    out_path = os.path.join(out_dir, "gundam_queries.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": time.time(), "queries": results}, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} query results to {out_path}")


if __name__ == "__main__":
    main()
