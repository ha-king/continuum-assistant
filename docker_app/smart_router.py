"""
Smart Router - Optimized routing logic with better maintainability
"""

from optimized_router import smart_route as optimized_smart_route
import logging

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
    
    # Log the routing decision
    if assistant_func:
        assistant_name = assistant_func.__name__ if hasattr(assistant_func, "__name__") else str(assistant_func)
        logger.info(f"Routed to: {assistant_name}")
    elif enhanced_prompt:
        logger.info("Direct response provided")
    else:
        logger.info("No specific routing, defaulting to teacher agent")
    
    return assistant_func, enhanced_prompt