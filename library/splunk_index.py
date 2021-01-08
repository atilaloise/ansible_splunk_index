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
description: This module manages splunk indexes
options:
    host:
        description: Splunk host where de index should be created.Defaults to localhost
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
    app:
        description: The app where this index should be created. ATTENTION! The app shoud already exists! Defaults to "search" app.
        required: true
        type: str
    disabled:
        description: disable index. defaults to False
        required: false
        type: bool
    clean:
        description: DANGER ZONE! it will Clean all index data. defaults to False
        required: false
        type: bool
    homePath:  
        description: Path to store the index. same as "homePath_expanded". ONly used at creation time! You cant update this
        required: false
        type: str
    homePath_maxDataSizeMB:
        description: Max size of homePath hot and Warm buckets inside home path. See "homePath.maxDataSizeMB" indexes.conf documentation.
        required: false
        type: int
    coldPath: 
        description: Path to store the index cold bucket. same as "coldPath_expanded". ONly used at creation time!You cant update this
        required: false
        type: str
    coldPath_maxDataSizeMB: 
        description: Max size cold buckets inside cold path. same as "coldPath.maxDataSizeMB"
        required: false
        type: str
    maxTotalDataSizeMB: 
        description: The maximum size of an index, in megabytes
        required: false
        type: str
    retention:  
        description: The retention period. Same as frozenTimePeriodInSecs.
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
    name: raw_search
    app: search
    maxTotalDataSizeMB: 800mb
    home_path: /splunk/hotbkts/raw_search/
    homePath_maxDataSizeMB: 500mb
    coldPath: /splunk/coldbkts/raw_search/
    coldPath_maxDataSizeMB: 600
    retention: 3600
    state: present
    host: localhost
    port: 8090
    username: admin
    password: Sup3rpasswrd
    scheme: https
    version: 8.1.0
    

- name: Creates a splunk index and set custom configurations
  splunk_index:
    name: raw_search
    state: absent
    host: localhost
    port: 8090
    username: admin
    password: Sup3rpasswrd
    scheme: https
    version: 8.1.0
'''

RETURN = '''
original_state:
    description: The original state of the param that was passed in
    type: str
changed_state:
    description: The output state that the module generates
    type: str
'''


import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from splunklib.client import connect
#from utils import *

def index_exists(service, name):
    return True if name in service.indexes else False

def index_create(service, name, **kwargs):
    service.indexes.create(name, **kwargs)

def index_update(service, name, **kwargs):
    index = service.indexes[name]
    index.update(**kwargs)

def index_enable(service, name):
    index = service.indexes[name]
    index.enable()

def index_disable(service, name):
    index = service.indexes[name]
    index.disable()

def index_clean(service, name):
    index = service.indexes[name]
    index.clean()

def index_delete(service, name):
    index = service.indexes[name]
    index.delete()

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
            disabled=dict(type="bool", default=False),
            app=dict(type="str", default="search"),
            push_bundle=dict(type="bool", default=False),
            clean=dict(type="bool", default=False),
            homePath=dict(type="str"),
            homePath_maxDataSizeMB=dict(type="str"),
            coldPath=dict(type="str"),
            coldPath_maxDataSizeMB=dict(type="str"),
            maxTotalDataSizeMB=dict(type="str"),
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
    disable_index = module.params["disabled"]
    clean_index = module.params["clean"]
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
    
    
    index_config['app'] = module.params["app"]
    
    if module.params["homePath"] is not None:
        index_config['homePath'] = module.params["homePath"]

    if module.params["homePath_maxDataSizeMB"] is not None:
        index_config['homePath.maxDataSizeMB']  = module.params["homePath_maxDataSizeMB"]
        
    if module.params["coldPath"] is not None:
        index_config['coldPath'] = module.params["coldPath"]

    if module.params["coldPath_maxDataSizeMB"] is not None:
        index_config['coldPath.maxDataSizeMB'] = module.params["coldPath_maxDataSizeMB"]

    if module.params["retention"] is not None:
        index_config['frozenTimePeriodInSecs'] = module.params["retention"]

    if module.params["maxTotalDataSizeMB"] is not None:
        index_config['maxTotalDataSizeMB'] = module.params["maxTotalDataSizeMB"]

    
    service = connect(**splunk_connection)


    
    if requested_state == 'present':
        if not index_exists(service, name):
            index_create(service, name, **index_config)
            if module.params["disabled"]:
                index_disable(service, name)
            result['changed']=True
        elif index_config:
            # remove unsuported values in update actions
            index_config.pop('homePath', None)
            index_config.pop('coldPath', None)
            index_config.pop('app', None)

            for key in index_config:
                if index_config[key] != service.indexes[name].content[key]:
                    index_new_config[key] = index_config[key]

            if index_new_config:
                index_update(service, name, **index_new_config)
                result['changed']=True

        if disable_index and (disable_index != bool(int(service.indexes[name].content["disabled"]))):
            index_disable(service, name)
            result['changed']=True
        elif (not disable_index) and (disable_index != bool(int(service.indexes[name].content["disabled"]))):
            index_enable(service, name)
            result['changed']=True
        
        if clean_index:
            index_clean(service, name)
            result['changed']=True

    else:
        if index_exists(service, name):
            index_delete(service, name)
            result['changed']=True
        else:
            result['changed']=False



    module.exit_json(**result)


if __name__ == "__main__":
    main()
