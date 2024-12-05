def test_start_container(docker_client, test_container):
    container = test_container
    assert container.name == "anything"
    assert container.status == "created"
    assert len(container.id) > 0
    assert len(container.short_id) == 12

def test_restart_container(docker_client, test_container):
    container = test_container
    container.restart()
    assert container.status == "running"
    container.rename("tester")
    assert container.name == "tester"
    assert container.status == "running"
    container.stop()
    assert container.status == "exited"
    response = container.delete()
