from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    CfnOutput
)


class PythonCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="hello.handler",
            code=_lambda.Code.from_asset("lambda"),
            function_name="HelloHandler"
        )

        fn_url = my_lambda.add_function_url(
           auth_type=_lambda.FunctionUrlAuthType.NONE,
        )

        CfnOutput(self, "TheUrl",
            value=fn_url.url
        )