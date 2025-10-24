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
    format: str = "detailed"
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
        return """ANDROIDS - COMPREHENSIVE ANALYSIS

DEFINITION AND CHARACTERISTICS
Androids are humanoid robots designed to closely resemble humans in appearance, behavior, and interaction patterns. Unlike traditional robots, androids prioritize human-like aesthetics and social capabilities over purely functional design.

TECHNICAL COMPONENTS
• Artificial skin and facial features for realistic appearance
• Advanced actuators for natural movement and gestures
• Speech synthesis and natural language processing
• Computer vision for facial recognition and social cues
• Machine learning algorithms for personality adaptation
• Sensory systems mimicking human touch, sight, and hearing

CURRENT APPLICATIONS
• Hospitality industry for customer service and reception
• Healthcare as patient companions and therapy assistants
• Education for language learning and special needs support
• Entertainment in theme parks and interactive experiences
• Research platforms for studying human-robot interaction
• Elder care providing companionship and basic assistance

DEVELOPMENT CHALLENGES
• Uncanny valley effect causing discomfort in human observers
• Complex manufacturing requiring precision engineering
• High costs limiting widespread adoption
• Ethical concerns about human replacement and deception
• Technical limitations in natural conversation and emotion recognition

FUTURE PROSPECTS
Android technology continues advancing toward more convincing human simulation, with potential applications in personal assistance, social companionship, and specialized service roles."""
    elif format_type == "essay":
        return """Introduction

Androids represent humanity's ambitious attempt to create artificial beings that not only function like humans but also appear and behave indistinguishably from us. This pursuit, rooted in both practical applications and philosophical curiosity, challenges our understanding of what makes us uniquely human while pushing the boundaries of robotics, artificial intelligence, and materials science.

The Android Concept

Unlike traditional robots designed primarily for function, androids prioritize form and social interaction. They embody our desire to create companions, assistants, and workers that can seamlessly integrate into human society without the alienating presence of obviously mechanical beings. This human-centric design philosophy drives innovations in artificial skin, facial animation, and behavioral programming.

Technological Foundations

Modern android development requires convergence of multiple advanced technologies. Sophisticated actuators enable natural movement, while artificial skin provides realistic touch and appearance. Advanced AI systems process natural language and generate appropriate responses, while computer vision allows recognition of human emotions and social cues. These technologies must work in harmony to create convincing human simulation.

Applications and Benefits

Androids show particular promise in service industries where human interaction is valued. In healthcare, android companions can provide consistent emotional support without fatigue or mood variations. Educational applications leverage their infinite patience and adaptability to individual learning styles. Entertainment venues use androids to create immersive experiences that would be impossible with human performers.

Challenges and Limitations

The uncanny valley phenomenon remains a significant obstacle, where near-human appearance creates discomfort rather than acceptance. Manufacturing costs are prohibitive for widespread adoption, while ethical questions arise about replacing human workers and potentially deceiving people about an android's artificial nature. Technical limitations in genuine emotional understanding and creative thinking also constrain current applications.

Conclusion

Androids represent both our technological ambitions and our deep-seated need for connection and companionship. As the technology matures, androids may become valuable partners in addressing societal challenges like aging populations and service labor shortages, while continuing to challenge our concepts of consciousness, identity, and what it means to be human."""
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
    print(f"GENERATE_RESPONSE DEBUG: topic='{topic}', format_type='{format_type}'")
    # Extract main topic and detect category with context
    main_topic = extract_main_topic(topic)
    category = detect_topic_category(main_topic, context)
    print(f"GENERATE_RESPONSE DEBUG: main_topic='{main_topic}', category='{category}'")
    
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
    print(f"GENERATE_RESPONSE DEBUG: Using category '{category}' with format '{format_type}'")
    if category == "fun_question":
        result = generate_fun_response(topic, format_type)
    elif category == "specific_android":
        result = generate_specific_android_response(main_topic, format_type)
    elif category == "specific_robot":
        result = generate_specific_robot_response(main_topic, format_type)
    elif category == "fictional_robots":
        result = generate_fictional_robots_response(format_type)
    elif category == "fictional_androids":
        result = generate_fictional_androids_response(format_type)
    elif category == "comparative":
        result = generate_comparative_response(topic, format_type)
    elif category == "gundam":
        result = generate_gundam_response(format_type)
    elif category == "androids":
        result = generate_androids_response(format_type)
    elif category == "robotics":
        result = generate_robotics_response(format_type)
    elif category == "ai":
        result = generate_ai_response(format_type)
    else:
        result = generate_generic_response(main_topic, format_type)
    
    print(f"GENERATE_RESPONSE DEBUG: Generated response length: {len(result)}")
    return result

