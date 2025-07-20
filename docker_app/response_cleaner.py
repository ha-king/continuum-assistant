"""
Response Cleaner - Remove routing information from responses
"""

"""Response Cleaner - Remove routing information from responses"""

import re
import os
from typing import List, Tuple, Optional

# Enable debug mode with environment variable
DEBUG = os.environ.get("RESPONSE_CLEANER_DEBUG", "false").lower() == "true"

# Content markers that indicate the start of real content
CONTENT_MARKERS = [
    "# ", "## ", "### ", 
    "Market Overview", "Cryptocurrency", "Analysis:", "Based on",
    "Key Findings", "Summary", "Introduction"
]

# Common prefixes that indicate routing information
ROUTING_PREFIXES = [
    "I'll help you", "I'll connect you", "I'll route you", "I'll analyze", "I'll provide",
    "Universal Assistant:", "Routing to:", "Financial Assistant:", "Research Assistant:",
    "This requires", "This analysis requires", "Please analyze", "Please provide",
    "Working...", "I'll identify", "I'll examine"
]

# Regex patterns to remove routing information
ROUTING_PATTERNS = [
    # Routing headers and internal dialog
    r"I'll (?:help|connect|route|analyze) (?:you|the) (?:analyze|with|to|and|identify|market) .+?(?:\n\n|$)",
    r"(?:This requires|This analysis requires) .+?(?:\n\n|$)",
    r"(?:Universal|Financial|Research|Tech) Assistant[,:]? .+?(?:\n\n|$)",
    r"Routing to: .+?(?:\n\n|$)",
    r"Working\.\.\.",
    
    # Complete first sentences that are internal dialog
    r"^I'll analyze the crypto market and identify coins with potential for significant gains\.",
    r"^I'll help you analyze the cryptocurrency market and identify coins with potential for 10x gains\.",
    r"^I'll provide a comprehensive analysis of the cryptocurrency market\.",
    
    # Query context
    r"Query: .+?(?:\n\n|$)",
    r"Context: .+?(?:\n\n|$)",
    r"Current Date/Time: .+?(?:\n\n|$)",
    r"(?:Special )?Instructions: .+?(?:\n\n|$)",
    r"Request: .+?(?:\n\n|$)",
    r"Data Sources Needed: .+?(?:\n\n|$)",
    r"please (?:analyze|provide):.+?(?:\n\n|$)",
    
    # Analysis structure headers that aren't part of content
    r"Market Overview Analysis:.+?(?:\n|$)",
    r"10x Potential Screening Criteria:.+?(?:\n|$)",
    r"Top 10x Candidates Analysis:.+?(?:\n|$)",
    r"Market Timing Factors:.+?(?:\n|$)",
    r"90-Day Forecast:.+?(?:\n|$)",
    r"Current date/time:.+?(?:\n|$)",
    r"Focus on coins.+?(?:\n|$)",
    
    # Lists of requested items
    r"^Current crypto market conditions and sentiment analysis$",
    r"^Identification of \d-\d coins with highest 10x potential in 90 days$",
    r"^Technical and fundamental analysis for each selection$",
    r"^Market catalysts, upcoming events, and growth drivers$",
    r"^Risk assessment and probability forecasts$",
    r"^Entry points and timeline predictions$",
    r"^Market cap considerations \(micro-cap vs established coins\)$",
]

# Precompile regex patterns for better performance
COMPILED_PATTERNS = [re.compile(pattern, re.MULTILINE | re.DOTALL) for pattern in ROUTING_PATTERNS]

def find_content_marker(content: str) -> Optional[int]:
    """Find the earliest content marker in the text"""
    earliest_idx = len(content)
    
    for marker in CONTENT_MARKERS:
        idx = content.find(marker)
        if idx > 0 and idx < earliest_idx:
            earliest_idx = idx
    
    return earliest_idx if earliest_idx < len(content) else None

def find_routing_prefix(content: str) -> Optional[Tuple[str, int]]:
    """Find routing prefix and the first paragraph break after it"""
    for prefix in ROUTING_PREFIXES:
        if content.startswith(prefix):
            first_para_break = content.find("\n\n")
            if first_para_break > 0:
                return prefix, first_para_break
    
    return None

def apply_regex_patterns(content: str) -> str:
    """Apply regex patterns to remove routing information"""
    for pattern in COMPILED_PATTERNS:
        content = pattern.sub("", content)
    
    # Clean up any extra newlines
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()

def clean_response(content: str, debug: bool = DEBUG) -> str:
    """Remove routing information from responses"""
    if not content:
        return content
    
    original_length = len(content)
    
    # Strategy 0: Handle special case for "Working..."
    if content.strip() == "Working...":
        return ""
    
    # Strategy 1: Find content marker
    marker_idx = find_content_marker(content)
    if marker_idx:
        cleaned = content[marker_idx:].strip()
        if debug:
            print(f"Response cleaner: Found content marker at index {marker_idx}")
            print(f"Original length: {original_length}, Cleaned length: {len(cleaned)}")
        return cleaned
    
    # Strategy 2: Find routing prefix
    prefix_result = find_routing_prefix(content)
    if prefix_result:
        prefix, break_idx = prefix_result
        cleaned = content[break_idx:].strip()
        if debug:
            print(f"Response cleaner: Found prefix '{prefix}', removed first paragraph")
            print(f"Original length: {original_length}, Cleaned length: {len(cleaned)}")
        return cleaned
    
    # Strategy 3: Apply regex patterns
    cleaned = apply_regex_patterns(content)
    
    # Strategy 4: Remove any remaining internal dialog at the beginning
    lines = cleaned.split('\n')
    if lines and any(line.startswith("I'll ") for line in lines[:2]):
        # Find the first line that doesn't start with internal dialog
        for i, line in enumerate(lines):
            if not (line.startswith("I'll ") or line.startswith("Universal Assistant") or line.startswith("Please ")):
                cleaned = '\n'.join(lines[i:])
                break
    
    if debug:
        print(f"Response cleaner: Applied regex patterns and removed internal dialog")
        print(f"Original length: {original_length}, Final length: {len(cleaned)}")
    
    return cleaned