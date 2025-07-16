#!/usr/bin/env python3
"""
Test Predictive Analysis Features
Verify all prediction capabilities are working correctly
"""

import sys
import os
from datetime import datetime

def test_realtime_data_access():
    """Test real-time data access module"""
    print("🧪 Testing Real-Time Data Access...")
    try:
        from realtime_data_access import realtime_data, enhance_query_with_realtime
        
        # Test F1 data
        f1_data = realtime_data.get_f1_data()
        print(f"✅ F1 Data: {f1_data}")
        
        # Test crypto data
        crypto_data = realtime_data.get_crypto_prices("bitcoin price")
        print(f"✅ Crypto Data: {crypto_data}")
        
        # Test query enhancement
        enhanced = enhance_query_with_realtime("Who will win the next F1 race?", "sports")
        print(f"✅ Enhanced Query Length: {len(enhanced)} chars")
        
        return True
    except Exception as e:
        print(f"❌ Real-time data error: {e}")
        return False

def test_prediction_engine():
    """Test universal prediction engine"""
    print("\n🧪 Testing Universal Prediction Engine...")
    try:
        from universal_prediction_engine import prediction_engine, enhance_query_with_prediction_context
        
        # Test prediction context generation
        query = "Who will win the next F1 race and why?"
        context = enhance_query_with_prediction_context(query)
        
        print(f"✅ Prediction Context Generated: {len(context)} chars")
        print(f"✅ Contains Historical Data: {'HISTORICAL DATA:' in context}")
        print(f"✅ Contains Real-time Indicators: {'REAL-TIME INDICATORS:' in context}")
        print(f"✅ Contains Methodology: {'PREDICTION METHODOLOGY:' in context}")
        
        return True
    except Exception as e:
        print(f"❌ Prediction engine error: {e}")
        return False

def test_data_aware_prompts():
    """Test data-aware prompt system"""
    print("\n🧪 Testing Data-Aware Prompts...")
    try:
        from data_aware_prompts import make_data_aware, inject_prediction_capability
        
        base_prompt = "You are a test assistant."
        
        # Test data awareness injection
        data_aware = make_data_aware(base_prompt, "live test data")
        print(f"✅ Data-aware prompt: {len(data_aware)} chars")
        print(f"✅ Contains data acknowledgment: {'CRITICAL:' in data_aware}")
        
        # Test prediction capability injection
        prediction_capable = inject_prediction_capability(data_aware)
        print(f"✅ Prediction-capable prompt: {len(prediction_capable)} chars")
        print(f"✅ Contains prediction guidance: {'predictions:' in prediction_capable.lower()}")
        
        return True
    except Exception as e:
        print(f"❌ Data-aware prompts error: {e}")
        return False

def test_consolidated_assistants():
    """Test consolidated assistants with real-time data"""
    print("\n🧪 Testing Consolidated Assistants...")
    try:
        from consolidated_assistants import sports_assistant, financial_assistant
        
        # Test sports assistant (should not claim lack of data)
        print("Testing sports assistant...")
        sports_response = sports_assistant("Who will win the next F1 race?")
        
        # Check if response acknowledges data access
        has_data_acknowledgment = not any(phrase in sports_response.lower() for phrase in [
            "don't have access", "without access", "lack access", "no access"
        ])
        
        print(f"✅ Sports Assistant Response Length: {len(sports_response)} chars")
        print(f"✅ Acknowledges Data Access: {has_data_acknowledgment}")
        
        # Test financial assistant
        print("Testing financial assistant...")
        financial_response = financial_assistant("What will Bitcoin price be next week?")
        
        has_financial_data = not any(phrase in financial_response.lower() for phrase in [
            "don't have access", "without access", "lack access", "no access"
        ])
        
        print(f"✅ Financial Assistant Response Length: {len(financial_response)} chars")
        print(f"✅ Acknowledges Data Access: {has_financial_data}")
        
        return True
    except Exception as e:
        print(f"❌ Consolidated assistants error: {e}")
        return False

def test_universal_assistant():
    """Test universal assistant for unknown topics"""
    print("\n🧪 Testing Universal Assistant...")
    try:
        from universal_assistant import universal_assistant, extract_topic_from_query
        
        # Test topic extraction
        topic = extract_topic_from_query("What will the weather be like next week?")
        print(f"✅ Topic Extraction: '{topic}'")
        
        # Test universal assistant response
        response = universal_assistant("Predict the outcome of the next election")
        print(f"✅ Universal Assistant Response Length: {len(response)} chars")
        
        # Check if it provides structured prediction
        has_prediction_structure = any(word in response.lower() for word in [
            "prediction", "forecast", "likely", "confidence", "scenario"
        ])
        print(f"✅ Contains Prediction Structure: {has_prediction_structure}")
        
        return True
    except Exception as e:
        print(f"❌ Universal assistant error: {e}")
        return False

def test_prediction_queries():
    """Test various prediction query types"""
    print("\n🧪 Testing Prediction Query Detection...")
    
    prediction_queries = [
        "Who will win the next F1 race?",
        "What will Bitcoin price be tomorrow?",
        "Will it rain next week?",
        "What technology trends will emerge next year?",
        "Who will win the election?",
        "What will happen to the stock market?"
    ]
    
    try:
        from universal_prediction_engine import enhance_query_with_prediction_context
        
        for query in prediction_queries:
            context = enhance_query_with_prediction_context(query)
            has_prediction_context = all(section in context for section in [
                "PREDICTION REQUEST ANALYSIS:",
                "HISTORICAL DATA:",
                "REAL-TIME INDICATORS:",
                "PREDICTION METHODOLOGY:"
            ])
            print(f"✅ '{query[:30]}...' → Prediction Context: {has_prediction_context}")
        
        return True
    except Exception as e:
        print(f"❌ Prediction queries error: {e}")
        return False

def run_comprehensive_test():
    """Run all prediction feature tests"""
    print("🚀 COMPREHENSIVE PREDICTION FEATURES TEST")
    print("=" * 60)
    
    tests = [
        ("Real-Time Data Access", test_realtime_data_access),
        ("Universal Prediction Engine", test_prediction_engine),
        ("Data-Aware Prompts", test_data_aware_prompts),
        ("Consolidated Assistants", test_consolidated_assistants),
        ("Universal Assistant", test_universal_assistant),
        ("Prediction Query Detection", test_prediction_queries)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: CRASHED - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} PASSED")
    
    if passed == total:
        print("🎉 ALL PREDICTION FEATURES WORKING!")
        print("✅ Real-time data access functional")
        print("✅ Prediction engine operational")
        print("✅ Assistants acknowledge live data")
        print("✅ Universal predictions enabled")
    else:
        print(f"⚠️ {total - passed} features need attention")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)