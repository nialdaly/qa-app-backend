#!/usr/bin/env python3
from aws_cdk import core
from sagemaker.sagemaker_stack import SageMakerStack

app = core.App()
SageMakerStack(app, "sagemaker-bert-endpoint-stack")
app.synth()