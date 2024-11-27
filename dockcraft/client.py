from .api.client import APIClient
from .containers import ContainerCollection


class DockerClient:
    def __init__(self, *args, **kwargs) -> None:
        self.api = APIClient(*args, **kwargs)

    @classmethod
    def from_env(cls, *args, **kwargs):
        if "logger" in kwargs:
            cls.logger = kwargs['logger']

        return cls(*args, **kwargs)

    @property
    def containers(self, *args, **kwargs):
        return ContainerCollection(client=self)
