#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.cdk_stack import CdkStack
from cdk.conversation_storage_stack import ConversationStorageStack
from cdk.user_profiles_stack import UserProfilesStack
from cdk.response_cache_stack import ResponseCacheStack

app = cdk.App()
# Production environment (existing)
main_stack = CdkStack(app, "StreamlitAssistantStack", env_name="prod")

# Add storage stacks
conversation_stack = ConversationStorageStack(app, "ConversationStorageStack")
user_profiles_stack = UserProfilesStack(app, "UserProfilesStack")
response_cache_stack = ResponseCacheStack(app, "ResponseCacheStack")

app.synth()