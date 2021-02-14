from aws_cdk import (
    core,
    aws_iam,
    aws_sagemaker
)

class SageMakerStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates the IAM role with SageMaker permissions
        sagemaker_role = aws_iam.Role(
            self,
            id='SageMaker-BERT-Endpoint-Role',
            assumed_by=aws_iam.ServicePrincipal('sagemaker.amazonaws.com')
        )
        sagemaker_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSageMakerFullAccess')
        )

        bucket_name = 'sagemaker-endpoint-artefacts'
        
        # Creates the SageMaker Model (BERT)
        sagemaker_model = aws_sagemaker.CfnModel(
            self,
            id='SageMaker-BERT-Model',
            execution_role_arn=sagemaker_role.role_arn,
            primary_container=aws_sagemaker.CfnModel.ContainerDefinitionProperty(
                image='763104351884.dkr.ecr.eu-west-1.amazonaws.com/pytorch-inference:1.4.0-cpu-py36-ubuntu16.04',
                model_data_url='s3://'+ bucket_name +'/bert-model/model.tar.gz',
                environment={
                    'SAGEMAKER_PROGRAM': 'predictor.py'
                }
            ),
            model_name='bert-model'
        )

        # Creates the SageMaker Endpoint Config
        sagemaker_endpoint_config = aws_sagemaker.CfnEndpointConfig(
            self,
            id='SageMaker-BERT-Endpoint-Config',
            production_variants=[aws_sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                initial_instance_count=1,
                initial_variant_weight=1.0,
                instance_type='ml.t2.xlarge',
                model_name=sagemaker_model.model_name,
                variant_name='bert-model'
            )],
            endpoint_config_name='bert-model-endpoint-config'
        )

        # Waits for the SageMaker Model to be created
        sagemaker_endpoint_config.add_depends_on(sagemaker_model)

        # Creates the SageMaker Endpoint
        sagemaker_model_endpoint = aws_sagemaker.CfnEndpoint(
            self,
            id='SageMaker-BERT-Endpoint',
            endpoint_config_name='bert-model-endpoint-config',
            endpoint_name='bert-model-endpoint'
        )

        # Waits for the SageMaker Endpoint Config to be created
        sagemaker_model_endpoint.add_depends_on(sagemaker_endpoint_config)