def test_platform_running(host):
    cmd = host.run('docker info')
    assert cmd.stdout.find("Running: 1") != -1

    platform = host.addr('localhost')
    assert platform.port(8080).is_reachable
