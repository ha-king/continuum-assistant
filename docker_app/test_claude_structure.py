"""
Test Claude Structure
Tests the structure of Claude integration without importing modules
"""

import os

def test_claude_structure():
    """Test the structure of Claude integration files"""
    print("TESTING CLAUDE INTEGRATION STRUCTURE")
    print("=" * 50)
    
    # Check file existence
    files_to_check = [
        "claude_tool_handler.py",
        "claude_aviation_assistant.py",
        "model_options.py"
    ]
    
    print("Checking file existence...")
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} does not exist")
    
    # Check claude_tool_handler.py structure
    print("\nChecking claude_tool_handler.py structure...")
    try:
        with open("claude_tool_handler.py", "r") as f:
            handler_code = f.read()
            
        # Check for key components
        checks = [
            ("ClaudeToolHandler class", "class ClaudeToolHandler"),
            ("AviationToolHandler class", "class AviationToolHandler"),
            ("AVIATION_TOOLS definition", "AVIATION_TOOLS ="),
            ("Tool use handling", "tool_use"),
            ("Tool result handling", "tool_result"),
            ("Tool use ID", "tool_use_id")
        ]
        
        for name, pattern in checks:
            if pattern in handler_code:
                print(f"✅ {name} found")
            else:
                print(f"❌ {name} not found")
    except Exception as e:
        print(f"❌ Error checking claude_tool_handler.py: {str(e)}")
    
    # Check claude_aviation_assistant.py structure
    print("\nChecking claude_aviation_assistant.py structure...")
    try:
        with open("claude_aviation_assistant.py", "r") as f:
            assistant_code = f.read()
            
        # Check for key components
        checks = [
            ("ClaudeAviationAssistant class", "class ClaudeAviationAssistant"),
            ("AVIATION_SYSTEM_PROMPT", "AVIATION_SYSTEM_PROMPT ="),
            ("aviation_assistant_claude function", "def aviation_assistant_claude"),
            ("Claude 4.0 reference", "claude-4-0")
        ]
        
        for name, pattern in checks:
            if pattern in assistant_code:
                print(f"✅ {name} found")
            else:
                print(f"❌ {name} not found")
    except Exception as e:
        print(f"❌ Error checking claude_aviation_assistant.py: {str(e)}")
    
    # Check app.py integration
    print("\nChecking app.py integration...")
    try:
        with open("app.py", "r") as f:
            app_code = f.read()
            
        # Check for key components
        checks = [
            ("Claude aviation assistant import", "from claude_aviation_assistant import"),
            ("Model options import", "from model_options import"),
            ("Claude 4.0 selection logic", "use_claude = selected_model =="),
            ("Claude aviation assistant usage", "aviation_assistant_claude if use_claude else")
        ]
        
        for name, pattern in checks:
            if pattern in app_code:
                print(f"✅ {name} found")
            else:
                print(f"❌ {name} not found")
    except Exception as e:
        print(f"❌ Error checking app.py: {str(e)}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_claude_structure()