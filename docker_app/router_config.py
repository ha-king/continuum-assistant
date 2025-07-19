"""
Router Configuration - Centralized routing rules
"""

import re

# Domain-specific keywords for routing
DOMAINS = {
    "time": ["time", "date", "day", "hour", "minute", "clock", "calendar"],
    "aviation": ["aircraft", "flight", "airport", "aviation", "faa", "plane", "pilot", "runway", "airline", "airways", "airspace", "atc", "cessna", "boeing", "airbus", "takeoff", "landing"],
    "formula1": ["f1", "formula 1", "formula one", "grand prix", "motorsport", "racing", "driver", "team", "lap", "circuit"],
    "financial": ["finance", "money", "invest", "stock", "market", "fund", "portfolio", "asset", "wealth"],
    "crypto": ["crypto", "bitcoin", "ethereum", "blockchain", "token", "coin", "wallet", "mining", "nft"],
    "web": ["browse", "website", "url", "link", "internet", "web", "online", "site", ".com", ".org", ".net"],
    "research": ["research", "study", "analyze", "investigate", "examine", "explore", "search", "find"],
    "math": ["calculate", "equation", "formula", "math", "solve", "number", "arithmetic", "algebra", "geometry"],
    "english": ["grammar", "write", "essay", "paragraph", "sentence", "word", "language", "literature", "text"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "cloud", "serverless", "iam", "vpc"],
    "legal": ["law", "legal", "attorney", "lawyer", "court", "judge", "case", "statute", "regulation"],
    "prediction": ["predict", "forecast", "will", "future", "next", "expect", "anticipate", "projection", "trend"]
}

# N-number pattern for aviation
def is_n_number(word):
    """Check if a word looks like an N-number (US aircraft registration)"""
    if not word:
        return False
    word = word.upper()
    # N followed by digits and optional letters
    # Must be at least 4 characters (N + at least 3 digits/letters)
    return bool(re.match(r'^N[0-9][0-9A-Z]{2,}$', word))

# Precompiled regex patterns for keyword matching
_DOMAIN_PATTERNS = {}

def _initialize_patterns():
    """Initialize precompiled regex patterns for all domains"""
    global _DOMAIN_PATTERNS
    if not _DOMAIN_PATTERNS:
        for domain_name, keywords in DOMAINS.items():
            _DOMAIN_PATTERNS[domain_name] = {
                'single_words': set(),
                'multi_words': []
            }
            
            for keyword in keywords:
                if ' ' not in keyword:
                    _DOMAIN_PATTERNS[domain_name]['single_words'].add(keyword)
                else:
                    # Precompile regex for multi-word phrases
                    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                    _DOMAIN_PATTERNS[domain_name]['multi_words'].append(pattern)

# Initialize patterns on module load
_initialize_patterns()

# Domain detection functions
def contains_keywords(text, domain):
    """Check if text contains any keywords for the specified domain (optimized)"""
    text_lower = text.lower()
    
    # Get patterns for the domain
    patterns = _DOMAIN_PATTERNS.get(domain)
    if not patterns:
        return False
    
    # Extract words only once
    words = set(re.findall(r'\b\w+\b', text_lower))
    
    # Check single-word matches (fast set operation)
    if any(word in patterns['single_words'] for word in words):
        return True
    
    # Check multi-word patterns
    for pattern in patterns['multi_words']:
        if pattern.search(text_lower):
            return True
    
    return False

def contains_word_in_list(text, word_list):
    """Check if text contains any word from the list as whole words"""
    text_lower = text.lower()
    return any(re.search(rf'\b{word}\b', text_lower) for word in word_list)

def has_n_number(text):
    """Check if text contains an N-number in an aviation context"""
    # First check for aviation context
    text_lower = text.lower()
    
    # If we have explicit aviation context, it's likely about aircraft
    if re.search(r'\baircraft\b', text_lower) or re.search(r'\bregistration\b', text_lower):
        return True
    
    # Check for non-aviation context
    non_aviation_terms = ["phone", "social", "ssn", "id", "identifier", "highway", "road", "route"]
    if any(re.search(rf'\b{term}\b', text_lower) for term in non_aviation_terms):
        return False
    
    # Look for N-numbers with at least 4 chars (N + 3 more)
    words = re.findall(r'\b[Nn][0-9][0-9A-Za-z]{2,}\b', text)
    if words:
        # If we found N-numbers and have aviation context, return True
        aviation_terms = ["plane", "flight", "tail", "faa", "aviation", "cessna", 
                         "boeing", "airbus", "piper", "beech", "pilot", "airport"]
        if any(re.search(rf'\b{term}\b', text_lower) for term in aviation_terms):
            return True
            
        # Short queries with N-numbers at the beginning are likely aviation
        return len(text.split()) < 6 and text.strip().upper().startswith('N')
    
    return False

