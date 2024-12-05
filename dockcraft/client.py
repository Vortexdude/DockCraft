from .api.client import APIClient
from .models.containers import ContainerCollection
from .models.images import ImageCollection


class DockerClient:
    def __init__(self, *args, **kwargs) -> None:
        self.api = APIClient(*args, **kwargs)

    @classmethod
    def from_env(cls, *args, **kwargs):
        if "logger" not in kwargs:
            from .settings import logger
            kwargs['logger'] = logger

        return cls(*args, **kwargs)

    @property
    def containers(self, *args, **kwargs):
        return ContainerCollection(client=self)

    @property
    def images(self, *args, **kwargs):
        return ImageCollection(client=self)
