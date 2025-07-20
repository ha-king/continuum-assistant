#!/usr/bin/env python3
"""
Test the validation fix for Claude API ValidationException:
'tool_use ids were found without tool_result blocks immediately after'
"""

import json
from claude_tool_handler import ClaudeToolHandler

def create_test_conversation():
    """Create a test conversation with missing tool_result after tool_use"""
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
            {"type": "text", "text": "You're welcome! Is there anything else you'd like to know?"},
            {"type": "tool_use", "id": "tool3", "name": "get_flight_position", "input": {"flight_id": "N628TS"}}
        ]},
        # Missing tool_result for tool3
    ]
    return messages

def test_validation_fix():
    """Test the validation fix"""
    print("Testing validation fix for Claude API ValidationException...")
    
    # Create test conversation with missing tool_results
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
    
    # Check if missing tool_results were added
    original_tool_uses = sum(1 for msg in messages if msg.get('role') == 'assistant' 
                            for item in msg.get('content', []) if isinstance(item, dict) and item.get('type') == 'tool_use'])
    original_tool_results = sum(1 for msg in messages if msg.get('role') == 'user' 
                               for item in msg.get('content', []) if isinstance(item, dict) and item.get('type') == 'tool_result'])
    fixed_tool_results = sum(1 for msg in fixed_messages if msg.get('role') == 'user' 
                            for item in msg.get('content', []) if isinstance(item, dict) and item.get('type') == 'tool_result'])
    
    print(f"\nOriginal tool uses: {original_tool_uses}")
    print(f"Original tool results: {original_tool_results}")
    print(f"Fixed tool results: {fixed_tool_results}")
    
    if fixed_tool_results == original_tool_uses:
        print("✅ Missing tool results were successfully added")
    else:
        print("❌ Not all tool uses have matching tool results")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_validation_fix()