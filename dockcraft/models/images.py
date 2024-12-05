from dockcraft.resources import Model, Collection

class Image(Model):
    pass

class ImageCollection(Collection):
    model = Image

    def list_images(self): pass

    def delete_images(self, image_id): pass

    def build_image(self, *args, **kwargs): pass
