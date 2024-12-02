from pydantic import BaseModel
from rich.console import Console
from .settings import is_debug, logger


class Collection:
    model = None

    def __init__(self, client):
        self.client = client
        self.console = Console()
        self.logger = logger

    @property
    def is_debug(self):
        return is_debug()

class Model(BaseModel):
    Id: str
    client: object = None

    @property
    def short_id(cls):
        return cls.Id[:12]

    @classmethod
    def prepare_model(cls, data, client=None):
        if client:
            data['client'] = client

        return cls.model_validate(data)
