# Lesson 2: Add a test to an existing role

* [home](./README.md)
* [back](./LESSON1.md)
* [next](./LESSON3.md)

* add linting to the default test
* add a testinfra test to check if docker compose gets installed
* initialize a new scenario and write a test to check if docker compose doesn't get insalled when the flag is set to false

## Initialize

Copy the folder `lesson2_geerlingguy.docker` into a new one and `cd` into it.

## edit the existing scenario

Place the .yamllint you created in lesson 1 in the default directory.

edit the `molecule/default/molecule.yml`

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

It adds lintng and testinfra test.

Now create a `tests` directory in `molecule/default` and add a file `test_default.py` with content

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

## Run the test 1

```bash
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "pip3 install testinfra; molecule test --all"
```

## Initialize a new scenario

```bash
docker run \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "molecule init scenario --verifier-name testinfra install_docker_without_docker_compose"
```

Now edit the `molecule/install_docker_without_docker_compose/molecule.yml` like this.

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
verifier:
  name: testinfra
```

## Write the test

To deactivate the docker compose installation you have to edit the playbook `molecule/install_docker_without_docker_compose/converge.yml`

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
```

Then add a python test `molecule/install_docker_without_dokcer_compose/tests/tests_default.py`

```python
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_docker_compose_working(host):
    cmd = host.run('docker-compose --version')

    assert cmd.rc != 0
```

## One adjustment to the generated code

The `molecule/install_docker_without_dokcer_compose/tests/configtest.py` line 19 is to long.
Just edit this file to look like this.

```python
"""PyTest Fixtures."""
from __future__ import absolute_import
import os
import pytest


def pytest_runtest_setup(item):
    """Run tests only when under molecule with testinfra installed."""
    try:
        import testinfra
    except ImportError:
        pytest.skip("Test requires testinfra", allow_module_level=True)
    if "MOLECULE_INVENTORY_FILE" in os.environ:
        pytest.testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
            os.environ["MOLECULE_INVENTORY_FILE"]
        ).get_hosts("all")
    else:
        pytest.skip(
            "Test should run only from inside molecule.",
            allow_module_level=True
        )
```

In real world scenarios, you can discuss these linting rules. Just make sure to not waste time with meaningless disussions.

## Run the test 2

```bash
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "pip3 install testinfra; molecule test --all"
```
