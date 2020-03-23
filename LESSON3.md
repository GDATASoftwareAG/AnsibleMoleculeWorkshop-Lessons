# Lesson 3: Add functionality to a role

* [home](./README.md)
* [back](./LESSON2.md)
* [next](./LESSON4.md)

## start

Go on with your result from lesson to or copy the `lesson2_geelingguy.docker.add_tests` directory.

## Initialize a new scenario

```bash
docker run \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "molecule init scenario --verifier-name testinfra install_docker_with_platform_container"
```

Copy some files from the previous scenario.

```bash
cp molecule/install_docker_without_docker_compose/molecule.yml molecule/install_docker_with_platform_container/molecule.yml
cp molecule/install_docker_without_docker_compose/tests/conftest.py molecule/install_docker_with_platform_container/tests/conftest.py
cp molecule/install_docker_without_docker_compose/converge.yml molecule/install_docker_with_platform_container/converge.yml
```

## Edit

Create a custom fact and place it here `files/docker_containers.fact`

```bash
#!/bin/bash

echo "[ $(docker ps --all --format "{{json .Names}},") ]" | sed "s#, ]# ]#g"
```

We want our new function to have a flag to turn it on.

Add this line to `defaults/main.yml`

```yaml
# run a docker platform?
docker_platform: false
```

Create a file `deploy-platform-container.yml` to the `tasks` directory

```yaml
---
- name: "Create custom fact directory"
  file:
   path: "/etc/ansible/facts.d"
   state: "directory"

- name: "Insert custom fact file for docker container"
  copy:
   src: files/docker_containers.fact
   dest: /etc/ansible/facts.d/docker_containers.fact
   mode: 0755

- name: reload ansible_local
  setup:
   filter: ansible_local

- name: "Install python3 pip"
  apt:
   name: python3-pip
   state: present

- name: "Install docker"
  pip:
   name:
    - docker
    - requests>=2.20.1
   executable: /usr/bin/pip3
   state: present

- name: "Run platform container (custom)"
  command: docker run --rm -d -p 8080:8000 --name ptl-whoami jwilder/whoami:latest
  when: '"ptl-whoami" not in ansible_local.docker_containers'
```

Notice that you access the fact by the filename we uploaded.

Include that tasks by editing the `tasks/main.yml`

```yaml
- include_tasks: deploy-platform-container.yml
  when: docker_platform | bool
```

## tests

Now you want to edit the playbook in your new scenario `molecule/install_docker_with_platform_container/converge.yml`

```yaml
---
- name: Converge
  hosts: all
  pre_tasks:
    - name: Update apt cache.
      apt: update_cache=yes cache_valid_time=600
      when: ansible_os_family == 'Debian'
  tasks:
    - name: "Include geerlingguy.docker"
      include_role:
        name: "geerlingguy.docker"
      vars:
        docker_install_compose: false
        docker_platform: true
```

And write a python test `tests/test_default.py`

```python
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_platform_running(host):
    cmd = host.run('docker info')
    assert cmd.stdout.find("Running: 1") != -1

    platform = host.addr('localhost')
    assert platform.port(8080).is_reachable
```

## Run the test

```bash
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "pip3 install testinfra; molecule test --all"
```
