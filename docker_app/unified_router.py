"""
Unified Router - Simplified routing logic in a single file
"""

import re
import logging
from typing import Dict, Callable, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('unified_router')

# Import telemetry (conditionally)
try:
    from app_telemetry import track_router_decision
    TELEMETRY_ENABLED = True
except ImportError:
    def track_router_decision(*args, **kwargs): pass
    TELEMETRY_ENABLED = False

# Domain keywords for routing
DOMAIN_KEYWORDS = {
    "time": ["time", "date", "day", "hour", "minute", "clock", "calendar"],
    "aviation": ["aircraft", "flight", "airport", "aviation", "faa", "plane", "pilot", "runway", 
                "airline", "airways", "airspace", "atc", "cessna", "boeing", "airbus"],
    "formula1": ["f1", "formula 1", "formula one", "grand prix", "motorsport", "racing", 
                "driver", "team", "lap", "circuit"],
    "finance": ["finance", "money", "invest", "stock", "market", "fund", "portfolio", "asset", 
               "wealth", "crypto", "bitcoin", "ethereum", "economy", "economic"],
    "tech": ["code", "programming", "software", "technology", "cyber", "security", "hack", 
            "encryption", "aws", "cloud", "ai", "artificial intelligence", "machine learning"],
    "research": ["research", "study", "analyze", "investigate", "examine", "explore", "search", "find"],
    "math": ["calculate", "equation", "formula", "math", "solve", "number", "arithmetic", "algebra"],
    "english": ["grammar", "write", "essay", "paragraph", "sentence", "word", "language", "literature"],
    "legal": ["law", "legal", "attorney", "lawyer", "court", "judge", "case", "statute", "regulation"],
    "prediction": ["predict", "forecast", "will", "future", "next", "expect", "anticipate", "projection"]
}

# Precompile regex patterns for keyword matching
DOMAIN_PATTERNS = {}
for domain_name, keywords in DOMAIN_KEYWORDS.items():
    DOMAIN_PATTERNS[domain_name] = {
        'single_words': set(),
        'multi_words': []
    }
    
    for keyword in keywords:
        if ' ' not in keyword:
            DOMAIN_PATTERNS[domain_name]['single_words'].add(keyword)
        else:
            # Precompile regex for multi-word phrases
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            DOMAIN_PATTERNS[domain_name]['multi_words'].append(pattern)

def contains_keywords(text: str, domain: str) -> bool:
    """Check if text contains any keywords for the specified domain"""
    text_lower = text.lower()
    
    # Get patterns for the domain
    patterns = DOMAIN_PATTERNS.get(domain)
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

def has_n_number(text: str) -> bool:
    """Check if text contains an N-number (US aircraft registration)"""
    # Look for N-numbers with at least 4 chars (N + 3 more)
    words = re.findall(r'\b[Nn][0-9][0-9A-Za-z]{2,}\b', text)
    if words:
        # Short queries with N-numbers at the beginning are likely aviation
        return len(text.split()) < 10 or text.strip().upper().startswith('N')
    
    return False

