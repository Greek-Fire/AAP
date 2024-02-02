from __future__ import absolute_import, division, print_function

__metaclass__ = type

import requests
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
    EmbeddedModuleFailure,
)

class SatelliteSession:
    def __init__(self, server_url, username, password, validate_certs):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.validate_certs = validate_certs
        self.session = requests.Session()

    def establish_session(self):
        try:
            self.session.auth = (self.username, self.password)
            self.session.verify = self.validate_certs
            # Test connection with a basic request
            test_url = f"{self.server_url}/api/v2/status"
            response = self.session.get(test_url)
            if response.status_code != 200:
                raise EmbeddedModuleFailure(f"Failed to establish session with {test_url} API: {response.text}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Could not create Satellite session: {to_native(e)}")

    def disconnect_session(self):
        self.session.close()

class Parameters:
    def __init__(self, name, satellite_session):
        self.endpoint = name
        self.session = satellite_session

    def get_parameters(self):
        aggregated_parameters = {}  # This will store all parameters in a single dictionary

        try:
            url = f"{self.session.server_url}/api/v2/{self.endpoint}"
            response = self.session.session.get(url)
            if response.status_code != 200:
                raise EmbeddedModuleFailure(f"Failed to get parameters from {url} API: {response.text}")

            data = response.json().get('results', [])

            for item in data:
                item_url = f"{url}/{item['id']}"
                results = self.session.session.get(item_url).json()
                aggregated_parameters[results['name']] = [{'name': d['name'], 'value': d['value']} for d in results['parameters']]

            return aggregated_parameters

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Could not get parameters: {to_native(e)}")
        finally:
            self.session.disconnect_session()

