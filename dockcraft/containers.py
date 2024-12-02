from .models.containers import Container
from .resources import Collection
from .utils import ExtraMeta


class ContainerCollection(Collection, metaclass=ExtraMeta):
    model = Container

    def list(self, all_containers=True) -> list[model]:
        response = self.client.api.containers(all_containers=all_containers)
        containers = [self.model.prepare_model(container, client=self.client) for container in response]
        if self.is_debug:
            self.logger.debug(containers)

        return containers

    def get(self, container_id):
        response = self.client.api.get_container(container_id)
        container = self.model.prepare_model(response, client=self.client)
        if self.is_debug:
            self.logger.debug(container)

        return container

    def create(self, image, command=None, **kwargs):
        response = self.client.api.create_container(image, command=command, **kwargs)
        container = self.model.prepare_model(response)
        if self.is_debug:
            self.logger.debug(container)

        return container

    def remove(self):
        pass

    def rename(self):
        pass
