from aws_cdk import (
    core,
    aws_iam,
    aws_s3
)

class S3Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        s3_bucket = aws_s3.Bucket(
            self,
            id='qa-app-client',
            bucket_name='qa-app-client',
            public_read_access=True,
            website_error_document='index.html',
            website_index_document='index.html'
        )