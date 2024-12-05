from dockcraft.exceptions import (BadParameters, ContainerAlreadyStarted,
                                  ContainerAlreadyStopped,
                                  ContainerDeletionError,
                                  ContainerNameAlreadyUsed,
                                  ContainerNotFoundError)
from dockcraft.resources import Model, Collection
from dockcraft.utils import ExtraMeta
from dockcraft.settings import logger


class Container(Model):

    @property
    def name(self):
        if self.attrs.get('Names'):
            return self.attrs['Names'][0].lstrip("/")
        elif self.attrs.get("Name"):
            return self.attrs.get("Name").lstrip("/")


    @property
    def image(self):
        image_id = self.attrs.get("ImageId", self.attrs['Image'])
        if not image_id:
            return None
        # return self.client.images.get(image_id.split(":")[1])
        return image_id

    @property
    def status(self):
        """
        The status of the container. For example, ``running``, or ``exited``.
        """
        if isinstance(self.attrs['State'], dict):
            return self.attrs['State']['Status']
        return self.attrs['State']

    @property
    def ports(self):
        """
        The ports that the container exposes as a dictionary.
        """
        return self.attrs.get('NetworkSettings', {}).get('Ports', {})

    def _reload(self):
        updated_args = self.client.api.inspect_container(self.id)
        self.attrs.update(updated_args)

    @staticmethod
    def _perform_api_action(action, *args, **kwargs):
        try:
            return action(*args, **kwargs)
        except (ContainerAlreadyStarted, ContainerAlreadyStopped, ContainerNameAlreadyUsed, BadParameters) as e:
            return e.message
        except (ContainerNotFoundError, ContainerDeletionError) as e:
            raise e
        except Exception as e:
            raise e

    def start(self):
        self._perform_api_action(self.client.api.start_container, self.id)
        self._reload()
        return self


    def stop(self):
        self._perform_api_action(self.client.api.stop_container, self.id)
        self._reload()
        return self


    def restart(self):
        self._perform_api_action(self.client.api.restart_container, self.id)
        self._reload()
        return self


    def delete(self):
        self._perform_api_action(self.client.api.delete_container, self.id)
        self._reload()
        return self


    def rename(self, name):
        self._perform_api_action(self.client.api.rename_container, self.id, name=name)
        self._reload()
        return self


class ContainerCollection(Collection, metaclass=ExtraMeta):
    model = Container

    def list(self, all_containers=True) -> list[model]:
        response = self.client.api.containers(all_containers=all_containers)
        containers = [self.model.prepare_model(attrs=container, client=self.client) for container in response]
        if not containers:
            logger.debug("No running container found")
        return self._dispatcher(containers)

    def get(self, container_id) -> model:
        response = self.client.api.inspect_container(container_id)
        container = self.model.prepare_model(attrs=response, client=self.client)
        return self._dispatcher(container)

    def create(self, image, command=None, **kwargs) -> model:
        response = self.client.api.create_container(image, command=command, **kwargs)
        return self.get(response['Id'])

    def prune(self, filters: dict=None) -> None:
        response = self.client.api.prune_containers(filters=filters)
        return self._dispatcher(response)

    def rename(self, container_id, name) -> None:
        response = self.client.api.rename_container(container_id, name)
        return self._dispatcher(response)
