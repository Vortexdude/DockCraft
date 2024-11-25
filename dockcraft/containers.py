from .resources import Collection
from .models.containers import Container


class ContainerCollection(Collection):
    model = Container

    def list(self, all_containers=True) -> list[model]:
        response = self.client.api.containers(all_containers=all_containers)
        return [self.model.prepare_model(container, client=self.client) for container in response]

    def get(self, container_id):
        container = self.client.api.get_container(container_id)
        return self.model.prepare_model(container, client=self.client)

    def remove(self):
        pass

    def rename(self):
        pass