def unified_route(prompt: str, datetime_context: str, assistants: Dict[str, Callable]) -> Tuple[Optional[Callable], Optional[str]]:
    """
    Simplified unified routing logic that determines the appropriate assistant
    
    Args:
        prompt: User's query
        datetime_context: Current date/time context
        assistants: Dictionary of assistant functions keyed by name
        
    Returns:
        Tuple of (assistant_function, enhanced_prompt)
    """
    # Check for direct time queries (highest priority)
    if contains_keywords(prompt, "time") and len(prompt.split()) < 5:
        logger.info(f"Router: '{prompt[:50]}...' -> direct_response (time query)")
        if TELEMETRY_ENABLED:
            track_router_decision(prompt, "direct_response", "direct_response", 1.0)
        return None, f"It is {datetime_context}"
    
    # Check for aviation queries with N-numbers
    if has_n_number(prompt) or (contains_keywords(prompt, "aviation") and 
                               any(word in prompt.lower() for word in ["flight", "aircraft", "airport"])):
        if "aviation" in assistants:
            logger.info(f"Router: '{prompt[:50]}...' -> aviation")
            if TELEMETRY_ENABLED:
                track_router_decision(prompt, "specialized_industries", "aviation_assistant", 0.9)
            return assistants["aviation"], f"{datetime_context}{prompt}"
    
    # Check for Formula 1 queries
    if contains_keywords(prompt, "formula1") or any(term in prompt.lower() for term in ["f1", "grand prix", "formula one", "racing", "driver", "team", "lap", "circuit"]):
        if "formula1" in assistants:
            logger.info(f"Router: '{prompt[:50]}...' -> formula1")
            if TELEMETRY_ENABLED:
                track_router_decision(prompt, "specialized_industries", "formula1_assistant", 0.9)
            return assistants["formula1"], f"{datetime_context}IMPORTANT: You have access to live F1 data. Use the real-time race information provided above to make informed predictions and analysis.\n\n{prompt}"
    
    # Check for prediction queries (route to universal)
    if contains_keywords(prompt, "prediction"):
        if "universal" in assistants:
            logger.info(f"Router: '{prompt[:50]}...' -> universal (prediction)")
            if TELEMETRY_ENABLED:
                track_router_decision(prompt, "universal", "universal_assistant", 0.8)
            return assistants["universal"], f"{datetime_context}PREDICTION QUERY: {prompt}"
    
    # Check for crypto queries
    if any(term in prompt.lower() for term in ["crypto", "bitcoin", "ethereum", "btc", "eth", "blockchain", "token", "coin", "wallet"]):
        if "business_finance" in assistants:
            logger.info(f"Router: '{prompt[:50]}...' -> business_finance (crypto)")
            if TELEMETRY_ENABLED:
                track_router_decision(prompt, "business_finance", "business_finance_assistant", 0.9)
            return assistants["business_finance"], f"{datetime_context}IMPORTANT: You have access to live cryptocurrency price data. Use the real-time market information provided above for accurate analysis.\n\n{prompt}"
    
    # Use domain detection from unified_assistants
    try:
        from unified_assistants import detect_domain
        domain = detect_domain(prompt)
        
        # Map domain to assistant key
        domain_to_assistant = {
            "business_finance": "business_finance",
            "tech_security": "tech_security",
            "research_knowledge": "research_knowledge",
            "specialized_industries": "specialized_industries",
            "universal": "universal"
        }
        
        assistant_key = domain_to_assistant.get(domain, "universal")
        
        if assistant_key in assistants:
            logger.info(f"Router: '{prompt[:50]}...' -> {assistant_key}")
            if TELEMETRY_ENABLED:
                track_router_decision(prompt, domain, f"{assistant_key}_assistant", 0.8)
            
            # Add domain-specific context
            enhanced_context = ""
            if assistant_key == "business_finance":
                enhanced_context = "IMPORTANT: You have access to real-time financial and market data.\n\n"
            elif assistant_key == "specialized_industries":
                enhanced_context = "IMPORTANT: You have access to specialized industry data including aviation and motorsports.\n\n"
            
            return assistants[assistant_key], f"{datetime_context}{enhanced_context}{prompt}"
    except ImportError:
        logger.warning("Could not import detect_domain from unified_assistants")
    
    # Default to universal assistant
    if "universal" in assistants:
        logger.info(f"Router: '{prompt[:50]}...' -> universal (default)")
        if TELEMETRY_ENABLED:
            track_router_decision(prompt, "default", "universal_assistant", 0.5)
        return assistants["universal"], f"{datetime_context}{prompt}"
    
    # If no assistants match, return None to use the default teacher agent
    logger.info(f"Router: '{prompt[:50]}...' -> None (fallback to teacher)")
    if TELEMETRY_ENABLED:
        track_router_decision(prompt, "fallback", "teacher_agent", 0.3)
    return None, None