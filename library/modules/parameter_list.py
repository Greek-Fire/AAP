#!/usr/bin/python
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.module_utils.fact_gather import SatelliteSession, Parameters

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
        session = SatelliteSession(
            module.params['server_url'], 
            module.params['username'], 
            module.params['password'], 
            module.params['validate_certs']
        )
        session.establish_session()

        parameters = Parameters(module.params['name'], session)
        results['parameters'] = parameters.get_parameters()
    except Exception as e:
        module.fail_json(msg=f"Error retrieving parameters: {to_native(e)}")
    finally:
        session.disconnect_session()

    module.exit_json(**results)

if __name__ == '__main__':
    main()
