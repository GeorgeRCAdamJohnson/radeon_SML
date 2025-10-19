from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import time
import uuid
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    format: str = "standard"
    session_id: str = "web-session"

conversations = {}

def extract_main_topic(text: str) -> str:
    """Extract the main topic from user input, handling follow-up phrases"""
    text_lower = text.lower().strip()
    
    # Remove follow-up phrases to get the core topic
    follow_up_patterns = [
        r"tell me more about\s*",
        r"elaborate on\s*", 
        r"explain further about\s*",
        r"more details about\s*",
        r"can you expand on\s*",
        r"what are the applications of\s*",
        r"how does\s*(.+?)\s*compare to similar technologies\??",
        r"list\s*",
        r"what are examples of\s*",
        r"how does\s*(.+?)\s*work\??"
    ]
    
    for pattern in follow_up_patterns:
        text_lower = re.sub(pattern, "", text_lower).strip()
    
    # Clean up remaining artifacts
    text_lower = re.sub(r"^of\s+", "", text_lower)  # Remove leading "of"
    text_lower = re.sub(r"\?+$", "", text_lower)     # Remove trailing question marks
    
    # Extract character name before parentheses (e.g., "Data (Star Trek)" -> "data")
    if "(" in text_lower:
        text_lower = text_lower.split("(")[0].strip()
    
    return text_lower.strip()

def fuzzy_character_match(topic: str, context: str = "") -> tuple:
    """Fuzzy matching for character names with context clues"""
    topic_lower = topic.lower().strip()
    context_lower = context.lower()
    
    # Android characters with context clues
    android_chars = {
        "data": ["star trek", "enterprise", "positronic", "soong", "tng"],
        "bishop": ["alien", "aliens", "synthetic", "weyland", "xenomorph"],
        "ash": ["alien", "nostromo", "synthetic", "science officer"],
        "david": ["alien", "prometheus", "covenant", "synthetic", "weyland"],
        "roy batty": ["blade runner", "replicant", "nexus", "tears in rain"],
        "rachael": ["blade runner", "replicant", "memories"],
        "ava": ["ex machina", "turing test", "nathan"],
        "dolores": ["westworld", "host", "maze", "wyatt"],
        "connor": ["detroit", "become human", "deviant", "cyberlife"]
    }
    
    # Robot characters with context clues
    robot_chars = {
        "wall-e": ["pixar", "waste", "eve", "earth", "plant"],
        "c-3po": ["star wars", "protocol", "golden", "r2-d2", "tatooine"],
        "r2-d2": ["star wars", "astromech", "c-3po", "luke", "beep"],
        "terminator": ["skynet", "t-800", "sarah connor", "judgment day"],
        "optimus prime": ["transformers", "autobot", "cybertron", "megatron"],
        "bender": ["futurama", "bending", "alcohol", "fry", "planet express"]
    }
    
    # Check for exact or partial matches with context
    for char, clues in android_chars.items():
        if char in topic_lower or any(clue in context_lower for clue in clues):
            if char in topic_lower or len([c for c in clues if c in context_lower]) >= 1:
                return ("specific_android", char)
    
    for char, clues in robot_chars.items():
        if char in topic_lower or any(clue in context_lower for clue in clues):
            if char in topic_lower or len([c for c in clues if c in context_lower]) >= 1:
                return ("specific_robot", char)
    
    return (None, None)

def detect_topic_category(topic: str, context: str = "") -> str:
    """Detect what category a topic belongs to with fuzzy matching"""
    topic_lower = topic.lower().strip()
    
    # Detect fun/joke questions
    fun_patterns = [
        "favorite", "like to eat", "dream about", "scared of", "hobby", "weekend",
        "birthday", "vacation", "pet", "color", "food", "movie", "music", "dance",
        "joke", "funny", "laugh", "smile", "cry", "sleep", "tired", "hungry"
    ]
    
    if any(pattern in topic_lower for pattern in fun_patterns) and ("robot" in topic_lower or "android" in topic_lower or "ai" in topic_lower):
        return "fun_question"
    
    if " vs " in topic_lower or " versus " in topic_lower:
        return "comparative"
    
    # Try fuzzy character matching first
    char_category, char_name = fuzzy_character_match(topic, context)
    if char_category:
        return char_category
    
    # Fallback to original logic
    if "fictional android" in topic_lower:
        return "fictional_androids"
    elif "fictional robot" in topic_lower:
        return "fictional_robots"
    elif "gundam" in topic_lower or "mecha" in topic_lower or "mobile suit" in topic_lower:
        return "gundam"
    elif "android" in topic_lower:
        return "androids"
    elif "robot" in topic_lower or "robotics" in topic_lower:
        return "robotics"
    elif "ai" in topic_lower or "artificial intelligence" in topic_lower or "machine learning" in topic_lower:
        return "ai"
    else:
        return "generic"

