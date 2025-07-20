"""
API Retry - Robust error handling and retries for API calls
"""

import time
import json
import boto3
import logging
from functools import wraps
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api_retry')

def retry_with_exponential_backoff(max_retries=3, initial_delay=1, max_delay=10):
    """
    Decorator for retrying API calls with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    # Don't retry on certain exceptions
                    if isinstance(e, (ValueError, TypeError, KeyError)):
                        logger.error(f"Non-retryable error: {str(e)}")
                        raise
                    
                    # Log retry attempt
                    if attempt < max_retries:
                        logger.warning(f"Retry {attempt+1}/{max_retries} after error: {str(e)}")
                        time.sleep(delay)
                        delay = min(delay * 2, max_delay)  # Exponential backoff
                    else:
                        logger.error(f"Failed after {max_retries} retries: {str(e)}")
            
            # If we get here, all retries failed
            raise last_exception
        
        return wrapper
    
    return decorator

class BedrockClient:
    """Wrapper for Bedrock client with retry logic"""
    
    def __init__(self, region_name='us-west-2'):
        self.client = boto3.client('bedrock-runtime', region_name=region_name)
    
    @retry_with_exponential_backoff(max_retries=3)
    def invoke_model(self, model_id, prompt, max_tokens=400, temperature=0.3):
        """
        Invoke Bedrock model with retry logic
        
        Args:
            model_id: Bedrock model ID
            prompt: Text prompt
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text
        """
        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                })
            )
            
            result = json.loads(response['body'].read())
            
            # Handle different response formats
            if 'content' in result:
                # Claude/Anthropic format
                return result.get('content', [{}])[0].get('text', '')
            elif 'completion' in result:
                # Titan/Amazon format
                return result.get('completion', '')
            else:
                return str(result)
                
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            error_msg = e.response.get('Error', {}).get('Message', str(e))
            
            # Log specific error details
            logger.error(f"Bedrock API error: {error_code} - {error_msg}")
            
            # Raise for retry
            raise

# Global instance
bedrock_client = BedrockClient()