# Routing rules with priority
ROUTING_RULES = [
    # Rule format: (name, condition_function, assistant_key, prompt_formatter, priority)
    
    # Time/date queries (highest priority)
    ("time", 
     lambda text: contains_keywords(text, "time"), 
     None, 
     lambda text, datetime: f"It is {datetime}", 
     100),
    
    # Aviation queries (very specific with N-numbers)
    ("aviation", 
     lambda text: has_n_number(text) or \
                 contains_keywords(text, "aviation") or \
                 any(re.search(rf'\b{word}\b', text.lower()) for word in ["flight status", "flight tracker", "aircraft", "airport"]) or \
                 re.search(r'\bpilot\b', text.lower()) is not None or \
                 re.search(r'\bairport\b', text.lower()) is not None or \
                 re.search(r'\bfaa\b', text.lower()) is not None or \
                 (re.search(r'\bjfk\b', text.lower()) is not None and re.search(r'\blax\b', text.lower()) is not None) or \
                 re.search(r'\b747\b|\b737\b|\b777\b|\b787\b|\ba320\b|\ba380\b', text.lower()) is not None or \
                 ("busiest airports" in text.lower()) or \
                 ("pilots navigate" in text.lower()), 
     "aviation", 
     lambda text, datetime: f"{datetime}{text}", 
     90),
    
    # Formula 1 queries (specific domain)
    ("formula1", 
     lambda text: contains_keywords(text, "formula1"), 
     "formula1", 
     lambda text, datetime: f"{datetime}IMPORTANT: You have access to live F1 data. Use the real-time race information provided above to make informed predictions and analysis.\n\n{text}", 
     80),
    
    # Prediction queries (universal assistant)
    ("prediction", 
     lambda text: contains_keywords(text, "prediction"), 
     "universal", 
     lambda text, datetime: f"{datetime}IMPORTANT: This is a prediction query. Use historical data and trends to provide a well-reasoned forecast.\n\n{text}", 
     75),
    
    # Crypto queries (specific financial domain)
    ("crypto", 
     lambda text: contains_keywords(text, "crypto"), 
     "financial", 
     lambda text, datetime: f"{datetime}IMPORTANT: You have access to live crypto price data. Use the real-time market information provided above for accurate analysis.\n\n{text}", 
     70),
    
    # Financial queries
    ("financial", 
     lambda text: contains_keywords(text, "financial"), 
     "financial", 
     lambda text, datetime: f"{datetime}IMPORTANT: You have access to financial market data. Use this information for accurate analysis.\n\n{text}", 
     65),
    
    # Math queries
    ("math", 
     lambda text: contains_keywords(text, "math"), 
     "math", 
     lambda text, datetime: f"{datetime}{text}", 
     60),
    
    # English language queries
    ("english", 
     lambda text: contains_keywords(text, "english"), 
     "english", 
     lambda text, datetime: f"{datetime}{text}", 
     60),
    
    # AWS queries
    ("aws", 
     lambda text: contains_keywords(text, "aws"), 
     "aws", 
     lambda text, datetime: f"{datetime}{text}", 
     60),
    
    # Legal queries
    ("legal", 
     lambda text: contains_keywords(text, "legal"), 
     "louisiana_legal", 
     lambda text, datetime: f"{datetime}{text}", 
     60),
    
    # Web browsing queries
    ("web", 
     lambda text: contains_keywords(text, "web"), 
     "web_browser", 
     lambda text, datetime: f"{datetime}{text}", 
     50),
    
    # Research queries
    ("research", 
     lambda text: contains_keywords(text, "research"), 
     "research", 
     lambda text, datetime: f"{datetime}{text}", 
     40),
    
    # Real-time queries
    ("realtime", 
     lambda text: any(re.search(rf'\b{word}\b', text.lower()) for word in ["current", "today", "now", "latest", "real-time"]), 
     "research", 
     lambda text, datetime: f"{datetime}{text}", 
     30),
]