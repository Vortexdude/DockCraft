from dockcraft.client import DockerClient


if __name__ == "__main__":
    api = DockerClient.from_env()

    # container = api.containers.create("python", name="anything", command="sleep infinity", ports={"8080/tcp": "8081"})
    container = api.containers.create("nginx", name="from_api", ports={"80/tcp": "8081"})
    containers = api.containers.list(all_containers=True)
    # for cont in containers:
    #     data = cont.rename("from-new-model")
    #     print(data)

    # api.containers.get(containers[0].short_id)
    # container = api.containers.create("python", name="anything", command="sleep infinity")
    # print(f"{container.id=}")
    # api.containers.rename(container.Id, "Newone")
    # ss = api.containers.prune()

    # ss = api.containers.rename(containers[0].Id, "newOne")
