"""
Response Processor - Process and enhance assistant responses
"""

import re
from typing import Dict, Any, Optional
from response_cleaner import clean_response

def process_response(content: str, original_query: str = "", user_data: Optional[Dict[str, Any]] = None) -> str:
    """
    Process response by cleaning and enhancing
    
    Args:
        content: Raw response from assistant
        original_query: Original user query
        user_data: User-specific data for personalization
        
    Returns:
        Processed response
    """
    if not content:
        return content
        
    # Step 1: Clean the response to remove routing information
    try:
        cleaned_content = clean_response(content)
        
        # Safety check: If cleaning removed too much content, use the original
        content_ratio = len(cleaned_content) / len(content) if content else 1.0
        if content_ratio < 0.5 and len(content) > 100:
            print(f"Warning: Response cleaner removed too much content ({content_ratio:.2f} ratio). Using original response.")
            cleaned_content = content
    except Exception as e:
        print(f"Error in response cleaner: {str(e)}")
        cleaned_content = content
    
    # Step 2: Format code blocks (ensure proper markdown)
    cleaned_content = format_code_blocks(cleaned_content)
    
    # Step 3: Extract and format references
    cleaned_content = format_references(cleaned_content)
    
    # Step 4: Add query-specific enhancements
    if "crypto" in original_query.lower() or "bitcoin" in original_query.lower():
        cleaned_content = add_crypto_disclaimer(cleaned_content)
    
    return cleaned_content

def format_code_blocks(content: str) -> str:
    """Ensure code blocks have proper markdown formatting"""
    # Find code blocks that might be missing proper formatting
    pattern = r'```(?!python|javascript|typescript|html|css|java|cpp|c#|ruby|go|rust|bash|shell)([^\n`]+)'
    
    # Add language identifier for code blocks missing it
    content = re.sub(pattern, r'```\1', content)
    
    return content

def format_references(content: str) -> str:
    """Format references section if present"""
    if "References" in content and not "**References" in content:
        content = content.replace("References", "**References**")
    
    return content

def add_crypto_disclaimer(content: str) -> str:
    """Add cryptocurrency disclaimer for crypto-related queries"""
    disclaimer = "\n\n*Note: Cryptocurrency investments involve significant risk. This analysis is for informational purposes only and should not be considered financial advice.*"
    
    if not content.endswith(disclaimer):
        content += disclaimer
    
    return content