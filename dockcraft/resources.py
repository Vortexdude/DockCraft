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

    def _dispatcher(self, response):
        if self.is_debug:
            if isinstance(response, list):
                self.logger.debug(f"{response=}")
                return response
            if "ContainersDeleted" in response.attrs:
                if response['ContainersDeleted']:
                    [self.logger.debug(f"Container deleted '{con[:12]}'") for con in response['ContainersDeleted']]
                else:
                    self.logger.debug("No Containers are deleted")
            else:
                self.logger.debug(f"{response=}")
        return response


class Model:
    id_attribute = 'Id'

    def __init__(self, attrs=None, client=None, collection=None):
        self.attrs = attrs
        self.client = client
        self.collection = collection

    @property
    def id(self):
        """The ID of the object"""
        return self.attrs.get(self.id_attribute)

    @property
    def short_id(self):
        return self.id[:12]

    @classmethod
    def prepare_model(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def dump(self):
        return {
            key: getattr(self, key)
            for key in [prop for prop in dir(self) if isinstance(getattr(type(self), prop, None), property)]
        }

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.short_id}>"

    def __call__(self, *args, **kwargs):
        return f"You should not call the {self.__class__.__name__} directly"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.short_id}>"
