# Lesson 5: advanced inventory

* [home](./README.md)
* [back](./LESSON4.md)

## Initialize

Start with a new role

```bash
docker run \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "molecule init role --verifier-name testinfra docker.swarm"
```

Copy some files from the previous roles.

```bash
cp ../some_role/meta/main.yml meta/main.yml
cp ../some_role/molecule/default/requirements.yml meta/main.yml
```

## add tasks

`tasks/main.yml`

```yaml
---
- include_tasks: manager.yml
  when: "'manager' in group_names"
- include_tasks: worker.yml
  when: "'worker' in group_names"
```

`tasks/manager.yml`

```yaml
---
- name: register docker info
  shell: docker info
  register: docker_info
  changed_when: false
- name: initialize the swarm
  shell: docker swarm init --advertise-addr {{ansible_default_ipv4.address}}
  when:
  - "docker_info.stdout.find('Swarm: inactive') != -1"
  - "not hostvars['DOCKER_SWARM_TOKEN_HOLDER']"
- name: "get docker swarm worker token"
  shell: docker swarm join-token -q worker
  register: worker_token
  changed_when: false
- name: "get docker swarm worker token"
  shell: docker swarm join-token -q manager
  register: manager_token
  changed_when: false
- name: add token-holder
  add_host:
    name: DOCKER_SWARM_TOKEN_HOLDER
    groups: ANSIBLE_DUMMY_HOSTS
    worker_token: "{{worker_token.stdout}}"
    manager_token: "{{manager_token.stdout}}"
    ip: "{{ansible_default_ipv4.address}}"
  when:
  - "not hostvars['DOCKER_SWARM_TOKEN_HOLDER']"
  changed_when: false
```

`tasks/worker.yml`

```yaml
---
- name: register docker info
  shell: docker info
  register: docker_info
  changed_when: false
- name: "join as a worker"
  shell: "docker swarm join --token {{hostvars['DOCKER_SWARM_TOKEN_HOLDER']['worker_token']}} {{hostvars['DOCKER_SWARM_TOKEN_HOLDER']['ip']}}:2377"
  when: "docker_info.stdout.find('Swarm: inactive') != -1"
  retries: 3
  delay: 20
```

## The tests

To get the tests running you need to have a more advanced inventory `molecule/default/molecule.yml`

```yaml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: node1
    image: "geerlingguy/docker-ubuntu1804-ansible:latest"
    command: /sbin/init
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    privileged: true
    pre_build_image: true
    groups:
      - manager
  - name: node2
    image: "geerlingguy/docker-ubuntu1804-ansible:latest"
    command: /sbin/init
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    privileged: true
    pre_build_image: true
    groups:
      - worker
provisioner:
  name: ansible
  config_options:
    defaults:
      interpreter_python: /usr/bin/python3
verifier:
  name: testinfra
```

Now get rolling by adding a test `molecule/default/tests/tests_default.py`

```python
def test_platform_running(host):
    cmd = host.run('docker info')
    assert cmd.stdout.find("Swarm: active") > 0

    ansible_vars = host.ansible.get_variables()
    if 'manager' in ansible_vars['group_names']:
        cmd = host.run('docker node ls')
        cmd.rc == 0
```

As we are still using the docker role form geerlingguy don't forget to edit the `molecule/default/converge.yml`.

```yaml
---
- name: Converge
  hosts: all
  pre_tasks:
    - name: Update apt cache.
      apt: update_cache=yes cache_valid_time=600
  tasks:
    - name: "Include docker.swarm"
      include_role:
        name: "docker.swarm"
```

## Run the test

```bash
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "pip3 install testinfra; molecule test --all"
```
