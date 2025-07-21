#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.cdk_stack import CdkStack
from docker_app.config_file import Config

app = cdk.App()

# Get AWS account and region from environment or use default values
account = app.node.try_get_context("account") or None  # Will use default account from AWS CLI config
region = app.node.try_get_context("region") or Config.DEPLOYMENT_REGION

# Production environment (existing)
main_stack = CdkStack(app, "StreamlitAssistantStack", 
                     env_name="prod",
                     env=cdk.Environment(
                         account=account,
                         region=region
                     ))

app.synth()