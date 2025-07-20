"""
Test Claude Aviation Assistant
Verifies that Claude 4.0 tool handling works correctly
"""

from claude_aviation_assistant import aviation_assistant_claude
from claude_tool_handler import AviationToolHandler, AVIATION_TOOLS
import time

def test_claude_aviation():
    """Test Claude aviation assistant with tool handling"""
    print("TESTING CLAUDE 4.0 AVIATION ASSISTANT")
    print("=" * 50)
    
    # Test queries
    test_queries = [
        "Where is N628TS now?",
        "What kind of aircraft is ElonJet?",
        "Tell me about N628TS"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        
        start_time = time.time()
        try:
            response = aviation_assistant_claude(query)
            end_time = time.time()
            
            print(f"Response time: {end_time - start_time:.2f} seconds")
            print(f"Response: {response}")
            
            # Check for error indicators
            if "error" in response.lower():
                print("❌ Test FAILED - Error in response")
            else:
                print("✅ Test PASSED")
        except Exception as e:
            print(f"❌ Test FAILED - Exception: {str(e)}")

def test_tool_handler():
    """Test the tool handler directly"""
    print("\n\nTESTING CLAUDE TOOL HANDLER")
    print("=" * 50)
    
    handler = AviationToolHandler()
    
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
    
    print("Testing tool handler with query: 'Where is N628TS now?'")
    try:
        result = handler.handle_conversation(messages, AVIATION_TOOLS)
        
        # Check if tool was used
        tool_used = False
        for message in messages:
            if message.get("role") == "assistant" and "tool_use" in str(message):
                tool_used = True
                break
        
        if tool_used:
            print("✅ Tool was used correctly")
        else:
            print("❌ Tool was not used")
            
        # Check for errors
        if "error" in result:
            print(f"❌ Error in result: {result['error']}")
        else:
            print("✅ No errors in result")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_claude_aviation()
    test_tool_handler()