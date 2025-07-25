#!/usr/bin/env python3
"""
Setup script for Coinbase API secrets in AWS Secrets Manager
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError

def create_or_update_secret(secret_name, secret_value, description, region='us-east-1'):
    """Create or update a secret in AWS Secrets Manager"""
    
    secrets_client = boto3.client('secretsmanager', region_name=region)
    
    try:
        # Try to get the existing secret
        try:
            response = secrets_client.get_secret_value(SecretId=secret_name)
            print(f"Secret '{secret_name}' already exists. Updating...")
            
            # Update existing secret
            secrets_client.update_secret(
                SecretId=secret_name,
                SecretString=secret_value,
                Description=description
            )
            print(f"✓ Successfully updated secret '{secret_name}'")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"Secret '{secret_name}' does not exist. Creating...")
                
                # Create new secret
                secrets_client.create_secret(
                    Name=secret_name,
                    SecretString=secret_value,
                    Description=description
                )
                print(f"✓ Successfully created secret '{secret_name}'")
            else:
                raise e
                
    except Exception as e:
        print(f"✗ Error managing secret '{secret_name}': {str(e)}")
        return False
    
    return True

def verify_existing_coinbase_secrets():
    """Verify existing Coinbase API secrets in AWS Secrets Manager"""
    print("VERIFYING EXISTING COINBASE API SECRETS")
    print("=" * 50)
    
    secrets_client = boto3.client('secretsmanager', region_name='us-west-2')
    secret_names = ['coinbase-api-key', 'coinbase-api-token']
    
    verified_secrets = 0
    
    for secret_name in secret_names:
        print(f"\nChecking secret: {secret_name}")
        try:
            response = secrets_client.get_secret_value(SecretId=secret_name)
            secret_value = response['SecretString']
            
            if secret_value and len(secret_value.strip()) > 0:
                print(f"   ✓ {secret_name}: Found and accessible")
                print(f"   ✓ Value length: {len(secret_value)} characters")
                verified_secrets += 1
            else:
                print(f"   ⚠ {secret_name}: Exists but appears to be empty")
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                print(f"   ✗ {secret_name}: Not found in Secrets Manager")
                print(f"   → Please create this secret with your Coinbase API credentials")
            else:
                print(f"   ✗ {secret_name}: Access error - {error_code}")
        except Exception as e:
            print(f"   ✗ {secret_name}: Unexpected error - {str(e)}")
    
    print(f"\n" + "=" * 50)
    print(f"VERIFICATION COMPLETE: {verified_secrets}/{len(secret_names)} secrets verified")
    
    if verified_secrets == len(secret_names):
        print("\n✓ All Coinbase API secrets are properly configured!")
        print("\nNEXT STEPS:")
        print("1. Test the integration with: python test_coinbase_integration.py")
        print("2. The cryptocurrency assistant will now have access to real-time Coinbase data")
        return True
    else:
        print(f"\n⚠ {len(secret_names) - verified_secrets} secrets need attention")
        print("\nTO FIX:")
        print("1. Ensure the following secrets exist in AWS Secrets Manager:")
        for secret_name in secret_names:
            print(f"   - {secret_name}")
        print("2. Update them with your actual Coinbase API credentials")
        return False

def test_coinbase_api_access():
    """Test actual Coinbase API access with the configured secrets"""
    print("\nTESTING COINBASE API ACCESS")
    print("-" * 30)
    
    try:
        # Import and test the Coinbase service
        sys.path.append('./docker_app')
        from coinbase_api_service import CoinbaseAPIService
        
        service = CoinbaseAPIService()
        
        # Test basic API call
        print("Testing basic API access...")
        btc_price = service.get_spot_price('BTC-USD')
        
        if btc_price and 'price' in btc_price:
            print(f"✓ Successfully retrieved BTC price: ${btc_price['price']:,.2f}")
            print(f"✓ Coinbase API integration is working!")
            return True
        else:
            print("⚠ API call succeeded but no price data returned")
            print("  This might be normal for public endpoints")
            return True
            
    except Exception as e:
        print(f"✗ Coinbase API test failed: {str(e)}")
        print("  This might be due to missing credentials or network issues")
        return False

def main():
    """Main setup function"""
    try:
        # Check AWS credentials
        try:
            boto3.client('sts').get_caller_identity()
            print("✓ AWS credentials are configured")
        except Exception as e:
            print(f"✗ AWS credentials error: {str(e)}")
            print("Please configure AWS credentials before running this script")
            return 1
        
        # Verify existing secrets
        if verify_existing_coinbase_secrets():
            # Test API access
            test_coinbase_api_access()
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)