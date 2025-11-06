#!/usr/bin/env python3
"""
Simple Wikipedia crawler runner without unicode issues
"""

import requests
import json
import time
from pathlib import Path
from urllib.parse import quote
from datetime import datetime

def get_wikipedia_content(title):
    """Fetch article content from Wikipedia API"""
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Radeon-SML-Knowledge-Crawler/1.0 (Educational)'
        })
        
        # Get page content
        content_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(title)
        content_response = session.get(content_url, timeout=10)
        
        if content_response.status_code != 200:
            print(f"Failed to fetch {title}: {content_response.status_code}")
            return None
        
        summary_data = content_response.json()
        
        # Get full page content
        full_url = f"https://en.wikipedia.org/api/rest_v1/page/html/{quote(title)}"
        full_response = session.get(full_url, timeout=15)
        
        if full_response.status_code == 200:
            import re
            html_content = full_response.text
            # Remove HTML tags and get text content
            text_content = re.sub(r'<[^>]+>', ' ', html_content)
            text_content = re.sub(r'\\s+', ' ', text_content).strip()
            full_content = text_content[:20000]  # Limit to 20k chars
        else:
            full_content = summary_data.get('extract', '')
        
        return {
            "title": summary_data.get('title', title),
            "url": f"https://en.wikipedia.org/wiki/{quote(title)}",
            "content": full_content,
            "summary": summary_data.get('extract', ''),
            "word_count": len(full_content.split()),
            "quality_score": 1.0,
            "domain": "robotics",
            "extracted_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error fetching {title}: {e}")
        return None

def main():
    print("Enhanced Wikipedia Knowledge Base Crawler")
    print("Building comprehensive robotics, AI, and automation knowledge...")
    
    # Comprehensive article list
    articles = [
        # Core robotics
        "Robot", "Robotics", "Industrial robot", "Autonomous robot", "Mobile robot",
        "Humanoid robot", "Robot operating system", "Robot locomotion", "Robot kinematics",
        "Robot dynamics", "Robot control", "Robot vision", "Robot manipulation",
        "Swarm robotics", "Medical robot", "Military robot", "Service robot",
        
        # AI and ML
        "Artificial intelligence", "Machine learning", "Deep learning", "Neural network",
        "Computer vision", "Natural language processing", "Expert system",
        "Reinforcement learning", "Supervised learning", "Unsupervised learning",
        
        # Automation
        "Automation", "Control theory", "Control system", "PID controller",
        "Industrial automation", "Process control", "Motion control", "Sensor",
        
        # Ethics
        "AI ethics", "Robot ethics", "Machine ethics", "Algorithmic bias",
        "AI alignment", "AI safety", "Three Laws of Robotics",
        
        # Advanced tech
        "Internet of Things", "Edge computing", "Cloud robotics", "Digital twin",
        "Augmented reality", "Virtual reality", "Autonomous vehicle",
        
        # Characters and fiction
        "Data (Star Trek)", "C-3PO", "R2-D2", "WALL-E", "Terminator",
        "HAL 9000", "Optimus Prime", "Blade Runner", "Ex Machina",
        
        # More robotics
        "Boston Dynamics", "ASIMO", "Pepper (robot)", "Sophia (robot)",
        "Robot arm", "End effector", "Actuator", "Servo motor",
        
        # More AI
        "GPT-3", "ChatGPT", "BERT", "Transformer (machine learning)",
        "Convolutional neural network", "Recurrent neural network",
        
        # Industry
        "Industry 4.0", "Smart factory", "Manufacturing", "Assembly line",
        "Quality control", "Predictive maintenance", "Digital transformation"
    ]
    
    knowledge_base = []
    crawled = 0
    total_words = 0
    
    for article in articles:
        print(f"Crawling: {article}")
        
        data = get_wikipedia_content(article)
        if data:
            knowledge_base.append(data)
            crawled += 1
            total_words += data['word_count']
            print(f"  Success: {data['word_count']} words")
        else:
            print(f"  Failed")
        
        # Rate limiting
        time.sleep(1)
        
        # Progress update
        if crawled % 10 == 0:
            print(f"Progress: {crawled} articles, {total_words:,} words")
    
    # Save results
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "enhanced_robotics_knowledge.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    
    print(f"\\nCrawling complete!")
    print(f"Articles: {crawled}")
    print(f"Total words: {total_words:,}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()