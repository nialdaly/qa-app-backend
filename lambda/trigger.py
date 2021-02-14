import boto3
from botocore.exceptions import ClientError
import json

sagemaker_runtime = boto3.client('sagemaker-runtime')
sagemaker_endpoint = 'bert-model-endpoint'

def exception_handler(e):
    return {
        'statusCode': 503,
        'body': str(e)
    }

def lambda_handler(event, context):
    try:
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=sagemaker_endpoint,
            Body=json.dumps(event),
            ContentType='application/json'
        )

        response_body = response['Body'].read().decode("utf-8")
        cleaned_response = response_body.replace('"', '')

        return {
            'statusCode': 200,
            'body': cleaned_response
        }

    except ClientError as e:
        if e.response['Error']['Code'] == 'ValidationError':
            return exception_handler("SageMaker model (BERT) endpoint unavailable")
        else:
            return exception_handler("SageMaker model (BERT) endpoint unavailable")