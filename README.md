# splunk_index
Ansible module to manage splunk indexes

##  Folder structure

    .
    ├── docker-env           # A docker based Splunk environment For testing.
    │   ├── cluster          # A cluster deployment of Splunk Platform.
    │   ├── standalone       # A Standalone deployment of Splunk Platform.
    ├── library              # Folder where this module resides.
    │   ├── splunk_index.py  #  !!!THE MODULE!!! 
    ├── tests                # Some Json test files to pass to this module during development.
    │   ├── args_delete_index.json      # Test index deletion.
    │   ├── args_index_custom_app.json  # Creates Index in a specific app.
    │   ├── args_index_max_size.json    # Creates or change index with custom max_size.
    │   ├── args_index_retention.json   # Creates or change index with custom retention.
    │   ├── args_index_simple.json      # Create a simple index.
    │   ├── args_setup_index.json       # Creates a full customized index.
    ├── README.md            # As it says..
    ├── requirements.txt     # case you want to use "pip install -r requirements.txt"



# Dependencies
THis module is build on top of Splunk SDK.

To install Splunk sdk use "`pip install splunk-sdk`"

# Testing 
You can test this module calling it with python and passing a json argument file like these in `test` folder.

```bash
python ./library/splunk_index.py ./test/args_index_simple.json
```

# Installing
## System Wide
You can add a local module in any of below locations as Ansible automatically loads all executable files found in those directories as modules.

> ~/.ansible/plugins/modules/
> 
> /usr/share/ansible/plugins/modules/

You can search and confirm the same by checking Ansible version, you can see the paths in ansible python module location line.

```shell
$ ansible --version

ansible 2.10.4
  config file = None
  configured module search path = ['/Users/atila/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.9/site-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.9.1 (default, Dec 29 2020, 09:45:39) [Clang 12.0.0 (clang-1200.0.32.28)]
```

## In Playbook project
By default ansible searches for modules inside any `library` folder within your Ansible Playbook project folder.
This repository follow this structure.

## In an Ansible role project
Just as in a playbook project. By default ansible searches for modules inside any `library` folder within your Ansible role project folder.


# Use

```yaml
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

```
