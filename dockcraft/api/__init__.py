from dockcraft.models.http_res import HttpRes


class BaseApiMixin(object):

    def get(self, endpoint, *args, **kwargs):
        raise NotImplementedError()

    def post(self, endpoint, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, endpoint, *args, **kwargs):
        raise NotImplementedError()

    @property
    def model(self):
        return HttpRes
