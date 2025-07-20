# Conversation Storage Implementation

This document describes the implementation of persistent conversation storage using the baggage-claim pattern.

## Architecture

The conversation storage system uses a combination of DynamoDB and S3:

1. **DynamoDB Table**: Stores metadata about conversations
   - Partition key: `conversation_id` (user_id)
   - Attributes: user_id, last_updated, message_count, s3_key, last_message

2. **S3 Bucket**: Stores the actual conversation data
   - Key format: `conversations/{user_id}/{timestamp}.json`
   - Content: JSON array of message objects

## Baggage-Claim Pattern

The baggage-claim pattern is used to minimize DynamoDB storage costs:

1. **Check-in**: When a conversation is saved, the full conversation history is stored in S3
2. **Claim ticket**: A reference to the S3 object is stored in DynamoDB
3. **Claim**: When loading a conversation, the reference is retrieved from DynamoDB and used to fetch the full data from S3

## Benefits

- **Cost-effective**: DynamoDB stores only metadata, reducing storage costs
- **Scalable**: S3 can handle large conversation histories efficiently
- **Performant**: DynamoDB provides fast lookups for conversation metadata
- **Durable**: Both DynamoDB and S3 provide high durability for data

## Implementation

The implementation consists of:

1. **CDK Stack**: Defines the DynamoDB table and S3 bucket
2. **Conversation Storage Module**: Provides the API for saving and loading conversations
3. **Streamlit Integration**: Loads conversations on login and saves after each message

## Usage

```python
# Load conversation when user logs in
load_user_conversation(user_id)

# Save conversation after each message
save_user_conversation(user_id)

# Delete conversation when clearing chat
conversation_storage.delete_conversation(user_id)
```

## Lifecycle

Conversations are automatically deleted from S3 after 30 days using S3 lifecycle rules.