# Lesson 4: dependend roles

* [home](./README.md)
* [back](./LESSON3.md)
* [next](./LESSON5.md)


## Initialize

start with a new role

```bash
docker run \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "molecule init role --verifier-name testinfra some_role"
```

## edit

create a custom fact and place it here `files/docker_containers.fact`

```bash
#!/bin/bash

echo "[ $(docker ps --all --format "{{json .Names}},") ]" | sed "s#, ]# ]#g"
```

configure dependency `meta/main.yml`

```yaml
dependencies:
  - name: geerlingguy.docker
```

let molecule auto download the dependency by adding it to `molecule/default/requirements.yml`

```yaml
---
- name: geerlingguy.docker
```

add your tasks from lesson 3 directly into the `tasks/main.yml`

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

write a python test `molecule/default/tests/tests_default.py`

```python
def test_platform_running(host):
    cmd = host.run('docker info')
    assert cmd.stdout.find("Running: 1") != -1

    platform = host.addr('localhost')
    assert platform.port(8080).is_reachable
```

dont forget to edit the playbook or otherwise the docker role will not work `molecule/default/converge.yml`

```yaml
---
- name: Converge
  hosts: all

  pre_tasks:
    - name: Update apt cache.
      apt: update_cache=yes cache_valid_time=600
    - name: Ensure packages
      apt:
        name:
          - apt-utils
        state: present
        force: true

  tasks:
    - name: "Include some_role"
      include_role:
        name: "some_role"
```

## Run the test

```bash
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "pip3 install testinfra; molecule test --all"
```