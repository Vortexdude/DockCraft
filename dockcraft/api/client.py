from ..request_dispatcher import HttpReq
from .containers import ContainerApiMixin


class APIClient(HttpReq, ContainerApiMixin):

    def get(self, url, /, *args, **kwargs):
        return self._get(url, *args, **kwargs)

    def post(self, url, /, *args, **kwargs):
        return self._post(url, *args, **kwargs)

    def delete(self, url, /, *args, **kwargs):
        return self._delete(url, *args, **kwargs)
