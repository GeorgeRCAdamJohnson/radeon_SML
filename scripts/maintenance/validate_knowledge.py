import json
import os

def validate_knowledge_base():
    print("=== KNOWLEDGE BASE VALIDATION ===\n")
    
    total_articles = 0
    total_words = 0
    
    # Check robotics knowledge
    robotics_file = 'data/enhanced_robotics_knowledge.json'
    if os.path.exists(robotics_file):
        with open(robotics_file, 'r', encoding='utf-8') as f:
            robotics_data = json.load(f)
            
        if isinstance(robotics_data, list):
            robotics_articles = len(robotics_data)
            robotics_words = sum(len(item.get('content', '').split()) for item in robotics_data)
        elif isinstance(robotics_data, dict):
            robotics_articles = len(robotics_data)
            robotics_words = sum(len(str(v).split()) for v in robotics_data.values())
        
        print(f"[ROBOTICS] Knowledge:")
        print(f"   Articles: {robotics_articles}")
        print(f"   Words: {robotics_words:,}")
        
        total_articles += robotics_articles
        total_words += robotics_words
    
    # Check ethics knowledge  
    ethics_file = 'data/enhanced_ethics_data.json'
    if os.path.exists(ethics_file):
        with open(ethics_file, 'r', encoding='utf-8') as f:
            ethics_data = json.load(f)
            
        if isinstance(ethics_data, list):
            ethics_articles = len(ethics_data)
            ethics_words = sum(len(item.get('content', '').split()) for item in ethics_data)
        elif isinstance(ethics_data, dict):
            ethics_articles = len(ethics_data)
            ethics_words = sum(len(str(v).split()) for v in ethics_data.values())
        
        print(f"\n[ETHICS] Knowledge:")
        print(f"   Articles: {ethics_articles}")
        print(f"   Words: {ethics_words:,}")
        
        total_articles += ethics_articles
        total_words += ethics_words
    
    print(f"\n[TOTAL] METRICS:")
    print(f"   Total Articles: {total_articles}")
    print(f"   Total Words: {total_words:,}")
    print(f"   Target: 900+ Articles • 4.2M Words")
    
    # Validation
    articles_ok = total_articles >= 900
    words_ok = total_words >= 4200000
    
    print(f"\n[VALIDATION]:")
    print(f"   Articles {'[OK]' if articles_ok else '[FAIL]'}: {total_articles} {'>==' if articles_ok else '<'} 900")
    print(f"   Words {'[OK]' if words_ok else '[FAIL]'}: {total_words:,} {'>==' if words_ok else '<'} 4.2M")
    
    # Recommendation on merging
    print(f"\n[RECOMMENDATION]:")
    if total_articles < 100:
        print("   Keep separate - small datasets, easier to manage")
    else:
        print("   Consider merging - large datasets benefit from unified structure")
        print("   Merged structure would allow better cross-referencing")

if __name__ == "__main__":
    validate_knowledge_base()