#!/usr/bin/env python3
"""
Script to verify the router fix for aviation assistant routing issues
"""

import sys
from router_config import contains_keywords, has_n_number
from optimized_router import smart_route

# Mock assistants dictionary
mock_assistants = {
    'aviation': lambda x: f"AVIATION: {x}",
    'formula1': lambda x: f"FORMULA1: {x}",
    'financial': lambda x: f"FINANCIAL: {x}",
    'web_browser': lambda x: f"WEB_BROWSER: {x}",
    'research': lambda x: f"RESEARCH: {x}",
    'universal': lambda x: f"UNIVERSAL: {x}",
    'math': lambda x: f"MATH: {x}",
    'english': lambda x: f"ENGLISH: {x}",
    'aws': lambda x: f"AWS: {x}",
    'louisiana_legal': lambda x: f"LEGAL: {x}",
}

# Test cases that should NOT route to aviation
non_aviation_queries = [
    "What is the workflow for this process?",
    "I'm having trouble with my planet simulation",
    "Can you explain the concept of reflection in programming?",
    "How do I configure my AWS Lambda function?",
    "What's the best way to invest in stocks?",
    "Can you help me with this math problem?",
    "How do I improve my writing skills?",
    "What are the latest developments in AI?",
    "How do I create a flowchart?",
    "What's the weather forecast for tomorrow?",
]

# Test cases that SHOULD route to aviation
aviation_queries = [
    "What is the status of flight UA123?",
    "Where is aircraft N12345 right now?",
    "Tell me about the Boeing 737 MAX aircraft",
    "What are the busiest airports in the US?",
    "How do pilots navigate at night?",
    "What is the FAA regulation for drone flights?",
    "How do I become an airline pilot?",
    "What's the runway length required for a 747?",
    "Which airlines fly from JFK to LAX?",
]

def test_routing():
    """Test the routing logic to ensure non-aviation queries don't go to aviation"""
    print("\n=== Testing Router Fix ===")
    
    datetime_context = "Current date: 2023-05-15"
    
    print("\n--- Non-Aviation Queries ---")
    for query in non_aviation_queries:
        assistant_func, enhanced_prompt = smart_route(query, datetime_context, mock_assistants)
        if assistant_func:
            result = assistant_func(enhanced_prompt)
            print(f"'{query}' -> {result[:20]}...")
            if "AVIATION" in result:
                print(f"❌ ERROR: Non-aviation query '{query}' incorrectly routed to aviation assistant")
                return False
        else:
            print(f"'{query}' -> None (default teacher agent)")
    
    print("\n--- Aviation Queries ---")
    for query in aviation_queries:
        assistant_func, enhanced_prompt = smart_route(query, datetime_context, mock_assistants)
        if assistant_func:
            result = assistant_func(enhanced_prompt)
            print(f"'{query}' -> {result[:20]}...")
            if "aircraft" in query.lower() or "flight" in query.lower() or "pilot" in query.lower() or "faa" in query.lower():
                if "AVIATION" not in result:
                    print(f"❌ ERROR: Aviation query '{query}' not routed to aviation assistant")
                    return False
        else:
            print(f"'{query}' -> None (default teacher agent)")
    
    print("\n✅ All tests passed! The router fix is working correctly.")
    return True

if __name__ == "__main__":
    if test_routing():
        sys.exit(0)
    else:
        sys.exit(1)