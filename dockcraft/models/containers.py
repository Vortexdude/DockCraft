from dockcraft.exceptions import (BadParameters, ContainerAlreadyStarted,
                                  ContainerAlreadyStopped,
                                  ContainerDeletionError,
                                  ContainerNameAlreadyUsed,
                                  ContainerNotFoundError)
from dockcraft.resources import Model
from dockcraft.utils import logging_dec


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

    @logging_dec()
    def start(self):
        return self._perform_api_action(self.client.api.start_container, self.Id)

    @logging_dec()
    def stop(self):
        return self._perform_api_action(self.client.api.stop_container, self.Id)

    @logging_dec()
    def restart(self):
        return self._perform_api_action(self.client.api.restart_container, self.Id)

    @logging_dec()
    def delete(self):
        return self._perform_api_action(self.client.api.delete_container, self.Id)

    @logging_dec()
    def rename(self, name):
        return self._perform_api_action(self.client.api.rename_container, self.Id, name=name)


    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.short_id}>"

    def __call__(self, *args, **kwargs):
        return f"You should not call the {self.__class__.__name__} directly"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.short_id}>"
