#!/usr/bin/env python3
import sys
sys.path.append('/home/ubuntu/.venv/lib/python3.12/site-packages')

# Test all assistants to identify which need fixing
assistants = [
    ('english_assistant', 'help me write a professional email'),
    ('language_assistant', 'translate hello to spanish'),
    ('financial_assistant', 'calculate profit margin'),
    ('aws_assistant', 'explain EC2 instances'),
    ('business_dev_assistant', 'business growth strategies'),
    ('lafayette_economic_assistant', 'economic opportunities in lafayette'),
    ('louisiana_legal_assistant', 'louisiana business law'),
    ('no_expertise', 'general question about weather')
]

for assistant_name, test_query in assistants:
    try:
        module = __import__(assistant_name)
        func = getattr(module, assistant_name)
        print(f"\nTesting {assistant_name}:")
        result = func(test_query)
        print(f"SUCCESS: {str(result)[:100]}...")
    except Exception as e:
        print(f"\nERROR in {assistant_name}: {str(e)}")
        if "'module' object is not callable" in str(e):
            print(f"NEEDS FIXING: {assistant_name} has use_llm issue")