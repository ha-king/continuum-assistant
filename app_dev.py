#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.cdk_stack import CdkStack

app = cdk.App()

# Development environment (new)
main_stack = CdkStack(app, "StreamlitAssistantStackDev", env_name="dev")

app.synth()