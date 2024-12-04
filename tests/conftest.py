import pytest

from dockcraft.client import DockerClient

@pytest.fixture
def client():
    return DockerClient.from_env()

@pytest.fixture
def containers() -> list:
    return DockerClient.from_env().containers.list(all_containers=True)

