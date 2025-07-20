import json
import boto3
import os
import cfnresponse

def handler(event, context):
    """
    Lambda function to update an existing secret with new Cognito details
    """
    try:
        # Extract parameters from the event
        properties = event['ResourceProperties']
        secret_name = properties.get('SecretName')
        pool_id = properties.get('PoolId')
        client_id = properties.get('ClientId')
        client_secret = properties.get('ClientSecret')
        
        if not all([secret_name, pool_id, client_id]):
            raise ValueError("Missing required parameters")
        
        # Initialize Secrets Manager client
        secrets_client = boto3.client('secretsmanager')
        
        # Get current secret value
        try:
            current_secret = secrets_client.get_secret_value(SecretId=secret_name)
            current_value = json.loads(current_secret['SecretString'])
        except Exception:
            # If secret doesn't exist or can't be read, create a new value
            current_value = {}
        
        # Update with new values
        new_value = {
            "pool_id": pool_id,
            "app_client_id": client_id,
        }
        
        # Only update client_secret if provided
        if client_secret:
            new_value["app_client_secret"] = client_secret
        elif "app_client_secret" in current_value:
            new_value["app_client_secret"] = current_value["app_client_secret"]
        
        # Update the secret
        secrets_client.update_secret(
            SecretId=secret_name,
            SecretString=json.dumps(new_value)
        )
        
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {
            'Message': f'Secret {secret_name} updated successfully'
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {
            'Message': f'Error updating secret: {str(e)}'
        })