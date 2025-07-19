"""
Response Cleaner - Remove routing information from responses
"""

import re

def clean_response(content: str) -> str:
    """
    Remove routing information from responses
    
    Args:
        content: Raw response from assistant
        
    Returns:
        Cleaned response without routing information
    """
    # Check if the content starts with routing information
    if content.startswith("I'll help you") or content.startswith("I'll connect you") or content.startswith("I'll route you"):
        # Find the first occurrence of a real content section (usually starts with #, ## or a complete sentence)
        content_markers = ["#", "Market Overview", "Cryptocurrency", "Analysis", "Based on"]
        
        for marker in content_markers:
            if marker in content:
                start_idx = content.find(marker)
                if start_idx > 0:
                    return content[start_idx:].strip()
    
    # Remove specific routing patterns
    patterns = [
        r"I'll (?:help|connect|route) you (?:analyze|with|to) the .+?(?:\.|\n)",
        r"(?:This requires|This analysis requires) .+?(?:\.|\n)",
        r"Universal Assistant: .+?(?:\n|$)",
        r"Routing to: .+?(?:\n|$)",
        r"Query: .+?(?:\n|$)",
        r"Context: .+?(?:\n|$)",
        r"Current Date/Time: .+?(?:\n|$)",
        r"(?:Special )?Instructions: .+?(?:\n|$)",
        r"Request: .+?(?:\n|$)",
        r"Data Sources Needed: .+?(?:\n|$)",
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
        content = re.sub(pattern, "", content, flags=re.MULTILINE)
    
    # Clean up any extra newlines
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = content.strip()
    
    return content