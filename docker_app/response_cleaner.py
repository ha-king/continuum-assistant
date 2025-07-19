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
    # Remove routing headers
    patterns = [
        r"I'll (?:connect|route) you (?:with|to) the .+? who .+?\n\n",
        r"Routing to: .+?\n\n",
        r"Query: .+?\n\n",
        r"Context: .+?\n\n",
        r"Current Date/Time: .+?\n\n",
        r"(?:Special )?Instructions: .+?\n\n",
        r"Request: .+?\n\n",
        r"Data Sources Needed: .+?\n\n",
    ]
    
    # Apply all patterns
    for pattern in patterns:
        content = re.sub(pattern, "", content, flags=re.MULTILINE)
    
    # Remove duplicate routing information
    content = re.sub(r"I'll (?:connect|route) you (?:with|to) the .+? who .+?$", "", content)
    
    # Remove any remaining routing information at the beginning
    content = re.sub(r"^Routing to: .+?$", "", content, flags=re.MULTILINE)
    
    # Clean up any extra newlines
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = content.strip()
    
    return content