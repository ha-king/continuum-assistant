"""
Optimized Smart Router - Improved routing logic with better maintainability
"""

import re
from router_config import ROUTING_RULES
from typing import Dict, Callable, Tuple, Optional, Any

def smart_route(prompt: str, datetime_context: str, assistants: Dict[str, Callable]) -> Tuple[Optional[Callable], Optional[str]]:
    """
    Smart routing based on priority and specificity with early returns for high-priority rules
    
    Args:
        prompt: User's query
        datetime_context: Current date/time context
        assistants: Dictionary of assistant functions keyed by name
        
    Returns:
        Tuple of (assistant_function, enhanced_prompt)
    """
    # Check high-priority rules first with early returns for efficiency
    try:
        # Time queries (highest priority - 100)
        if contains_keywords(prompt, "time"):
            print(f"Router: '{prompt[:50]}...' -> direct_response (Rule: time, Priority: 100)")
            return None, f"It is {datetime_context}"
        
        # Aviation queries (priority - 90)
        if has_n_number(prompt) or contains_keywords(prompt, "aviation") or \
           any(re.search(rf'\b{word}\b', prompt.lower()) for word in ["flight status", "flight tracker", "aircraft", "airport"]) or \
           re.search(r'\bpilot\b|\bairport\b|\bfaa\b', prompt.lower()) is not None:
            if "aviation" in assistants:
                print(f"Router: '{prompt[:50]}...' -> aviation (Rule: aviation, Priority: 90)")
                return assistants["aviation"], f"{datetime_context}{prompt}"
        
        # Formula 1 queries (priority - 80)
        if contains_keywords(prompt, "formula1"):
            if "formula1" in assistants:
                print(f"Router: '{prompt[:50]}...' -> formula1 (Rule: formula1, Priority: 80)")
                return assistants["formula1"], f"{datetime_context}IMPORTANT: You have access to live F1 data. Use the real-time race information provided above to make informed predictions and analysis.\n\n{prompt}"
    except Exception as e:
        print(f"Error in high-priority routing: {str(e)}")
    
    # For other rules, use the original approach but with sorted rules by priority
    best_match = None
    highest_priority = -1
    matched_rule = None
    all_matches = []
    
    # Sort rules by priority (highest first) for faster matching
    sorted_rules = sorted(ROUTING_RULES, key=lambda rule: rule[4], reverse=True)
    
    # Check each rule in order of priority
    for name, condition_func, assistant_key, prompt_formatter, priority in sorted_rules:
        # Skip already checked high-priority rules
        if name in ["time", "aviation", "formula1"]:
            continue
            
        try:
            if condition_func(prompt):
                all_matches.append((name, priority))
                if priority > highest_priority:
                    highest_priority = priority
                    matched_rule = name
                    
                    # Handle direct responses
                    if assistant_key is None:
                        best_match = (None, prompt_formatter(prompt, datetime_context))
                    # Handle assistant routing
                    elif assistant_key in assistants:
                        best_match = (assistants[assistant_key], prompt_formatter(prompt, datetime_context))
                        # Early return for high confidence matches
                        if priority >= 70:  # Only for high confidence matches
                            break
        except Exception as e:
            print(f"Error in rule {name}: {str(e)}")
    
    # Log the routing decision
    if best_match:
        assistant_name = get_assistant_name(best_match[0])
        print(f"Router: '{prompt[:50]}...' -> {assistant_name} (Rule: {matched_rule}, Priority: {highest_priority})")
        if len(all_matches) > 1:
            print(f"  All matches: {all_matches}")
    else:
        print(f"Router: '{prompt[:50]}...' -> No specific rule matched, defaulting to teacher agent")
    
    # Return the best match or None if no rules matched
    return best_match if best_match else (None, None)

def get_assistant_name(assistant_func: Callable) -> str:
    """Get the name of the assistant function for logging"""
    if assistant_func is None:
        return "direct_response"
    return assistant_func.__name__ if hasattr(assistant_func, "__name__") else str(assistant_func)

def log_routing_decision(prompt: str, assistant_func: Optional[Callable], rule_name: Optional[str] = None) -> None:
    """Log the routing decision for analysis"""
    assistant_name = get_assistant_name(assistant_func)
    print(f"Routing: '{prompt[:50]}...' -> {assistant_name} (Rule: {rule_name})")

def analyze_routing_patterns(history: list) -> Dict[str, Any]:
    """Analyze routing patterns to identify potential improvements"""
    patterns = {}
    for entry in history:
        prompt, assistant = entry["prompt"], entry["assistant"]
        # Add analysis logic here
    return patterns