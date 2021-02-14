import os
import tarfile
import urllib.request
import boto3
from botocore.client import ClientError

def create_s3_bucket(bucket_name, aws_region):
    ''' Creates the S3 bucket for the SageMaker model artefacts '''
    s3_resource = boto3.resource('s3')
    s3_resource.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': aws_region
        }
    )
    print(bucket_name + ' created successfully')

def upload_file(bucket_name, file_name):
    ''' Uploads the model artefacts to the S3 bucket '''
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(bucket_name).upload_file(
        Filename=file_name, 
        Key=file_name
    )
    print('Local model artefacts uploaded to S3')

def create_model_artefacts(model_artefacts_path, bucket_name, file_name, aws_region):
    s3_resource = boto3.resource('s3')

    if not os.path.exists(model_artefacts_path):
        os.makedirs(model_artefacts_path)
        print('Local model artefacts directory created')

        # Model artefacts URLs referencing HuggingFace's own S3 bucket
        config = 'https://s3.amazonaws.com/models.huggingface.co/bert/bert-large-uncased-whole-word-masking-finetuned-squad-config.json'
        vocab = 'https://s3.amazonaws.com/models.huggingface.co/bert/bert-large-uncased-whole-word-masking-finetuned-squad-vocab.txt'
        model = 'https://s3.amazonaws.com/models.huggingface.co/bert/bert-large-uncased-whole-word-masking-finetuned-squad-pytorch_model.bin'

        # Downloads each model artefact
        urllib.request.urlretrieve(config, model_artefacts_path + '/config_file.json')
        urllib.request.urlretrieve(vocab, model_artefacts_path + '/vocab.txt')
        urllib.request.urlretrieve(model, model_artefacts_path + '/pytorch_model.bin')

        # Zips the model artefacts up as a tarball object
        with tarfile.open(model_artefacts_path + '/model.tar.gz', 'w:gz') as f:
            f.add(model_artefacts_path + '/config_file.json', arcname='./config_file.json')
            f.add(model_artefacts_path + '/vocab.txt', arcname='./vocab.txt')
            f.add(model_artefacts_path + '/pytorch_model.bin', arcname='./pytorch_model.bin')
            f.add('./sagemaker_predictor/requirements.txt', arcname='./code/requirements.txt')
            f.add('./sagemaker_predictor/predictor.py', arcname='./code/predictor.py')

        print('Model tarball object created')

        os.remove(model_artefacts_path + '/config_file.json')
        os.remove(model_artefacts_path + '/vocab.txt')
        os.remove(model_artefacts_path + '/pytorch_model.bin')

    else:
        print('Local model artefacts directory already exists')

    try:
        s3_resource.meta.client.head_bucket(Bucket=bucket_name)
        print(bucket_name + ' bucket already exists')
    except ClientError:
        create_s3_bucket(bucket_name, aws_region)
        upload_file(bucket_name, file_name)