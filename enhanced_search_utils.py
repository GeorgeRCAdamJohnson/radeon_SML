"""
Enhanced search utilities for improved agent reasoning
Minimal implementation to work with existing JSON + Index structure
"""

import json
from typing import List, Dict, Any, Optional

class EnhancedKnowledgeSearch:
    def __init__(self, knowledge_file: str, index_file: str):
        with open(knowledge_file, 'r', encoding='utf-8') as f:
            self.knowledge = json.load(f)
        with open(index_file, 'r', encoding='utf-8') as f:
            self.index = json.load(f)
    
    def find_by_entity(self, entity_name: str, entity_type: str = None) -> List[Dict]:
        """Find entries by entity name and optional type"""
        results = []
        
        # Search in index first
        if entity_type and entity_type in self.index['entities']:
            if entity_name in self.index['entities'][entity_type]:
                # Get entries from knowledge base
                for entry in self.knowledge:
                    if entry['title'] == entity_name or entity_name.lower() in entry['title'].lower():
                        results.append(entry)
        
        # Fallback to full search
        if not results:
            for entry in self.knowledge:
                if entity_name.lower() in entry['title'].lower() or entity_name.lower() in entry['content'].lower():
                    results.append(entry)
        
        return results
    
    def find_related_entities(self, entity_name: str) -> Dict[str, List[str]]:
        """Find entities related to the given entity"""
        for entry in self.knowledge:
            if hasattr(entry, 'get') and entry.get('related_entities'):
                if entity_name.lower() in entry['title'].lower():
                    return entry['related_entities']
        return {}
    
    def find_by_tags(self, tags: List[str]) -> List[Dict]:
        """Find entries that match any of the given tags"""
        results = []
        for entry in self.knowledge:
            entry_tags = entry.get('tags', [])
            if any(tag in entry_tags for tag in tags):
                results.append(entry)
        return results
    
    def find_pilots_and_mobile_suits(self) -> List[Dict]:
        """Find pilot-mobile suit relationships"""
        relationships = []
        for rel in self.index['relationships']['pilots']:
            pilot_data = self.find_by_entity(rel['pilot'], 'characters')
            suit_data = self.find_by_entity(rel['mobile_suit'], 'mobile_suits')
            relationships.append({
                'pilot': rel['pilot'],
                'mobile_suit': rel['mobile_suit'],
                'pilot_data': pilot_data[0] if pilot_data else None,
                'suit_data': suit_data[0] if suit_data else None
            })
        return relationships
    
    def enhanced_search(self, query: str) -> Dict[str, Any]:
        """Enhanced search that combines multiple search strategies"""
        results = {
            'direct_matches': [],
            'tag_matches': [],
            'related_entities': {},
            'relationships': []
        }
        
        # Direct text search
        for entry in self.knowledge:
            if query.lower() in entry['title'].lower() or query.lower() in entry['content'].lower():
                results['direct_matches'].append(entry)
        
        # Tag-based search
        query_words = query.lower().split()
        for entry in self.knowledge:
            entry_tags = entry.get('tags', [])
            if any(word in tag for tag in entry_tags for word in query_words):
                results['tag_matches'].append(entry)
        
        # Find relationships if query matches known entities
        for entity_type, entities in self.index['entities'].items():
            for entity_name in entities:
                if query.lower() in entity_name.lower():
                    results['related_entities'][entity_name] = self.find_related_entities(entity_name)
        
        return results

# Example usage for reasoning agent
def demonstrate_enhanced_search():
    """Show how the enhanced search improves agent reasoning"""
    searcher = EnhancedKnowledgeSearch(
        'data/enhanced_robotics_knowledge.json',
        'data/knowledge_index.json'
    )
    
    # Query: "What mobile suits does Amuro Ray pilot?"
    amuro_results = searcher.enhanced_search("Amuro Ray")
    pilot_relationships = searcher.find_pilots_and_mobile_suits()
    
    print("Enhanced search results for 'Amuro Ray':")
    print(f"Direct matches: {len(amuro_results['direct_matches'])}")
    print(f"Related entities: {amuro_results['related_entities']}")
    
    # Query: "Find all mecha with beam weapons"
    mecha_results = searcher.find_by_tags(['mecha', 'beam_weapons'])
    print(f"\nMecha with beam weapons: {len(mecha_results)} found")
    
    return searcher

if __name__ == "__main__":
    demonstrate_enhanced_search()