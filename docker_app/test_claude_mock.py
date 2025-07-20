"""
Test Claude Tool Format with Mock Data
Tests the Claude tool handling with mock data
"""

from typing import Dict, List, Any

class MockClaudeToolHandler:
    """Mock implementation of Claude tool handler for testing"""
    
    def __init__(self):
        self.tools_executed = []
    
    def handle_conversation(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """Handle a conversation with tools using mock data"""
        # Check if this is a flight query
        query = self._get_last_user_query(messages)
        if not query:
            return {"error": "No user query found"}
        
        # Check if query is about N628TS
        if "N628TS" in query or "elonjet" in query.lower():
            # Simulate tool use for flight position
            tool_use_id = "tooluse_mock_123456"
            tool_name = "get_flight_position"
            tool_params = {"flight_id": "N628TS"}
            
            # Add tool use to messages
            messages.append({
                "role": "assistant", 
                "content": [{
                    "type": "tool_use",
                    "id": tool_use_id,
                    "name": tool_name,
                    "input": tool_params
                }]
            })
            
            # Execute tool (mock)
            tool_result = self._execute_tool(tool_name, tool_params)
            
            # Add tool result to messages
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": tool_result
                }]
            })
            
            # Add final response
            messages.append({
                "role": "assistant",
                "content": [{
                    "type": "text",
                    "text": "N628TS is a Gulfstream G650ER owned by a private owner. According to the flight data, it is currently on the ground and not transmitting flight data."
                }]
            })
            
            return {
                "messages": messages,
                "response": {
                    "content": [{
                        "type": "text",
                        "text": "N628TS is a Gulfstream G650ER owned by a private owner. According to the flight data, it is currently on the ground and not transmitting flight data."
                    }]
                }
            }
        else:
            # Regular response without tool use
            messages.append({
                "role": "assistant",
                "content": [{
                    "type": "text",
                    "text": f"I don't have specific information about that aircraft. Please provide a registration number like N628TS."
                }]
            })
            
            return {
                "messages": messages,
                "response": {
                    "content": [{
                        "type": "text",
                        "text": f"I don't have specific information about that aircraft. Please provide a registration number like N628TS."
                    }]
                }
            }
    
    def _get_last_user_query(self, messages: List[Dict]) -> str:
        """Get the last user query from messages"""
        for message in reversed(messages):
            if message.get("role") == "user":
                content = message.get("content", "")
                if isinstance(content, str):
                    return content
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            return item.get("text", "")
                        elif isinstance(item, str):
                            return item
        return ""
    
    def _execute_tool(self, tool_name: str, params: Dict) -> Dict:
        """Mock tool execution"""
        self.tools_executed.append((tool_name, params))
        
        if tool_name == "get_flight_position":
            flight_id = params.get("flight_id")
            if flight_id == "N628TS":
                return {
                    "position": "N628TS: Gulfstream G650ER (Private owner) - Currently on ground, not transmitting flight data"
                }
        
        return {"error": "Unknown tool or parameters"}

def test_mock_conversation():
    """Test a mock conversation with tool use"""
    print("TESTING MOCK CLAUDE CONVERSATION")
    print("=" * 50)
    
    handler = MockClaudeToolHandler()
    
    # Test with a query that should trigger tool use
    messages = [
        {
            "role": "system",
            "content": "You are an aviation assistant. Use tools to get flight information."
        },
        {
            "role": "user",
            "content": "Where is N628TS now?"
        }
    ]
    
    print("Query: Where is N628TS now?")
    result = handler.handle_conversation(messages, [])
    
    # Check if tool was used
    tool_used = False
    tool_result_found = False
    
    for message in messages:
        if message.get("role") == "assistant":
            content = message.get("content", [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "tool_use":
                        tool_used = True
        
        if message.get("role") == "user":
            content = message.get("content", [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "tool_result":
                        tool_result_found = True
    
    print(f"Tool was used: {'✅ Yes' if tool_used else '❌ No'}")
    print(f"Tool result found: {'✅ Yes' if tool_result_found else '❌ No'}")
    
    # Check final response
    final_message = messages[-1]
    if final_message.get("role") == "assistant":
        content = final_message.get("content", [])
        if isinstance(content, list) and len(content) > 0:
            if isinstance(content[0], dict) and content[0].get("type") == "text":
                print(f"Final response: {content[0].get('text')}")
    
    # Check conversation flow
    print("\nConversation flow:")
    for i, message in enumerate(messages):
        role = message.get("role")
        content_type = "unknown"
        
        if isinstance(message.get("content"), list) and len(message.get("content")) > 0:
            content = message.get("content")[0]
            if isinstance(content, dict):
                content_type = content.get("type", "unknown")
        
        print(f"{i+1}. {role}: {content_type}")
    
    # Verify correct sequence: user -> assistant (tool_use) -> user (tool_result) -> assistant (text)
    expected_sequence = ["system", "user", "assistant", "user", "assistant"]
    actual_sequence = [message.get("role") for message in messages]
    
    if actual_sequence == expected_sequence:
        print("\n✅ Conversation sequence is correct")
    else:
        print("\n❌ Conversation sequence is incorrect")
        print(f"Expected: {expected_sequence}")
        print(f"Actual: {actual_sequence}")

if __name__ == "__main__":
    test_mock_conversation()