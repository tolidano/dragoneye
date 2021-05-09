import json
import subprocess
import sys
from typing import Optional

import requests
from dragoneye.utils.app_logger import logger
from dragoneye.dragoneye_exception import DragoneyeException
from dragoneye.utils.value_validator import validate_uuid


class AzureAuthorizer:

    @staticmethod
    def get_authorization_token(tenant_id: Optional[str] = None,
                                client_id: Optional[str] = None,
                                client_secret: Optional[str] = None) -> str:
        """
        This function generates a JWT bearer token.

        If client_id and client_secret are provided, it will generate the token using these credentials.

        Otherwise, it will attempt to generate a token from your CLI credentials, using
        `az account get-access-token <https://docs.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az_account_get_access_token>`__
        """
        logger.info('Will try to generate JWT bearer token...')
        if not (client_id and client_secret and tenant_id):
            token = AzureAuthorizer._get_token_from_az_cli()
        else:
            token = AzureAuthorizer._get_token_from_credentials(tenant_id, client_id, client_secret)

        logger.info('JWT bearer token generated successfully')
        return f'Bearer {token}'

    @staticmethod
    def _get_token_from_credentials(tenant_id: str, client_id: str, client_secret: str) -> str:
        validate_uuid(tenant_id, 'Invalid tenant id')
        validate_uuid(client_id, 'Invalid client id')

        response = requests.post(
            url=f'https://login.microsoftonline.com/{tenant_id}/oauth2/token',
            data={
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret,
                'resource': 'https://management.azure.com/'
            }
        )

        if response.status_code != 200:
            raise DragoneyeException(f'Failed to authenticate. status code: {response.status_code}\n'
                                     f'Reason: {response.text}')

        response_body = json.loads(response.text)
        access_token = response_body['access_token']
        return access_token

    @staticmethod
    def _get_token_from_az_cli() -> str:
        with subprocess.Popen(['az', 'account', 'get-access-token'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as process:
            stdout, stderr = process.communicate()
            process.__enter__()
            if stderr:
                raise DragoneyeException('Failed to authenticate.\n'
                                         f'Reason: {stderr.decode(sys.stderr.encoding)}')
            output = stdout.decode(sys.stdout.encoding)
            ind = output.rindex('}') + 1
            output = output[:ind]
            return json.loads(output)['accessToken']