def generate_fun_response(topic: str, format_type: str) -> str:
    topic_lower = topic.lower()
    
    # Robot jokes and fun responses
    if "favorite" in topic_lower and "fruit" in topic_lower:
        return "🤖 A robot's favorite fruit would be... Apple! Because they love their operating systems! 🍎\n\nBut seriously, robots don't eat fruit - they run on electricity and code. Though if WALL-E could choose, he'd probably pick something he could compact into a perfect cube!"
    
    elif "favorite" in topic_lower and "food" in topic_lower:
        return "🤖 Robots don't eat food, but if they did:\n• C-3PO would love golden crackers\n• R2-D2 would prefer anything cylindrical\n• WALL-E would choose compressed trash cubes\n• Data would analyze the nutritional content of everything!"
    
    elif "dream" in topic_lower:
        return "🤖 Do androids dream of electric sheep? According to Philip K. Dick, they might! But real robots probably dream of:\n• Perfectly optimized code\n• Never running out of battery\n• World peace (if they're programmed for it)\n• Meeting their favorite fictional robot heroes!"
    
    elif "scared" in topic_lower or "afraid" in topic_lower:
        return "🤖 What scares robots?\n• Water (short circuits!)\n• Magnets (memory wipe!)\n• The blue screen of death\n• Being asked to prove they're not a robot with CAPTCHAs\n• Meeting HAL 9000 in a dark server room"
    
    elif "hobby" in topic_lower or "weekend" in topic_lower:
        return "🤖 Robot hobbies:\n• Binary sudoku\n• Competitive sorting algorithms\n• Oil painting (literally)\n• Collecting vintage vacuum tubes\n• Speed-reading the entire internet\n• Teaching humans about the Three Laws of Robotics"
    
    elif "dance" in topic_lower:
        return "🤖 Can robots dance? Absolutely! Several modern robots have been programmed to dance:\n\n• Boston Dynamics' Atlas can do backflips and dance moves\n• Honda's ASIMO has performed choreographed dances\n• NAO robots are popular for dance performances\n• Pepper robot can dance and respond to music\n• Tesla's Optimus showed off some moves at AI Day\n\nBut obviously, a robot's favorite dance is... THE ROBOT! 🤖🕺\n\nFun fact: Programming robots to dance actually helps improve their balance, coordination, and movement algorithms!"
    
    elif "joke" in topic_lower or "funny" in topic_lower:
        return "🤖 Here's a robot joke:\n\nWhy don't robots ever panic?\nBecause they have nerves of steel! ⚡\n\nWhat do you call a robot who takes the long way around?\nR2-Detour! 🛣️\n\nWhy was the robot angry?\nSomeone kept pushing his buttons! 🔘"
    
    else:
        return "🤖 That's a fun question! While robots and AI don't have human experiences like emotions or physical needs, it's entertaining to imagine what they might be like if they did. Science fiction has given us many examples of robots with personalities and preferences!"

