#!/usr/bin/env python3
from aws_cdk import core
from sagemaker_stack.sagemaker_stack import SageMakerStack
from lambda_stack.lambda_stack import LambdaStack
from s3_stack.s3_stack import S3Stack

app = core.App()

env = {'region': 'eu-west-1'}

sagemaker_stack = SageMakerStack(app, 'sagemaker-bert-endpoint-stack', env=env)
lambda_stack = LambdaStack(app, 'lambda-bert-trigger-stack', env=env)

lambda_stack.add_dependency(sagemaker_stack)

s3_stack = S3Stack(app, 's3-client-bucket-stack', env=env)

app.synth()