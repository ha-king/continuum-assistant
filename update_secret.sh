#!/bin/bash

# Script to update Cognito secret with new pool ID and client ID
# Usage: ./update_secret.sh <env> <pool_id> <client_id>

ENV=$1
POOL_ID=$2
CLIENT_ID=$3

if [ -z "$ENV" ] || [ -z "$POOL_ID" ] || [ -z "$CLIENT_ID" ]; then
  echo "Usage: ./update_secret.sh <env> <pool_id> <client_id>"
  echo "Example: ./update_secret.sh prod pool-us-west-2_abcdef123 1a2b3c4d5e6f7g8h9i0j"
  exit 1
fi

SECRET_NAME="StreamlitParamCognitoSecret12345-${ENV}"

# Get current secret value
echo "Getting current secret value..."
CURRENT_SECRET=$(aws secretsmanager get-secret-value --secret-id $SECRET_NAME --query 'SecretString' --output text)

if [ $? -ne 0 ]; then
  echo "Error getting secret value. Make sure the secret exists and you have permission to access it."
  exit 1
fi

# Extract client secret from current secret
CLIENT_SECRET=$(echo $CURRENT_SECRET | jq -r '.app_client_secret')

if [ -z "$CLIENT_SECRET" ]; then
  echo "Warning: Could not extract client secret from current secret. Using placeholder."
  CLIENT_SECRET="placeholder"
fi

# Create new secret value
NEW_SECRET=$(cat <<EOF
{
  "pool_id": "$POOL_ID",
  "app_client_id": "$CLIENT_ID",
  "app_client_secret": "$CLIENT_SECRET"
}
EOF
)

# Update secret
echo "Updating secret with new values..."
aws secretsmanager update-secret --secret-id $SECRET_NAME --secret-string "$NEW_SECRET"

if [ $? -eq 0 ]; then
  echo "Secret updated successfully!"
  echo "New values:"
  echo "  Pool ID: $POOL_ID"
  echo "  Client ID: $CLIENT_ID"
  echo "  Client Secret: [preserved from existing secret]"
else
  echo "Error updating secret."
  exit 1
fi