from dockcraft.client import DockerClient
from dockcraft.settings import logger


if __name__ == "__main__":
    client = DockerClient()
    cd = client.from_env(logger=logger)
    logger.debug("using logger_client")

    containers = cd.containers.list(all_containers=True)
    # for container in containers:
    #     container.start()
    res = cd.containers.create("python", name="anything", command="sleep infinity")
    print(res)
