# Molecule workshop steps

Here you find the lessons where we start the parts of our workshops from.

Most of the steps are also the target of their previous step.

## Links

* [molecule documentation](https://molecule.readthedocs.io/en/latest/)
* [molecule github](https://github.com/ansible-community/molecule)
* [molecule docker](https://quay.io/repository/ansible/molecule)
* [testinfra documentation](https://testinfra.readthedocs.io/en/latest/)

## Running Molecule within a role with the latest image

IMPORTANT: If you want to run these tests locally your docker engine must use the storage-engine aufs

Just create or edit the config file /etc/docker/daemon.json with content

```json
{
  "storage-driver": "aufs"
}
```

then run in a role directory

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "pip3 install testinfra; molecule test -s default"
```

[Lesson 1](./LESSON1.md)

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


## Lesson 2: Add a test to an existing role

### Initialize

```
docker run  -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "molecule init scenario --verifier-name testinfra install_docker_without_docker_compose"
```

### Run the test

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "pip3 install testinfra; molecule test --all"

```

## Lesson 3: Add functionality to a role

### Initialize


```
docker run  -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "molecule init scenario --verifier-name testinfra install_docker_with_platform_container"
```

### Run the test

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "pip3 install testinfra; molecule test --all"

```

## Lesson 4: dependend roles

### Initialize



### Run the test

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "pip3 install testinfra; molecule test --all"

```

## Lesson 5: advanced inventory

### Initialize



### Run the test

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "pip3 install testinfra; molecule test --all"

```

## you want to give us your power for the workshop?


```
docker run -d --rm --name gitlab-runner -v /var/run/docker.sock:/var/run/docker.sock -v /home/gitlab-runner:/home/gitlab-runner -v /buiilds:/builds --privileged    gitlab/gitlab-runner:latest
```

```
docker exec -it gitlab-runner /bin/bash
```

```
gitlab-runner register -n   --url https://gitlab.com/   --registration-token GZqpz8aRxUqiY3FsNqAz   --executor docker   --description "MYRUNNERNAME"   --docker-image "docker:19.03.1"  --docker-volumes /var/run/docker.sock:/var/run/docker.sock --docker-volumes /home/gitlab-runner:/home/gitlab-runner --docker-volumes /builds:/builds --tag-list molecule-workshop
```

This registeres a gitlab-runner on your local machine that can be used in the workshop. This is for careful use and should be killed after the workshop.