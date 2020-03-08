# Lesson 2: Add a test to an existing role

[home](./README.md)
[back](./LESSON1.md)
[next](./LESSON3.md)

* add linting to the default test
* add a testinfra test to check if docker compose gets installed
* initialize a new scenario and write a test to check if docker compose doesn't get insalled when the flag is set to false

## Initialize

Copy the folder `lesson2_geerlingguy.docker`


## edit the existing scenario

place the .yamllint you created in lesson 1 in the default directory

edit the molecule/default/molecule.yml
```yaml
---
dependency:
  name: galaxy
driver:
  name: docker
lint: |
  set -e
  yamllint .
  ansible-lint .
  flake8
platforms:
  - name: instance
    image: "geerlingguy/docker-ubuntu1804-ansible:latest"
    command: ${MOLECULE_DOCKER_COMMAND:-""}
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    privileged: true
    pre_build_image: true
provisioner:
  name: ansible
scenario:
  name: default
verifier:
  name: testinfra
```

its adds lintng and testinfra test.

now create a tests directory in `molecule/default` and add a file `test_default.py` with content

```python
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_docker_compose_working(host):
    cmd = host.run('docker-compose --version')

    assert cmd.rc == 0


def test_for_docker_engine(host):
    cmd = host.run('docker info')

    assert cmd.rc == 0
    assert cmd.stdout.find("Running: 0") != -1
```

## Initialize a new scenario

```
docker run  -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "molecule init scenario --verifier-name testinfra install_docker_without_docker_compose"
```

## write the test

to deactivate the docker compose installation you have to edit the playbook `install_docker_without_docker_compose/converge.yml`

```yaml
---
- name: Converge
  hosts: all
  roles:
    - role: geerlingguy.docker
      vars:
        docker_install_compose: false

```

and then add a python test `install_docker_without_dokcer_compose/tests/tests_default.py`

`install_docker_without_docker_compose/tests/test_default.py`
```python
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_docker_compose_working(host):
    cmd = host.run('docker-compose --version')

    assert cmd.rc != 0
```

## Run the test

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "pip3 install testinfra; molecule test --all"

```