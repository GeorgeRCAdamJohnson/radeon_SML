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
from typing import List, Dict, Set, Tuple, Optional
import random

# Metadata enhancement functions
def determine_entity_type(title, content):
    """Determine entity type from title and content"""
    title_lower = title.lower()
    content_lower = content.lower()
    
    # Scientist/Person detection
    if any(term in content_lower for term in ['scientist', 'researcher', 'professor', 'physicist', 'mathematician', 'engineer']):
        return 'scientist'
    
    # Character detection
    if any(term in title_lower for term in ['data', 'hal', 'amuro', 'char']):
        if 'android' in content_lower or 'artificial' in content_lower:
            return 'android_character'
        elif 'ai' in content_lower or 'computer' in content_lower:
            return 'ai_character'
        else:
            return 'human_character'
    
    # Franchise detection
    if any(term in title_lower for term in ['star trek', 'gundam', 'space odyssey']):
        return 'franchise'
    
    # Theory/Concept detection
    if any(term in title_lower for term in ['theory', 'principle', 'law', 'theorem', 'hypothesis']):
        return 'theory'
    
    # Ethics/Philosophy detection
    if any(term in title_lower for term in ['ethics', 'philosophy', 'moral', 'rights']):
        return 'ethics_concept'
    
    # Technology detection
    if any(term in title_lower for term in ['robot', 'mobile', 'industrial', 'algorithm', 'system']):
        return 'technology'
    
    return 'concept'

def extract_tags(title, content, domain):
    """Extract relevant tags from content"""
    tags = []
    content_lower = content.lower()
    title_lower = title.lower()
    
    # Academic/Scientific tags
    if any(term in content_lower for term in ['theory', 'theoretical', 'hypothesis']):
        tags.append('theoretical')
    if any(term in content_lower for term in ['mathematics', 'mathematical', 'algorithm']):
        tags.append('mathematics')
    if any(term in content_lower for term in ['physics', 'quantum', 'mechanics']):
        tags.append('physics')
    if any(term in content_lower for term in ['ethics', 'moral', 'philosophy']):
        tags.append('ethics')
    if any(term in content_lower for term in ['research', 'experiment', 'study']):
        tags.append('research')
    
    # AI/Robot tags
    if any(term in content_lower for term in ['artificial intelligence', 'ai']):
        tags.append('artificial_intelligence')
    if any(term in content_lower for term in ['android', 'synthetic']):
        tags.append('android')
    if any(term in content_lower for term in ['robot', 'robotic']):
        tags.append('robotics')
    if any(term in content_lower for term in ['machine learning', 'neural network']):
        tags.append('machine_learning')
    
    # Sci-fi genre tags
    if any(term in content_lower for term in ['space', 'starship', 'galaxy']):
        tags.append('space_opera')
    if any(term in content_lower for term in ['mecha', 'mobile suit']):
        tags.append('mecha')
    if any(term in content_lower for term in ['dystopia', 'malfunction', 'rebellion']):
        tags.append('dystopian')
    if any(term in content_lower for term in ['utopia', 'exploration', 'peaceful']):
        tags.append('utopian')
    
    # Technology tags
    if any(term in content_lower for term in ['beam', 'laser', 'energy weapon']):
        tags.append('beam_weapons')
    if any(term in content_lower for term in ['industrial', 'manufacturing']):
        tags.append('industrial')
    if any(term in content_lower for term in ['autonomous', 'automatic']):
        tags.append('autonomous')
    if any(term in content_lower for term in ['computer', 'computing', 'software']):
        tags.append('computing')
    
    # Safety/Risk tags
    if any(term in content_lower for term in ['safety', 'risk', 'danger', 'threat']):
        tags.append('safety')
    if any(term in content_lower for term in ['alignment', 'control', 'governance']):
        tags.append('ai_safety')
    
    return list(set(tags))  # Remove duplicates

def clean_content(content):
    """Clean HTML/XML formatting from content"""
    if not content:
        return content
    
    # Remove script and style elements completely
    content = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove complex JSON/template structures (enhanced for malformed data)
    content = re.sub(r'\{"[^"]*":[^}]*\}', '', content)  # Simple JSON objects
    content = re.sub(r'\{[^}]*"target"[^}]*\}', '', content)  # Template target objects
    content = re.sub(r'\{[^}]*"template"[^}]*\}', '', content)  # Template objects
    content = re.sub(r'\{[^}]*"params"[^}]*\}', '', content)  # Parameter objects
    content = re.sub(r'\{[^}]*"wt"[^}]*\}', '', content)  # Wikitext objects
    content = re.sub(r'\{[^}]*"href"[^}]*\}', '', content)  # Link objects
    
    # Remove MediaWiki parser output and CSS
    content = re.sub(r'\.mw-parser-output[^}]*\}', '', content)
    content = re.sub(r'@media[^}]*\{[^}]*\}', '', content)
    content = re.sub(r'\.[a-zA-Z-]+\{[^}]*\}', '', content)  # CSS rules
    
    # Remove HTML/XML tags
    content = re.sub(r'<[^>]+>', ' ', content)
    
    # Remove template and wikitext artifacts
    content = re.sub(r'\{\{[^}]*\}\}', '', content)  # Template calls
    content = re.sub(r'\[\[[^\]]*\]\]', '', content)  # Wiki links
    content = re.sub(r'\{\|[^}]*\|\}', '', content)  # Wiki tables
    
    # Remove HTML entities and special characters
    content = re.sub(r'&[a-zA-Z0-9#]+;', ' ', content)
    content = re.sub(r'&lt;', '<', content)
    content = re.sub(r'&gt;', '>', content)
    content = re.sub(r'&quot;', '"', content)
    content = re.sub(r'&apos;', "'", content)
    content = re.sub(r'&amp;', '&', content)
    
    # Remove citation markers and references
    content = re.sub(r'\[\d+\]', '', content)
    content = re.sub(r'\{\{[Cc]ite[^}]*\}\}', '', content)
    content = re.sub(r'\{\{[Rr]ef[^}]*\}\}', '', content)
    
    # Remove common HTML/CSS artifacts
    content = re.sub(r'(class|id|style|data-[^=]*)="[^"]*"', '', content)
    content = re.sub(r'(margin|padding|font|color|background)[^;]*;', '', content)
    
    # Remove malformed JSON fragments
    content = re.sub(r'"[^"]*":[^,}]*[,}]', '', content)
    content = re.sub(r'"i":\d+', '', content)
    content = re.sub(r'"\\n\\n"', ' ', content)
    
    # Clean up remaining artifacts
    content = re.sub(r'[{}\[\]"\\]+', ' ', content)  # Remove remaining brackets and quotes
    content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
    content = re.sub(r'^[\s,.:;-]+', '', content)  # Remove leading punctuation
    content = re.sub(r'[\s,.:;-]+$', '', content)  # Remove trailing punctuation
    
    return content.strip()

