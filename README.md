# DockCraft
Emphasizing crafting Docker solutions.
: Branch Master

##### Common imports
```python
from dockcraft.client import DockerClient
from dockcraft.settings import logger
client = DockerClient()
api = client.from_env(logger=logger)
```


#### Working with containers

##### Create New Container

```python
api.containers.create("python", name="DockCraft", command="sleep infinity")
```



1. List all the running containers
``` python
containers = api.containers.list(all_containers=True)
for container in containers:
    print(container)

```

2. Stop all containers
```python
for container in containers:
    container.stop()

```
3. restart all containers
```python
for container in containers:
    container.restart()

```
4. start all containers
```python
for container in containers:
    container.start()

```
5. Remove all containers
```python
for container in containers:
    container.delete()

```
6. Delete all containers
```python
for container in containers:
    container.delete()

```
7. rename all containers
```python
for container in containers:
    container.rename()

```
