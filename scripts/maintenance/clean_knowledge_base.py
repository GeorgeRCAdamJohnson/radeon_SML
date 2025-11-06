#!/usr/bin/env python3
"""
Quick Knowledge Base Content Cleaner
Cleans existing knowledge base without re-crawling
"""

import json
import re
from pathlib import Path

def aggressive_clean_content(content):
    """Aggressively clean malformed content"""
    if not content:
        return content
    
    # Remove MediaWiki parser output and CSS
    content = re.sub(r'\.mw-parser-output[^}]*}', '', content)
    content = re.sub(r'@media[^}]*\{[^}]*\}', '', content)
    content = re.sub(r'\.[a-zA-Z-]+\{[^}]*\}', '', content)
    
    # Remove complex JSON/template structures
    content = re.sub(r'\{"[^"]*":[^}]*\}', '', content)
    content = re.sub(r'\{[^}]*"target"[^}]*\}', '', content)
    content = re.sub(r'\{[^}]*"template"[^}]*\}', '', content)
    content = re.sub(r'\{[^}]*"params"[^}]*\}', '', content)
    content = re.sub(r'\{[^}]*"wt"[^}]*\}', '', content)
    content = re.sub(r'\{[^}]*"href"[^}]*\}', '', content)
    
    # Remove HTML tags and attributes
    content = re.sub(r'<[^>]+>', ' ', content)
    content = re.sub(r'&lt;[^&]*&gt;', ' ', content)
    
    # Remove HTML entities
    content = re.sub(r'&[a-zA-Z0-9#]+;', ' ', content)
    content = re.sub(r'&quot;', '"', content)
    content = re.sub(r'&amp;', '&', content)
    
    # Remove Wikipedia artifacts
    content = re.sub(r'\[\d+\]', '', content)
    content = re.sub(r'\{\{[^}]*\}\}', '', content)
    content = re.sub(r'\[\[[^\]]*\]\]', '', content)
    
    # Remove CSS and style attributes
    content = re.sub(r'(class|id|style|data-[^=]*)="[^"]*"', '', content)
    content = re.sub(r'(font-style|padding|margin|color|background)[^;]*;', '', content)
    
    # Remove malformed JSON fragments
    content = re.sub(r'"[^"]*":[^,}]*[,}]', '', content)
    content = re.sub(r'"i":\d+', '', content)
    content = re.sub(r'"\n\n"', ' ', content)
    
    # Clean up artifacts
    content = re.sub(r'[{}[\]"\\]+', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'^[\s,.:;-]+', '', content)
    content = re.sub(r'[\s,.:;-]+$', '', content)
    
    return content.strip()

def clean_knowledge_base():
    """Clean the existing knowledge base"""
    kb_file = Path("data/enhanced_robotics_knowledge.json")
    
    if not kb_file.exists():
        print("Knowledge base file not found")
        return
    
    print("Loading knowledge base...")
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb_data = json.load(f)
    
    cleaned_count = 0
    total_articles = len(kb_data) if isinstance(kb_data, list) else len(kb_data.get('articles', []))
    
    print(f"Cleaning {total_articles} articles...")
    
    # Handle both list and dict formats
    articles = kb_data if isinstance(kb_data, list) else kb_data.get('articles', [])
    
    for article in articles:
        if isinstance(article, dict) and 'content' in article:
            original_content = article['content']
            cleaned_content = aggressive_clean_content(original_content)
            
            if cleaned_content != original_content:
                article['content'] = cleaned_content
                cleaned_count += 1
                
                # Also clean summary if present
                if 'summary' in article:
                    article['summary'] = aggressive_clean_content(article['summary'])
    
    # Save cleaned knowledge base
    backup_file = kb_file.with_suffix('.backup.json')
    print(f"Creating backup: {backup_file}")
    if backup_file.exists():
        backup_file.unlink()
    kb_file.rename(backup_file)
    
    print(f"Saving cleaned knowledge base...")
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, indent=2, ensure_ascii=False)
    
    print(f"[SUCCESS] Cleaned {cleaned_count}/{total_articles} articles")
    print(f"[SUCCESS] Backup saved as: {backup_file}")
    print(f"[SUCCESS] Clean knowledge base saved: {kb_file}")

if __name__ == "__main__":
    clean_knowledge_base()