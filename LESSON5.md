# Lesson 5: advanced inventory

[home](./README.md)
[back](./LESSON4.md)

## Initialize



## Run the test

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):$(pwd) -w $(pwd) --user root quay.io/ansible/molecule:3.0.2 /bin/sh -c "pip3 install testinfra; molecule test --all"

```