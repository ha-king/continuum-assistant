#!/usr/bin/env python3
import sys
sys.path.append('/home/ubuntu/.venv/lib/python3.12/site-packages')

# Test charter number query routing
try:
    from web_browser_assistant import web_browser_assistant
    from research_assistant import research_assistant
    
    query = "what is the charter number of infascination, llc"
    
    print("Testing Web Browser Assistant:")
    web_result = web_browser_assistant(query)
    print("Result:", str(web_result)[:200] + "...")
    
    print("\nTesting Research Assistant:")
    research_result = research_assistant(query)
    print("Result:", str(research_result)[:200] + "...")
    
except Exception as e:
    print("ERROR:", str(e))
    import traceback
    traceback.print_exc()