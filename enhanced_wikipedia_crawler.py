#!/usr/bin/env python3
"""
Enhanced Wikipedia Knowledge Base Crawler for Radeon SML

This script crawls comprehensive Wikipedia articles about robotics, AI, automation,
and related topics to build a much more extensive knowledge base for better AI responses.
"""

import requests
import json
import time
import re
from pathlib import Path
from urllib.parse import quote
from datetime import datetime
from typing import List, Dict, Set, Tuple
import random

class EnhancedWikipediaCrawler:
    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Radeon-SML-Knowledge-Crawler/1.0 (Educational; Contact: user@example.com)'
        })
        
        self.crawled_articles = set()
        self.knowledge_base = []
        self.crawl_stats = {
            "articles_crawled": 0,
            "total_words": 0,
            "failed_requests": 0,
            "start_time": datetime.now()
        }

    def get_wikipedia_content(self, title: str) -> Tuple[str, str, str]:
        """Fetch article content from Wikipedia API"""
        try:
            # Get page content
            content_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(title)
            content_response = self.session.get(content_url, timeout=10)
            
            if content_response.status_code != 200:
                print(f"❌ Failed to fetch summary for {title}: {content_response.status_code}")
                return None, None, None
            
            summary_data = content_response.json()
            
            # Get full page content
            full_url = f"https://en.wikipedia.org/api/rest_v1/page/html/{quote(title)}"
            full_response = self.session.get(full_url, timeout=15)
            
            if full_response.status_code != 200:
                print(f"⚠️ Using summary only for {title}")
                full_content = summary_data.get('extract', '')
            else:
                # Extract text from HTML (basic text extraction)
                html_content = full_response.text
                # Remove HTML tags and get text content
                text_content = re.sub(r'<[^>]+>', ' ', html_content)
                text_content = re.sub(r'\s+', ' ', text_content).strip()
                full_content = text_content[:50000]  # Limit to 50k chars
            
            return (
                summary_data.get('title', title),
                summary_data.get('extract', ''),
                full_content
            )
            
        except Exception as e:
            print(f"❌ Error fetching {title}: {e}")
            self.crawl_stats["failed_requests"] += 1
            return None, None, None

    def crawl_external_sources(self):
        """Crawl external academic and popular science sources"""
        print("\n🌐 Crawling external sources...")
        
        # arXiv AI ethics papers (metadata)
        arxiv_queries = ["AI+ethics", "machine+ethics", "algorithmic+fairness", "AI+bias"]
        for query in arxiv_queries[:2]:  # Limit queries
            try:
                url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    # Parse basic XML and extract titles/abstracts
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response.content)
                    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry')[:3]:
                        title_elem = entry.find('.//{http://www.w3.org/2005/Atom}title')
                        summary_elem = entry.find('.//{http://www.w3.org/2005/Atom}summary')
                        if title_elem is not None and summary_elem is not None:
                            title = title_elem.text.strip()
                            summary = summary_elem.text.strip()[:2000]
                            
                            article_data = {
                                "title": f"arXiv: {title}",
                                "url": f"https://arxiv.org/search/?query={query}",
                                "content": summary,
                                "summary": summary[:500],
                                "word_count": len(summary.split()),
                                "quality_score": 1.5,  # Academic papers get higher score
                                "domain": "academic",
                                "extracted_at": datetime.now().isoformat()
                            }
                            self.knowledge_base.append(article_data)
                            self.crawl_stats["articles_crawled"] += 1
                            print(f"✅ arXiv: {title[:50]}...")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ arXiv crawl error: {e}")
    
    def get_related_articles(self, title: str, max_related: int = 5) -> List[str]:
        """Get related articles from Wikipedia"""
        try:
            # Search for related articles
            search_url = "https://en.wikipedia.org/api/rest_v1/page/related/" + quote(title)
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                related_data = response.json()
                related_titles = []
                
                for page in related_data.get('pages', [])[:max_related]:
                    related_titles.append(page.get('title', ''))
                
                return [t for t in related_titles if t and t not in self.crawled_articles]
            
        except Exception as e:
            print(f"⚠️ Could not get related articles for {title}: {e}")
        
        return []

    def calculate_quality_score(self, content: str, summary: str) -> float:
        """Calculate quality score for content"""
        score = 1.0
        
        # Length factors
        if len(content) > 5000:
            score += 0.2
        elif len(content) > 2000:
            score += 0.1
        
        # Content quality indicators
        technical_terms = len(re.findall(r'\b(algorithm|system|technology|method|process|analysis|research|development|engineering|science)\b', content.lower()))
        score += min(technical_terms * 0.02, 0.3)
        
        # References and citations
        citations = len(re.findall(r'\[\d+\]', content))
        score += min(citations * 0.01, 0.2)
        
        # Completeness
        if summary and len(summary) > 200:
            score += 0.1
        
        return min(score, 2.0)

    def crawl_article(self, title: str, domain: str = "robotics") -> bool:
        """Crawl a single Wikipedia article"""
        if title in self.crawled_articles:
            return False
        
        print(f"📖 Crawling: {title}")
        
        article_title, summary, content = self.get_wikipedia_content(title)
        
        if not article_title or not content:
            return False
        
        # Process content
        word_count = len(content.split())
        quality_score = self.calculate_quality_score(content, summary)
        
        article_data = {
            "title": article_title,
            "url": f"https://en.wikipedia.org/wiki/{quote(title)}",
            "content": content,
            "summary": summary,
            "word_count": word_count,
            "quality_score": quality_score,
            "domain": domain,
            "extracted_at": datetime.now().isoformat()
        }
        
        self.knowledge_base.append(article_data)
        self.crawled_articles.add(title)
        
        self.crawl_stats["articles_crawled"] += 1
        self.crawl_stats["total_words"] += word_count
        
        print(f"✅ {article_title} - {word_count} words (quality: {quality_score:.2f})")
        
        # Rate limiting
        time.sleep(random.uniform(0.5, 1.5))
        
        return True

    def crawl_comprehensive_knowledge_base(self):
        """Crawl comprehensive robotics and AI knowledge"""
        
        print("🤖 Starting Enhanced Wikipedia Knowledge Crawling...")
        print("=" * 60)
        
        # Core robotics topics
        robotics_articles = [
            "Robot", "Robotics", "Industrial robot", "Autonomous robot", "Mobile robot",
            "Humanoid robot", "Robot operating system", "Robot locomotion", "Robot kinematics",
            "Robot dynamics", "Robot control", "Robot vision", "Robot manipulation",
            "Swarm robotics", "Medical robot", "Military robot", "Service robot",
            "Agricultural robot", "Space robot", "Underwater robot", "Robot ethics",
            "Human-robot interaction", "Robot learning", "Robot navigation",
            "Robot sensing", "Actuator", "Robot arm", "End effector", "Robot gripper"
        ]
        
        # AI and Machine Learning
        ai_articles = [
            "Artificial intelligence", "Machine learning", "Deep learning", "Neural network",
            "Computer vision", "Natural language processing", "Expert system",
            "Knowledge representation", "Machine reasoning", "Cognitive science",
            "Artificial neural network", "Convolutional neural network", "Recurrent neural network",
            "Reinforcement learning", "Supervised learning", "Unsupervised learning",
            "Transfer learning", "Feature learning", "Pattern recognition",
            "Speech recognition", "Image recognition", "Facial recognition",
            "AI ethics", "Explainable AI", "AI safety", "AI alignment"
        ]
        
        # Automation and Control
        automation_articles = [
            "Automation", "Control theory", "Control system", "Feedback control",
            "PID controller", "Programmable logic controller", "SCADA", "Industrial automation",
            "Process control", "Motion control", "Servo motor", "Stepper motor",
            "Sensor", "Actuator", "Human-machine interface", "Manufacturing execution system",
            "Computer-integrated manufacturing", "Flexible manufacturing system",
            "Automated guided vehicle", "Assembly line", "Quality control"
        ]
        
        # Advanced Technologies
        advanced_articles = [
            "Internet of Things", "Edge computing", "Cloud robotics", "5G technology",
            "Augmented reality", "Virtual reality", "Digital twin", "Blockchain",
            "Quantum computing", "Embedded system", "Real-time computing",
            "Distributed computing", "Parallel computing", "GPU computing",
            "FPGA", "Microcontroller", "Single-board computer", "Raspberry Pi", "Arduino"
        ]
        
        # Engineering and Mathematics
        engineering_articles = [
            "Systems engineering", "Software engineering", "Electrical engineering",
            "Mechanical engineering", "Control engineering", "Signal processing",
            "Digital signal processing", "Linear algebra", "Calculus", "Statistics",
            "Probability theory", "Optimization", "Algorithm", "Data structure",
            "Software architecture", "Design pattern", "Agile software development"
        ]
        
        # Industry and Applications
        industry_articles = [
            "Industry 4.0", "Smart factory", "Smart manufacturing", "Digital transformation",
            "Cyber-physical system", "Smart city", "Autonomous vehicle", "Drone",
            "3D printing", "Additive manufacturing", "Computer-aided design",
            "Computer-aided manufacturing", "Product lifecycle management",
            "Supply chain management", "Logistics", "Warehouse automation"
        ]
        
        # Ethics and Philosophy (Enhanced)
        ethics_articles = [
            "AI ethics", "Artificial intelligence ethics", "Robot ethics", "Roboethics",
            "Machine ethics", "Algorithmic bias", "Explainable artificial intelligence",
            "AI alignment", "AI safety", "Algorithmic accountability", "AI governance",
            "Laws of robotics", "Three Laws of Robotics", "Isaac Asimov",
            "Human-robot interaction", "Social robot", "Companion robot", "Robot rights",
            "Artificial moral agents", "Self-driving car", "Trolley problem",
            "Moral machine experiment", "Vehicle automation", "Autonomous car liability",
            "Ethics of self-driving cars", "Android (robot)", "Artificial consciousness",
            "Machine consciousness", "Synthetic biology ethics", "Transhumanism",
            "Cyborg", "Brain-computer interface", "Neural implant", "Human enhancement",
            "Technology ethics", "Computer ethics", "Information ethics",
            "Privacy", "Surveillance", "Digital rights", "Algorithmic transparency",
            "Artificial general intelligence", "Singularity", "Technological singularity",
            "Fairness (machine learning)", "AI bias", "Algorithmic fairness",
            "Ethics of artificial intelligence", "AI governance", "Responsible AI",
            "AI regulation", "AI policy", "Digital ethics", "Computational ethics"
        ]
        
        # Sci-Fi Ethics and Cultural Impact
        scifi_ethics_articles = [
            "Blade Runner", "Ex Machina", "Westworld", "Black Mirror", "I, Robot",
            "The Matrix", "Terminator (franchise)", "Ghost in the Shell",
            "Artificial intelligence in fiction", "Robot in science fiction",
            "Cyberpunk", "Transhumanism in fiction", "Android (robot)",
            "Cyborg in fiction", "AI takeover", "Technological dystopia",
            "Science fiction and prediction", "Ethics in science fiction",
            "Philosophy of artificial intelligence", "Mind uploading",
            "Digital immortality", "Posthumanism", "Bioethics"
        ]
        
        # Academic and Research Topics
        academic_articles = [
            "Machine learning ethics", "Algorithmic decision-making",
            "Automated decision support system", "Expert system ethics",
            "Neural network interpretability", "AI transparency",
            "Fairness through awareness", "Differential privacy",
            "Federated learning", "Adversarial machine learning",
            "AI safety research", "Value alignment problem",
            "Instrumental convergence", "Orthogonality thesis",
            "Intelligence explosion", "Friendly artificial intelligence",
            "AI control problem", "AI boxing", "Oracle AI",
            "Artificial consciousness", "Hard problem of consciousness",
            "Chinese room", "Turing test", "Moravec's paradox"
        ]
        
        # Combine all article lists
        all_articles = [
            ("robotics", robotics_articles),
            ("ai", ai_articles), 
            ("automation", automation_articles),
            ("advanced_tech", advanced_articles),
            ("engineering", engineering_articles),
            ("industry", industry_articles),
            ("ethics", ethics_articles),
            ("scifi_ethics", scifi_ethics_articles),
            ("academic", academic_articles)
        ]
        
        # Crawl articles by domain
        for domain, articles in all_articles:
            print(f"\n🔍 Crawling {domain.upper()} articles...")
            
            for article in articles:
                if self.crawl_article(article, domain):
                    # Get some related articles for deeper coverage
                    if len(self.crawled_articles) < 200:  # Limit total articles
                        related = self.get_related_articles(article, 2)
                        for related_article in related[:2]:  # Limit related articles
                            if len(self.crawled_articles) >= 200:
                                break
                            self.crawl_article(related_article, domain)
                
                # Progress update
                if self.crawl_stats["articles_crawled"] % 10 == 0:
                    elapsed = datetime.now() - self.crawl_stats["start_time"]
                    print(f"📊 Progress: {self.crawl_stats['articles_crawled']} articles, "
                          f"{self.crawl_stats['total_words']:,} words, "
                          f"{elapsed.total_seconds():.0f}s elapsed")
                
                # Safety limit
                if len(self.crawled_articles) >= 180:  # Leave room for external sources
                    print("🛑 Reached article limit (180), stopping crawl")
                    break
            
            if len(self.crawled_articles) >= 180:  # Leave room for external sources
                break
        
        # Crawl external sources
        if len(self.crawled_articles) < 200:
            self.crawl_external_sources()

    def save_knowledge_base(self):
        """Save the crawled knowledge base"""
        # Save main knowledge base
        output_file = self.output_dir / "enhanced_robotics_knowledge.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
        
        # Save crawl statistics
        stats_file = self.output_dir / "crawl_statistics.json"
        
        final_stats = {
            "articles_crawled": self.crawl_stats["articles_crawled"],
            "total_words": self.crawl_stats["total_words"],
            "failed_requests": self.crawl_stats["failed_requests"],
            "start_time": self.crawl_stats["start_time"].isoformat(),
            "end_time": datetime.now().isoformat(),
            "total_duration_seconds": (datetime.now() - self.crawl_stats["start_time"]).total_seconds(),
            "articles_per_minute": self.crawl_stats["articles_crawled"] / ((datetime.now() - self.crawl_stats["start_time"]).total_seconds() / 60),
            "average_words_per_article": self.crawl_stats["total_words"] / max(self.crawl_stats["articles_crawled"], 1),
            "knowledge_base_file": str(output_file)
        }
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(final_stats, f, indent=2)
        
        print(f"\n📚 Knowledge base saved: {output_file}")
        print(f"📊 Statistics saved: {stats_file}")
        
        return output_file, stats_file

    def print_final_summary(self):
        """Print crawling summary"""
        elapsed = datetime.now() - self.crawl_stats["start_time"]
        
        print("\n" + "=" * 60)
        print("🎉 ENHANCED KNOWLEDGE BASE CRAWLING COMPLETE!")
        print("=" * 60)
        print(f"📈 Articles crawled: {self.crawl_stats['articles_crawled']}")
        print(f"📖 Total words: {self.crawl_stats['total_words']:,}")
        print(f"⏱️ Total time: {elapsed.total_seconds():.1f} seconds")
        print(f"⚡ Rate: {self.crawl_stats['articles_crawled'] / (elapsed.total_seconds() / 60):.1f} articles/minute")
        print(f"📊 Average article length: {self.crawl_stats['total_words'] / max(self.crawl_stats['articles_crawled'], 1):.0f} words")
        print(f"❌ Failed requests: {self.crawl_stats['failed_requests']}")
        
        # Top domains
        domain_counts = {}
        for article in self.knowledge_base:
            domain = article.get('domain', 'unknown')
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        print(f"\n📂 Articles by domain:")
        for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {domain}: {count} articles")

def main():
    """Main crawling function"""
    print("🚀 Enhanced Wikipedia Knowledge Base Crawler")
    print("Building comprehensive robotics, AI, and automation knowledge...")
    
    crawler = EnhancedWikipediaCrawler()
    
    try:
        crawler.crawl_comprehensive_knowledge_base()
        output_file, stats_file = crawler.save_knowledge_base()
        crawler.print_final_summary()
        
        print(f"\n✅ SUCCESS! Enhanced knowledge base ready for Radeon SML")
        print(f"📁 Knowledge file: {output_file}")
        print(f"📊 Stats file: {stats_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Crawling interrupted by user")
        if crawler.knowledge_base:
            print("💾 Saving partial results...")
            crawler.save_knowledge_base()
            crawler.print_final_summary()
    
    except Exception as e:
        print(f"\n❌ Error during crawling: {e}")
        if crawler.knowledge_base:
            print("💾 Saving partial results...")
            crawler.save_knowledge_base()

if __name__ == "__main__":
    main()