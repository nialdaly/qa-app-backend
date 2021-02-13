#!/usr/bin/env python3

from aws_cdk import core

from qa_app_backend.qa_app_backend_stack import QaAppBackendStack


app = core.App()
QaAppBackendStack(app, "qa-app-backend")

app.synth()
