class BaseException(Exception):
    message = None
    def __init__(self):
        super().__init__(self.message)


class ContainerException(BaseException):
    def __init__(self, container):
        if len(container) >= 12:
            container = container[:12]

        self.message = self.message.format(container)
        super().__init__()


class InternalSeverError(BaseException):
    message = "Facing Internal Server Error"


class ContainerNotFoundError(ContainerException):
    message = "Container {} not found"
    def __init__(self, container):
        super().__init__(container)


class ContainerAlreadyStopped(ContainerException):
    message = "container {} already stopped"
    def __init__(self, container):
        super().__init__(container)


class ContainerNameAlreadyUsed(ContainerException):
    message = "name {} already in use"
    def __init__(self, container):
        super().__init__(container)


class ContainerDeletionError(ContainerException):
    message = "Container {} is in running state"
    def __init__(self, container):
        super().__init__(container)

class BadParameters(BaseException):
    def __init__(self):
        self.message = "Bad Params"
        super().__init__()
