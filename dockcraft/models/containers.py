from dockcraft.exceptions import (BadParameters, ContainerAlreadyStarted,
                                  ContainerAlreadyStopped,
                                  ContainerDeletionError,
                                  ContainerNameAlreadyUsed,
                                  ContainerNotFoundError)
from dockcraft.resources import Model, Collection
from dockcraft.utils import ExtraMeta


class Container(Model):

    def _perform_api_action(self, action, *args, **kwargs):
        try:
            action(*args, **kwargs)
        except (ContainerAlreadyStarted, ContainerAlreadyStopped, ContainerNameAlreadyUsed, BadParameters) as e:
            return e.message
        except (ContainerNotFoundError, ContainerDeletionError) as e:
            raise e
        except Exception as e:
            raise e
        return self.model_dump(mode='json', exclude={"client"})

    def start(self):
        return self._perform_api_action(self.client.api.start_container, self.Id)


    def stop(self):
        return self._perform_api_action(self.client.api.stop_container, self.Id)


    def restart(self):
        return self._perform_api_action(self.client.api.restart_container, self.Id)


    def delete(self):
        return self._perform_api_action(self.client.api.delete_container, self.Id)


    def rename(self, name):
        return self._perform_api_action(self.client.api.rename_container, self.Id, name=name)


    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.short_id}>"

    def __call__(self, *args, **kwargs):
        return f"You should not call the {self.__class__.__name__} directly"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.short_id}>"


class ContainerCollection(Collection, metaclass=ExtraMeta):
    model = Container

    def list(self, all_containers=True) -> list[model]:
        response = self.client.api.containers(all_containers=all_containers)
        containers = [self.model.prepare_model(container, client=self.client) for container in response]
        return self._dispatcher(containers)

    def get(self, container_id) -> model:
        response = self.client.api.get_container(container_id)
        container = self.model.prepare_model(response, client=self.client)
        return self._dispatcher(container)

    def create(self, image, command=None, **kwargs) -> model:
        response = self.client.api.create_container(image, command=command, **kwargs)
        container = self.model.prepare_model(response)
        return self._dispatcher(container)

    def prune(self, filters: dict=None) -> None:
        response = self.client.api.prune_containers(filters=filters)
        return self._dispatcher(response)

    def rename(self, container_id, name) -> None:
        response = self.client.api.rename_container(container_id, name)
        return self._dispatcher(response)
