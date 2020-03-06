# Molecule workshop steps

Here you find the stages / steps where we start the parts of our workshops from.

Most of the steps are also the target of their previous step.

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
