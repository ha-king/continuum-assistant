"""
Data-Aware System Prompts
Automatically inject data acknowledgment into all assistant prompts
"""

def make_data_aware(base_prompt: str, data_type: str = "real-time") -> str:
    """Convert any prompt to acknowledge data access"""
    data_acknowledgment = f"""
CRITICAL: You have access to {data_type} data in your query context. 
Always use the live data provided. Never claim you lack access to current information.
"""
    return f"{data_acknowledgment}\n{base_prompt}"

def inject_prediction_capability(prompt: str) -> str:
    """Add prediction capability to any prompt"""
    prediction_addon = """
For predictions: Use provided data to make informed forecasts with confidence levels and reasoning.
"""
    return f"{prompt}\n{prediction_addon}"