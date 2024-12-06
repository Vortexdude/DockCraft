from ..api import BaseApiMixin
from ..exceptions import InternalSeverError
from ..utils import ExtraMeta


class ImageApiMixin(BaseApiMixin, metaclass=ExtraMeta):
    def images(self, all_images=False):
        """Fetching all the images similar to `docker images` GET /images/json"""

        params = {'all': "true" if all_images else "false"}

        endpoint = "/images/json"
        response = self.model.format(self.get(endpoint, query_param=params))

        if response.status_code != 200:
            return
        return response.body

    def inspect_image(self, image_id):
        """Inspecting image similar to `docker inspect` GET /images/{image_id}/json"""
        endpoint = f"/images/{image_id}/json"
        response = self.model.format(self.get(endpoint))
        if response.status_code != 200:
            raise Exception(f"Error while inspecting image: Status code {response.status_code}")
        return response.body

    def build_image(self, docker_file=None, tags=None, extrahosts=None, remote=None, platform=None, version=None):
        pass


    def image_history(self, image_id):
        """similar to `docker history` GET /images/{image_id}/history"""

        endpoint = f"/images/{image_id}/history"
        response = self.model.format(self.get(endpoint))
        if response.status_code != 200:
            raise Exception(f"error while image history: Status Code : {response.status_code}")
        return response.body

    def tag_image(self, image_id, repo, tag):
        """similar to `docker image tag` POST /images/{image}/tag"""

        params = {
            "repo": repo,
            "tag": tag
        }
        endpoint = f"/images/{image_id}/tag"
        response = self.model.format(self.post(endpoint, query_params=params))
        if response.status_code == 201:
            return response.body

    def remove_image(self, image_id):
        """remove the image similar to docker rmi DELETE /images/{image_id}"""

        endpoint = f"/images/{image_id}"
        response = self.model.format(self.delete(endpoint))
        if response.status_code == 200:
            return response.body
        elif response.status_code == 404:
            raise Exception("Image not found")
        elif response.status_code == 409:
            raise Exception("Conflict")
        else:
            raise InternalSeverError()

    def search_image(self, name, limit=10):
        params = dict(
            term=name,
            limit=limit
        )
        endpoint = "/images/search"
        response = self.model.format(self.get(endpoint, query_param=params))

        if response.status_code == 200:
            return response.body
        else:
            raise InternalSeverError()
