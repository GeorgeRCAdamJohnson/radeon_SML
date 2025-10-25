#!/usr/bin/env python3
"""Call server.generate_gundam_response for desired formats and save outputs."""
import json
import os
import sys
import time

# Ensure repo root is importable
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import server


def main():
    formats = ["detailed", "essay", "standard", "summary", "list"]
    results = []

    out_dir = os.path.join(repo_root, "data")
    os.makedirs(out_dir, exist_ok=True)

    for fmt in formats:
        try:
            text = server.generate_gundam_response(fmt)
        except Exception as e:
            text = f"ERROR: {e}"

        results.append({
            "format": fmt,
            "response": text,
            "timestamp": time.time()
        })

    out_path = os.path.join(out_dir, "gundam_server_responses.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": time.time(), "responses": results}, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} responses to {out_path}")


if __name__ == "__main__":
    main()
