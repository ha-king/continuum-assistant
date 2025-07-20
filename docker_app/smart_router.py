"""
Smart Router - Optimized routing logic with better maintainability
"""

from optimized_router import smart_route as optimized_smart_route
from parallel_processing import process_with_assistants
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('smart_router')

def smart_route(prompt: str, datetime_context: str, assistants: dict) -> tuple:
    """
    Smart routing based on priority and specificity
    Returns: (assistant_function, enhanced_prompt)
    """
    # Use the optimized router
    assistant_func, enhanced_prompt = optimized_smart_route(prompt, datetime_context, assistants)
    
    # For ambiguous queries that might benefit from multiple assistants
    if not assistant_func and not enhanced_prompt:
        # Check if query might benefit from parallel processing
        if is_complex_query(prompt):
            logger.info(f"Complex query detected, trying parallel processing: {prompt[:50]}...")
            
            # Select relevant assistants for this query
            relevant_assistants = select_relevant_assistants(prompt, assistants)
            
            if relevant_assistants:
                # Process with multiple assistants in parallel
                result, assistant_name = process_with_assistants(
                    prompt, datetime_context, relevant_assistants
                )
                logger.info(f"Parallel processing used {assistant_name}")
                return None, result
    
    # Log the routing decision
    if assistant_func:
        assistant_name = assistant_func.__name__ if hasattr(assistant_func, "__name__") else str(assistant_func)
        logger.info(f"Routed to: {assistant_name}")
    elif enhanced_prompt:
        logger.info("Direct response provided")
    else:
        logger.info("No specific routing, defaulting to teacher agent")
    
    return assistant_func, enhanced_prompt

def is_complex_query(prompt: str) -> bool:
    """Determine if a query is complex enough to benefit from parallel processing"""
    # Check for multiple topics in the same query
    topics = ['finance', 'technology', 'aviation', 'sports', 'research', 'math']
    topic_count = sum(1 for topic in topics if re.search(rf'\b{topic}\b', prompt.lower()))
    
    # Complex if it contains multiple topics or is very long
    return topic_count > 1 or len(prompt.split()) > 30

def select_relevant_assistants(prompt: str, assistants: dict) -> dict:
    """Select relevant assistants for a given query"""
    relevant = {}
    
    # Simple keyword matching for demonstration
    if 'finance' in prompt.lower() and 'financial' in assistants:
        relevant['financial'] = assistants['financial']
    
    if any(tech in prompt.lower() for tech in ['code', 'programming', 'software']) and 'research' in assistants:
        relevant['research'] = assistants['research']
    
    if 'aviation' in prompt.lower() and 'aviation' in assistants:
        relevant['aviation'] = assistants['aviation']
    
    # Always include universal assistant if available
    if 'universal' in assistants:
        relevant['universal'] = assistants['universal']
    
    # Limit to 3 assistants maximum
    if len(relevant) > 3:
        # Keep universal and the 2 most specific
        keys_to_keep = ['universal'] + list(relevant.keys())[:2]
        relevant = {k: relevant[k] for k in keys_to_keep if k in relevant}
    
    return relevant