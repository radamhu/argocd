#!/bin/bash

echo ' Logging ... \n'
bw get totp VodafoneGroup_rolandcsaba.adam && saml2aws login --force --region=eu-central-1 --profile=saml && sed 's+command: aws+command: /usr/local/bin/aws+g' ~/.kube/config
# echo '(.venv) ➜  saml2aws script'
# saml2aws script 
echo ' Echo saml2aws env ... \n'
saml2aws exec env | grep '^AWS_SESSION_TOKEN\|ACCESS_KEY\|SECRET_ACCESS_KEY' | sort | sed -e 's/^/export /'
# export AWS_ACCESS_KEY_ID=
# export AWS_SECRET_ACCESS_KEY=
# export AWS_SESSION_TOKEN=
echo ' Running sam build ... \n'
# sam build --debug --profile saml
sam build 

# def lambda_handler(event, context):
#    session = boto3.Session(profile_name='saml')
#
# (.venv) ➜ sam local invoke GrafanaIncidentHandler -e events/event.json
# {"errorMessage": "The config profile (saml) could not be found"
# File (.env) is in ignored set, skipping it
# no such file samconfig.toml
# No environment variables found for function 'GrafanaIncidentHandler'
# Loading AWS credentials from session with profile 'None'


# def lambda_handler(event, context):
#    session = boto3.Session(profile_name='saml')
# (.venv) ➜ sam local invoke GrafanaIncidentHandler -e events/event.json --profile saml
# 05 Jan 2024 12:04:34,297 [ERROR] (rapid) Init failed error=errResetReceived InvokeID=

# sam build --profile saml
# sam local

# boto3 OK
# session = boto3.Session()
# sts = session.resource('sts')
# AWS_ACCOUNT_ID = sts.get_caller_identity()["Account"]
# sam local invoke GrafanaIncidentHandler -e events/event.json --profile saml

# boto3 OK
# sts = boto3.client("sts")
# account_id = sts.get_caller_identity()["Account"]

# csabaroland.adam
# The available resources are:
#    - cloudformation
#    - cloudwatch
#    - dynamodb
#    - ec2
#    - glacier
#    - iam
#    - opsworks
#    - s3
#    - sns
#    - sq

# https://github.com/awsdocs/aws-lambda-developer-guide/blob/main/sample-apps/blank-python/4-invoke.sh

# You need to set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
# Your home directory (~) is not copied to Docker container, so AWS_PROFILE will not work.
echo ' Running sam local invoke \n'
sam local invoke GrafanaSmsNotifier -e events/event.json --profile saml --env-vars env.json
# sam deploy --guided --profile saml