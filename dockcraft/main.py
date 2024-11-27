from dockcraft.client import DockerClient
from dockcraft.settings import logger


if __name__ == "__main__":
    client = DockerClient()
    cd = client.from_env(logger=logger)
    logger.debug("using logger_client")

    containers = cd.containers.list(all_containers=True)
    for container in containers:
        print(container.rename("Sandbox_ready"))