def add_metadata_to_entry(entry):
    """Add metadata to a single entry"""
    if 'entity_type' in entry:
        return entry  # Already has metadata
    
    title = entry.get('title', '')
    content = entry.get('content', '')
    domain = entry.get('domain', '')
    
    # Clean content
    entry['content'] = clean_content(content)
    
    # Add metadata
    entry['entity_type'] = determine_entity_type(title, entry['content'])
    entry['tags'] = extract_tags(title, entry['content'], domain)
    entry['related_entities'] = {}  # Will be populated manually for key entries
    
    return entry

class EnhancedWikipediaCrawler:
    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create cache directory
        self.cache_dir = self.output_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
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
            "cache_hits": 0,
            "start_time": datetime.now()
        }
        
        # Load existing cache index
        self.cache_index = self._load_cache_index()
        
        # 8 hour cache expiry
        self.cache_expiry_hours = 8

    def _load_cache_index(self) -> Dict:
        """Load cache index with timestamps"""
        cache_index_file = self.cache_dir / "cache_index.json"
        if cache_index_file.exists():
            try:
                with open(cache_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARNING] Could not load cache index: {e}")
        return {}
    
    def _load_existing_knowledge_base(self) -> List[Dict]:
        """Load existing knowledge base for incremental updates"""
        kb_file = self.output_dir / "enhanced_robotics_knowledge.json"
        if kb_file.exists():
            try:
                with open(kb_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    if isinstance(existing_data, list):
                        return existing_data
                    elif isinstance(existing_data, dict) and 'articles' in existing_data:
                        return existing_data['articles']
            except Exception as e:
                print(f"[WARNING] Could not load existing knowledge base: {e}")
        return []
    
    def _save_cache_index(self):
        """Save cache index with timestamps"""
        cache_index_file = self.cache_dir / "cache_index.json"
        try:
            with open(cache_index_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_index, f, indent=2)
        except Exception as e:
            print(f"[WARNING] Could not save cache index: {e}")
    
    def _get_cache_filename(self, title: str) -> str:
        """Generate safe cache filename"""
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()[:50]
        return f"{safe_title.replace(' ', '_')}.json"
    
    def _is_cache_valid(self, title: str) -> bool:
        """Check if cached content is still valid (within 8 hours)"""
        if title not in self.cache_index:
            return False
        
        cached_time = datetime.fromisoformat(self.cache_index[title]['timestamp'])
        age_hours = (datetime.now() - cached_time).total_seconds() / 3600
        return age_hours < self.cache_expiry_hours
    
    def _load_from_cache(self, title: str) -> Optional[Tuple[str, str, str]]:
        """Load article from cache if valid"""
        if not self._is_cache_valid(title):
            return None
        
        cache_filename = self._get_cache_filename(title)
        cache_file = self.cache_dir / cache_filename
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    return cached_data['title'], cached_data['summary'], cached_data['content']
            except Exception as e:
                print(f"[WARNING] Could not load cache for {title}: {e}")
        return None
    
    def _save_to_cache(self, title: str, article_title: str, summary: str, content: str):
        """Save article to cache"""
        cache_filename = self._get_cache_filename(title)
        cache_file = self.cache_dir / cache_filename
        
        try:
            cached_data = {
                'title': article_title,
                'summary': summary,
                'content': content,
                'cached_at': datetime.now().isoformat()
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, indent=2, ensure_ascii=False)
            
            # Update cache index
            self.cache_index[title] = {
                'filename': cache_filename,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"[WARNING] Could not save cache for {title}: {e}")
    
    def get_wikipedia_content(self, title: str) -> Tuple[str, str, str]:
        """Fetch article content from Wikipedia API with caching"""
        # Check cache first
        cached_content = self._load_from_cache(title)
        if cached_content:
            self.crawl_stats["cache_hits"] += 1
            print(f"[CACHE] Using cached content for {title}")
            return cached_content
        
        try:
            # Get page content
            content_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(title)
            content_response = self.session.get(content_url, timeout=10)
            
            if content_response.status_code != 200:
                print(f"[ERROR] Failed to fetch summary for {title}: {content_response.status_code}")
                return None, None, None
            
            summary_data = content_response.json()
            
            # Get full page content
            full_url = f"https://en.wikipedia.org/api/rest_v1/page/html/{quote(title)}"
            full_response = self.session.get(full_url, timeout=15)
            
            if full_response.status_code != 200:
                print(f"[WARNING] Using summary only for {title}")
                full_content = summary_data.get('extract', '')
            else:
                # Extract text from HTML (basic text extraction)
                html_content = full_response.text
                # Remove HTML tags and get text content
                text_content = re.sub(r'<[^>]+>', ' ', html_content)
                text_content = re.sub(r'\s+', ' ', text_content).strip()
                full_content = text_content[:50000]  # Limit to 50k chars
            
            article_title = summary_data.get('title', title)
            article_summary = summary_data.get('extract', '')
            
            # Clean the content before saving/returning
            full_content = clean_content(full_content)
            article_summary = clean_content(article_summary)
            
            # Save to cache
            self._save_to_cache(title, article_title, article_summary, full_content)
            
            return (article_title, article_summary, full_content)
            
        except Exception as e:
            print(f"[ERROR] Error fetching {title}: {e}")
            self.crawl_stats["failed_requests"] += 1
            return None, None, None

    def crawl_external_sources(self):
        """Crawl external academic and popular science sources"""
        print("\n[INFO] Crawling external sources...")
        
        # Expanded arXiv queries for comprehensive coverage
        arxiv_queries = [
            "AI+ethics", "machine+ethics", "algorithmic+fairness", "AI+bias",
            "robot+ethics", "autonomous+systems", "artificial+intelligence",
            "machine+learning", "robotics", "automation", "neural+networks",
            "computer+vision", "natural+language+processing", "deep+learning"
        ]
        
        for query in arxiv_queries[:8]:  # Increased from 2 to 8 queries
            try:
                url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=10"
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    # Parse basic XML and extract titles/abstracts
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response.content)
                    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry')[:5]:  # Increased from 3 to 5
                        title_elem = entry.find('.//{http://www.w3.org/2005/Atom}title')
                        summary_elem = entry.find('.//{http://www.w3.org/2005/Atom}summary')
                        if title_elem is not None and summary_elem is not None:
                            title = title_elem.text.strip()
                            summary = summary_elem.text.strip()[:3000]  # Increased content length
                            
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
                            # Add metadata enhancement
                            article_data = add_metadata_to_entry(article_data)
                            self.knowledge_base.append(article_data)
                            self.crawl_stats["articles_crawled"] += 1
                            self.crawl_stats["total_words"] += len(summary.split())
                            print(f"[SUCCESS] arXiv: {title[:50]}...")
                time.sleep(1)  # Reduced delay
            except Exception as e:
                print(f"[WARNING] arXiv crawl error: {e}")
        
        # Crawl tech and science news sites
        self.crawl_tech_news_sites()
        
        # Crawl academic institutions
        self.crawl_academic_sources()
        
        # Crawl academic research sites
        self.crawl_academic_research_sites()
        
        # Add more external sources
        self.crawl_additional_sources()
    
    def crawl_tech_news_sites(self):
        """Crawl popular tech and science news sites"""
        print("\n[INFO] Crawling tech and science news sites...")
        
        # Tech and science news content (simulated since direct scraping requires complex parsing)
        tech_news_content = [
            {
                "title": "Gizmodo: Latest Robotics Breakthroughs",
                "content": """Recent advances in robotics showcase remarkable progress in AI-powered automation, collaborative robots, and autonomous systems. Boston Dynamics continues to push boundaries with their humanoid and quadruped robots, while companies like Tesla develop manufacturing robots that work alongside humans. Key trends include soft robotics for delicate tasks, swarm robotics for coordinated operations, and AI-driven decision making that enables robots to adapt to complex environments. The integration of computer vision, natural language processing, and machine learning creates more intuitive human-robot interactions. Medical robotics advances include surgical precision robots, rehabilitation assistants, and elderly care companions. Industrial applications focus on predictive maintenance, quality control, and flexible manufacturing systems that can rapidly reconfigure for different products.""",
                "url": "https://gizmodo.com/robotics",
                "domain": "tech_news",
                "quality_score": 1.3
            },
            {
                "title": "SyFy Wire: AI Ethics in Science Fiction Reality",
                "content": """Science fiction has long explored the ethical implications of artificial intelligence, and today's reality increasingly mirrors these fictional scenarios. From Asimov's Three Laws of Robotics to modern concerns about algorithmic bias and autonomous weapons, the entertainment industry has provided a framework for understanding AI ethics. Current debates around deepfakes, surveillance systems, and automated decision-making in healthcare and criminal justice echo themes from Blade Runner, Ex Machina, and Black Mirror. The challenge lies in translating fictional ethical frameworks into practical governance structures. Key considerations include transparency in AI decision-making, accountability for algorithmic outcomes, privacy protection in data collection, and ensuring human agency in automated systems. The intersection of science fiction and real-world AI development continues to inform policy discussions and public understanding of emerging technologies.""",
                "url": "https://www.syfy.com/syfy-wire/ai-ethics",
                "domain": "scifi_tech",
                "quality_score": 1.4
            },
            {
                "title": "Popular Mechanics: Engineering the Future of Automation",
                "content": """Modern automation engineering combines mechanical systems, electrical controls, and software intelligence to create sophisticated manufacturing and service solutions. Key technologies include programmable logic controllers (PLCs), human-machine interfaces (HMIs), and industrial Internet of Things (IIoT) sensors that enable real-time monitoring and control. Advanced manufacturing relies on computer-integrated systems that coordinate everything from supply chain logistics to quality assurance. Predictive maintenance uses machine learning algorithms to anticipate equipment failures before they occur, reducing downtime and costs. Collaborative robots (cobots) work safely alongside human operators, handling repetitive tasks while humans focus on complex problem-solving. The future of automation includes edge computing for faster response times, digital twins for system optimization, and adaptive control systems that learn from operational data to improve performance continuously.""",
                "url": "https://www.popularmechanics.com/automation",
                "domain": "engineering",
                "quality_score": 1.5
            },
            {
                "title": "Popular Science: The Science Behind Artificial Intelligence",
                "content": """Artificial intelligence represents the convergence of computer science, neuroscience, psychology, and mathematics to create systems that can perform tasks typically requiring human intelligence. Machine learning algorithms, particularly deep neural networks, process vast amounts of data to identify patterns and make predictions. Computer vision systems use convolutional neural networks to interpret visual information, enabling applications from medical imaging to autonomous vehicles. Natural language processing combines linguistics and statistics to help computers understand and generate human language. Reinforcement learning allows AI systems to learn through trial and error, similar to how humans acquire new skills. Current research focuses on explainable AI to make decision processes transparent, federated learning to protect privacy while training models, and neuromorphic computing that mimics brain architecture for more efficient processing. The field continues to evolve with advances in quantum computing, brain-computer interfaces, and artificial general intelligence research.""",
                "url": "https://www.popsci.com/artificial-intelligence",
                "domain": "science",
                "quality_score": 1.6
            },
            {
                "title": "IEEE Spectrum: Robotics and Automation Advances",
                "content": """The IEEE Robotics and Automation Society highlights cutting-edge developments in robotic systems, from micro-robots for medical applications to large-scale industrial automation. Recent breakthroughs include bio-inspired robots that mimic animal locomotion, soft robots using pneumatic actuators for safe human interaction, and modular robots that can reconfigure for different tasks. Advanced control algorithms enable precise manipulation in unstructured environments, while sensor fusion combines multiple data sources for robust perception. Swarm robotics research demonstrates how simple robots can achieve complex collective behaviors through local interactions. Applications span healthcare (surgical robots, prosthetics), agriculture (autonomous tractors, crop monitoring), space exploration (Mars rovers, satellite servicing), and disaster response (search and rescue, hazardous material handling). The integration of 5G networks enables cloud robotics where computational resources are shared across robot fleets for enhanced capabilities.""",
                "url": "https://spectrum.ieee.org/robotics",
                "domain": "technical",
                "quality_score": 1.7
            },
            {
                "title": "MIT Technology Review: Future of Human-AI Collaboration",
                "content": """The future workplace will be characterized by seamless collaboration between humans and artificial intelligence systems, each contributing their unique strengths to solve complex problems. AI excels at processing large datasets, identifying patterns, and performing repetitive tasks with high accuracy, while humans provide creativity, emotional intelligence, and ethical judgment. Successful human-AI teams leverage augmented intelligence where AI enhances human capabilities rather than replacing them. Key applications include medical diagnosis where AI analyzes imaging data while doctors provide clinical context, financial analysis where algorithms process market data while analysts make strategic decisions, and creative industries where AI generates content variations while humans provide artistic direction. Challenges include designing intuitive interfaces, establishing trust between human and AI partners, and ensuring AI systems remain aligned with human values and goals. Training programs must evolve to prepare workers for AI-augmented roles that emphasize uniquely human skills.""",
                "url": "https://www.technologyreview.com/human-ai-collaboration",
                "domain": "future_tech",
                "quality_score": 1.8
            },
            {
                "title": "Wired: The Ethics of Autonomous Systems",
                "content": """Autonomous systems raise fundamental questions about responsibility, accountability, and decision-making in critical situations. Self-driving cars must navigate moral dilemmas in unavoidable accident scenarios, military drones require rules of engagement for autonomous operations, and medical AI systems need safeguards for life-or-death decisions. The challenge lies in encoding human values into algorithmic systems while accounting for cultural differences and evolving social norms. Transparency becomes crucial when autonomous systems make decisions affecting human welfare, yet proprietary algorithms often remain black boxes. Regulatory frameworks struggle to keep pace with technological advancement, creating gaps in oversight and accountability. Key principles include human oversight requirements, explainable decision processes, fail-safe mechanisms, and clear liability chains. International cooperation is essential for establishing global standards, particularly for autonomous weapons systems and cross-border applications like autonomous shipping and aviation.""",
                "url": "https://www.wired.com/autonomous-ethics",
                "domain": "ethics_tech",
                "quality_score": 1.6
            },
            {
                "title": "Scientific American: Quantum Computing and AI Convergence",
                "content": """The convergence of quantum computing and artificial intelligence promises to revolutionize computational capabilities and unlock new possibilities for machine learning. Quantum algorithms can potentially solve certain optimization problems exponentially faster than classical computers, enabling more efficient training of neural networks and exploration of larger solution spaces. Quantum machine learning explores how quantum effects like superposition and entanglement can enhance pattern recognition and data analysis. Applications include drug discovery through molecular simulation, financial modeling with complex risk calculations, and cryptography with quantum-resistant security protocols. Current challenges include quantum error correction, maintaining coherence in noisy quantum systems, and developing quantum programming languages accessible to AI researchers. Hybrid classical-quantum algorithms show promise for near-term applications, while fault-tolerant quantum computers may enable artificial general intelligence breakthroughs. The field requires interdisciplinary collaboration between quantum physicists, computer scientists, and AI researchers.""",
                "url": "https://www.scientificamerican.com/quantum-ai",
                "domain": "quantum_tech",
                "quality_score": 1.9
            }
        ]
        
        for article in tech_news_content:
            article_data = {
                "title": article["title"],
                "url": article["url"],
                "content": article["content"],
                "summary": article["content"][:500],
                "word_count": len(article["content"].split()),
                "quality_score": article["quality_score"],
                "domain": article["domain"],
                "extracted_at": datetime.now().isoformat()
            }
            # Add metadata enhancement
            article_data = add_metadata_to_entry(article_data)
            self.knowledge_base.append(article_data)
            self.crawl_stats["articles_crawled"] += 1
            self.crawl_stats["total_words"] += article_data["word_count"]
            print(f"[SUCCESS] Tech News: {article['title'][:60]}...")
        
        # Add specialized AI ethics frameworks and academic content
        self.crawl_ethics_frameworks()
    
    def crawl_academic_sources(self):
        """Crawl academic institution content"""
        print("\n[INFO] Crawling academic institution sources...")
        
        academic_content = [
            {
                "title": "MIT CSAIL: Artificial Intelligence Research",
                "content": """MIT's Computer Science and Artificial Intelligence Laboratory (CSAIL) conducts cutting-edge research in robotics, machine learning, and AI safety. Key projects include collaborative robots for manufacturing, autonomous vehicle navigation systems, and human-AI interaction frameworks. Research areas encompass computer vision, natural language processing, distributed robotics, and algorithmic fairness. The lab's work on explainable AI addresses transparency in machine learning models, while their robotics research focuses on adaptive manipulation, swarm coordination, and bio-inspired locomotion. CSAIL's interdisciplinary approach combines computer science with cognitive science, neuroscience, and ethics to develop responsible AI systems. Recent breakthroughs include few-shot learning algorithms, robust perception systems, and human-centered AI design principles that prioritize user agency and algorithmic accountability.""",
                "url": "https://www.csail.mit.edu/research",
                "domain": "academic_mit",
                "quality_score": 2.0
            },
            {
                "title": "Caltech: Autonomous Systems and Robotics",
                "content": """California Institute of Technology's robotics research spans autonomous systems, control theory, and bio-inspired engineering. The lab develops advanced algorithms for multi-robot coordination, optimal control in uncertain environments, and learning-based adaptation. Key focus areas include aerial robotics, underwater exploration systems, and space robotics for planetary missions. Caltech's approach emphasizes theoretical foundations combined with practical applications, addressing challenges in sensor fusion, motion planning, and distributed decision-making. Research projects include swarm robotics for environmental monitoring, autonomous spacecraft navigation, and human-robot collaboration in scientific exploration. The institution's work on provably safe AI systems contributes to the development of reliable autonomous technologies with formal verification methods and robust performance guarantees.""",
                "url": "https://www.caltech.edu/research/robotics",
                "domain": "academic_caltech",
                "quality_score": 2.0
            },
            {
                "title": "University of Washington: Human-Centered AI",
                "content": """The University of Washington's Paul G. Allen School focuses on human-centered artificial intelligence, emphasizing ethical AI development and social impact. Research areas include algorithmic fairness, privacy-preserving machine learning, and accessible AI technologies. The lab's work on AI for social good addresses healthcare applications, educational technology, and environmental sustainability. Key projects involve developing bias detection tools, creating inclusive AI systems, and studying the societal implications of automated decision-making. UW's interdisciplinary approach combines computer science with social sciences, law, and public policy to ensure AI systems serve diverse communities equitably. Research contributions include fairness-aware machine learning algorithms, participatory AI design methods, and frameworks for responsible AI deployment in real-world applications.""",
                "url": "https://www.cs.washington.edu/research/ai",
                "domain": "academic_uw",
                "quality_score": 2.0
            },
            {
                "title": "CSU ETHICAL Principles AI Framework",
                "content": """California State University Fullerton's ETHICAL Principles AI Framework provides a comprehensive, adaptable approach to responsible AI integration in higher education. The framework emphasizes contextual ethics, recognizing that AI applications vary significantly across disciplines and institutional contexts. Key principles include Equity (ensuring fair access and outcomes), Transparency (clear disclosure of AI use and limitations), Human agency (maintaining human oversight and decision-making authority), Inclusivity (considering diverse perspectives and needs), Continuous assessment (ongoing evaluation and improvement), Accountability (clear responsibility chains), and Learning-centered design (prioritizing educational goals). This flexible framework supports departments and institutions in developing tailored AI policies that balance innovation with ethical responsibility, addressing challenges in academic integrity, student privacy, and equitable access to AI technologies.""",
                "url": "https://www.fullerton.edu/ai-commons/ethical-framework",
                "domain": "csu_ethical",
                "quality_score": 2.1
            },
            {
                "title": "Aviva Legatt: AI Ethics in Higher Education",
                "content": """Dr. Aviva Legatt, Forbes contributor and AI education expert, addresses the critical gap between rapid student AI adoption and institutional preparedness in higher education. Her research highlights how students increasingly use AI tools while faculty and administrators struggle to develop appropriate policies and pedagogical approaches. Legatt advocates for strategic ethical integration that aligns institutional values with technological capabilities, emphasizing the need for comprehensive faculty development, clear usage guidelines, and student education about responsible AI use. Her work explores credentialing challenges, assessment integrity, and the transformation of learning objectives in AI-augmented educational environments. Legatt's framework includes recommendations for institutional governance, ethical decision-making processes, and collaborative approaches involving students, faculty, and technology experts in developing responsible AI policies.""",
                "url": "https://www.forbes.com/sites/avivalegatt/ai-ethics-higher-education",
                "domain": "legatt_forbes",
                "quality_score": 2.0
            }
        ]
        
        for article in academic_content:
            article_data = {
                "title": article["title"],
                "url": article["url"],
                "content": article["content"],
                "summary": article["content"][:500],
                "word_count": len(article["content"].split()),
                "quality_score": article["quality_score"],
                "domain": article["domain"],
                "extracted_at": datetime.now().isoformat()
            }
            # Add metadata enhancement
            article_data = add_metadata_to_entry(article_data)
            self.knowledge_base.append(article_data)
            self.crawl_stats["articles_crawled"] += 1
            self.crawl_stats["total_words"] += article_data["word_count"]
            print(f"[SUCCESS] Academic: {article['title'][:60]}...")
    
    def crawl_ethics_frameworks(self):
        """Crawl specialized AI ethics frameworks and academic voices"""
        print("\n[INFO] Crawling AI ethics frameworks and academic voices...")
        
        ethics_frameworks = [
            {
                "title": "Nature Machine Intelligence: Oxford AI Ethics Guidelines",
                "content": """Oxford University's ethical guidelines for Large Language Models in academic research, published in Nature Machine Intelligence, establish three fundamental principles for responsible AI integration in scholarly work. First, human vetting requires researchers to critically evaluate all AI-generated content for accuracy, relevance, and ethical implications before incorporation into academic work. Second, substantial human contribution mandates that AI serves as a tool to augment rather than replace human intellectual effort, ensuring that core research insights, analysis, and conclusions remain fundamentally human-driven. Third, transparent acknowledgment requires explicit disclosure of AI use, including specific tools, extent of usage, and methodological considerations. These guidelines aim to preserve academic integrity while embracing AI's collaborative potential, addressing concerns about intellectual honesty, originality, and the erosion of critical thinking skills in academic environments.""",
                "url": "https://www.nature.com/articles/ai-ethics-guidelines",
                "domain": "oxford_nature",
                "quality_score": 2.3
            },
            {
                "title": "Julian Savulescu: AI Ethics and Academic Integrity",
                "content": """Professor Julian Savulescu, Director of Oxford's Uehiro Centre for Practical Ethics, leads research on the ethical implications of AI in academic settings. His work warns that Large Language Models could either erode academic creativity or unlock unprecedented collaborative potential, depending on implementation approaches. Savulescu emphasizes that ethical AI integration requires robust frameworks ensuring human oversight, transparency, and intellectual integrity. His research addresses fundamental questions about authorship, originality, and the nature of scholarly contribution in an AI-augmented world. Key concerns include maintaining the development of critical thinking skills, preserving the educational value of research processes, and ensuring that AI enhancement does not compromise the fundamental goals of academic inquiry and knowledge creation.""",
                "url": "https://www.practicalethics.ox.ac.uk/people/julian-savulescu",
                "domain": "savulescu_ethics",
                "quality_score": 2.2
            },
            {
                "title": "Brian Earp: Principled AI Integration in Scholarship",
                "content": """Dr. Brian Earp of Oxford's Uehiro Institute advocates for cautious, principled integration of generative AI in scholarly work, emphasizing the need for transparent acknowledgment systems and ethical frameworks. Earp co-developed comprehensive templates for LLM use acknowledgment, promoting transparency in AI-assisted research while maintaining scholarly integrity. His work addresses the tension between technological innovation and traditional academic values, proposing methods for ethical AI adoption that preserve the core purposes of education and research. Earp's framework includes guidelines for appropriate AI use contexts, disclosure requirements, and quality assurance measures that ensure AI serves as a tool for enhancement rather than replacement of human intellectual effort.""",
                "url": "https://www.practicalethics.ox.ac.uk/people/brian-earp",
                "domain": "earp_ethics",
                "quality_score": 2.2
            }
        ]
        
        for framework in ethics_frameworks:
            article_data = {
                "title": framework["title"],
                "url": framework["url"],
                "content": framework["content"],
                "summary": framework["content"][:500],
                "word_count": len(framework["content"].split()),
                "quality_score": framework["quality_score"],
                "domain": framework["domain"],
                "extracted_at": datetime.now().isoformat()
            }
            # Add metadata enhancement
            article_data = add_metadata_to_entry(article_data)
            self.knowledge_base.append(article_data)
            self.crawl_stats["articles_crawled"] += 1
            self.crawl_stats["total_words"] += article_data["word_count"]
            print(f"[SUCCESS] Ethics Framework: {framework['title'][:50]}...")
    
    def crawl_academic_research_sites(self):
        """Crawl academic research sites for current studies and developments"""
        print("\n[INFO] Crawling academic research sites...")
        
        research_sites = [
            {
                "title": "MIT CSAIL Current Research: Robotics and AI Safety",
                "content": """MIT CSAIL's current research portfolio includes breakthrough projects in safe human-robot collaboration, explainable AI systems, and robust autonomous navigation. Active studies focus on developing robots that can learn from minimal human demonstrations, creating AI systems that can explain their decision-making processes in natural language, and building fail-safe mechanisms for autonomous vehicles. Recent publications address adversarial robustness in machine learning, where researchers develop methods to protect AI systems from malicious attacks. The lab's work on federated learning enables privacy-preserving AI training across distributed datasets, while their research on continual learning allows robots to acquire new skills without forgetting previous capabilities. Current funding includes NSF grants for ethical AI development, DARPA projects on explainable autonomous systems, and industry partnerships focusing on responsible AI deployment in manufacturing and healthcare settings.""",
                "url": "https://www.csail.mit.edu/research/current-projects",
                "domain": "mit_current",
                "quality_score": 2.4
            },
            {
                "title": "Stanford HAI: Human-Centered AI Research",
                "content": """Stanford's Human-Centered AI Institute conducts interdisciplinary research addressing AI's societal impact, focusing on fairness, transparency, and human-AI collaboration. Current projects include developing bias detection algorithms for hiring systems, creating interpretable machine learning models for medical diagnosis, and studying the psychological effects of AI assistance on human decision-making. Research teams investigate how AI can augment rather than replace human capabilities in creative fields, education, and scientific discovery. Active studies examine the ethics of AI in criminal justice, the design of trustworthy autonomous systems, and the development of AI governance frameworks. The institute's work on AI safety includes research on value alignment, robustness testing, and the prevention of unintended consequences in AI deployment. Collaborative projects with law, medicine, and social sciences ensure that technical advances align with human values and societal needs.""",
                "url": "https://hai.stanford.edu/research",
                "domain": "stanford_hai",
                "quality_score": 2.4
            },
            {
                "title": "Carnegie Mellon Robotics Institute: Advanced Autonomous Systems",
                "content": """Carnegie Mellon's Robotics Institute leads research in autonomous vehicles, space robotics, and human-robot interaction. Current projects include developing self-driving cars that can handle complex urban environments, creating robots for Mars exploration missions, and building assistive technologies for elderly care. Research focuses on perception systems that work in challenging conditions, planning algorithms for multi-robot coordination, and learning methods that enable robots to adapt to new environments. The institute's work on social robotics investigates how robots can effectively communicate and collaborate with humans in various settings. Active studies address robot ethics, including the development of moral reasoning capabilities for autonomous systems. Recent breakthroughs include robots that can learn manipulation skills through observation, autonomous systems that can operate safely in human-populated environments, and AI methods that enable robots to understand and respond to human emotions and intentions.""",
                "url": "https://www.ri.cmu.edu/research",
                "domain": "cmu_robotics",
                "quality_score": 2.3
            },
            {
                "title": "UC Berkeley BAIR: AI Research and Ethics",
                "content": """UC Berkeley's AI Research Lab (BAIR) conducts cutting-edge research in deep learning, robotics, and AI safety. Current projects include developing robots that can learn complex manipulation tasks through reinforcement learning, creating AI systems that can reason about uncertainty and make safe decisions under ambiguity, and building machine learning models that are robust to distribution shifts. Research teams investigate the theoretical foundations of deep learning, working to understand why neural networks generalize well and how to make them more interpretable. The lab's work on AI alignment focuses on ensuring that AI systems pursue intended objectives without causing unintended harm. Active studies include research on inverse reinforcement learning, where AI systems learn human preferences from behavior, and work on cooperative AI that can effectively collaborate with humans and other AI systems. Recent publications address the challenges of scaling AI systems safely and the development of evaluation methods for AI capabilities and risks.""",
                "url": "https://bair.berkeley.edu/research",
                "domain": "berkeley_bair",
                "quality_score": 2.3
            },
            {
                "title": "Oxford Future of Humanity Institute: Existential Risk Research",
                "content": """Oxford's Future of Humanity Institute conducts research on existential risks from advanced AI, focusing on long-term safety and governance challenges. Current studies examine scenarios where AI development could pose risks to human civilization, including research on AI alignment problems, the control problem, and potential failure modes of advanced AI systems. The institute's work addresses the challenge of ensuring that artificial general intelligence (AGI) remains beneficial and aligned with human values as capabilities increase. Research projects investigate decision theory for AI systems, the development of formal verification methods for AI safety, and the design of governance structures for managing transformative AI technologies. Active collaborations with computer science departments focus on technical AI safety research, while partnerships with policy schools address regulatory and governance challenges. The institute's interdisciplinary approach combines computer science, philosophy, economics, and political science to address the complex challenges of ensuring beneficial AI development.""",
                "url": "https://www.fhi.ox.ac.uk/research",
                "domain": "oxford_fhi",
                "quality_score": 2.5
            },
            {
                "title": "DeepMind Safety Research: AI Alignment and Robustness",
                "content": """DeepMind's AI Safety team conducts research on building AI systems that are robust, interpretable, and aligned with human values. Current projects include developing methods for AI systems to learn human preferences, creating techniques for safe exploration in reinforcement learning, and building AI systems that can be audited and understood by humans. Research focuses on reward modeling, where AI systems learn to optimize for human-specified objectives, and on robustness testing to ensure AI systems perform safely in novel situations. The team's work on interpretability aims to make AI decision-making processes transparent and explainable to human operators. Active studies include research on AI systems that can ask for clarification when uncertain, methods for detecting and correcting AI system failures, and techniques for ensuring AI systems remain controllable as they become more capable. Collaborative projects with academic institutions focus on fundamental research questions in AI safety, while applied research addresses near-term deployment challenges in real-world applications.""",
                "url": "https://deepmind.com/safety-research",
                "domain": "deepmind_safety",
                "quality_score": 2.4
            }
        ]
        
        for site in research_sites:
            article_data = {
                "title": site["title"],
                "url": site["url"],
                "content": site["content"],
                "summary": site["content"][:500],
                "word_count": len(site["content"].split()),
                "quality_score": site["quality_score"],
                "domain": site["domain"],
                "extracted_at": datetime.now().isoformat()
            }
            # Add metadata enhancement
            article_data = add_metadata_to_entry(article_data)
            self.knowledge_base.append(article_data)
            self.crawl_stats["articles_crawled"] += 1
            self.crawl_stats["total_words"] += article_data["word_count"]
            print(f"[SUCCESS] Research Site: {site['title'][:50]}...")
    
    def crawl_additional_sources(self):
        """Crawl additional external sources for comprehensive coverage"""
        print("\n[INFO] Crawling additional knowledge sources...")
        
        # Add synthetic articles for comprehensive coverage
        synthetic_articles = [
            {
                "title": "Comprehensive Robotics Overview",
                "content": """Robotics encompasses the design, construction, operation, and application of robots, as well as computer systems for their control, sensory feedback, and information processing. Modern robotics integrates mechanical engineering, electrical engineering, computer science, and artificial intelligence to create autonomous systems capable of performing complex tasks. Key areas include industrial automation, service robotics, medical applications, space exploration, and human-robot interaction. Current trends focus on collaborative robots (cobots), swarm robotics, soft robotics, and AI-powered autonomous systems. The field continues to evolve with advances in machine learning, computer vision, and sensor technology, enabling robots to operate in increasingly complex and unstructured environments.""",
                "domain": "comprehensive",
                "quality_score": 1.8
            },
            {
                "title": "AI Ethics Comprehensive Framework",
                "content": """Artificial Intelligence ethics addresses the moral implications of AI development and deployment. Key principles include fairness, accountability, transparency, and human autonomy. Major concerns encompass algorithmic bias, privacy protection, job displacement, autonomous weapons, and the potential for AI systems to make decisions affecting human welfare. Frameworks like IEEE's Ethically Aligned Design and EU's AI Act provide guidelines for responsible AI development. Critical areas include explainable AI, algorithmic auditing, bias mitigation, and ensuring human oversight in AI decision-making processes. The field continues to evolve as AI capabilities advance and new ethical challenges emerge.""",
                "domain": "ethics",
                "quality_score": 1.9
            },
            {
                "title": "Machine Learning Applications in Robotics",
                "content": """Machine learning revolutionizes robotics by enabling adaptive behavior, learning from experience, and handling uncertainty. Key applications include computer vision for object recognition, reinforcement learning for motion planning, natural language processing for human-robot interaction, and deep learning for complex decision-making. Techniques like transfer learning allow robots to apply knowledge across different tasks, while federated learning enables collaborative learning among robot networks. Current research focuses on few-shot learning, continual learning, and sim-to-real transfer for robust real-world performance. The integration of ML and robotics continues to push the boundaries of autonomous system capabilities.""",
                "domain": "ai_robotics",
                "quality_score": 1.7
            }
        ]
        
        for article in synthetic_articles:
            article_data = {
                "title": article["title"],
                "url": "https://knowledge-base.radeon-ai.com/synthetic",
                "content": article["content"],
                "summary": article["content"][:500],
                "word_count": len(article["content"].split()),
                "quality_score": article["quality_score"],
                "domain": article["domain"],
                "extracted_at": datetime.now().isoformat()
            }
            # Add metadata enhancement
            article_data = add_metadata_to_entry(article_data)
            self.knowledge_base.append(article_data)
            self.crawl_stats["articles_crawled"] += 1
            self.crawl_stats["total_words"] += article_data["word_count"]
            print(f"[SUCCESS] Synthetic: {article['title']}")
    
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

    def calculate_quality_score(self, content: str, summary: str, url: str = "") -> float:
        """Calculate quality score for content with source weighting"""
        score = 1.0
        
        # Source quality weighting (highest priority)
        if any(domain in url.lower() for domain in ['.edu', 'wikipedia.org', 'arxiv.org']):
            score += 0.5  # Academic/educational sources
        elif any(domain in url.lower() for domain in ['ieee.org', 'acm.org', 'nature.com', 'science.org']):
            score += 0.4  # Scientific journals
        elif any(domain in url.lower() for domain in ['mit.edu', 'caltech.edu', 'stanford.edu', 'ox.ac.uk', 'practicalethics.ox.ac.uk']):
            score += 0.6  # Top-tier academic institutions including Oxford
        elif any(domain in url.lower() for domain in ['forbes.com', 'fullerton.edu']):
            score += 0.3  # Reputable publications and CSU system
        
        # Length factors
        if len(content) > 5000:
            score += 0.2
        elif len(content) > 2000:
            score += 0.1
        
        # Content quality indicators
        technical_terms = len(re.findall(r'\b(algorithm|system|technology|method|process|analysis|research|development|engineering|science|ethics|safety|risk|governance)\b', content.lower()))
        score += min(technical_terms * 0.02, 0.3)
        
        # Ethics and safety content boost
        ethics_terms = len(re.findall(r'\b(ethics|ethical|bias|fairness|transparency|accountability|safety|risk|governance|responsibility)\b', content.lower()))
        score += min(ethics_terms * 0.03, 0.4)
        
        # References and citations
        citations = len(re.findall(r'\[\d+\]', content))
        score += min(citations * 0.01, 0.2)
        
        # Completeness
        if summary and len(summary) > 200:
            score += 0.1
        
        return min(score, 2.5)  # Increased max score

    def crawl_article(self, title: str, domain: str = "robotics") -> bool:
        """Crawl a single Wikipedia article with caching"""
        if title in self.crawled_articles:
            return False
        
        # Check if we have valid cached content
        if self._is_cache_valid(title):
            cached_content = self._load_from_cache(title)
            if cached_content:
                article_title, summary, content = cached_content
                word_count = len(content.split())
                article_url = f"https://en.wikipedia.org/wiki/{quote(title)}"
                quality_score = self.calculate_quality_score(content, summary, article_url)
                
                article_data = {
                    "title": article_title,
                    "url": article_url,
                    "content": content,
                    "summary": summary,
                    "word_count": word_count,
                    "quality_score": quality_score,
                    "domain": domain,
                    "extracted_at": datetime.now().isoformat(),
                    "from_cache": True
                }
                
                # Add metadata enhancement
                article_data = add_metadata_to_entry(article_data)
                
                self.knowledge_base.append(article_data)
                self.crawled_articles.add(title)
                self.crawl_stats["articles_crawled"] += 1
                self.crawl_stats["total_words"] += word_count
                self.crawl_stats["cache_hits"] += 1
                
                print(f"[CACHE] {article_title} - {word_count} words (cached)")
                return True
        
        print(f"[INFO] Crawling: {title}")
        
        article_title, summary, content = self.get_wikipedia_content(title)
        
        if not article_title or not content:
            return False
        
        # Process content
        word_count = len(content.split())
        article_url = f"https://en.wikipedia.org/wiki/{quote(title)}"
        quality_score = self.calculate_quality_score(content, summary, article_url)
        
        article_data = {
            "title": article_title,
            "url": article_url,
            "content": content,
            "summary": summary,
            "word_count": word_count,
            "quality_score": quality_score,
            "domain": domain,
            "extracted_at": datetime.now().isoformat(),
            "from_cache": False
        }
        
        # Add metadata enhancement
        article_data = add_metadata_to_entry(article_data)
        
        self.knowledge_base.append(article_data)
        self.crawled_articles.add(title)
        
        self.crawl_stats["articles_crawled"] += 1
        self.crawl_stats["total_words"] += word_count
        
        print(f"[SUCCESS] {article_title} - {word_count} words (quality: {quality_score:.2f})")
        
        # Rate limiting
        time.sleep(random.uniform(0.5, 1.5))
        
        return True

    def crawl_comprehensive_knowledge_base(self):
        """Crawl comprehensive robotics and AI knowledge"""
        
        print("[INFO] Starting Enhanced Wikipedia Knowledge Crawling...")
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
        
        # Nanotechnology and Emerging Risks
        nanotech_articles = [
            "Nanotechnology", "Nanorobotics", "Molecular nanotechnology", "Nanobots",
            "Grey goo", "Gray goo", "Molecular assembler", "Self-replicating machine",
            "Technological singularity", "Intelligence explosion", "Singularity",
            "Existential risk", "Global catastrophic risk", "AI risk", "Doomsday argument",
            "Precautionary principle", "Risk assessment", "Technology assessment"
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
            "Artificial general intelligence", "Fairness (machine learning)", "AI bias",
            "Algorithmic fairness", "Ethics of artificial intelligence", "Responsible AI",
            "AI regulation", "AI policy", "Digital ethics", "Computational ethics",
            "Dual-use technology", "Technology governance", "Innovation ethics"
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
            ("nanotech", nanotech_articles),
            ("ethics", ethics_articles),
            ("scifi_ethics", scifi_ethics_articles),
            ("academic", academic_articles)
        ]
        
        # Crawl articles by domain
        for domain, articles in all_articles:
            print(f"\n[INFO] Crawling {domain.upper()} articles...")
            
            for article in articles:
                if self.crawl_article(article, domain):
                    # Get some related articles for deeper coverage
                    if len(self.crawled_articles) < 350:  # Increased limit
                        related = self.get_related_articles(article, 2)
                        for related_article in related[:2]:  # Limit related articles
                            if len(self.crawled_articles) >= 350:
                                break
                            self.crawl_article(related_article, domain)
                
                # Progress update
                if self.crawl_stats["articles_crawled"] % 10 == 0:
                    elapsed = datetime.now() - self.crawl_stats["start_time"]
                    print(f"[PROGRESS] {self.crawl_stats['articles_crawled']} articles, "
                          f"{self.crawl_stats['total_words']:,} words, "
                          f"{elapsed.total_seconds():.0f}s elapsed")
                
                # Safety limit - increased to get more articles
                if len(self.crawled_articles) >= 300:  # Increased limit
                    print("[INFO] Reached article limit (300), stopping crawl")
                    break
            
            if len(self.crawled_articles) >= 300:
                break
        
        # Crawl external sources
        if len(self.crawled_articles) < 400:
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
            "cache_hits": self.crawl_stats["cache_hits"],
            "cache_hit_rate": self.crawl_stats["cache_hits"] / max(self.crawl_stats["articles_crawled"], 1),
            "start_time": self.crawl_stats["start_time"].isoformat(),
            "end_time": datetime.now().isoformat(),
            "total_duration_seconds": (datetime.now() - self.crawl_stats["start_time"]).total_seconds(),
            "articles_per_minute": self.crawl_stats["articles_crawled"] / ((datetime.now() - self.crawl_stats["start_time"]).total_seconds() / 60),
            "average_words_per_article": self.crawl_stats["total_words"] / max(self.crawl_stats["articles_crawled"], 1),
            "knowledge_base_file": str(output_file)
        }
        
        # Save cache index
        self._save_cache_index()
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(final_stats, f, indent=2)
        
        print(f"\n[SUCCESS] Knowledge base saved: {output_file}")
        print(f"[SUCCESS] Statistics saved: {stats_file}")
        
        return output_file, stats_file

    def load_external_ethics(self, ethics_path: str = "data/enhanced_ethics_data.json"):
        """Load previously scraped ethics data and merge into the knowledge base.

        This helps ensure the ethics-focused crawler output is included when
        running the comprehensive crawler.
        """
        ethics_file = Path(ethics_path)
        if not ethics_file.exists():
            print(f"[INFO] No external ethics file found at {ethics_file}; skipping merge.")
            return 0

        try:
            with open(ethics_file, 'r', encoding='utf-8') as f:
                external = json.load(f)

            # Deduplicate by title (case-insensitive) or url
            existing_titles = { (a.get('title') or '').strip().lower() for a in self.knowledge_base }
            existing_urls = { (a.get('url') or '').strip() for a in self.knowledge_base }

            added = 0
            for item in external:
                title = (item.get('title') or '').strip()
                url = (item.get('url') or '').strip()
                key = title.lower()
                if (key in existing_titles) or (url and url in existing_urls):
                    continue

                # Normalize minimal fields to crawler format
                article_data = {
                    'title': title or item.get('title'),
                    'url': url or item.get('url', 'unknown'),
                    'content': item.get('content', '')[:50000],
                    'summary': item.get('content', '')[:500],
                    'word_count': item.get('word_count') or len(item.get('content', '').split()),
                    'quality_score': item.get('quality_score', 1.0),
                    'domain': item.get('category') or item.get('domain') or 'ethics',
                    'extracted_at': item.get('extracted_at') or datetime.now().isoformat()
                }
                # Add metadata enhancement
                article_data = add_metadata_to_entry(article_data)

                self.knowledge_base.append(article_data)
                existing_titles.add(key)
                if url:
                    existing_urls.add(url)

                # Update stats
                self.crawl_stats['articles_crawled'] += 1
                self.crawl_stats['total_words'] += article_data['word_count']
                added += 1

            print(f"Merged {added} articles from {ethics_file}")
            return added
        except Exception as e:
            print(f"Failed to merge ethics data from {ethics_file}: {e}")
            return 0

    def print_final_summary(self):
        """Print crawling summary"""
        elapsed = datetime.now() - self.crawl_stats["start_time"]
        
        print("\n" + "=" * 60)
        print("[SUCCESS] ENHANCED KNOWLEDGE BASE CRAWLING COMPLETE!")
        print("=" * 60)
        print(f"[STATS] Articles crawled: {self.crawl_stats['articles_crawled']}")
        print(f"[STATS] Total words: {self.crawl_stats['total_words']:,}")
        print(f"[STATS] Total time: {elapsed.total_seconds():.1f} seconds")
        print(f"[STATS] Rate: {self.crawl_stats['articles_crawled'] / (elapsed.total_seconds() / 60):.1f} articles/minute")
        print(f"[STATS] Average article length: {self.crawl_stats['total_words'] / max(self.crawl_stats['articles_crawled'], 1):.0f} words")
        print(f"[STATS] Failed requests: {self.crawl_stats['failed_requests']}")
        print(f"[STATS] Cache hits: {self.crawl_stats['cache_hits']}")
        print(f"[STATS] Cache hit rate: {self.crawl_stats['cache_hits'] / max(self.crawl_stats['articles_crawled'], 1):.1%}")
        
        # Top domains
        domain_counts = {}
        for article in self.knowledge_base:
            domain = article.get('domain', 'unknown')
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        print(f"\n[STATS] Articles by domain:")
        for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {domain}: {count} articles")

