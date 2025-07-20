"""
Model Options Configuration
Centralized configuration for Bedrock model options
"""

# Available Bedrock models
BEDROCK_MODELS = [
    "us.amazon.nova-pro-v1:0",
    "us.amazon.nova-lite-v1:0", 
    "us.amazon.nova-micro-v1:0",
    "anthropic.claude-3-5-haiku-20241022-v1:0",
    "anthropic.claude-3-5-sonnet-20241022-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-4-0:0"  # Added Claude 4.0
]

# Default model
DEFAULT_MODEL = "anthropic.claude-4-0:0"

def get_model_options():
    """Get list of available model options"""
    return BEDROCK_MODELS

def get_default_model():
    """Get default model"""
    return DEFAULT_MODEL