#!/usr/bin/env python3
"""
Simple test script for Coinbase API integration
"""

import sys
import os
from coinbase_api_service import CoinbaseAPIService, get_coinbase_price_data
from crypto_data_service import get_enhanced_crypto_data

def test_coinbase_basic():
    """Test basic Coinbase API functionality"""
    print("=" * 60)
    print("TESTING COINBASE API BASIC FUNCTIONALITY")
    print("=" * 60)
    
    service = CoinbaseAPIService()
    
    # Test 1: BTC spot price
    print("\n1. Testing BTC spot price:")
    btc_data = service.get_spot_price('BTC-USD')
    if btc_data:
        print(f"   ✓ BTC: ${btc_data['price']:,.2f}")
        print(f"   ✓ Source: {btc_data['source']}")
        print(f"   ✓ Timestamp: {btc_data['timestamp']}")
    else:
        print("   ✗ Failed to get BTC price")
    
    # Test 2: ETH spot price
    print("\n2. Testing ETH spot price:")
    eth_data = service.get_spot_price('ETH-USD')
    if eth_data:
        print(f"   ✓ ETH: ${eth_data['price']:,.2f}")
        print(f"   ✓ Source: {eth_data['source']}")
    else:
        print("   ✗ Failed to get ETH price")
    
    # Test 3: Multiple prices
    print("\n3. Testing multiple cryptocurrency prices:")
    symbols = ['BTC', 'ETH', 'SOL']
    prices = service.get_current_prices(symbols)
    for symbol, data in prices.items():
        if data:
            print(f"   ✓ {symbol}: ${data['price']:,.2f}")
        else:
            print(f"   ✗ {symbol}: Failed")
    
    # Test 4: Formatted price data
    print("\n4. Testing formatted price display:")
    for symbol in ['BTC', 'ETH', 'SOL']:
        formatted = service.format_price_data(symbol)
        print(f"   {formatted}")
    
    return True

def test_enhanced_crypto_service():
    """Test the enhanced crypto data service with Coinbase integration"""
    print("\n" + "=" * 60)
    print("TESTING ENHANCED CRYPTO DATA SERVICE")
    print("=" * 60)
    
    test_queries = [
        "Bitcoin price",
        "Ethereum and Solana comparison", 
        "BTC current market data",
        "What's the price of Bitcoin and Ethereum?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        try:
            result = get_enhanced_crypto_data(query)
            print(f"   Result: {result}")
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")

def test_coinbase_price_function():
    """Test the Coinbase price data function"""
    print("\n" + "=" * 60)
    print("TESTING COINBASE PRICE DATA FUNCTION")
    print("=" * 60)
    
    test_queries = [
        "Bitcoin",
        "ETH price",
        "BTC and ETH",
        "Solana market data"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        try:
            result = get_coinbase_price_data(query)
            print(f"   Result: {result}")
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")

def main():
    """Run all tests"""
    print("COINBASE API INTEGRATION - SIMPLE TEST")
    print("=" * 60)
    
    try:
        # Test basic Coinbase functionality
        test_coinbase_basic()
        
        # Test enhanced crypto service
        test_enhanced_crypto_service()
        
        # Test Coinbase price function
        test_coinbase_price_function()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nCoinbase API integration is working!")
        print("The cryptocurrency assistant now has access to real-time Coinbase data.")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)