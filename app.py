#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.cdk_stack import CdkStack

app = cdk.App()
# Production environment (existing)
main_stack = CdkStack(app, "StreamlitAssistantStack", env_name="prod")

app.synth()