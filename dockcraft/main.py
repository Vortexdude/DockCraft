from dockcraft.client import DockerClient


if __name__ == "__main__":
    api = DockerClient.from_env()

    # containers = api.containers.list(all_containers=True)
    # res = api.containers.create("python", name="anything", command="sleep infinity")
    # containers = api.containers.list(all_containers=True)
    ss = api.containers.prune()

    # ss = api.containers.rename(containers[0].Id, "newOne")
    print(ss)
