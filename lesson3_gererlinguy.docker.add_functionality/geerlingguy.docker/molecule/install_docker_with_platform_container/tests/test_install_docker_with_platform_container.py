import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_platform_running(host):
    cmd = host.run('docker info')
    assert cmd.stdout.find("Running: 1") != -1

    platform = host.addr('localhost')
    assert platform.port(8080).is_reachable
