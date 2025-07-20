"""
Parallel Processing - Run multiple assistants concurrently
"""

import concurrent.futures
from typing import Dict, Callable, List, Tuple, Any

def process_with_assistants(prompt: str, datetime_context: str, assistants_to_try: Dict[str, Callable], 
                           timeout: int = 30) -> Tuple[str, str]:
    """
    Process prompt with multiple assistants in parallel and return best result
    
    Args:
        prompt: User query
        datetime_context: Current date/time context
        assistants_to_try: Dictionary of assistant functions to try
        timeout: Maximum time to wait for results in seconds
        
    Returns:
        Tuple of (result, assistant_name)
    """
    if not assistants_to_try:
        return "No assistants available to process your request.", "none"
    
    results = {}
    errors = {}
    
    # Define worker function
    def call_assistant(name, assistant):
        try:
            return name, assistant(f"{datetime_context}{prompt}")
        except Exception as e:
            return name, f"Error with {name}: {str(e)}"
    
    # Process in parallel with timeout
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(3, len(assistants_to_try))) as executor:
        future_to_name = {
            executor.submit(call_assistant, name, assistant): name
            for name, assistant in assistants_to_try.items()
        }
        
        # Get results as they complete
        for future in concurrent.futures.as_completed(future_to_name, timeout=timeout):
            name = future_to_name[future]
            try:
                name, result = future.result()
                results[name] = result
            except Exception as e:
                errors[name] = str(e)
    
    # Return first successful result or error message
    if results:
        # Get first result (could implement more sophisticated selection)
        first_name = list(results.keys())[0]
        return results[first_name], first_name
    else:
        error_msg = "; ".join([f"{name}: {error}" for name, error in errors.items()])
        return f"All assistants failed: {error_msg}", "error"

def get_best_response(responses: List[Tuple[str, str, float]]) -> Tuple[str, str]:
    """
    Select the best response from multiple assistants based on confidence
    
    Args:
        responses: List of (response, assistant_name, confidence) tuples
        
    Returns:
        Tuple of (best_response, assistant_name)
    """
    if not responses:
        return "No responses available.", "none"
    
    # Sort by confidence (highest first)
    sorted_responses = sorted(responses, key=lambda x: x[2], reverse=True)
    
    # Return highest confidence response
    return sorted_responses[0][0], sorted_responses[0][1]