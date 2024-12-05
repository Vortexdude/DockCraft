import pytest
from dockcraft.client import DockerClient

DUMMY_CONTAINER = {
    "name": "anything",
    "image": "python",
    "command": "sleep infinity"
}


@pytest.fixture()
def docker_client():
    client =  DockerClient.from_env()
    yield client

    for container in client.containers.list(all_containers=True):
        try:
            container.stop()
            container.delete()
        except Exception as e:
            print(f"Cleanup failed for container {container.id}: {e}")

@pytest.fixture()
def test_container(docker_client) -> list:
    container = docker_client.containers.create(**DUMMY_CONTAINER)
    return container

    try:
        container.delete()
    except Exception as e:
        pass
