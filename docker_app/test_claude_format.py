"""
Test Claude Tool Format
Verifies that the tool format is correct without making API calls
"""

def test_tool_format():
    """Test that the tool format is correct for Claude"""
    print("TESTING CLAUDE TOOL FORMAT")
    print("=" * 50)
    
    # Example tool use from Claude
    tool_use = {
        "type": "tool_use",
        "id": "tooluse_WEo1w2e_Q-SZ7CPUKu6vLg",
        "name": "get_flight_position",
        "input": {
            "flight_id": "N628TS"
        }
    }
    
    # Correct tool result format
    tool_result = {
        "type": "tool_result",
        "tool_use_id": "tooluse_WEo1w2e_Q-SZ7CPUKu6vLg",
        "content": {
            "position": "N628TS: Gulfstream G650ER (Private owner) - Currently on ground, not transmitting flight data"
        }
    }
    
    # Example conversation flow
    conversation = [
        {"role": "user", "content": "Where is N628TS now?"},
        {"role": "assistant", "content": [tool_use]},
        {"role": "user", "content": [tool_result]},
        {"role": "assistant", "content": "N628TS is a Gulfstream G650ER owned by a private owner. According to the flight data, it is currently on the ground and not transmitting flight data."}
    ]
    
    # Verify the format
    print("Checking conversation format...")
    
    # Check 1: Tool use must have an ID
    if "id" not in tool_use:
        print("❌ Tool use missing ID")
    else:
        print("✅ Tool use has ID")
    
    # Check 2: Tool result must reference the tool use ID
    if tool_result.get("tool_use_id") != tool_use.get("id"):
        print("❌ Tool result ID doesn't match tool use ID")
    else:
        print("✅ Tool result references correct tool use ID")
    
    # Check 3: Tool result must follow tool use in conversation
    tool_use_index = -1
    tool_result_index = -1
    
    for i, message in enumerate(conversation):
        content = message.get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "tool_use":
                        tool_use_index = i
                    elif item.get("type") == "tool_result":
                        tool_result_index = i
    
    if tool_use_index == -1:
        print("❌ No tool use found in conversation")
    elif tool_result_index == -1:
        print("❌ No tool result found in conversation")
    elif tool_result_index != tool_use_index + 1:
        print("❌ Tool result does not immediately follow tool use")
    else:
        print("✅ Tool result immediately follows tool use")
    
    # Check our implementation in claude_tool_handler.py
    print("\nChecking our implementation...")
    try:
        with open("claude_tool_handler.py", "r") as f:
            handler_code = f.read()
            
        # Check for key components
        if "tool_use_id" in handler_code and "tool_result" in handler_code:
            print("✅ Tool handler contains required components")
        else:
            print("❌ Tool handler missing required components")
            
        # Check for proper message structure
        if "messages.append({\"role\": \"assistant\", \"content\":" in handler_code and "messages.append({\"role\": \"user\", \"content\":" in handler_code:
            print("✅ Tool handler uses correct message structure")
        else:
            print("❌ Tool handler uses incorrect message structure")
    except Exception as e:
        print(f"❌ Error checking implementation: {str(e)}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_tool_format()