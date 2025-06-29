#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.pipeline_stack import PipelineStack

app = cdk.App()
PipelineStack(app, "StreamlitPipelineStack")
app.synth()