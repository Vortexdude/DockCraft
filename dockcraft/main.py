from dockcraft.client import DockerClient


if __name__ == "__main__":
    api = DockerClient.from_env()
    containers = api.containers.list(all_containers=True)
    for container in containers:
        print(container)

    # res = cd.containers.create("python", name="anything", command="sleep infinity")
    # print(res)
