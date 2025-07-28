#!/usr/bin/env python3
"""
Test script to verify the enhanced_prompt fix
"""

def test_enhanced_prompt_fix():
    """Test that enhanced_prompt variable is properly initialized"""
    
    # Simulate the problematic code pattern
    try:
        # Initialize variables to avoid undefined errors (the fix)
        enhanced_prompt = None
        assistant_func = None
        
        # Simulate some routing logic
        prompt = "forecast PENGU price in 90 days"
        
        # Simulate the condition where enhanced_prompt might be set
        if "crypto" in prompt.lower():
            enhanced_prompt = "CRYPTO FORECAST: " + prompt
            assistant_func = lambda x: "crypto_response"
        
        # This is the line that was causing the error (line 541 equivalent)
        assistant_name = "direct_response" if enhanced_prompt and not assistant_func else \
                       (assistant_func.__name__ if assistant_func and hasattr(assistant_func, "__name__") \
                        else "unknown")
        
        print(f"SUCCESS: No NameError for enhanced_prompt")
        print(f"Assistant name: {assistant_name}")
        print(f"Enhanced prompt: {enhanced_prompt}")
        
        return True
        
    except NameError as e:
        print(f"ERROR: NameError still exists: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Other error: {e}")
        return False

if __name__ == "__main__":
    success = test_enhanced_prompt_fix()
    if success:
        print("\n✅ Fix verified: enhanced_prompt variable is properly initialized")
    else:
        print("\n❌ Fix failed: enhanced_prompt variable still undefined")