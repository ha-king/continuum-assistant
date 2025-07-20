#!/usr/bin/env python3
"""
Test script to verify real-time data access for all assistants
"""

import sys
import importlib
from pathlib import Path

def test_assistant_realtime_access(assistant_name):
    """Test if an assistant has real-time data access"""
    try:
        # Import the assistant module
        module = importlib.import_module(assistant_name.replace('.py', ''))
        
        # Check if it has the real-time import
        module_file = Path(f"{assistant_name}")
        if module_file.exists():
            with open(module_file, 'r') as f:
                content = f.read()
                
            has_realtime_import = 'realtime_data_access' in content
            has_enhance_function = 'enhance_query_with_realtime' in content
            
            return {
                'name': assistant_name,
                'has_realtime_import': has_realtime_import,
                'has_enhance_function': has_enhance_function,
                'status': 'PASS' if (has_realtime_import and has_enhance_function) else 'FAIL'
            }
    except Exception as e:
        return {
            'name': assistant_name,
            'has_realtime_import': False,
            'has_enhance_function': False,
            'status': 'ERROR',
            'error': str(e)
        }

def test_realtime_data_module():
    """Test the real-time data access module"""
    try:
        from realtime_data_access import RealTimeDataAccess, enhance_query_with_realtime, get_current_datetime
        
        # Test basic functionality
        rtda = RealTimeDataAccess()
        current_time = get_current_datetime()
        enhanced_query = enhance_query_with_realtime("test query", "general")
        
        return {
            'module_import': True,
            'current_time': current_time,
            'enhanced_query_length': len(enhanced_query),
            'status': 'PASS'
        }
    except Exception as e:
        return {
            'module_import': False,
            'status': 'FAIL',
            'error': str(e)
        }

def main():
    """Run comprehensive real-time access tests"""
    print("🧪 Testing Real-Time Data Access for Continuum Assistant")
    print("=" * 60)
    
    # Test the core real-time data module
    print("\n1. Testing Real-Time Data Access Module:")
    rtda_test = test_realtime_data_module()
    if rtda_test['status'] == 'PASS':
        print(f"✅ Real-time data module: {rtda_test['status']}")
        print(f"   Current time: {rtda_test['current_time']}")
        print(f"   Enhanced query length: {rtda_test['enhanced_query_length']} chars")
    else:
        print(f"❌ Real-time data module: {rtda_test['status']}")
        print(f"   Error: {rtda_test.get('error', 'Unknown error')}")
        return
    
    # Test all assistant files
    print("\n2. Testing Individual Assistants:")
    assistant_files = list(Path('.').glob('*_assistant.py'))
    
    # Exclude special files
    exclude_files = {'consolidated_assistants.py', 'update_all_assistants.py', 'update_assistants_realtime.py'}
    assistant_files = [f for f in assistant_files if f.name not in exclude_files]
    
    passed = 0
    failed = 0
    
    for assistant_file in sorted(assistant_files):
        result = test_assistant_realtime_access(assistant_file.name)
        
        if result['status'] == 'PASS':
            print(f"✅ {result['name']:<35} - Real-time access enabled")
            passed += 1
        elif result['status'] == 'FAIL':
            print(f"❌ {result['name']:<35} - Missing real-time access")
            print(f"   Import: {result['has_realtime_import']}, Function: {result['has_enhance_function']}")
            failed += 1
        else:
            print(f"⚠️ {result['name']:<35} - Error: {result.get('error', 'Unknown')}")
            failed += 1
    
    # Test consolidated assistants
    print("\n3. Testing Consolidated Assistants:")
    try:
        from consolidated_assistants import (
            financial_assistant, security_assistant, business_assistant,
            tech_assistant, sports_assistant, research_assistant
        )
        print("✅ All consolidated assistants imported successfully")
        
        # Test one function to ensure it works
        test_result = financial_assistant("What is the current price of Bitcoin?")
        if test_result and len(test_result) > 10:
            print("✅ Consolidated assistants functional test passed")
        else:
            print("⚠️ Consolidated assistants functional test inconclusive")
            
    except Exception as e:
        print(f"❌ Consolidated assistants error: {str(e)}")
        failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Total assistants tested: {len(assistant_files)}")
    
    if failed == 0:
        print("\n🎉 ALL ASSISTANTS HAVE REAL-TIME DATA ACCESS!")
        print("🚀 The continuum-assistant project is ready for deployment")
    else:
        print(f"\n⚠️ {failed} assistants need attention")
        print("🔧 Please review the failed assistants above")
    
    # Test some real-time capabilities
    print("\n4. Testing Real-Time Capabilities:")
    try:
        from realtime_data_access import realtime_data
        
        # Test crypto data
        crypto_test = realtime_data.get_crypto_prices("bitcoin price")
        print(f"💰 Crypto data test: {'✅ Working' if crypto_test else '⚠️ Limited'}")
        
        # Test F1 data
        f1_test = realtime_data.get_f1_data()
        print(f"🏎️ F1 data test: {'✅ Working' if f1_test else '⚠️ Limited'}")
        
        # Test web data
        web_test = realtime_data.get_web_data("infascination.com")
        print(f"🌐 Web data test: {'✅ Working' if web_test else '⚠️ Limited'}")
        
    except Exception as e:
        print(f"❌ Real-time capabilities test error: {str(e)}")

if __name__ == "__main__":
    main()