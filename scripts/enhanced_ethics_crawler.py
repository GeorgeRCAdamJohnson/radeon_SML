#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin, urlparse
import re

class EnhancedEthicsCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.data = []
        
    def crawl_wikipedia_ethics(self):
        """Crawl AI ethics Wikipedia pages"""
        ethics_pages = [
            "Ethics_of_artificial_intelligence", "AI_alignment", "Algorithmic_bias",
            "Machine_ethics", "Artificial_general_intelligence", "AI_safety",
            "Explainable_artificial_intelligence", "Fairness_(machine_learning)",
            "AI_governance", "Responsible_AI", "AI_ethics", "Robot_ethics",
            "Algorithmic_accountability", "AI_transparency", "Digital_ethics",
            "Computational_ethics", "Technology_ethics", "Computer_ethics",
            "Information_ethics", "Bioethics", "Medical_ethics", "Research_ethics",
            "Engineering_ethics", "Professional_ethics", "Applied_ethics"
        ]
        
        for page in ethics_pages:
            try:
                url = f"https://en.wikipedia.org/wiki/{page}"
                response = self.session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                content = soup.find('div', {'id': 'mw-content-text'})
                if content:
                    text = content.get_text()
                    self.data.append({
                        'source': 'Wikipedia',
                        'title': page.replace('_', ' '),
                        'url': url,
                        'content': text[:5000],
                        'category': 'AI Ethics'
                    })
                time.sleep(1)
            except Exception as e:
                print(f"Error crawling {page}: {e}")
    
    def crawl_popular_science_topics(self):
        """Crawl popular science and technology topics"""
        # Use Wikipedia for popular science topics since direct site crawling may be blocked
        pop_science_topics = [
            "Popular_Mechanics", "Popular_Science", "MIT_Technology_Review",
            "Wired_(magazine)", "IEEE_Spectrum", "Scientific_American",
            "Technology_journalism", "Science_communication",
            "Emerging_technologies", "Future_technology"
        ]
        
        for topic in pop_science_topics:
            try:
                url = f"https://en.wikipedia.org/wiki/{topic}"
                response = self.session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                content = soup.find('div', {'id': 'mw-content-text'})
                if content:
                    text = content.get_text()[:3000]
                    self.data.append({
                        'source': 'Popular Science Wiki',
                        'title': topic.replace('_', ' '),
                        'url': url,
                        'content': text,
                        'category': 'Popular Science'
                    })
                time.sleep(1)
            except Exception as e:
                print(f"Error crawling {topic}: {e}")
    
    def crawl_scifi_ethics(self):
        """Crawl sci-fi AI ethics content"""
        scifi_topics = [
            "Isaac_Asimov", "Three_Laws_of_Robotics", "Blade_Runner", "Ex_Machina",
            "Westworld", "Black_Mirror", "I,_Robot", "The_Matrix", "Terminator_(franchise)",
            "Artificial_intelligence_in_fiction", "Robot_in_science_fiction",
            "Cyberpunk", "Transhumanism_in_fiction", "Android_(robot)",
            "Cyborg_in_fiction", "AI_takeover", "Technological_dystopia",
            "Ghost_in_the_Shell", "2001:_A_Space_Odyssey", "HAL_9000",
            "Star_Trek", "Data_(Star_Trek)", "Philosophy_of_artificial_intelligence",
            "Mind_uploading", "Digital_immortality", "Posthumanism",
            "Science_fiction_and_prediction", "Ethics_in_science_fiction"
        ]
        
        for topic in scifi_topics:
            try:
                url = f"https://en.wikipedia.org/wiki/{topic}"
                response = self.session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                content = soup.find('div', {'id': 'mw-content-text'})
                if content:
                    text = content.get_text()
                    self.data.append({
                        'source': 'Wikipedia Sci-Fi',
                        'title': topic.replace('_', ' '),
                        'url': url,
                        'content': text[:4000],
                        'category': 'Sci-Fi Ethics'
                    })
                time.sleep(1)
            except Exception as e:
                print(f"Error crawling {topic}: {e}")
    
    def crawl_arxiv_ethics(self):
        """Crawl arXiv AI ethics papers (metadata only)"""
        ethics_queries = [
            "AI+ethics", "machine+ethics", "algorithmic+fairness", 
            "AI+bias", "explainable+AI", "AI+governance"
        ]
        
        for query in ethics_queries:
            try:
                url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=10"
                response = self.session.get(url)
                
                if response.status_code == 200:
                    # Use regex to extract titles and summaries from XML
                    import re
                    content = response.text
                    
                    # Extract entries using regex
                    entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
                    
                    for entry in entries[:5]:  # Limit to 5 per query
                        title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                        summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                        
                        if title_match and summary_match:
                            title = title_match.group(1).strip()
                            summary = summary_match.group(1).strip()[:1000]
                            
                            self.data.append({
                                'source': 'arXiv',
                                'title': title,
                                'content': summary,
                                'category': 'Academic Research'
                            })
                
                time.sleep(2)
            except Exception as e:
                print(f"Error crawling arXiv {query}: {e}")
    
    def save_data(self, filename='enhanced_ethics_data.json'):
        """Save crawled data to JSON file"""
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.data)} articles to {filepath}")
        
        # Print statistics
        sources = {}
        categories = {}
        for item in self.data:
            sources[item['source']] = sources.get(item['source'], 0) + 1
            categories[item['category']] = categories.get(item['category'], 0) + 1
        
        print("\nSources:")
        for source, count in sources.items():
            print(f"  {source}: {count} articles")
        
        print("\nCategories:")
        for category, count in categories.items():
            print(f"  {category}: {count} articles")

def main():
    crawler = EnhancedEthicsCrawler()
    
    print("Starting enhanced ethics data crawling...")
    
    print("1. Crawling Wikipedia AI Ethics pages...")
    crawler.crawl_wikipedia_ethics()
    
    print("2. Crawling Popular Science topics...")
    crawler.crawl_popular_science_topics()
    
    print("3. Crawling Sci-Fi Ethics content...")
    crawler.crawl_scifi_ethics()
    
    print("4. Crawling arXiv papers...")
    crawler.crawl_arxiv_ethics()
    
    print("5. Saving data...")
    crawler.save_data()
    
    print("Enhanced ethics crawling complete!")

if __name__ == "__main__":
    main()