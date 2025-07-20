#!/usr/bin/env python3
\"\"\"
Test the validation fix for Claude API ValidationException
\"\"\"

import json
from claude_tool_handler import ClaudeToolHandler

def create_test_conversation():
    """Create a test conversation with mismatched tool_use and tool_result"""
    messages = [
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": [
            {"type": "text", "text": "I'll check the weather for you."},
            {"type": "tool_use", "id": "tool1", "name": "get_weather", "input": {"location": "Seattle"}}
        ]},
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool1", "content": {"temperature": 72, "condition": "sunny"}}
        ]},
        {"role": "assistant", "content": [
            {"type": "text", "text": "The weather in Seattle is sunny with a temperature of 72°F."}
        ]},
        {"role": "user", "content": "What about tomorrow?"},
        {"role": "assistant", "content": [
            {"type": "text", "text": "I'll check the forecast for tomorrow."},
            {"type": "tool_use", "id": "tool2", "name": "get_forecast", "input": {"location": "Seattle", "days": 1}}
        ]},
        # Missing tool_result for tool2
        {"role": "user", "content": "Thanks!"},
        {"role": "assistant", "content": [
            {"type": "text", "text": "You're welcome! Is there anything else you'd like to know?"}
        ]},
        {"role": "user", "content": "What's the flight status of N628TS?"},
        {"role": "assistant", "content": [
            {"type": "text", "text": "I'll check the flight status for you."},
            {"type": "tool_use", "id": "tool3", "name": "get_flight_position", "input": {"flight_id": "N628TS"}}
        ]},
        # Orphaned tool_result (no matching tool_use)
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool3", "content": {"position": {"lat": 47.6, "lng": -122.3}}},
            {"type": "tool_result", "tool_use_id": "tool4", "content": {"error": "Flight not found"}}
        ]}
    ]
    return messages

def test_validation_fix():
    """Test the validation fix"""
    print("Testing validation fix for Claude API ValidationException...")
    
    # Create test conversation with mismatched tool_use and tool_result
    messages = create_test_conversation()
    
    # Print original conversation
    print("\nOriginal conversation:")
    print(f"Number of messages: {len(messages)}")
    print("Tool use IDs:", [item.get('id') for msg in messages if msg.get('role') == 'assistant' 
                           for item in msg.get('content', []) if isinstance(item, dict) and item.get('type') == 'tool_use'])
    print("Tool result IDs:", [item.get('tool_use_id') for msg in messages if msg.get('role') == 'user' 
                              for item in msg.get('content', []) if isinstance(item, dict) and item.get('type') == 'tool_result'])
    
    # Create handler and validate conversation
    handler = ClaudeToolHandler()
    fixed_messages = handler._validate_conversation_history(messages)
    
    # Print fixed conversation
    print("\nFixed conversation:")
    print(f"Number of messages: {len(fixed_messages)}")
    print("Tool use IDs:", [item.get('id') for msg in fixed_messages if msg.get('role') == 'assistant' 
                           for item in msg.get('content', []) if isinstance(item, dict) and item.get('type') == 'tool_use'])
    print("Tool result IDs:", [item.get('tool_use_id') for msg in fixed_messages if msg.get('role') == 'user' 
                              for item in msg.get('content', []) if isinstance(item, dict) and item.get('type') == 'tool_result'])
    
    # Check if orphaned tool_result was removed
    original_tool_results = sum(1 for msg in messages if msg.get('role') == 'user' 
                               for item in msg.get('content', []) if isinstance(item, dict) and item.get('type') == 'tool_result')
    fixed_tool_results = sum(1 for msg in fixed_messages if msg.get('role') == 'user' 
                            for item in msg.get('content', []) if isinstance(item, dict) and item.get('type') == 'tool_result')
    
    print(f"\nOriginal tool results: {original_tool_results}")
    print(f"Fixed tool results: {fixed_tool_results}")
    
    if original_tool_results > fixed_tool_results:
        print("✅ Orphaned tool results were successfully removed")
    else:
        print("❌ Orphaned tool results were not removed")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_validation_fix()