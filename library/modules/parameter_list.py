#!/usr/bin/python
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import requests
from ansible.module_utils.basic import AnsibleModule
from ansible.errors import AnsibleModuleError
from ansible.module_utils._text import to_native

DOCUMENTATION = '''
---
module: parameter_list
short_description: Get a list of parameters from Satellite
description:
    - "This module retrieves a list of parameters from Satellite."
author:
    - Louis Tiches
options:
    name:
        description:
        - The name of the endpoint to retrieve parameters from.
        required: true
        type: str
'''

EXAMPLES = '''
- name: Retrieve information about a specific datastore cluster
  parameter_list:
    name: locations
    username: admin
    password: password123
    server_url: vcenter.example.com
    validate_certs: false
'''

class SatelliteParameters:
    def __init__(self, name, server_url, username, password, validate_certs):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.validate_certs = validate_certs
        self.endpoint = name

    def _make_request(self, url):
        """Helper method to make a request and handle exceptions."""
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to get data from {url} API: {response.text}")
            return response.json()
        except requests.exceptions.RequestException as e:
            raise AnsibleModuleError(f"HTTP request failed: {to_native(e)}")

    def get_parameters(self):
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.verify = self.validate_certs

        url = f"{self.server_url}/api/v2/{self.endpoint}"
        data = self._make_request(url).get('results', [])

        parameters = []
        for item in data:
            item_url = f"{url}/{item['id']}"
            results = self._make_request(item_url)
            _dict = {
                results['name']: [{'name': d['name'], 'value': d['value']} for d in results['parameters']]
            }
            parameters.append(_dict)

        self.session.close()
        return parameters

def main():
    module_args = {
        'name': {'type': 'str', 'required': True},
        'server_url': {'type': 'str', 'required': True},
        'username': {'type': 'str', 'required': True},
        'password': {'type': 'str', 'required': True, 'no_log': True},
        'validate_certs': {'type': 'bool', 'default': True},
    }

    results = {'changed': False, 'parameters': None, 'error': ''}

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(**results)

    try:
        satellite = SatelliteParameters(
            module.params['name'], 
            module.params['server_url'], 
            module.params['username'], 
            module.params['password'], 
            module.params['validate_certs']
        )
        results['parameters'] = satellite.get_parameters()
    except Exception as e:
        module.fail_json(msg=f"Error retrieving parameters: {to_native(e)}")

    module.exit_json(**results)

if __name__ == '__main__':
    main()