from dockcraft.client import DockerClient


if __name__ == "__main__":
    cd = DockerClient.from_env()

    res = cd.containers.create("python", name="anything", command="sleep infinity")
    print(res)
