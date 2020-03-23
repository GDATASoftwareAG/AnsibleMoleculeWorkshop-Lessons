# Lesson 1: Initialize a role and pass a test

* [home](./README.md)
* [next](./LESSON2.md)

To get the workshop going, we start with a rather simple task by just initializing a molecule test and pass the tests.

You can play around with it, by editing for example some boolean values and see how the linter kicks in.

## Initialize

```bash
docker run \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "molecule init role --verifier-name testinfra rolename"
```

Now navigate into the folder of your new role.

```bash
cd rolename
```

## copy the .yamllint

add a .yamllin file to folder `molecule/default/.yamllint`

```yaml
---
# Based on ansible-lint config
extends: default

rules:
  braces:
    max-spaces-inside: 1
    level: error
  brackets:
    max-spaces-inside: 1
    level: error
  colons:
    max-spaces-after: -1
    level: error
  commas:
    max-spaces-after: -1
    level: error
  comments: disable
  comments-indentation: disable
  document-start: disable
  empty-lines:
    max: 3
    level: error
  hyphens:
    level: error
  indentation: disable
  key-duplicates: enable
  line-length: disable
  new-line-at-end-of-file: disable
  new-lines:
    type: unix
  trailing-spaces: disable
  truthy: enable
```

## Edit

To get the linting going just add this to your `molecule/default/molecule.yml`

```yaml
lint: |
  set -e
  yamllint .
  ansible-lint .
```

Now you have to edit the meta/main.yml to pass the linter.

```yaml
galaxy_info:
  author: me
  description: myrole
  company: mycompany
  license: MIT
  min_ansible_version: 2.8
  platforms:
  - name: ubuntu
```

## Run the test

```bash
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):$(pwd) -w $(pwd) \
  --user root \
  quay.io/ansible/molecule:3.0.2 \
  /bin/sh -c "pip3 install testinfra; molecule test"
```
