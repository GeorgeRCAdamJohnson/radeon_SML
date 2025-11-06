#!/usr/bin/env python3
import wikipedia
import json
import os
import time
from datetime import datetime

def crawl_ethics_articles():
    """Crawl Wikipedia for AI and robotics ethics articles"""
    
    ethics_topics = [
        # AI Ethics
        "AI ethics",
        "Artificial intelligence ethics", 
        "Algorithmic bias",
        "Explainable artificial intelligence",
        "AI alignment",
        "Machine ethics",
        "Artificial general intelligence",
        "AI safety",
        "Algorithmic accountability",
        "AI governance",
        
        # Robot Ethics
        "Robot ethics",
        "Roboethics",
        "Laws of robotics",
        "Isaac Asimov",
        "Three Laws of Robotics",
        "Human-robot interaction",
        "Social robot",
        "Companion robot",
        "Robot rights",
        "Artificial moral agents",
        
        # Autonomous Vehicle Ethics
        "Self-driving car",
        "Autonomous vehicle",
        "Trolley problem",
        "Moral machine experiment",
        "Vehicle automation",
        "Autonomous car liability",
        "Ethics of self-driving cars",
        
        # Synthetic Human Ethics
        "Android (robot)",
        "Humanoid robot",
        "Artificial consciousness",
        "Machine consciousness",
        "Synthetic biology ethics",
        "Transhumanism",
        "Cyborg",
        "Brain-computer interface",
        "Neural implant",
        "Human enhancement",
        
        # Related Ethics Topics
        "Technology ethics",
        "Computer ethics",
        "Information ethics",
        "Bioethics",
        "Medical ethics",
        "Research ethics",
        "Privacy",
        "Surveillance",
        "Digital rights",
        "Algorithmic transparency"
    ]
    
    articles = []
    failed_topics = []
    
    print(f"Starting ethics Wikipedia crawl for {len(ethics_topics)} topics...")
    
    for i, topic in enumerate(ethics_topics, 1):
        try:
            print(f"[{i}/{len(ethics_topics)}] Crawling: {topic}")
            
            # Search for the topic
            search_results = wikipedia.search(topic, results=3)
            if not search_results:
                print(f"  No results found for: {topic}")
                failed_topics.append(topic)
                continue
            
            # Get the first result
            page_title = search_results[0]
            page = wikipedia.page(page_title)
            
            # Extract content
            article = {
                "title": page.title,
                "url": page.url,
                "content": page.content,
                "summary": page.summary,
                "categories": getattr(page, 'categories', []),
                "links": page.links[:20],  # Limit links
                "word_count": len(page.content.split()),
                "crawled_date": datetime.now().isoformat(),
                "source_topic": topic,
                "domain": "ethics"
            }
            
            articles.append(article)
            print(f"  ✓ Crawled: {page.title} ({article['word_count']} words)")
            
            # Rate limiting
            time.sleep(1)
            
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                # Try the first disambiguation option
                page = wikipedia.page(e.options[0])
                article = {
                    "title": page.title,
                    "url": page.url,
                    "content": page.content,
                    "summary": page.summary,
                    "categories": getattr(page, 'categories', []),
                    "links": page.links[:20],
                    "word_count": len(page.content.split()),
                    "crawled_date": datetime.now().isoformat(),
                    "source_topic": topic,
                    "domain": "ethics"
                }
                articles.append(article)
                print(f"  ✓ Crawled (disambiguated): {page.title} ({article['word_count']} words)")
            except Exception as e2:
                print(f"  ✗ Failed after disambiguation: {topic} - {e2}")
                failed_topics.append(topic)
                
        except Exception as e:
            print(f"  ✗ Failed: {topic} - {e}")
            failed_topics.append(topic)
            
        # Progress update every 10 articles
        if i % 10 == 0:
            print(f"Progress: {i}/{len(ethics_topics)} topics processed")
    
    return articles, failed_topics

def save_articles(articles, output_dir="../data/wikipedia"):
    """Save articles to JSON files"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save individual articles
    for article in articles:
        filename = f"ethics_{article['title'].replace(' ', '_').replace('/', '_')}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
    
    # Save summary
    summary = {
        "total_articles": len(articles),
        "total_words": sum(a['word_count'] for a in articles),
        "crawl_date": datetime.now().isoformat(),
        "domain": "ethics",
        "articles": [{"title": a['title'], "word_count": a['word_count'], "url": a['url']} for a in articles]
    }
    
    with open(os.path.join(output_dir, "ethics_summary.json"), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    return summary

if __name__ == "__main__":
    print("AI and Robotics Ethics Wikipedia Crawler")
    print("=" * 50)
    
    # Crawl articles
    articles, failed = crawl_ethics_articles()
    
    # Save results
    summary = save_articles(articles)
    
    # Print results
    print("\n" + "=" * 50)
    print("CRAWL COMPLETE")
    print(f"✓ Successfully crawled: {len(articles)} articles")
    print(f"✓ Total words: {summary['total_words']:,}")
    print(f"✗ Failed topics: {len(failed)}")
    
    if failed:
        print("\nFailed topics:")
        for topic in failed:
            print(f"  - {topic}")
    
    print(f"\nArticles saved to: ../data/wikipedia/")
    print("Run this script to enhance your ethics knowledge base!")