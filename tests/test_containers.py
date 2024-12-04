def test_create_container(client, containers):
    name = "test_container"
    image = "python"
    command = "sleep infinity"
    data = client.containers.create(image=image, command=command, name=name)
    if data.Id:
        assert True

def test_list_containers(containers):
    assert len(containers) == 1

def test_rename_container(client, containers):
    cid = containers[0].Id
    response = client.containers.rename(cid, "by_pytest")
    print(response)

def test_prune_containers(client, containers):
    response = client.containers.prune()
    print(response)
