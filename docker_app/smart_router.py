"""
Smart Router - Eliminates hardcoded routing logic
"""

def smart_route(prompt: str, datetime_context: str, assistants: dict) -> tuple:
    """
    Smart routing based on priority and specificity
    Returns: (assistant_function, enhanced_prompt)
    """
    prompt_lower = prompt.lower()
    words = prompt.split()
    
    # Priority 1: Time/Date queries (highest priority)
    time_keywords = ['what time', 'what day', 'current time', 'current date', 'time is it', 'day is it']
    if any(keyword in prompt_lower for keyword in time_keywords):
        return None, f"It is {datetime_context}"
    
    # Priority 2: Aviation queries (N-numbers are very specific)
    if any(word.upper().startswith('N') and len(word) >= 4 for word in words) or \
       any(word in prompt_lower for word in ['aircraft', 'flight', 'airport', 'aviation', 'faa']):
        return assistants['aviation'], f"{datetime_context}{prompt}"
    
    # Priority 3: F1/Racing queries (specific domain)
    if any(word in prompt_lower for word in ['f1', 'formula 1', 'formula one', 'grand prix', 'motorsport']):
        enhanced_prompt = f"{datetime_context}IMPORTANT: You have access to live F1 data. Use the real-time race information provided above to make informed predictions and analysis.\n\n{prompt}"
        return assistants['sports'], enhanced_prompt
    
    # Priority 4: Crypto queries (specific financial domain)
    if any(word in prompt_lower for word in ['crypto', 'bitcoin', 'ethereum', 'apecoin', 'coinbase']):
        enhanced_prompt = f"{datetime_context}IMPORTANT: You have access to live crypto price data. Use the real-time market information provided above for accurate analysis.\n\n{prompt}"
        return assistants['financial'], enhanced_prompt
    
    # Priority 5: Web/Research queries (only if no specific domain detected)
    if any(word in prompt_lower for word in ['browse', '.com', 'website', 'visit']):
        return assistants['web_browser'], f"{datetime_context}{prompt}"
    
    # Priority 6: General real-time queries
    if any(word in prompt_lower for word in ['current', 'today', 'now', 'latest', 'real-time']):
        return assistants['research'], f"{datetime_context}{prompt}"
    
    # Default: Use teacher agent
    return None, None