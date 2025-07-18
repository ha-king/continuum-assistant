"""
Optimized Smart Router - Improved routing logic with better maintainability
"""

import re
from router_config import ROUTING_RULES
from typing import Dict, Callable, Tuple, Optional, Any

def smart_route(prompt: str, datetime_context: str, assistants: Dict[str, Callable]) -> Tuple[Optional[Callable], Optional[str]]:
    """
    Smart routing based on priority and specificity
    
    Args:
        prompt: User's query
        datetime_context: Current date/time context
        assistants: Dictionary of assistant functions keyed by name
        
    Returns:
        Tuple of (assistant_function, enhanced_prompt)
    """
    # Track the highest priority match
    best_match = None
    highest_priority = -1
    matched_rule = None
    all_matches = []
    
    # Check each rule in order of priority
    for name, condition_func, assistant_key, prompt_formatter, priority in ROUTING_RULES:
        try:
            if condition_func(prompt):
                all_matches.append((name, priority))
                if priority > highest_priority:
                    highest_priority = priority
                    matched_rule = name
                    
                    # Handle direct responses (like time queries)
                    if assistant_key is None:
                        best_match = (None, prompt_formatter(prompt, datetime_context))
                    # Handle assistant routing
                    elif assistant_key in assistants:
                        best_match = (assistants[assistant_key], prompt_formatter(prompt, datetime_context))
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