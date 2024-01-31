from __future__ import absolute_import, division, print_function

__metaclass__ = type

import requests
from ansible.module_utils.basic import AnsibleModule
from ansible.errors import AnsibleModuleError
from ansible.module_utils._text import to_native
from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
    EmbeddedModuleFailure,
)

class SatelliteSession:
    def __init__(self, server_url, username, password, validate_certs):
        self._satellite_url = server_url
        self._username = username
        self._password = password
        self._ssl_verify = validate_certs
            
    def establish_session(self):
        try:
            session = requests.Session()
            session.auth = (self._username, self._password)
            session.verify = self._ssl_verify
            url = f"{self._satellite_url}/api/v2/{self._endpoint}"

            response = session.get(url)

            if response.status_code != 200:
                raise EmbeddedModuleFailure(
                    f"Failed to establish session with {url} API: {response.text}"
                )
            
        except requests.exceptions.RequestException as e:
            raise AnsibleModuleError(f"Count create Satellite session: {to_native(e)}")
        
    def disconnect_session(self):
        try:
            session = requests.Session()
            url = f"{self._satellite_url}/api/v2/{self._endpoint}"

            response = session.delete(url)

            if response.status_code != 200:
                raise EmbeddedModuleFailure(
                    f"Failed to disconnect session with {url} API: {response.text}"
                )
            
        except requests.exceptions.RequestException as e:
            raise AnsibleModuleError(f"Count disconnect Satellite session: {to_native(e)}")
        
class Parameters:
    def __init__(self, name, server_url, username, password, validate_certs):
        self._endpoint = name
        self.server_url = server_url
        self._username = username
        self._password = password
        self.validate_certs = validate_certs

    def get_parameters(self):
        try:
            session = SatelliteSession(self._satellite_url, self._username, self._password, self._ssl_verify)
            session.establish_session()
            url = f"{self._satellite_url}/api/v2/{self._endpoint}"

            response = session.get(url)

            if response.status_code != 200:
                raise EmbeddedModuleFailure(
                    f"Failed to get parameters from {url} API: {response.text}"
                )
            
            data = response.json()['results']

            ids_list = [item['id'] for item in data if 'id' in item]

            return ids_list
            
        except requests.exceptions.RequestException as e:
            raise AnsibleModuleError(f"Count get parameters: {to_native(e)}")
        
