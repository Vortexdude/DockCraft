from dockcraft.utils import unix2dt
from dockcraft.resources import Model, Collection

class Image(Model):

    @property
    def id(self):
        return self.attrs.get("Id").split(":")[1]

    @property
    def created(self):
        _dt = int(self.attrs.get("Created"))
        return unix2dt(_dt)

    @property
    def labels(self):
        return self.attrs.get("Labels")

    @property
    def tags(self):
        return self.attrs.get("RepoTags")[0].split(":")[1]


class ImageCollection(Collection):
    model = Image

    def list_images(self, *args, **kwargs):
        response = self.client.api.images(*args, **kwargs)
        images = [self.model.prepare_model(attrs=image) for image in response]
        if not images:
            self.logger.debug("No Images found")
        return self._dispatcher(images)

    def inspect_image(self, *args, **kwargs):
        response = self.client.api.inspect_image(*args, **kwargs)
        return response

    def delete_images(self, image_id): pass

    def build_image(self, *args, **kwargs): pass

    def search_image(self, *args, **kwargs):
        return self.client.api.search_image(*args, **kwargs)
