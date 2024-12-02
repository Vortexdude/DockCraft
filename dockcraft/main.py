from dockcraft.client import DockerClient
from rich.console import Console

console = Console()




if __name__ == "__main__":
    api = DockerClient.from_env()
    with console.status("[bold green] working on the task ") as status:
        containers = api.containers.list(all_containers=True)
        for container in containers:
            console.log(container)

    res = api.containers.create("python", name="anything", command="sleep infinity")