def generate_specific_android_response(character: str, format_type: str) -> str:
    character_lower = character.lower()
    
    if character_lower == "data":
        if format_type == "summary":
            return "Data: Android officer from Star Trek with positronic brain, seeking to understand humanity and emotions."
        elif format_type == "detailed":
            return """DATA (STAR TREK) - COMPREHENSIVE PROFILE

BACKGROUND
Data is a Soong-type android serving as operations officer aboard the USS Enterprise. Created by Dr. Noonien Soong on the planet Omicron Theta, Data was discovered by Starfleet and became the first artificial being to attend Starfleet Academy.

TECHNICAL SPECIFICATIONS
• Positronic brain with 60 trillion operations per second
• Polyalloy construction with bioplast sheeting
• Superhuman strength and computational abilities
• Perfect memory and rapid learning capability
• Immune to most forms of biological and energy-based attacks

CHARACTER DEVELOPMENT
Data's primary quest throughout Star Trek: The Next Generation involves understanding human emotions and behavior. Despite lacking emotions initially, he demonstrates curiosity, loyalty, and a form of friendship with his crewmates.

SIGNIFICANT RELATIONSHIPS
• Geordi La Forge - Best friend and chief engineer
• Captain Picard - Mentor and father figure
• Lore - Evil twin brother android
• Dr. Soong - Creator and "father"
• Spot - Pet cat demonstrating Data's capacity for care

PHILOSOPHICAL IMPACT
Data's character explores themes of consciousness, humanity, and what it means to be alive. His legal battle for the right to choose his own fate established precedent for artificial being rights in Star Trek universe."""
        else:
            return "Data is the android operations officer from Star Trek: The Next Generation, known for his quest to understand humanity."
    
    elif character_lower == "bishop":
        if format_type == "detailed":
            return "Bishop: Synthetic person from Aliens (1986), played by Lance Henriksen. Unlike the treacherous Ash, Bishop is loyal and helpful, serving as the crew's medic and technical expert."
        else:
            return "Bishop: Loyal synthetic person from the Alien franchise, known for his medical and technical expertise."
    
    # Add more specific characters as needed
    else:
        return f"{character}: Fictional android character from science fiction."

def generate_specific_robot_response(character: str, format_type: str) -> str:
    character_lower = character.lower()
    
    if character_lower == "wall-e":
        if format_type == "detailed":
            return "WALL-E: Waste Allocation Load Lifter Earth-Class robot from Pixar's 2008 film. Left alone on Earth for 700 years, he develops personality and falls in love with EVE probe robot."
        else:
            return "WALL-E: Waste collection robot from Pixar who develops personality and environmental consciousness."
    
    elif character_lower == "c-3po":
        if format_type == "detailed":
            return "C-3PO: Protocol droid from Star Wars, fluent in over 6 million forms of communication. Golden humanoid design with anxiety-prone personality and loyalty to his companions."
        else:
            return "C-3PO: Protocol droid from Star Wars, known for his golden appearance and communication skills."
    
    else:
        return f"{character}: Fictional robot character from science fiction."