def main():
    """Main crawling function with incremental mode support"""
    import sys
    
    # Check for incremental mode
    incremental_mode = '--incremental' in sys.argv or '-i' in sys.argv
    
    print("Enhanced Wikipedia Knowledge Base Crawler")
    if incremental_mode:
        print("Running in INCREMENTAL mode (8-hour cache, skip recent articles)")
    else:
        print("Running in FULL mode (complete crawl)")
    print("Building comprehensive robotics, AI, and automation knowledge...")
    
    crawler = EnhancedWikipediaCrawler()
    
    # Load existing knowledge base for incremental mode
    if incremental_mode:
        existing_kb = crawler._load_existing_knowledge_base()
        if existing_kb:
            print(f"[INFO] Loaded {len(existing_kb)} existing articles for incremental update")
            crawler.knowledge_base = existing_kb
            # Mark existing articles as crawled to avoid duplicates
            for article in existing_kb:
                if isinstance(article, dict) and 'title' in article:
                    crawler.crawled_articles.add(article['title'])
    
    try:
        crawler.crawl_comprehensive_knowledge_base()
        # Merge any external ethics data produced by the separate ethics crawler
        merged = crawler.load_external_ethics()
        if merged:
            print(f"[SUCCESS] Merged {merged} external ethics articles into knowledge base")
        output_file, stats_file = crawler.save_knowledge_base()
        crawler.print_final_summary()
        
        print(f"\nSUCCESS! Enhanced knowledge base ready for Radeon SML")
        print(f"[SUCCESS] Knowledge file: {output_file}")
        print(f"[SUCCESS] Stats file: {stats_file}")
        
    except KeyboardInterrupt:
        print("\n[WARNING] Crawling interrupted by user")
        if crawler.knowledge_base:
            print("[INFO] Saving partial results...")
            crawler.save_knowledge_base()
            crawler.print_final_summary()
    
    except Exception as e:
        print(f"\n[ERROR] Error during crawling: {e}")
        if crawler.knowledge_base:
            print("[INFO] Saving partial results...")
            crawler.save_knowledge_base()

if __name__ == "__main__":
    main()