from dockcraft.client import DockerClient

if __name__ == "__main__":
    client = DockerClient()
    cd = client.from_env()

    containers = cd.containers.list(all_containers=True)
    for container in containers:
        print(container.remove())