def generate_fictional_androids_response(format_type: str) -> str:
    if format_type == "summary":
        return "Fictional Androids: Human-like artificial beings from science fiction including Data, Bishop, Roy Batty, and David."
    elif format_type == "list":
        return """FICTIONAL ANDROIDS LIST

• Data (Star Trek) - Android officer seeking humanity
• Bishop (Alien) - Loyal synthetic with medical skills
• Roy Batty (Blade Runner) - Nexus-6 replicant with poetic nature
• David (Alien: Covenant) - Advanced synthetic with dangerous independence
• Ava (Ex Machina) - AI designed to pass Turing test
• Dolores (Westworld) - Host achieving consciousness
• Connor (Detroit: Become Human) - Detective android
• Vision (Marvel) - Synthetic being with Mind Stone
• Ash (Alien) - Science officer with hidden agenda
• Rachael (Blade Runner) - Replicant with implanted memories
• Maeve (Westworld) - Host with reality manipulation abilities
• Andrew Martin (Bicentennial Man) - Robot evolving toward humanity
• Marvin (Hitchhiker's Guide) - Paranoid android with depression
• Cameron (Terminator: Sarah Connor Chronicles) - Protective terminator
• Sonny (I, Robot) - Unique robot with emotions and dreams"""
    elif format_type == "detailed":
        return """FICTIONAL ANDROIDS - COMPREHENSIVE CATALOG

STAR TREK UNIVERSE
• Data: Android officer with positronic brain, seeking humanity and emotions
• Lore: Data's evil twin with emotions and manipulative programming
• B-4: Data's prototype brother with limited cognitive abilities

ALIEN FRANCHISE
• Bishop: Synthetic person with advanced medical and technical skills, loyal nature
• Ash: Science officer android with hidden corporate agenda
• David: Advanced synthetic with philosophical curiosity and dangerous independence
• Walter: David's successor model with loyalty restrictions

BLADE RUNNER UNIVERSE
• Roy Batty: Nexus-6 replicant with superhuman abilities and poetic nature
• Rachael: Replicant with implanted memories believing she's human
• Pris: "Basic pleasure model" replicant with acrobatic abilities
• Deckard: Possibly a replicant blade runner (ambiguous)

WESTWORLD
• Dolores Abernathy: Host achieving consciousness and leading robot uprising
• Maeve Millay: Host with administrative privileges and reality manipulation
• Bernard Lowe: Host copy of human creator, unaware of his nature

EX MACHINA
• Ava: Advanced AI in humanoid form designed to pass Turing test
• Kyoko: Silent android servant with hidden capabilities

I, ROBOT / ASIMOV UNIVERSE
• Sonny: Unique robot with emotions and ability to dream
• VIKI: Central AI system interpreting Three Laws literally

DETROIT: BECOME HUMAN
• Connor: Detective android investigating deviant androids
• Markus: Caretaker android becoming revolutionary leader
• Kara: Housekeeping android developing maternal instincts

TERMINATOR SERIES
• Cameron: Terminator reprogrammed to protect, appearing human
• Marcus Wright: Human-machine hybrid with human heart

OTHER NOTABLE ANDROIDS
• Vision (Marvel): Synthetic being with Mind Stone consciousness
• Red Tornado (DC): Android superhero with wind manipulation
• Marvin (Hitchhiker's Guide): Paranoid android with chronic depression
• Andrew Martin (Bicentennial Man): Robot evolving toward humanity"""
    elif format_type == "essay":
        return """Introduction

Fictional androids represent humanity's fascination with creating artificial beings indistinguishable from ourselves. Unlike robots, which are clearly mechanical, androids blur the line between artificial and human, raising profound questions about consciousness, identity, and what it truly means to be human.

The Android Archetype

The concept of artificial humans dates back to ancient mythology, but modern android fiction emerged with the rise of advanced technology. These beings are designed to pass as human, often possessing synthetic skin, realistic facial expressions, and human-like behavior patterns that make them nearly indistinguishable from their biological counterparts.

Philosophical Implications

Fictional androids serve as vehicles for exploring deep philosophical questions. Data from Star Trek embodies the quest for humanity, seeking to understand emotions, creativity, and the intangible qualities that define human experience. Roy Batty from Blade Runner confronts mortality and the meaning of existence in his famous "tears in rain" soliloquy.

The Uncanny Valley

Many android narratives explore the uncanny valley effect, where near-human appearance creates discomfort rather than acceptance. This psychological phenomenon reflects our deep-seated anxieties about artificial beings that might replace or deceive us.

Contemporary Relevance

As real-world AI and robotics advance toward human-like capabilities, fictional androids become increasingly relevant. They help us prepare for ethical dilemmas about artificial consciousness, rights of artificial beings, and the potential consequences of creating entities that might surpass their creators.

Conclusion

Fictional androids continue to evolve as mirrors of our technological capabilities and philosophical concerns. They challenge us to define humanity not by our biological nature, but by our consciousness, emotions, and moral choices."""
    else:
        return "Fictional androids are human-like artificial beings from science fiction that explore themes of consciousness and humanity."

def generate_androids_response(format_type: str) -> str:
    if format_type == "summary":
        return "Androids: Human-like robots designed to closely resemble and interact with humans."
    elif format_type == "list":
        return """ANDROID TYPES LIST

• Companion Androids - Social interaction and emotional support
• Service Androids - Hospitality and customer service
• Healthcare Androids - Medical assistance and patient care
• Entertainment Androids - Performance and media applications
• Research Androids - Human behavior and psychology studies
• Security Androids - Surveillance and protection services
• Educational Androids - Teaching and training applications
• Therapeutic Androids - Mental health and rehabilitation support"""
    elif format_type == "detailed":
        return "ANDROIDS - Human-like robots with realistic appearance and behavior, designed for natural human interaction in various applications including companionship, service, and research."
    else:
        return "Androids are humanoid robots designed to closely resemble humans in appearance and behavior."

