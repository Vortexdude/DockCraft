from dockcraft.exceptions import (BadParameters, ContainerAlreadyExists,
                                  ContainerAlreadyStarted,
                                  ContainerAlreadyStopped,
                                  ContainerDeletionError,
                                  ContainerNameAlreadyUsed,
                                  ContainerNotFoundError, InternalSeverError)
# local import
from ..api import BaseApiMixin
from ..utils import container_dict, ExtraMeta


class ContainerApiMixin(BaseApiMixin, metaclass=ExtraMeta):

    def containers(self, all_containers=True):
        """fetching all the containers using 'GET' '/containers/json' """

        all_containers = "true" if all_containers else "false"

        endpoint = f"/containers/json?all={all_containers}"
        response = self.model.format(self.get(endpoint))

        if response.status_code != 200:
            raise Exception(response.body)

        return response.body

    def inspect_container(self, container_id):
        """Inspect the container similar to 'docker inspect {Id} /containers/{id}/json' """

        endpoint = f"/containers/{container_id}/json"
        response = self.model.format(self.get(endpoint))
        if response.status_code == 200:
            return response.body
        elif response.status_code == 404:
            raise ContainerNotFoundError(container_id)
        else:
            raise InternalSeverError()


    def create_container(self, image, name=None, command=None, hostname=None, user=None, platform=None):
        """creating the container with 'POST' '/containers/create' """

        params = {}
        if name:
            params['name'] = name
        if platform:
            params['platform'] = platform

        endpoint = "/containers/create"
        docker_config = container_dict(image, command=command, hostname=hostname, user=user)
        response = self.model.format(self.post(endpoint, payload=docker_config, query_param=params))

        if response.status_code == 201:
            return response.body
        elif response.status_code == 409:
            raise ContainerAlreadyExists(response.body['message'])
        else:
            raise InternalSeverError()

    def start_container(self, container_id):
        """Starting the container using 'POST' '/containers/{container_id}/start' """

        endpoint = f"/containers/{container_id}/start"
        response = self.model.format(self.post(endpoint))
        if response.status_code == 204:
            return "Container Created Successfully" # this goes to log

        elif response.status_code == 304:
            raise ContainerAlreadyStarted(container_id)

        else:
            raise InternalSeverError()

    def stop_container(self, container_id):
        """Stopping the containers 'POST' '/containers/{container_id}/stop' """

        endpoint = f"/containers/{container_id}/stop"
        response = self.model.format(self.post(endpoint))
        if response.status_code == 204:
            return response.body # This to filter by the model itself

        elif response.status_code == 304:
            raise ContainerAlreadyStopped(container_id)

        elif response.status_code == 404:
            raise ContainerNotFoundError(container_id)

        else:
            raise InternalSeverError()

    def restart_container(self, container_id):
        """Restarting the containers 'POST' '/containers/{container_id}/restart' """

        endpoint = f"/containers/{container_id}/restart"
        response = self.model.format(self.post(endpoint))
        if response.status_code == 204:
            return response.body # This to filter by the model itself

        elif response.status_code == 404:
            raise ContainerNotFoundError(container_id)

        else:
            raise InternalSeverError()

    def delete_container(self, container_id):
        """Remove a container. Similar to the 'docker rm' command. => DELETE /containers/{container_id} """

        endpoint = f"/containers/{container_id}"
        response = self.model.format(self.delete(endpoint))
        if response.status_code == 204:
            return response.body # This to filter by the model itself

        elif response.status_code == 400:
            raise BadParameters()

        elif response.status_code == 404:
            raise ContainerNotFoundError(container_id)

        elif response.status_code == 409:
            raise ContainerDeletionError(container_id)

        else:
            raise InternalSeverError()

    def rename_container(self, container_id, name):
        """Renaming the container using 'POST' '/containers/{container_id}/rename' """

        endpoint = f"/containers/{container_id}/rename"
        params = {"name": name}
        response = self.model.format(self.post(endpoint, query_param=params))
        if response.status_code == 204:
            return response.body # This to filter by the model itself

        elif response.status_code == 404:
            raise ContainerNotFoundError(container_id)

        elif response.status_code == 400:
            raise ContainerNameAlreadyUsed(container_id[:12])

        else:
            raise InternalSeverError()

    def prune_containers(self, filters:dict=None):
        """Delete stopped containers similar to 'docker container prune' => POST /containers/prune."""

        endpoint = "/containers/prune"
        params = {}
        if filters:
            params['filters'] = filters
        response = self.model.format(self.post(endpoint, query_param=params))
        if response.status_code == 200:
            return response.body # This to filter by the model itself
        else:
            raise InternalSeverError()
