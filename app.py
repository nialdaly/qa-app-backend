#!/usr/bin/env python3
from aws_cdk import core
from sagemaker.sagemaker_stack import SageMakerStack
from lambda_stack.lambda_stack import LambdaStack

app = core.App()

sagemaker_stack = SageMakerStack(app, 'sagemaker-bert-endpoint-stack', env={'region': 'eu-west-1'})
lambda_stack = LambdaStack(app, 'lambda-bert-trigger-stack', env={'region': 'eu-west-1'})

# Lambda stack should be created after the SageMaker stack
lambda_stack.add_dependency(sagemaker_stack)
app.synth()