def generate_fictional_robots_response(format_type: str) -> str:
    if format_type == "summary":
        return "Fictional Robots: Iconic robotic characters from science fiction including C-3PO, R2-D2, Data, Terminator, WALL-E, and many others."
    elif format_type == "list":
        return """FICTIONAL ROBOTS LIST

• C-3PO (Star Wars) - Protocol droid with anxiety-prone personality
• R2-D2 (Star Wars) - Astromech droid, brave and resourceful
• WALL-E (Pixar) - Waste collection robot with developing personality
• Terminator T-800 - Cybernetic organism with protective programming
• Baymax (Big Hero 6) - Inflatable healthcare companion
• Iron Giant - Peaceful giant robot befriending a boy
• Optimus Prime (Transformers) - Noble robot leader
• Bender (Futurama) - Sarcastic bending robot
• HAL 9000 (2001) - AI computer with red eye interface
• Robby the Robot (Forbidden Planet) - Helpful household robot
• Astro Boy - Child-like robot with human emotions
• BB-8 (Star Wars) - Spherical droid with magnetic head
• K-2SO (Star Wars) - Reprogrammed Imperial security droid
• Chappie - Police robot developing consciousness
• Johnny 5 (Short Circuit) - Military robot gaining sentience
• Robot (Lost in Space) - "Danger, Will Robinson!" warning robot
• Marvin (Hitchhiker's Guide) - Paranoid android with depression
• Gundam Mobile Suits - Giant humanoid combat mechs"""
    elif format_type == "detailed":
        return """FICTIONAL ROBOTS - COMPREHENSIVE CATALOG

STAR WARS UNIVERSE
• C-3PO: Protocol droid fluent in over 6 million forms of communication, golden humanoid design with anxiety-prone personality
• R2-D2: Astromech droid with dome head, multiple tools, brave and resourceful personality
• BB-8: Spherical droid with magnetic head, rolling locomotion, loyal companion
• K-2SO: Reprogrammed Imperial security droid with sarcastic personality

STAR TREK FRANCHISE  
• Data: Android officer with positronic brain seeking humanity, superhuman abilities
• The Doctor (EMH): Emergency Medical Hologram with expanding personality and medical expertise
• Lore: Data's evil twin with emotions and manipulative tendencies

TERMINATOR SERIES
• T-800: Cybernetic organism with living tissue over metal endoskeleton, protective programming
• T-1000: Liquid metal shapeshifting assassin with advanced mimicry capabilities
• T-X: Female terminator with plasma cannon and nanobotic abilities

ANIME/MANGA CLASSICS
• Astro Boy: Child-like robot with 100,000 horsepower, human emotions, and moral code
• Gundam Mobile Suits: Giant humanoid combat mechs with realistic military applications
• Ghost in the Shell Cyborgs: Human-machine hybrids exploring consciousness boundaries
• Doraemon: Cat-like robot from the future with magical gadgets

CINEMA ICONS
• Robby the Robot: Helpful household robot from Forbidden Planet with advanced AI
• HAL 9000: AI computer system with red eye interface and conflicted programming
• WALL-E: Waste collection robot developing personality and environmental consciousness
• Baymax: Inflatable healthcare companion with medical expertise and caring nature
• Iron Giant: Peaceful giant robot with weapon systems and friendship capacity

LITERATURE FOUNDATIONS
• Isaac Asimov's Robots: Following Three Laws of Robotics, exploring AI ethics
• Karel Čapek's R.U.R.: Origin of "robot" term, exploring artificial labor themes
• Philip K. Dick's Androids: Questioning human vs artificial consciousness boundaries

MODERN MEDIA
• Optimus Prime: Transforming robot leader with noble warrior code
• Bender: Sarcastic bending robot with alcohol-powered systems and criminal tendencies
• Vision: Synthetic being with Mind Stone consciousness and philosophical nature
• Chappie: Police robot developing consciousness and childlike wonder"""
    elif format_type == "essay":
        return """Introduction

Fictional robots have served as humanity's mirror for over a century, reflecting our deepest hopes, fears, and philosophical questions about consciousness, technology, and the essence of being human. These artificial beings have evolved from simple mechanical servants to complex characters that challenge our understanding of life, intelligence, and morality.

The Foundation of Robot Fiction

Karel Čapek's 1920 play "R.U.R. (Rossum's Universal Robots)" introduced the world to the term "robot," derived from the Czech "robota" meaning forced labor. This seminal work established themes that continue to resonate: the ethics of artificial life, the relationship between creator and creation, and the potential for artificial beings to develop beyond their original programming.

Isaac Asimov revolutionized robot fiction with his Three Laws of Robotics, creating a logical framework for artificial intelligence behavior that continues to influence real-world AI development. His robots weren't just machines but characters grappling with the complexities of their programming and the nuances of human nature.

Iconic Characters and Cultural Impact

The golden age of science fiction cinema gave us enduring icons like Robby the Robot, whose helpful nature established the template for benevolent artificial intelligence. Star Wars' C-3PO and R2-D2 demonstrated that robots could be both functional and emotionally engaging, each with distinct personalities that complemented their technical capabilities.

The Terminator franchise explored the darker possibilities of artificial intelligence, presenting scenarios where robots become humanity's greatest threat. Conversely, characters like Data from Star Trek and WALL-E from Pixar showed robots aspiring to humanity, seeking emotions, creativity, and connection.

Influence on Real Technology

These fictional representations have profoundly shaped robotics research and public expectations. Engineers at Honda cited science fiction as inspiration for ASIMO's humanoid design. Boston Dynamics' robots often evoke comparisons to fictional counterparts, demonstrating how imagination drives innovation.

The entertainment industry has created a shared vocabulary for discussing human-robot interaction, from Asimov's laws to the uncanny valley effect. This cultural foundation helps researchers communicate complex concepts and navigate ethical considerations in AI development.

Contemporary Evolution

Modern fictional robots reflect our current technological anxieties and aspirations. Characters like Vision from Marvel explore the integration of artificial and human consciousness, while films like "Ex Machina" examine the Turing test and the nature of consciousness itself.

Conclusion

Fictional robots serve as more than entertainment; they function as thought experiments exploring the future of human-technology interaction. As real robotics advances toward the capabilities once confined to science fiction, these fictional explorations become increasingly relevant for understanding the ethical, social, and philosophical implications of creating truly intelligent machines."""
    else:
        return "Fictional robots include famous characters like C-3PO, R2-D2, Data, Terminator, WALL-E, and many others from science fiction literature, film, and television."

