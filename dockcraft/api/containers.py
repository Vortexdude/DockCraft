from dockcraft.exceptions import (BadParameters, ContainerAlreadyExists,
                                  ContainerAlreadyStarted,
                                  ContainerAlreadyStopped,
                                  ContainerDeletionError,
                                  ContainerNameAlreadyUsed,
                                  ContainerNotFoundError, InternalSeverError)
# local import
from ..api import BaseApiMixin
from ..utils import container_dict, logging_dec


class ContainerApiMixin(BaseApiMixin):

    @logging_dec()
    def containers(self, all_containers=True):
        """fetching all the containers using 'GET' '/containers/json' """

        all_containers = "true" if all_containers else "false"

        endpoint = f"/containers/json?all={all_containers}"
        response = self.model.format(self.get(endpoint))

        if response.status_code != 200:
            raise Exception(response.body)

        return response.body

    @logging_dec()
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

    @logging_dec()
    def start_container(self, container_id):
        """Starting the container using 'POST' '/containers/{container_id}/start' """

        endpoint = f"/containers/{container_id}/start"
        response = self.model.format(self.post(endpoint))
        if response.status_code == 204:
            self.logger.debug("container started successfully")
            return response.status_code # no need to do this

        elif response.status_code == 304:
            raise ContainerAlreadyStarted(container_id)

        else:
            raise InternalSeverError()

    @logging_dec()
    def stop_container(self, container_id):
        """Stopping the containers 'POST' '/containers/{container_id}/stop' """

        endpoint = f"/containers/{container_id}/stop"
        response = self.model.format(self.post(endpoint))
        if response.status_code == 204:
            return response.body

        elif response.status_code == 304:
            raise ContainerAlreadyStopped(container_id)

        elif response.status_code == 404:
            raise ContainerNotFoundError(container_id)

        else:
            raise InternalSeverError()

    @logging_dec()
    def restart_container(self, container_id):
        """Restarting the containers 'POST' '/containers/{container_id}/restart' """

        endpoint = f"/containers/{container_id}/restart"
        response = self.model.format(self.post(endpoint))
        if response.status_code == 204:
            return response.body

        elif response.status_code == 404:
            raise ContainerNotFoundError(container_id)

        else:
            raise InternalSeverError()

    @logging_dec()
    def delete_container(self, container_id):
        """Deleting the container using 'DELETE' '/containers/{container_id}' """

        endpoint = f"/containers/{container_id}"
        response = self.model.format(self.delete(endpoint))
        if response.status_code == 204:
            return f"<Container {container_id[:12]}>"

        elif response.status_code == 400:
            raise BadParameters()

        elif response.status_code == 404:
            raise ContainerNotFoundError(container_id)

        elif response.status_code == 409:
            raise ContainerDeletionError(container_id)

        else:
            raise InternalSeverError()

    @logging_dec()
    def rename_container(self, container_id, name):
        """Renaming the container using 'POST' '/containers/{container_id}/rename' """

        endpoint = f"/containers/{container_id}/rename"
        params = {"name": name}
        response = self.model.format(self.post(endpoint, query_param=params))
        if response.status_code == 204:
            return response.body

        elif response.status_code == 404:
            raise ContainerNotFoundError(container_id)

        elif response.status_code == 400:
            raise ContainerNameAlreadyUsed(container_id[:12])

        else:
            raise InternalSeverError()
