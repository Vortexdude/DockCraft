from ..request_dispatcher import HttpReq
from .containers import ContainerApiMixin


class APIClient(HttpReq, ContainerApiMixin):
    def __init__(self, *args, **kwargs):
        if "logger" in kwargs:
            self.logger = kwargs['logger']

        HttpReq.__init__(self, *args, **kwargs)
        ContainerApiMixin.__init__(self)


    def get(self, url, /, *args, **kwargs):
        """basic api get request"""
        return self._get(url, *args, **kwargs)

    def post(self, url, /, *args, **kwargs):
        """basic api post request"""
        return self._post(url, *args, **kwargs)

    def delete(self, url, /, *args, **kwargs):
        """basic api delete request"""
        return self._delete(url, *args, **kwargs)
