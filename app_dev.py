#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.cdk_stack import CdkStack
from cdk.conversation_storage_stack import ConversationStorageStack
from cdk.user_profiles_stack import UserProfilesStack
from cdk.response_cache_stack import ResponseCacheStack

app = cdk.App()

# Development environment (new)
main_stack = CdkStack(app, "StreamlitAssistantStackDev", env_name="dev")

# Add storage stacks with dev suffix
conversation_stack = ConversationStorageStack(app, "ConversationStorageStackDev")
user_profiles_stack = UserProfilesStack(app, "UserProfilesStackDev")
response_cache_stack = ResponseCacheStack(app, "ResponseCacheStackDev")

app.synth()