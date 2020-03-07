def test_docker_compose_working(host):
    cmd = host.run('docker-compose --version')

    assert cmd.rc != 0
