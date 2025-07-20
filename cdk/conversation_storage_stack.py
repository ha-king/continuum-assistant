from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy,
    Duration,
)
from constructs import Construct

class ConversationStorageStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket for conversation data storage
        self.conversation_bucket = s3.Bucket(
            self, "ConversationBucket",
            bucket_name=f"user-conversations-data-{self.account}-{self.region}",
            removal_policy=RemovalPolicy.RETAIN,  # Retain data when stack is deleted
            lifecycle_rules=[
                s3.LifecycleRule(
                    expiration=Duration.days(30),  # Auto-delete after 30 days
                    enabled=True
                )
            ],
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )
        
        # Create DynamoDB table for conversation metadata
        self.conversation_table = dynamodb.Table(
            self, "ConversationMetadataTable",
            table_name="user-conversations",
            partition_key=dynamodb.Attribute(
                name="conversation_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,  # Retain data when stack is deleted
            time_to_live_attribute="expiry_time"
        )