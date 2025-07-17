"""
Test Claude Integration
Tests the integration of Claude 4.0 with the aviation assistant
"""

from claude_aviation_assistant import AVIATION_SYSTEM_PROMPT
from claude_tool_handler import AVIATION_TOOLS
from typing import Dict, List, Any
import json

def test_claude_integration():
    """Test the integration of Claude 4.0 with the aviation assistant"""
    print("TESTING CLAUDE 4.0 INTEGRATION")
    print("=" * 50)
    
    # Check system prompt
    print("Checking aviation system prompt...")
    if "tools" in AVIATION_SYSTEM_PROMPT.lower():
        print("✅ System prompt mentions tools")
    else:
        print("❌ System prompt doesn't mention tools")
    
    # Check aviation tools
    print("\nChecking aviation tools...")
    if len(AVIATION_TOOLS) > 0:
        print(f"✅ Found {len(AVIATION_TOOLS)} aviation tools")
        
        # Check tool definitions
        for i, tool in enumerate(AVIATION_TOOLS):
            print(f"\nTool {i+1}: {tool.get('name', 'unnamed')}")
            
            # Check required fields
            has_name = "name" in tool
            has_description = "description" in tool
            has_schema = "input_schema" in tool
            
            print(f"  Has name: {'✅' if has_name else '❌'}")
            print(f"  Has description: {'✅' if has_description else '❌'}")
            print(f"  Has input schema: {'✅' if has_schema else '❌'}")
            
            # Check schema format
            if has_schema:
                schema = tool.get("input_schema", {})
                has_properties = "properties" in schema
                has_required = "required" in schema
                
                print(f"  Schema has properties: {'✅' if has_properties else '❌'}")
                print(f"  Schema has required fields: {'✅' if has_required else '❌'}")
    else:
        print("❌ No aviation tools found")
    
    # Check app integration
    print("\nChecking app integration...")
    try:
        with open("app.py", "r") as f:
            app_code = f.read()
            
        if "aviation_assistant_claude" in app_code:
            print("✅ Claude aviation assistant imported in app.py")
        else:
            print("❌ Claude aviation assistant not imported in app.py")
            
        if "use_claude" in app_code and "selected_model" in app_code:
            print("✅ Model selection logic found in app.py")
        else:
            print("❌ Model selection logic not found in app.py")
    except Exception as e:
        print(f"❌ Error checking app integration: {str(e)}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_claude_integration()