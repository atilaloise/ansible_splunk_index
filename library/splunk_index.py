#!/usr/bin/env python

# Copyright: (c) 2020, Atila Aloise de Almeida <atilaloise@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: splunk_index
short_description: Manipulate splunk indexes easily
version_added: "1.0.0"
description: This module creates, configure and delete splunk indexes
options:
    host:
        description: Splunk host where de index should be created. Defaults to localhost
        required: true
        type: str
    port:
        description: Splunk administration port. Defaults to 8089
        required: true
        type: str
    username:
        description: User with create index capabilitie. Defaults to admin
        required: true
        type: str
    password:
        description: User password.
        required: true
        type: str
    version:
        description: Splunk version.
        required: true
        type: str
    scheme:
        description: Scheme for connection. Can be http or https. Defaults to https
        required: true
        type: str
    name:
        description: The name of the index to be manipulated.
        required: true
        type: str
    home_path:  
        description: Path to store the index. same as "homePath_expanded"
        required: false
        type: str
    home_max_size:
        description: Max size for hot and Warm buckets inside home path. same as "homePath.maxDataSizeMB"
        required: false
        type: int
    cold_bucket_path: 
        description: Path to store the index cold bucket. same as "coldPath_expanded"
        required: false
        type: str
    cold_bucket_max_size: 
        description: Max size cold buckets inside cold path. same as "coldPath.maxDataSizeMB"
        required: false
        type: str
    retention:  frozenTimePeriodInSecs
        description: The retention period. Could be in Seconds, minutes, days, months or years.
        required: false
        type: str
    state: 
        description: The desired state for the index. Defaults to Present
        required: true
        type: str


author:
    - Atila Aloise de Almeida (@atilaloise)
'''

EXAMPLES = r'''
- name: Creates a splunk index and set custom configurations
  splunk_index:
    name: myindex
    version: 8.1.0
    home_path:
    home_max_size:
    cold_bucket_path:
    cold_bucket_max_size:
    retention:
    state: present

- name: Delete a splunk index
  splunk_index:
    name: myindex
    version: 8.1.0
    state: absent
'''

RETURN = r'''
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
my_useful_info:
    description: The dictionary containing information about your system.
    type: dict
    returned: always
    sample: {
        'foo': 'bar',
        'answer': 42,
    }
'''


import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from splunklib.client import connect
from utils import *

def index_exists(service, name):
    return True if name in service.indexes else False

def index_create(service, name, **kwargs):
    service.indexes.create(name, **kwargs)

# def index_remove(service, name):
#     return name, kwargs


# def index_update(service, name, **kwargs):
#     return name, kwargs


from ansible.module_utils.basic import AnsibleModule

def main():
    """ Process the module """

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            host=dict(type="str", default="localhost"),
            port=dict(type="int", default="8089"),
            username=dict(type="str", default="admin"),
            password=dict(type="str", required=True, no_log=True),
            scheme=dict(type="str", choices=["http", "https"], default="https"),
            version=dict(type="str", required=True),
            home_path=dict(type="str"),
            home_max_size=dict(type="str"),
            cold_bucket_path=dict(type="str"),
            cold_bucket_max_size=dict(type="str"),
            retention=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=([("state", "present", ["name", "password"])]),
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        changed_state={}
    )

    if module.check_mode:
        module.exit_json(**result)
    
    requested_state = module.params["state"]
    
    name = module.params["name"]

    splunk_connection={}
    
    splunk_connection["host"] = module.params["host"]
    splunk_connection["port"] = module.params["port"]
    splunk_connection["username"] = module.params["username"]
    splunk_connection["password"] = module.params["password"]
    splunk_connection["version"] = module.params["version"]
    splunk_connection["scheme"] = module.params["scheme"]

    index_config = {}
    index_new_config = {}

    if module.params["home_path"] is not None:
        index_config['home_path'] = module.params["home_path"]

    if module.params["home_max_size"] is not None:
        index_config['home_max_size']  = module.params["home_max_size"]
        
    if module.params["cold_bucket_path"] is not None:
        index_config['cold_bucket_path'] = module.params["cold_bucket_path"]

    if module.params["cold_bucket_max_size"] is not None:
        index_config['cold_bucket_max_size'] = module.params["cold_bucket_max_size"]

    if module.params["retention"] is not None:
        index_config['retention'] = module.params["retention"]

    
    service = connect(**splunk_connection)


    
    if requested_state == 'present':
        if not index_exists(service, name):
            created_index = index_create(service, name, **index_config)
            result['changed']=True
        elif index_config:
            existent_index = index_exists(service, name)
            for key in index_config:
                if index_config[key] != existent_index[key]:
                    index_new_config[key] = index_config[key]
                    
            if index_new_config:
                index_update(service, name, **index_new_config)
                result['changed']=True
            
    else:
        if index_exists(name):
            removed_index = index_remove(service, name)
            result['changed']=True
        else:
            result['changed']=False

    
















    module.exit_json(**result)


if __name__ == "__main__":
    main()
