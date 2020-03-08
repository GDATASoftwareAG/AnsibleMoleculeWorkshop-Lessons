## Lesson 1: Initialize a role and pass a test

To get the workshop going, we start with a rather simple task by just initializing a molecule test and pass the tests.

You can play around with it, by editing for example some boolean values and see how the linter kicks in.

### Initialize

```
docker run  -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "molecule init role --verifier-name testinfra rolename"
```

### Edit

To get the linting going just add this to your molecule/molecule.yml

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
  platforms:
  - name: ubuntu
```

We also like the truthy check, so remove this line, from your molecule/default/.yamlint.yml

```
  truthy: disable
```

### Run the test

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "pip3 install testinfra; molecule test"

```