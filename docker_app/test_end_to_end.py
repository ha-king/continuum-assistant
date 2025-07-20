"""
End-to-End Test Suite
Tests the complete workflow from user query to response
"""

import time
from typing import Dict, Any

# Import core components
from app import create_teacher_agent_with_datetime
from aviation_assistant import aviation_assistant
from shared_knowledge import store_knowledge, retrieve_knowledge
from aircraft_registry import get_registration
from aviation_data_access import aviation_data

def test_aviation_workflow():
    """Test the complete aviation workflow"""
    print("TESTING AVIATION WORKFLOW")
    print("=" * 50)
    
    # Step 1: Store knowledge about ElonJet
    print("Step 1: Storing knowledge about ElonJet...")
    store_knowledge("elonjet", "ElonJet is the tracking name for Elon Musk's private jet with registration N628TS", "test")
    
    # Step 2: Query about ElonJet through teacher agent
    print("\nStep 2: Querying about ElonJet through teacher agent...")
    query = "Where is ElonJet now?"
    
    # Create fresh teacher agent
    teacher = create_teacher_agent_with_datetime()
    
    # Process query through teacher agent
    print(f"Query: {query}")
    start_time = time.time()
    response = teacher(query)
    end_time = time.time()
    
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(f"Response: {response}")
    
    # Step 3: Direct query to aviation assistant
    print("\nStep 3: Directly querying aviation assistant...")
    direct_query = "What is ElonJet's tail number?"
    
    start_time = time.time()
    direct_response = aviation_assistant(direct_query)
    end_time = time.time()
    
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(f"Response: {direct_response}")
    
    # Step 4: Check if knowledge was properly stored and shared
    print("\nStep 4: Checking knowledge storage...")
    kb_result = retrieve_knowledge("elonjet")
    if kb_result:
        print(f"Knowledge found: {kb_result.get('data')}")
    else:
        print("No knowledge found for 'elonjet'")
    
    # Summary
    print("\nTEST SUMMARY")
    print("=" * 50)
    print(f"Teacher agent routing: {'PASSED' if 'N628TS' in str(response) else 'FAILED'}")
    print(f"Aviation assistant direct query: {'PASSED' if 'N628TS' in str(direct_response) else 'FAILED'}")
    print(f"Knowledge sharing: {'PASSED' if kb_result else 'FAILED'}")

if __name__ == "__main__":
    # Run test
    test_aviation_workflow()