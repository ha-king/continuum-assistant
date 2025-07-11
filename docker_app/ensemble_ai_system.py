import boto3
import json
import asyncio
from datetime import datetime
import statistics

class EnsembleAISystem:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        self.models = [
            "us.amazon.nova-pro-v1:0",
            "anthropic.claude-3-5-sonnet-20241022-v1:0",
            "anthropic.claude-3-5-haiku-20241022-v1:0"
        ]
        self.domain_models = {
            'financial': ["us.amazon.nova-pro-v1:0", "anthropic.claude-3-5-sonnet-20241022-v1:0"],
            'technical': ["anthropic.claude-3-5-sonnet-20241022-v1:0", "us.amazon.nova-pro-v1:0"],
            'creative': ["anthropic.claude-3-5-haiku-20241022-v1:0", "us.amazon.nova-lite-v1:0"]
        }
        
    def detect_query_domain(self, query):
        """Detect query domain for model selection"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['price', 'market', 'finance', 'crypto', 'trading']):
            return 'financial'
        elif any(word in query_lower for word in ['code', 'technical', 'algorithm', 'programming']):
            return 'technical'
        elif any(word in query_lower for word in ['creative', 'story', 'design', 'art']):
            return 'creative'
        else:
            return 'general'
    
    async def get_model_response(self, model_id, prompt, system_prompt=""):
        """Get response from a specific model"""
        try:
            response = self.bedrock.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 400,
                    "temperature": 0.3,
                    "system": system_prompt
                })
            )
            
            result = json.loads(response['body'].read())
            return result.get('content', [{}])[0].get('text', '')
        except Exception as e:
            print(f"Model {model_id} error: {str(e)}")
            return ""
    
    async def ensemble_consensus(self, query, system_prompt=""):
        """Get consensus from multiple models"""
        domain = self.detect_query_domain(query)
        selected_models = self.domain_models.get(domain, self.models[:2])
        
        # Get responses from multiple models
        tasks = [self.get_model_response(model, query, system_prompt) for model in selected_models]
        responses = await asyncio.gather(*tasks)
        
        # Filter out empty responses
        valid_responses = [r for r in responses if r.strip()]
        
        if not valid_responses:
            return "No valid responses from ensemble models"
        
        # Generate consensus
        consensus_prompt = f"""
        Multiple AI models provided these responses to: "{query}"
        
        Responses:
        {chr(10).join([f"Model {i+1}: {resp}" for i, resp in enumerate(valid_responses)])}
        
        Provide a consensus response that:
        1. Combines the best insights from all responses
        2. Resolves any contradictions
        3. Provides the most accurate and comprehensive answer
        """
        
        consensus = await self.get_model_response(
            "anthropic.claude-3-5-sonnet-20241022-v1:0", 
            consensus_prompt
        )
        
        return consensus if consensus else valid_responses[0]
    
    def fine_tune_domain_response(self, query, base_response, domain):
        """Apply domain-specific fine-tuning to response"""
        domain_prompts = {
            'financial': "Enhance this financial response with specific metrics, market context, and risk considerations:",
            'technical': "Enhance this technical response with implementation details, best practices, and code examples:",
            'creative': "Enhance this creative response with more vivid details, emotional resonance, and artistic elements:"
        }
        
        if domain in domain_prompts:
            enhancement_prompt = f"{domain_prompts[domain]}\n\nOriginal: {base_response}"
            try:
                response = self.bedrock.invoke_model(
                    modelId="us.amazon.nova-pro-v1:0",
                    body=json.dumps({
                        "messages": [{"role": "user", "content": enhancement_prompt}],
                        "max_tokens": 300,
                        "temperature": 0.2
                    })
                )
                
                result = json.loads(response['body'].read())
                enhanced = result.get('content', [{}])[0].get('text', base_response)
                return enhanced
            except:
                return base_response
        
        return base_response

# Global instance
ensemble_ai = EnsembleAISystem()

async def get_ensemble_response(query, system_prompt=""):
    """Get ensemble AI response"""
    return await ensemble_ai.ensemble_consensus(query, system_prompt)

def get_fine_tuned_response(query, base_response):
    """Get domain fine-tuned response"""
    domain = ensemble_ai.detect_query_domain(query)
    return ensemble_ai.fine_tune_domain_response(query, base_response, domain)