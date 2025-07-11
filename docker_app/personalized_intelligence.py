import json
from datetime import datetime
import boto3

class PersonalizedIntelligence:
    def __init__(self):
        self.user_profiles = {}
        self.conversation_memory = {}
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        
    def analyze_user_expertise(self, user_id, query, response_feedback=None):
        """Analyze user expertise level from interactions"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'expertise_level': 'intermediate',
                'preferred_topics': [],
                'technical_depth': 'balanced',
                'interaction_count': 0,
                'last_active': datetime.now().isoformat()
            }
        
        profile = self.user_profiles[user_id]
        profile['interaction_count'] += 1
        profile['last_active'] = datetime.now().isoformat()
        
        # Analyze query complexity
        technical_indicators = ['API', 'algorithm', 'protocol', 'implementation', 'architecture']
        basic_indicators = ['what is', 'how to', 'explain', 'simple']
        
        technical_score = sum(1 for indicator in technical_indicators if indicator.lower() in query.lower())
        basic_score = sum(1 for indicator in basic_indicators if indicator.lower() in query.lower())
        
        if technical_score > basic_score and profile['interaction_count'] > 5:
            profile['expertise_level'] = 'advanced'
        elif basic_score > technical_score:
            profile['expertise_level'] = 'beginner'
        
        return profile
    
    def personalize_response(self, user_id, query, base_response):
        """Personalize response based on user profile"""
        profile = self.user_profiles.get(user_id, {})
        expertise = profile.get('expertise_level', 'intermediate')
        
        personalization_prompt = f"""
        Adapt this response for a {expertise} level user:
        Original: {base_response[:500]}...
        
        Adjustments needed:
        - Beginner: Add definitions, use simple language, provide examples
        - Intermediate: Balance technical detail with clarity
        - Advanced: Include technical specifics, assume domain knowledge
        
        Provide the adapted response:
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId="us.amazon.nova-micro-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": personalization_prompt}],
                    "max_tokens": 400,
                    "temperature": 0.3
                })
            )
            
            result = json.loads(response['body'].read())
            personalized = result.get('content', [{}])[0].get('text', base_response)
            
            return personalized
            
        except Exception as e:
            print(f"Personalization error: {str(e)}")
            return base_response
    
    def maintain_conversation_context(self, user_id, query, response):
        """Maintain conversation memory for context"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        # Add current interaction
        self.conversation_memory[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response[:200] + "..." if len(response) > 200 else response
        })
        
        # Keep only last 10 interactions
        if len(self.conversation_memory[user_id]) > 10:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-10:]
    
    def get_conversation_context(self, user_id):
        """Get recent conversation context"""
        memory = self.conversation_memory.get(user_id, [])
        if not memory:
            return ""
        
        context_parts = []
        for interaction in memory[-3:]:  # Last 3 interactions
            context_parts.append(f"Previous Q: {interaction['query'][:100]}...")
        
        return "Recent conversation context: " + " | ".join(context_parts)
    
    def suggest_follow_up_questions(self, user_id, current_query, response):
        """Generate personalized follow-up suggestions"""
        profile = self.user_profiles.get(user_id, {})
        expertise = profile.get('expertise_level', 'intermediate')
        
        suggestion_prompt = f"""
        Based on this {expertise} level user's query about: {current_query}
        And the response provided, suggest 3 relevant follow-up questions that would:
        1. Deepen their understanding
        2. Explore related topics
        3. Apply the knowledge practically
        
        Format as: "You might also ask:"
        """
        
        try:
            response_obj = self.bedrock.invoke_model(
                modelId="us.amazon.nova-micro-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": suggestion_prompt}],
                    "max_tokens": 150,
                    "temperature": 0.4
                })
            )
            
            result = json.loads(response_obj['body'].read())
            suggestions = result.get('content', [{}])[0].get('text', '')
            
            return suggestions
            
        except Exception as e:
            print(f"Suggestion error: {str(e)}")
            return ""
    
    def detect_user_intent(self, query):
        """Detect user intent for better routing"""
        intents = {
            'learning': ['learn', 'understand', 'explain', 'teach me'],
            'problem_solving': ['how to', 'fix', 'solve', 'troubleshoot'],
            'analysis': ['analyze', 'compare', 'evaluate', 'assess'],
            'research': ['find', 'search', 'lookup', 'investigate'],
            'planning': ['plan', 'strategy', 'roadmap', 'approach']
        }
        
        query_lower = query.lower()
        detected_intents = []
        
        for intent, keywords in intents.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_intents.append(intent)
        
        return detected_intents[0] if detected_intents else 'general'
    
    def generate_user_insights(self, user_id):
        """Generate insights about user behavior and preferences"""
        profile = self.user_profiles.get(user_id, {})
        memory = self.conversation_memory.get(user_id, [])
        
        if not memory:
            return "No interaction history available"
        
        # Analyze interaction patterns
        topics = []
        for interaction in memory:
            # Simple topic extraction (could be enhanced with NLP)
            query = interaction['query'].lower()
            if 'crypto' in query or 'bitcoin' in query:
                topics.append('cryptocurrency')
            elif 'aws' in query or 'cloud' in query:
                topics.append('cloud_computing')
            elif 'market' in query or 'finance' in query:
                topics.append('finance')
        
        most_common_topic = max(set(topics), key=topics.count) if topics else 'general'
        
        insights = {
            'expertise_level': profile.get('expertise_level', 'intermediate'),
            'interaction_count': profile.get('interaction_count', 0),
            'primary_interest': most_common_topic,
            'engagement_level': 'high' if len(memory) > 5 else 'moderate'
        }
        
        return insights

# Global instance
personalized_intel = PersonalizedIntelligence()

def get_personalized_response(user_id, query, base_response):
    """Get personalized response for user"""
    # Analyze user and update profile
    personalized_intel.analyze_user_expertise(user_id, query)
    
    # Personalize the response
    personalized_response = personalized_intel.personalize_response(user_id, query, base_response)
    
    # Maintain conversation context
    personalized_intel.maintain_conversation_context(user_id, query, personalized_response)
    
    # Generate follow-up suggestions
    suggestions = personalized_intel.suggest_follow_up_questions(user_id, query, personalized_response)
    
    if suggestions:
        personalized_response += f"\n\n{suggestions}"
    
    return personalized_response

def get_user_insights(user_id):
    """Get insights about user behavior"""
    return personalized_intel.generate_user_insights(user_id)