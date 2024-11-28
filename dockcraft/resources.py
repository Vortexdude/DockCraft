from pydantic import BaseModel


class Collection:
    model = None

    def __init__(self, client):
        self.client = client

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
