from dockcraft.exceptions import (ContainerNotFoundError,
    InternalSeverError, ContainerAlreadyStopped,
    ContainerNameAlreadyUsed, BadParameters, ContainerDeletionError)

from functools import wraps


def logging(level="debug"):
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            if level == "debug":
                if function.__doc__:
                    self.logger.debug(f"Invoking function '{function.__name__}' with args {kwargs}")
                    self.logger.debug(function.__doc__)

            elif level == "info":
                if function.__doc__:
                    self.logger.info(function.__doc__)

            elif level == "warning":
                if function.__doc__:
                    self.logger.warning(function.__doc__)

            result = function(self, *args, **kwargs)
            return result
        return wrapper
    return decorator



class BaseApiMixin(object):

    def get(self, endpoint, *args, **kwargs):
        raise NotImplementedError()

    def post(self, endpoint, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, endpoint, *args, **kwargs):
        raise NotImplementedError()


class ContainerApiMixin(BaseApiMixin):

    @logging("debug")
    def containers(self, all_containers=True):
        """fetching all the containers using /containers/json endpoint"""

        all_containers = "true" if all_containers else "false"

        endpoint = f"/containers/json?all={all_containers}"
        response = self.get(endpoint)

        if str(response['Status-Code']) != "200":
            raise Exception(f"{response['body']}")

        return response['body']

    @logging("debug")
    def create_container(self, image, command=None, **kwargs):
        params = {}
        if "name" in kwargs:
            params.update({"name": kwargs['name']})

        endpoint = "/containers/create"
        kwargs['image'] = image
        response = self.post(endpoint, payload=kwargs, query_param=params)
        if str(response['Status-Code']) == "201":
            return response['body']
        else:
            raise Exception(response['body'])

    @logging("debug")
    def stop_container(self, container_id):
        endpoint = f"/containers/{container_id}/stop"
        response = self.post(endpoint)
        if str(response['Status-Code']) == "204":
            return response['body']

        elif str(response['Status-Code']) == "304":
            raise ContainerAlreadyStopped(container_id)

        elif str(response['Status-Code']) == "404":
            raise ContainerNotFoundError(container_id)

        else:
            raise InternalSeverError()

    @logging("debug")
    def restart_container(self, container_id):
        endpoint = f"/containers/{container_id}/restart"
        response = self.post(endpoint)
        if str(response['Status-Code']) == "204":
            return response['body']

        elif str(response['Status-Code']) == "404":
            raise ContainerNotFoundError(container_id)

        else:
            raise InternalSeverError()

    @logging("debug")
    def delete_container(self, container_id):
        endpoint = f"/containers/{container_id}"
        response = self.delete(endpoint)
        print(f"{response=}")
        if str(response['Status-Code']) == "204":
            return f"<Container {container_id[:12]}>"

        elif str(response['Status-Code']) == "400":
            raise BadParameters()

        elif str(response['Status-Code']) == "404":
            raise ContainerNotFoundError(container_id)

        elif str(response['Status-Code']) == "409":
            raise ContainerDeletionError(container_id)

        else:
            raise ContainerNotFoundError(container_id)

    @logging("debug")
    def rename_container(self, container_id, name):
        endpoint = f"/containers/{container_id}/rename"
        params = {"name": name}
        response = self.post(endpoint, query_param=params)
        if str(response['Status-Code']) == "204":
            return response['body']

        elif str(response['Status-Code']) == "404":
            raise ContainerNotFoundError(container_id)

        elif str(response['Status-Code']) == "400":
            raise ContainerNameAlreadyUsed(container_id[:12])

        else:
            raise InternalSeverError()
