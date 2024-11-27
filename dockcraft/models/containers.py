from dockcraft.resources import Model
from dockcraft.exceptions import ContainerNameAlreadyUsed, ContainerNotFoundError
from dockcraft.utils import logging_dec


class Container(Model):

    @classmethod
    def prepare_model(cls, data, client=None):
        if client:
            data['client'] = client

        return cls.model_validate(data)

    @logging_dec()
    def stop(self):
        return self.client.api.stop_container(self.Id)

    @logging_dec()
    def restart(self):
        return self.client.api.restart_container(self.Id)

    @logging_dec()
    def delete(self):
        return self.client.api.delete_container(self.Id)

    @logging_dec()
    def rename(self, name):
        try:
            self.client.api.rename_container(self.Id, name=name)
        except ContainerNameAlreadyUsed as e:
            return e.message
        except ContainerNotFoundError as e:
            raise e

        return self.model_dump(mode='json', exclude={"client"})

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.short_id}>"

    def __call__(self, *args, **kwargs):
        return f"You should not call the {self.__class__.__name__} direcly"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.short_id}>"
