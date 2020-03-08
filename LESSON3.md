# Lesson 3: Add functionality to a role

* [home](./README.md)
* [back](./LESSON2.md)
* [next](./LESSON4.md)

## start

go on with your result from lesson to or copy the `lesson2_geelingguy.docker.add_tests` directory

## Initialize

```bash
docker run \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "molecule init scenario --verifier-name testinfra install_docker_with_platform_container"
```

## edit

create a custom fact and place it here `files/docker_containers.fact`

```bash
#!/bin/bash

echo "[ $(docker ps --all --format "{{json .Names}},") ]" | sed "s#, ]# ]#g"
```

we want our new function to have a flag to turn it on

add this line to `defaults/main.yml`
```yaml
# run a docker platform?
docker_platform: false
```

create a file `deploy-platform-container.yml` to the `tasks` directory

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

include that tasks by editing the `tasks/main.yml`
```yaml
- include_tasks: deploy-platform-container.yml
  when: docker_platform | bool
```

## tests

you now want to edit the playbook in your new scenario `install_docker_with_platform_container`

```yaml
---
- name: Converge
  hosts: all
  roles:
    - role: geerlingguy.docker
      vars:
        docker_install_compose: false
```

and write a python test `tests/test_default.py`

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