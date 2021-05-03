![Dragoneye](dragoneye_header.png)

![CD](https://github.com/indeni/dragoneye/actions/workflows/cd.yaml/badge.svg) 
![PyPI](https://img.shields.io/badge/python-3.7+-blue.svg)
![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

# dragoneye
dragoneye is a Python tool that is used to collect data about a cloud environment using the cloud provider's APIs. It is intended to function as component in other tools who have the need to collect data quickly (multi-threaded), or as a command line to collect a snapshot of a cloud account.

dragoneye currently supports AWS (AssumeRole and AccessKey based collection) and Azure (with client secret).

# Setup
Clone this git repository, navigate to the root directory where `setup.py` is located and run:
```
pip install .
```
(note the period at the end of the command)

We recommend doing this within a virtual environment, like so:
```
python3.9 -m venv ./venv
. ./venv/bin/activate
pip install .
```

# Usage

## Programmatic Usage
Create an instance of one of the CollectRequest classes, such as AwsAccessKeyCollectRequest, AwsAssumeRoleCollectRequest, AzureCollectRequest and call the `collect` function. For example:

```python
from dragoneye import AwsScanner, AwsCloudScanSettings, AzureScanner, AzureCloudScanSettings, AwsSessionFactory, AzureAuthorizer

### AWS ###
aws_settings = AwsCloudScanSettings(
    commands_path='/Users/dev/python/dragoneye/aws_commands_example.yaml',
    account_name='default', default_region='us-east-1', regions_filter=['us-east-1']
)

# Using environment variables
session = AwsSessionFactory.get_session(profile_name=None, region='us-east-1')  # Raises exception if authentication is unsuccessful
aws_scan_output_directory = AwsScanner(session, aws_settings).scan()

# Using an AWS Profile
session = AwsSessionFactory.get_session(profile_name='MyProfile', region='us-east-1')  # Raises exception if authentication is unsuccessful
aws_scan_output_directory = AwsScanner(session, aws_settings).scan()

# Assume Role
session = AwsSessionFactory.get_session_using_assume_role(external_id='...',
                                                          role_arn="...",
                                                          region='us-east-1')
aws_scan_output_directory = AwsScanner(session, aws_settings).scan()

### Azure ###

azure_settings = AzureCloudScanSettings(
    commands_path='/Users/dev/python/dragoneye/azure_commands_example.yaml',
    subscription_id='...',
    account_name='my-account'
)

token = AzureAuthorizer.get_authorization_token(
    tenant_id='...',
    client_id='...',
    client_secret='...'
)  # Raises exception if authentication is unsuccessful
azure_scan_output_directory = AzureScanner(token, azure_settings).scan()

```

## CLI usage

### For collecting data from AWS
```
dragoneye aws
```

### For collecting data from Azure with a client secret
```
dragoneye azure
```