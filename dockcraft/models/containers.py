from dockcraft.resources import Model


class Container(Model):

    @classmethod
    def prepare_model(cls, data, client=None):
        if client:
            data['client'] = client
            cls.client = client

        return cls.model_validate(data)

    def stop(self):
        return self.client.api.stop_container(self.Id)

    def restart(self):
        return self.client.api.restart_container(self.Id)

    def remove(self):
        return self.client.api.delete_container(self.Id)

    def rename(self, name):
        return self.client.api.rename_container(self.Id, name=name)


    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>: {self.short_id}"

    def __call__(self, *args, **kwargs):
        return f"You should not call the {self.__class__.__name__} direcly"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>: {self.short_id}"
