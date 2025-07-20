"""
Streaming - Implement streaming responses for better user experience
"""

import streamlit as st
from typing import Callable, Optional, Any

def get_streaming_response(agent: Any, prompt: str) -> str:
    """
    Get streaming response from an agent
    
    Args:
        agent: Agent with streaming capability
        prompt: User query
        
    Returns:
        Full response text
    """
    placeholder = st.empty()
    full_response = ""
    
    try:
        # Check if agent has streaming capability
        if hasattr(agent, 'stream'):
            for chunk in agent.stream(prompt):
                full_response += chunk
                # Display with cursor effect
                placeholder.markdown(full_response + "▌")
            
            # Final display without cursor
            placeholder.markdown(full_response)
        else:
            # Fallback for agents without streaming
            response = agent(prompt)
            full_response = str(response)
            placeholder.markdown(full_response)
    except Exception as e:
        error_msg = f"Error during streaming: {str(e)}"
        placeholder.markdown(error_msg)
        full_response = error_msg
    
    return full_response

def stream_with_references(agent: Any, prompt: str) -> tuple:
    """
    Stream response and extract references
    
    Args:
        agent: Agent with streaming capability
        prompt: User query
        
    Returns:
        Tuple of (response_text, references_text)
    """
    full_response = get_streaming_response(agent, prompt)
    
    # Extract references if present
    references = ""
    if "**References Used:**" in full_response:
        ref_start = full_response.find("**References Used:**")
        if ref_start != -1:
            references = full_response[ref_start:]
            response_text = full_response[:ref_start].strip()
        else:
            response_text = full_response
    else:
        response_text = full_response
    
    return response_text, references