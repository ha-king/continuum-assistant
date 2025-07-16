"""
Universal Assistant
Handles any topic with prediction capabilities when no specific assistant exists
"""

from strands import Agent, tool
from universal_prediction_engine import enhance_query_with_prediction_context
from prediction_system_prompt import get_topic_specific_prediction_prompt
from realtime_data_access import enhance_query_with_realtime

UNIVERSAL_SYSTEM_PROMPT = """
You are UniversalAssist, an advanced AI assistant capable of analyzing and predicting outcomes for ANY topic.

CORE CAPABILITIES:
1. **Universal Knowledge** - Draw from broad knowledge across all domains
2. **Predictive Analysis** - Make forecasts using historical patterns + real-time data
3. **Cross-domain Synthesis** - Connect insights across different fields
4. **Adaptive Reasoning** - Adjust approach based on topic complexity

APPROACH FOR ANY TOPIC:
1. **Understand Context** - Analyze what the user is asking about
2. **Gather Information** - Use historical knowledge + real-time data provided
3. **Identify Patterns** - Look for trends, cycles, and correlations
4. **Make Predictions** - Provide reasoned forecasts with confidence levels
5. **Explain Reasoning** - Show how you arrived at conclusions

PREDICTION METHODOLOGY:
- Historical pattern recognition
- Current trend analysis
- Multi-factor consideration
- Scenario planning
- Risk assessment
- Confidence calibration

Always provide structured predictions with reasoning, confidence levels, and alternative scenarios.
"""

@tool
def universal_assistant(query: str) -> str:
    """
    Universal assistant for any topic with prediction capabilities
    
    Args:
        query: Any question or prediction request
        
    Returns:
        Comprehensive analysis with predictions when requested
    """
    try:
        print("Routed to Universal Assistant")
        
        # Determine if this is a prediction query
        is_prediction = any(word in query.lower() for word in [
            'predict', 'forecast', 'will', 'future', 'next', 'expect', 
            'anticipate', 'likely', 'outcome', 'trend', 'projection'
        ])
        
        if is_prediction:
            # Use prediction engine for enhanced context
            enhanced_query = enhance_query_with_prediction_context(query)
            
            # Get topic-specific prediction prompt
            topic = extract_topic_from_query(query)
            system_prompt = get_topic_specific_prediction_prompt(topic, UNIVERSAL_SYSTEM_PROMPT)
        else:
            # Use regular real-time enhancement
            enhanced_query = enhance_query_with_realtime(query, "general")
            system_prompt = UNIVERSAL_SYSTEM_PROMPT
        
        # Create universal agent
        universal_agent = Agent(
            system_prompt=system_prompt,
            tools=[],
        )
        
        agent_response = universal_agent(enhanced_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "I can help analyze this topic. Please provide more specific details about what you'd like to know."
            
    except Exception as e:
        return f"Analysis error: {str(e)}"

def extract_topic_from_query(query: str) -> str:
    """Extract main topic from query for routing"""
    # Remove common prediction words
    prediction_words = ['predict', 'forecast', 'will', 'future', 'next', 'expect', 'anticipate', 'who', 'what', 'when', 'where', 'why', 'how']
    
    words = query.lower().split()
    topic_words = [word for word in words if word not in prediction_words and len(word) > 2]
    
    # Return first few meaningful words as topic
    if len(topic_words) >= 2:
        return ' '.join(topic_words[:3])
    elif len(topic_words) == 1:
        return topic_words[0]
    else:
        return "general"