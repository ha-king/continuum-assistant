#!/usr/bin/env python3
import sys
sys.path.append('/home/ubuntu/.venv/lib/python3.12/site-packages')

# Test the web browser assistant with strands_tools integration
try:
    from web_browser_assistant import web_browser_assistant
    print("Testing web browser assistant with strands_tools integration...")
    
    query = "browse and summarize infascination.com"
    result = web_browser_assistant(query)
    
    print("SUCCESS: Web browser assistant working with strands_tools")
    print("Result preview:", str(result)[:300] + "...")
    
except Exception as e:
    print("ERROR:", str(e))
    import traceback
    traceback.print_exc()