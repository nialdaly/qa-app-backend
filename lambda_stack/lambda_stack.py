from aws_cdk import (
    core,
    aws_iam,
    aws_lambda as _lambda
)

class LambdaStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates the IAM role with Lambda permissions
        lambda_role = aws_iam.Role(
            self,
            id='Lambda-BERT-Endpoint-Role',
            assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com')
        )
        lambda_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSageMakerFullAccess')
        )
        
        lambda_function = _lambda.Function(
            self,
            id='Lambda-BERT-Trigger',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='trigger.lambda_handler',
            function_name='Lambda-BERT-Trigger',
            role=lambda_role
        )