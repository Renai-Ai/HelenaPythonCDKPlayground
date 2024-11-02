#!/usr/bin/env python3

import aws_cdk as cdk

from python_cdk.python_cdk_stack import PythonCdkStack


app = cdk.App()
PythonCdkStack(app, "PythonCdkStack")

app.synth()
