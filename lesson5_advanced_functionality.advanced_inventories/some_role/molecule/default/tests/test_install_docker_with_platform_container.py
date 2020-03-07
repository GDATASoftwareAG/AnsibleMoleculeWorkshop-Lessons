def test_platform_running(host):
    cmd = host.run('docker info')
    assert cmd.stdout.find("Swarm: active") > 0

    ansible_vars = host.ansible.get_variables()
    if 'manager' in ansible_vars['group_names']:
        cmd = host.run('docker node ls')
        cmd.rc == 0