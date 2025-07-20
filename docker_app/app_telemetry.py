"""
Telemetry integration for app.py
"""

import time
import uuid
import os

# Import telemetry (conditionally)
try:
    from telemetry import log_user_interaction, track_user_session, track_assistant_performance, track_routing_decision
    TELEMETRY_ENABLED = True
except ImportError:
    # Create dummy functions if telemetry module is not available
    def log_user_interaction(*args, **kwargs): pass
    def track_user_session(*args, **kwargs): pass
    def track_assistant_performance(*args, **kwargs): pass
    def track_routing_decision(*args, **kwargs): pass
    TELEMETRY_ENABLED = False

# Generate a session ID for this app instance
SESSION_ID = str(uuid.uuid4())

def track_app_startup():
    """Track application startup"""
    if not TELEMETRY_ENABLED:
        return
        
    track_user_session(
        user_id="system",
        session_id=SESSION_ID,
        action="app_startup",
        metadata={
            "app_version": os.environ.get("APP_VERSION", "unknown"),
            "environment": os.environ.get("ENVIRONMENT", "prod")
        }
    )

def track_user_query(user_id: str, query: str, tab_id: int):
    """Track user query"""
    if not TELEMETRY_ENABLED:
        return
        
    log_user_interaction(
        user_id=user_id,
        event_type="query",
        query=query,
        assistant_used="pending",
        response_time_ms=0,
        metadata={
            "tab_id": tab_id,
            "session_id": SESSION_ID,
            "query_length": len(query)
        }
    )

def track_assistant_response(user_id: str, query: str, assistant_used: str, response_time_ms: int, tab_id: int):
    """Track assistant response"""
    if not TELEMETRY_ENABLED:
        return
        
    log_user_interaction(
        user_id=user_id,
        event_type="response",
        query=query,
        assistant_used=assistant_used,
        response_time_ms=response_time_ms,
        metadata={
            "tab_id": tab_id,
            "session_id": SESSION_ID
        }
    )
    
    # Track assistant performance
    track_assistant_performance(
        assistant_name=assistant_used,
        query_type=detect_query_type(query),
        response_time_ms=response_time_ms,
        token_count=estimate_token_count(query),
        success=True
    )

def track_router_decision(query: str, matched_rule: str, assistant_used: str, confidence: float = 0.8):
    """Track router decision"""
    if not TELEMETRY_ENABLED:
        return
        
    track_routing_decision(
        query=query,
        matched_rule=matched_rule,
        assistant_used=assistant_used,
        confidence=confidence
    )

def track_tab_change(user_id: str, old_tab: int, new_tab: int):
    """Track tab change"""
    if not TELEMETRY_ENABLED:
        return
        
    track_user_session(
        user_id=user_id,
        session_id=SESSION_ID,
        action="tab_change",
        metadata={
            "old_tab": old_tab,
            "new_tab": new_tab
        }
    )

def track_error(user_id: str, query: str, error_message: str, tab_id: int):
    """Track error"""
    if not TELEMETRY_ENABLED:
        return
        
    log_user_interaction(
        user_id=user_id,
        event_type="error",
        query=query,
        assistant_used="error",
        response_time_ms=0,
        metadata={
            "tab_id": tab_id,
            "session_id": SESSION_ID,
            "error_message": error_message[:200]  # Truncate long error messages
        }
    )

def detect_query_type(query: str) -> str:
    """Detect the type of query based on content"""
    query_lower = query.lower()
    
    # Define patterns for different query types
    patterns = {
        "crypto": ["crypto", "bitcoin", "ethereum", "token", "blockchain", "coin"],
        "finance": ["finance", "stock", "market", "investment", "portfolio"],
        "aviation": ["flight", "aircraft", "airport", "aviation", "plane"],
        "formula1": ["f1", "formula 1", "racing", "grand prix", "driver"],
        "tech": ["code", "programming", "software", "algorithm", "api"],
        "prediction": ["predict", "forecast", "future", "will", "expect"]
    }
    
    # Check for matches
    for query_type, keywords in patterns.items():
        if any(keyword in query_lower for keyword in keywords):
            return query_type
    
    return "general"

def estimate_token_count(text: str) -> int:
    """Estimate token count based on text length"""
    # Rough estimate: 1 token ≈ 4 characters for English text
    return len(text) // 4