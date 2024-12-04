from dockcraft.client import DockerClient


if __name__ == "__main__":
    api = DockerClient.from_env()

    # container = api.containers.create("python", name="anything", command="sleep infinity")
    # containers = api.containers.list(all_containers=True)
    # for cont in containers:
    #     data = cont.rename("from-new-model")
    #     print(data)

    # api.containers.get(containers[0].short_id)
    # container = api.containers.create("python", name="anything", command="sleep infinity")
    # print(f"{container.id=}")
    # api.containers.rename(container.Id, "Newone")
    # ss = api.containers.prune()

    # ss = api.containers.rename(containers[0].Id, "newOne")