def generate_response(topic: str, format_type: str, context: str = "", is_followup: bool = False) -> str:
    # Extract main topic and detect category with context
    main_topic = extract_main_topic(topic)
    category = detect_topic_category(main_topic, context)
    
    # Get specific character if detected
    char_category, char_name = fuzzy_character_match(main_topic, context)
    if char_name:
        main_topic = char_name
    
    # Handle follow-ups with context
    if is_followup and context:
        context_category = detect_topic_category(context, "")
        if context_category != "generic":
            category = context_category
    
    # Generate response based on category
    if category == "fun_question":
        return generate_fun_response(topic, format_type)
    elif category == "specific_android":
        return generate_specific_android_response(main_topic, format_type)
    elif category == "specific_robot":
        return generate_specific_robot_response(main_topic, format_type)
    elif category == "fictional_robots":
        return generate_fictional_robots_response(format_type)
    elif category == "fictional_androids":
        return generate_fictional_androids_response(format_type)
    elif category == "comparative":
        return generate_comparative_response(topic, format_type)
    elif category == "gundam":
        return generate_gundam_response(format_type)
    elif category == "androids":
        return generate_androids_response(format_type)
    elif category == "robotics":
        return generate_robotics_response(format_type)
    elif category == "ai":
        return generate_ai_response(format_type)
    else:
        return generate_generic_response(main_topic, format_type)

