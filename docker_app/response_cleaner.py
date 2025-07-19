"""
Response Cleaner - Remove routing information from responses
"""

import re
import os

# Enable debug mode with environment variable
DEBUG = os.environ.get("RESPONSE_CLEANER_DEBUG", "false").lower() == "true"

def clean_response(content: str, debug: bool = DEBUG) -> str:
    """
    Remove routing information from responses
    
    Args:
        content: Raw response from assistant
        
    Returns:
        Cleaned response without routing information
    """
    if not content:
        return content
        
    # First approach: Find the start of real content using markers
    content_markers = ["# ", "## ", "### ", "Market Overview", "Cryptocurrency", "Analysis:", "Based on"]
    
    # Try to find the earliest content marker
    earliest_idx = len(content)
    for marker in content_markers:
        idx = content.find(marker)
        if idx > 0 and idx < earliest_idx:
            earliest_idx = idx
    
    # If we found a valid marker, return everything from that point
    if earliest_idx < len(content):
        cleaned = content[earliest_idx:].strip()
        if debug:
            print(f"Response cleaner: Found content marker at index {earliest_idx}")
            print(f"Original length: {len(content)}, Cleaned length: {len(cleaned)}")
        return cleaned
    
    # Second approach: Remove known routing patterns
    # Common prefixes that indicate routing information
    prefixes = [
        "I'll help you", "I'll connect you", "I'll route you", 
        "Universal Assistant:", "Routing to:", "Financial Assistant:",
        "This requires", "This analysis requires"
    ]
    
    # Check if content starts with any of these prefixes
    for prefix in prefixes:
        if content.startswith(prefix):
            # Find the first paragraph break after the prefix
            first_para_break = content.find("\n\n")
            if first_para_break > 0:
                cleaned = content[first_para_break:].strip()
                if debug:
                    print(f"Response cleaner: Found prefix '{prefix}', removed first paragraph")
                    print(f"Original length: {len(content)}, Cleaned length: {len(cleaned)}")
                return cleaned
    
    # Third approach: Use regex to remove specific patterns
    patterns = [
        # Routing headers
        r"I'll (?:help|connect|route) you (?:analyze|with|to) .+?(?:\n\n|$)",
        r"(?:This requires|This analysis requires) .+?(?:\n\n|$)",
        r"(?:Universal|Financial|Research|Tech) Assistant: .+?(?:\n\n|$)",
        r"Routing to: .+?(?:\n\n|$)",
        
        # Query context
        r"Query: .+?(?:\n\n|$)",
        r"Context: .+?(?:\n\n|$)",
        r"Current Date/Time: .+?(?:\n\n|$)",
        r"(?:Special )?Instructions: .+?(?:\n\n|$)",
        r"Request: .+?(?:\n\n|$)",
        r"Data Sources Needed: .+?(?:\n\n|$)",
        
        # Analysis structure headers that aren't part of content
        r"Market Overview Analysis:.+?(?:\n|$)",
        r"10x Potential Screening Criteria:.+?(?:\n|$)",
        r"Top 10x Candidates Analysis:.+?(?:\n|$)",
        r"Market Timing Factors:.+?(?:\n|$)",
        r"90-Day Forecast:.+?(?:\n|$)",
        r"Current date/time:.+?(?:\n|$)",
        r"Focus on coins.+?(?:\n|$)",
    ]
    
    # Apply all patterns
    for pattern in patterns:
        content = re.sub(pattern, "", content, flags=re.MULTILINE | re.DOTALL)
    
    # Clean up any extra newlines
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = content.strip()
    
    if debug:
        print(f"Response cleaner: Applied regex patterns")
        print(f"Final cleaned length: {len(content)}")
    
    return content