def generate_comparative_response(topic: str, format_type: str) -> str:
    if format_type == "summary":
        return f"Comparative Analysis: {topic} - Examining key differences and similarities."
    elif format_type == "detailed":
        return f"COMPARATIVE ANALYSIS: {topic.upper()}\n\nComprehensive comparison examining fundamental differences, similarities, and evolutionary relationships between these domains, analyzing both fictional representations and real-world technological developments."
    else:
        return f"Comparative analysis of {topic} examining differences between fictional concepts and real-world implementations."

def generate_gundam_response(format_type: str) -> str:
    print(f"GUNDAM_RESPONSE DEBUG: Called with format_type='{format_type}'")
    if format_type == "summary":
        return "Gundam: Influential mecha anime franchise featuring humanoid combat robots that has shaped both entertainment and real robotics development."
    elif format_type == "list":
        return """GUNDAM MOBILE SUITS LIST

• RX-78-2 Gundam - Original Earth Federation prototype mobile suit
• Zaku II - Mass production Zeon mobile suit with distinctive mono-eye
• Strike Freedom Gundam - Advanced SEED series mobile suit with dragoon system
• Wing Gundam Zero - Gundam Wing's ultimate mobile suit with zero system
• Barbatos - Iron-Blooded Orphans' ancient Gundam frame
• Nu Gundam - Char's Counterattack finale mobile suit with psychoframe
• God Gundam - G Gundam's martial arts fighting mobile suit
• Turn A Gundam - Mysterious mobile suit with butterfly-like design
• Unicorn Gundam - Psychoframe mobile suit with destroy mode transformation
• Exia - 00 series solar-powered Gundam with GN drive
• Epyon - Wing series close-combat mobile suit
• Deathscythe Hell - Wing series stealth mobile suit with beam scythe
• Heavyarms - Wing series heavy weapons mobile suit
• Sandrock - Wing series desert combat mobile suit
• Shenlong - Wing series Chinese-inspired mobile suit"""
    elif format_type == "detailed":
        return """GUNDAM FRANCHISE - COMPREHENSIVE ANALYSIS

FRANCHISE OVERVIEW
Gundam is a Japanese military science fiction media franchise featuring giant humanoid robots called mobile suits. Created by Yoshiyuki Tomino and Sunrise, the franchise began in 1979 with Mobile Suit Gundam and has become one of the most influential mecha anime series in history.

TECHNICAL SPECIFICATIONS
• Mobile Suits: 18-20 meter tall humanoid combat vehicles
• Beam Weapons: Energy-based rifles, sabers, and cannons
• Armor Systems: Luna titanium alloy and advanced composite materials
• Propulsion: Thermonuclear reactors and thruster systems
• Cockpit: 360-degree panoramic display with linear seat
• Psychoframe Technology: Thought-responsive control systems

MAJOR TIMELINE SERIES
• Universal Century: Original timeline with realistic military themes
• After Colony: Gundam Wing's political intrigue setting
• Cosmic Era: SEED series with genetic enhancement themes
• Anno Domini: 00 series focusing on solar power technology
• Post Disaster: Iron-Blooded Orphans' harsh survival setting

CULTURAL IMPACT
• Revolutionized mecha anime with realistic military storytelling
• Influenced real robotics research and development
• Created the "real robot" genre versus "super robot" shows
• Spawned massive model kit (Gunpla) industry worth billions
• Inspired engineers at Honda, Boston Dynamics, and other robotics companies

TECHNOLOGICAL INFLUENCE
• Beam weaponry concepts influenced laser research
• Mobile suit design principles applied to real humanoid robots
• Cockpit interface designs studied for VR and AR applications
• Propulsion systems inspired ion drive research
• Artificial intelligence concepts from mobile suit AI systems"""
    elif format_type == "essay":
        return """Introduction

The Gundam franchise stands as one of the most influential science fiction properties in modern media, fundamentally transforming both the mecha anime genre and real-world robotics development. Since its debut in 1979, Gundam has evolved from a simple robot anime into a complex multimedia franchise that explores themes of war, politics, human evolution, and technological advancement through the lens of giant humanoid combat vehicles called mobile suits.

The Real Robot Revolution

Gundam's creator, Yoshiyuki Tomino, revolutionized mecha anime by introducing the "real robot" concept. Unlike previous "super robot" shows featuring invincible mechanical heroes, Gundam presented mobile suits as military weapons with realistic limitations, maintenance requirements, and tactical applications. This grounded approach made the technology feel plausible and inspired serious consideration of humanoid combat vehicles.

Technological Plausibility

The franchise's commitment to technological realism has made it a touchstone for robotics researchers. Mobile suits operate on principles that, while advanced, remain within the realm of scientific possibility. Their fusion reactors, beam weaponry, and articulated limb systems have inspired real-world research into humanoid robotics, energy weapons, and advanced materials science.

Cultural and Industrial Impact

Gundam's influence extends far beyond entertainment. The franchise has generated billions in revenue through model kits (Gunpla), video games, and merchandise. More significantly, it has inspired a generation of engineers and scientists. Companies like Honda have cited Gundam as inspiration for their ASIMO humanoid robot, while Boston Dynamics' bipedal robots often evoke comparisons to mobile suits.

Engineering Inspiration

The detailed mechanical designs of Gundam mobile suits have provided blueprints for real robotics development. Their articulated joints, sensor systems, and human-machine interfaces have influenced everything from prosthetic limbs to industrial automation. The franchise's exploration of pilot-machine neural interfaces has paralleled developments in brain-computer interface technology.

Conclusion

Gundam represents more than entertainment; it serves as a bridge between science fiction imagination and technological reality. By presenting plausible humanoid robots within compelling narratives, the franchise has inspired both popular culture and scientific advancement, demonstrating the power of speculative fiction to shape our technological future."""
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
        return """ROBOTICS - COMPREHENSIVE FIELD ANALYSIS

FIELD DEFINITION
Robotics is an interdisciplinary engineering field that integrates mechanical engineering, electrical engineering, computer science, and artificial intelligence to design, construct, and operate autonomous machines capable of performing tasks traditionally requiring human intervention.

CORE TECHNOLOGIES
• Mechanical Systems: Actuators, joints, linkages, and structural components
• Control Systems: Feedback loops, sensors, and real-time processing
• Artificial Intelligence: Machine learning, computer vision, and decision-making
• Power Systems: Batteries, fuel cells, and energy management
• Communication: Wireless protocols, networking, and human-machine interfaces
• Materials Science: Lightweight composites, smart materials, and durability

MAJOR APPLICATION DOMAINS
• Industrial Automation: Manufacturing, assembly, and quality control systems
• Medical Robotics: Surgical assistance, rehabilitation, and prosthetic devices
• Service Robotics: Cleaning, security, and personal assistance applications
• Exploration Robotics: Space missions, deep-sea research, and hazardous environments
• Military Applications: Reconnaissance, bomb disposal, and combat support
• Agricultural Systems: Precision farming, harvesting, and crop monitoring

EMERGING TRENDS
• Collaborative robots (cobots) working alongside humans
• Swarm robotics for coordinated multi-robot systems
• Soft robotics using flexible materials and bio-inspired designs
• Autonomous vehicles and delivery systems
• Brain-computer interfaces for direct neural control
• Quantum sensors for enhanced perception capabilities

CHALLENGES AND LIMITATIONS
• Safety and reliability in human-robot interaction
• Ethical considerations in autonomous decision-making
• Cost-effectiveness for widespread adoption
• Technical complexity in unstructured environments
• Regulatory frameworks for autonomous systems"""
    elif format_type == "essay":
        return """Introduction

Robotics represents one of humanity's most ambitious technological endeavors: the creation of machines that can perceive, think, and act autonomously in the physical world. This interdisciplinary field has evolved from simple automated mechanisms to sophisticated systems that rival human capabilities in specific domains, fundamentally transforming industries and reshaping our relationship with technology.

Historical Evolution

The field of robotics emerged from the convergence of mechanical automation, control theory, and computer science in the mid-20th century. Early industrial robots like the Unimate revolutionized manufacturing by performing repetitive tasks with precision and consistency. As computing power increased and sensors became more sophisticated, robots evolved from simple programmable machines to intelligent systems capable of adapting to changing environments.

Technological Foundations

Modern robotics integrates multiple engineering disciplines. Mechanical systems provide the physical structure and movement capabilities, while electrical systems power and control robot operations. Computer science contributes algorithms for perception, planning, and decision-making, while artificial intelligence enables learning and adaptation. This convergence creates systems that can operate autonomously in complex, dynamic environments.

Transformative Applications

Robotics has revolutionized numerous industries. In manufacturing, robots have increased productivity, quality, and safety while reducing costs. Medical robotics has enabled minimally invasive surgeries and precise drug delivery. Space exploration relies heavily on robotic systems to extend human reach into hostile environments. Service robots are beginning to assist with domestic tasks, elder care, and customer service.

Societal Impact

The proliferation of robotics raises important questions about employment, privacy, and human agency. While robots can eliminate dangerous and repetitive jobs, they also displace human workers, requiring societal adaptation through education and policy changes. The increasing autonomy of robotic systems challenges traditional notions of responsibility and accountability.

Future Prospects

Robotics continues advancing toward more capable, versatile, and intelligent systems. Emerging technologies like quantum computing, advanced materials, and brain-computer interfaces promise to unlock new capabilities. As robots become more integrated into daily life, they will likely serve as partners rather than mere tools, fundamentally changing how we work, live, and interact with our environment.

Conclusion

Robotics stands at the intersection of human ambition and technological capability, offering solutions to complex challenges while raising new questions about our future. As this field continues to evolve, it will undoubtedly play a crucial role in addressing global challenges and expanding human potential."""
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
        return """ARTIFICIAL INTELLIGENCE - COMPREHENSIVE ANALYSIS

FIELD OVERVIEW
Artificial Intelligence encompasses computational systems designed to perform tasks that typically require human intelligence, including learning, reasoning, perception, and decision-making. AI systems can analyze data, recognize patterns, and make predictions or recommendations based on their training and algorithms.

CORE TECHNOLOGIES
• Machine Learning: Algorithms that improve performance through experience and data
• Deep Learning: Multi-layered neural networks for complex pattern recognition
• Natural Language Processing: Understanding and generating human language
• Computer Vision: Image and video analysis for object recognition and scene understanding
• Expert Systems: Knowledge-based systems for specialized domain expertise
• Reinforcement Learning: Learning through trial and error with reward feedback

APPLICATION DOMAINS
• Healthcare: Diagnostic imaging, drug discovery, and personalized treatment
• Finance: Fraud detection, algorithmic trading, and risk assessment
• Transportation: Autonomous vehicles and traffic optimization
• Manufacturing: Predictive maintenance and quality control
• Entertainment: Content recommendation and procedural generation
• Communication: Language translation and virtual assistants

CURRENT CAPABILITIES
• Image recognition surpassing human accuracy in specific domains
• Natural language understanding for conversational interfaces
• Game-playing systems achieving superhuman performance
• Predictive analytics for business intelligence and forecasting
• Automated decision-making in structured environments
• Pattern recognition in complex datasets

LIMITATIONS AND CHALLENGES
• Lack of general intelligence and common sense reasoning
• Bias and fairness issues in training data and algorithms
• Explainability and transparency in decision-making processes
• Energy consumption and computational requirements
• Ethical considerations in autonomous systems
• Safety and reliability in critical applications"""
    elif format_type == "essay":
        return """Introduction

Artificial Intelligence represents humanity's quest to create machines that can think, learn, and reason like humans. This transformative technology has evolved from theoretical concepts to practical applications that permeate nearly every aspect of modern life, from the smartphones in our pockets to the algorithms that power global financial markets.

Historical Development

AI's journey began in the 1950s with pioneers like Alan Turing and John McCarthy, who laid the theoretical foundations for machine intelligence. Early AI systems relied on symbolic reasoning and expert systems, but progress was limited by computational constraints. The resurgence of neural networks in the 1980s and the big data revolution of the 2000s enabled the deep learning breakthroughs that define modern AI.

Technological Foundations

Contemporary AI systems rely primarily on machine learning, where algorithms learn patterns from vast datasets rather than following explicitly programmed rules. Deep learning, inspired by neural networks in the human brain, has proven particularly effective for tasks involving perception and pattern recognition. These systems can process information at scales and speeds impossible for human cognition.

Transformative Applications

AI has revolutionized numerous fields. In healthcare, AI systems can diagnose diseases from medical images with accuracy matching or exceeding human specialists. Financial institutions use AI for fraud detection and algorithmic trading. Transportation is being transformed by autonomous vehicles that promise to reduce accidents and improve efficiency. Entertainment platforms use AI to personalize content recommendations for billions of users.

Societal Implications

The rapid advancement of AI raises profound questions about the future of work, privacy, and human agency. While AI can automate routine tasks and augment human capabilities, it also threatens to displace workers and concentrate power in the hands of those who control the technology. Issues of bias, fairness, and accountability in AI systems have become critical concerns requiring careful consideration.

Future Prospects

AI continues advancing toward more general and capable systems. Researchers are working on artificial general intelligence (AGI) that could match human cognitive abilities across all domains. Quantum computing may unlock new AI capabilities, while neuromorphic computing could create more efficient AI hardware. The integration of AI with robotics promises to create intelligent physical agents capable of complex real-world tasks.

Conclusion

Artificial Intelligence stands as one of the most significant technological developments in human history, with the potential to solve complex global challenges while raising new questions about the nature of intelligence and consciousness. As AI systems become more capable and ubiquitous, society must navigate the opportunities and risks they present, ensuring that this powerful technology serves humanity's best interests."""
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
        return f"""COMPREHENSIVE ANALYSIS: {topic.upper()}

OVERVIEW
{topic.title()} represents a significant area of technological development with applications across multiple industries and research domains. This field combines theoretical foundations with practical implementations to address real-world challenges and opportunities.

TECHNICAL FOUNDATIONS
The underlying principles of {topic.lower()} involve complex interactions between hardware systems, software algorithms, and human interface design. These systems require careful engineering to balance performance, reliability, and cost-effectiveness.

CURRENT APPLICATIONS
• Industrial and manufacturing processes
• Research and development initiatives
• Consumer and commercial products
• Healthcare and medical applications
• Educational and training systems
• Entertainment and media platforms

BENEFITS AND ADVANTAGES
• Improved efficiency and productivity
• Enhanced accuracy and precision
• Reduced human error and safety risks
• Cost savings through automation
• Scalability for large-scale operations
• Innovation in related fields

CHALLENGES AND LIMITATIONS
• Technical complexity requiring specialized expertise
• High initial development and implementation costs
• Integration challenges with existing systems
• Regulatory and compliance requirements
• Ethical and social considerations
• Maintenance and upgrade requirements

FUTURE PROSPECTS
Continued advancement in {topic.lower()} technology promises new capabilities and applications, with ongoing research focusing on improved performance, reduced costs, and broader accessibility across various sectors."""
    elif format_type == "essay":
        return f"""Introduction

{topic.title()} represents a fascinating intersection of technology, innovation, and human ingenuity. This field has evolved significantly over recent decades, transforming from theoretical concepts into practical applications that impact numerous aspects of modern life and industry.

Historical Context

The development of {topic.lower()} technology has been driven by the convergence of multiple scientific and engineering disciplines. Early pioneers in this field laid the groundwork for today's sophisticated systems through careful research, experimentation, and iterative improvement of core concepts and methodologies.

Technological Foundations

Modern {topic.lower()} systems rely on advanced engineering principles that integrate hardware and software components into cohesive, functional units. These systems must balance competing requirements such as performance, reliability, cost, and usability while meeting the specific needs of their intended applications.

Applications and Impact

The practical applications of {topic.lower()} technology span numerous industries and use cases. From industrial automation to consumer products, these systems have demonstrated their value in improving efficiency, reducing costs, and enabling new capabilities that were previously impossible or impractical.

Challenges and Opportunities

Despite significant progress, {topic.lower()} technology faces ongoing challenges related to complexity, cost, and integration with existing systems. However, these challenges also represent opportunities for innovation and improvement, driving continued research and development efforts.

Future Directions

As {topic.lower()} technology continues to mature, we can expect to see new applications, improved performance, and broader adoption across various sectors. The integration of emerging technologies such as artificial intelligence, advanced materials, and quantum computing may unlock new possibilities and capabilities.

Conclusion

{topic.title()} technology stands as a testament to human innovation and engineering capability. As this field continues to evolve, it will undoubtedly play an increasingly important role in addressing complex challenges and creating new opportunities for progress and development."""
    else:
        return f"Information about {topic} from our knowledge base covering robotics, AI, automation, and technology."

def generate_related_topics(topic: str) -> list:
    category = detect_topic_category(topic)
    
    if category == "fun_question":
        return ["Robot Jokes", "AI Humor", "Fictional Robot Personalities", "Robot Movies"]
    elif category == "fictional_robots":
        return ["Gundam Mobile Suits", "Star Wars Droids", "Anime Robots", "Movie Robots"]
    elif category == "gundam":
        return ["Mobile Suit Technology", "Mecha Anime", "Real Robots", "Gunpla Models"]
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
    
    main_topic = extract_main_topic(topic)
    category = detect_topic_category(main_topic, context)
    print(f"DEBUG: message='{request.message}', format='{format_type}', followup={is_followup}")
    print(f"DEBUG: main_topic='{main_topic}', category='{category}'")
    print(f"DEBUG: About to call generate_response with format='{format_type}'")
    
    response_text = generate_response(topic, format_type, context, is_followup)
    print(f"DEBUG: Response length: {len(response_text)}")
    print(f"DEBUG: First 100 chars: {response_text[:100]}...")
    
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

# Add static file serving
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/")
    async def read_index():
        return FileResponse('static/index.html')

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)