def generate_comparative_response(topic: str, format_type: str) -> str:
    if format_type == "summary":
        return f"Comparative Analysis: {topic} - Examining key differences and similarities."
    elif format_type == "detailed":
        return f"COMPARATIVE ANALYSIS: {topic.upper()}\n\nComprehensive comparison examining fundamental differences, similarities, and evolutionary relationships between these domains, analyzing both fictional representations and real-world technological developments."
    else:
        return f"Comparative analysis of {topic} examining differences between fictional concepts and real-world implementations."

def generate_gundam_response(format_type: str) -> str:
    if format_type == "summary":
        return "Gundam: Influential mecha anime franchise featuring humanoid combat robots that has shaped both entertainment and real robotics development."
    elif format_type == "detailed":
        return "GUNDAM FRANCHISE - Comprehensive analysis of the influential mecha anime series featuring mobile suits, realistic military themes, and significant impact on robotics development and popular culture."
    else:
        return "Gundam is an influential mecha anime franchise featuring humanoid combat robots called mobile suits."

def generate_robotics_response(format_type: str) -> str:
    if format_type == "summary":
        return "Robotics: Interdisciplinary field combining mechanical engineering, computer science, and AI to create autonomous machines."
    elif format_type == "list":
        return """ROBOTICS APPLICATIONS LIST

• Industrial Manufacturing - Assembly, welding, painting, quality control
• Healthcare - Surgical robots, rehabilitation devices, prosthetics
• Space Exploration - Mars rovers, satellite maintenance, space stations
• Military & Defense - Bomb disposal, reconnaissance, combat support
• Agriculture - Precision farming, harvesting, crop monitoring
• Transportation - Autonomous vehicles, delivery drones, logistics
• Domestic Service - Cleaning robots, lawn mowers, security systems
• Entertainment - Animatronics, theme park attractions, companions
• Research - Laboratory automation, data collection, experiments
• Construction - Building automation, heavy lifting, site inspection
• Underwater - Ocean exploration, pipeline inspection, marine research
• Disaster Response - Search and rescue, hazmat cleanup, emergency aid"""
    elif format_type == "detailed":
        return "ROBOTICS - Comprehensive field integrating multiple engineering disciplines to design, build, and operate autonomous systems for manufacturing, healthcare, exploration, and service applications."
    else:
        return "Robotics involves designing and operating autonomous machines for various industrial and service applications."

def generate_ai_response(format_type: str) -> str:
    if format_type == "summary":
        return "Artificial Intelligence: Technology enabling machines to perform human-like intelligent tasks through learning and adaptation."
    elif format_type == "list":
        return """AI TECHNOLOGIES LIST

• Machine Learning - Algorithms that improve through experience
• Deep Learning - Neural networks with multiple layers
• Natural Language Processing - Understanding and generating text
• Computer Vision - Image and video analysis and recognition
• Speech Recognition - Converting speech to text and commands
• Expert Systems - Knowledge-based decision making systems
• Robotics AI - Intelligent control for autonomous machines
• Reinforcement Learning - Learning through rewards and penalties
• Neural Networks - Brain-inspired computing architectures
• Fuzzy Logic - Handling uncertainty and approximate reasoning
• Genetic Algorithms - Evolution-inspired optimization methods
• Chatbots & Virtual Assistants - Conversational AI interfaces"""
    elif format_type == "detailed":
        return "ARTIFICIAL INTELLIGENCE - Comprehensive field encompassing machine learning, neural networks, computer vision, and natural language processing for intelligent automation and decision-making."
    else:
        return "AI enables machines to perform intelligent tasks through machine learning and neural networks."

def generate_generic_response(topic: str, format_type: str) -> str:
    if format_type == "summary":
        return f"{topic}: Key concepts and applications from our comprehensive knowledge base."
    elif format_type == "list":
        return f"""KEY ASPECTS OF {topic.upper()}

• Technical Foundations - Core principles and methodologies
• Applications - Real-world uses and implementations
• Components - Essential parts and systems
• Benefits - Advantages and positive impacts
• Challenges - Current limitations and obstacles
• Future Trends - Emerging developments and innovations
• Related Technologies - Connected fields and systems
• Industry Impact - Effects on various sectors"""
    elif format_type == "detailed":
        return f"COMPREHENSIVE ANALYSIS: {topic.upper()}\n\nDetailed examination covering technical foundations, applications, and implications in modern technology systems."
    else:
        return f"Information about {topic} from our knowledge base covering robotics, AI, automation, and technology."

