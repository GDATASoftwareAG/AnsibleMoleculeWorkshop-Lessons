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