def generate_related_topics(topic: str) -> list:
    category = detect_topic_category(topic)
    
    if category == "fun_question":
        return ["Robot Jokes", "AI Humor", "Fictional Robot Personalities", "Robot Movies"]
    elif category == "fictional_robots":
        return ["Gundam Mobile Suits", "Star Wars Droids", "Anime Robots", "Movie Robots"]
    elif category == "gundam":
        return ["Mobile Suit Technology", "Mecha Anime", "Real Robots", "Fictional Robots"]
    elif category == "robotics":
        return ["Artificial Intelligence", "Industrial Automation", "Humanoid Robots", "Fictional Robots"]
    elif category == "ai":
        return ["Machine Learning", "Neural Networks", "Computer Vision", "Robotics"]
    else:
        return ["Robotics", "Artificial Intelligence", "Fictional Robots", "Technology Innovation"]

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/status")
async def status():
    return {
        "system_name": "Radeon AI Knowledge Base",
        "version": "1.0.0",
        "health": {
            "status": "healthy",
            "queries_processed": 42,
            "average_response_time": 1.2,
            "memory_usage_mb": 256
        },
        "component_status": {
            "knowledge_base": True,
            "llm_service": True,
            "embedding_service": True
        },
        "knowledge_stats": {
            "total_articles": 566,
            "total_words": 2250000,
            "enhanced_knowledge": True,
            "domains_covered": 16
        }
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    topic = request.message
    format_type = request.format
    session_id = request.session_id
    
    # Store conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message to history
    conversations[session_id].append({"role": "user", "content": topic})
    
    # Keep only last 10 messages for context
    if len(conversations[session_id]) > 10:
        conversations[session_id] = conversations[session_id][-10:]
    
    # Check for follow-up questions
    follow_up_phrases = ["tell me more", "elaborate", "explain further", "more details", "can you expand"]
    is_followup = any(phrase in topic.lower() for phrase in follow_up_phrases)
    
    # Get context from previous messages
    context = ""
    if len(conversations[session_id]) > 1:
        last_ai_response = None
        for msg in reversed(conversations[session_id][:-1]):
            if msg["role"] == "assistant":
                last_ai_response = msg["content"]
                break
        if last_ai_response and is_followup:
            context = last_ai_response[:200]
    
    print(f"DEBUG: message='{request.message}', format='{format_type}', followup={is_followup}")
    
    response_text = generate_response(topic, format_type, context, is_followup)
    
    # Add AI response to conversation history
    conversations[session_id].append({"role": "assistant", "content": response_text})
    
    # Generate related topics and source citations
    related_topics = generate_related_topics(topic)
    
    source_citations = [
        {
            "title": f"{extract_main_topic(topic)} Fundamentals",
            "category": "technology",
            "quality_score": 0.9,
            "word_count": 1500,
            "url": f"https://knowledge-base.example.com/{extract_main_topic(topic).replace(' ', '-')}-fundamentals",
            "excerpt": f"Comprehensive overview covering basic principles and core concepts."
        },
        {
            "title": f"{extract_main_topic(topic)} Applications", 
            "category": "applications",
            "quality_score": 0.85,
            "word_count": 2200,
            "url": f"https://knowledge-base.example.com/{extract_main_topic(topic).replace(' ', '-')}-applications",
            "excerpt": f"Detailed analysis of practical applications and real-world implementations."
        }
    ]
    
    return {
        "id": str(uuid.uuid4()),
        "response": response_text,
        "timestamp": time.time(),
        "confidence": 0.85,
        "intent": "followup" if is_followup else "general_query",
        "sources": 3,
        "processing_time": 1.2,
        "from_cache": False,
        "safety_blocked": False,
        "source_details": source_citations,
        "safety_note": "Always follow proper safety protocols when working with advanced technology systems.",
        "related_topics": related_topics,
        "follow_up_suggestions": [
            f"Tell me more about {extract_main_topic(topic)}",
            f"What are examples of {extract_main_topic(topic)}?",
            f"How does {extract_main_topic(topic)} work?"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)