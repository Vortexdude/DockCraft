import logging
from shlex import split
from functools import wraps

banner = """ \n
 _____                                                                            _____ 
( ___ )                                                                          ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
 |   | ██████╗  ██████╗  ██████╗██╗  ██╗ ██████╗██████╗  █████╗ ███████╗████████╗ |   | 
 |   | ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝ |   | 
 |   | ██║  ██║██║   ██║██║     █████╔╝ ██║     ██████╔╝███████║█████╗     ██║    |   | 
 |   | ██║  ██║██║   ██║██║     ██╔═██╗ ██║     ██╔══██╗██╔══██║██╔══╝     ██║    |   | 
 |   | ██████╔╝╚██████╔╝╚██████╗██║  ██╗╚██████╗██║  ██║██║  ██║██║        ██║    |   | 
 |   | ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝    |   | 
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
(_____)                                                                          (_____)
\n"""

class CustomFormatter(logging.Formatter):
    GREEN = "\x1b[32m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    GRAY = "\x1b[38;20m"
    LIGHT_GRAY = "\033[0;37m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    WHITE = "\x1b[0m"
    RESET = "\x1b[0m"

    custom_format = "%(logger_namespace)s %(asctime)s %(levelname)6s - %(message)s"
    time_format = "%Y-%m-%dT%H:%M:%S"

    FORMATS = {
        logging.DEBUG: BLUE + custom_format + RESET,
        logging.INFO: CYAN + custom_format + RESET,
        logging.WARNING: YELLOW + custom_format + RESET,
        logging.ERROR: RED + custom_format + RESET,
        logging.CRITICAL: BOLD_RED + custom_format + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.time_format)
        return formatter.format(record)


class CustomLogger:
    def __init__(self, log_level: str, logger_namespace):
        if log_level is None:
            raise Exception('Unable to find the log level')
        log_levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        logger = logging.getLogger(__name__)
        logger.setLevel(log_levels[log_level])
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CustomFormatter())
        logger.addHandler(console_handler)
        self.logger = logging.LoggerAdapter(
            logger,
            {"logger_namespace": logger_namespace}
        )
        self.log_level = self.logger.logger.level

    def get_logger(self):
        return self.logger


def logging_dec():
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            # logger =
            if hasattr(self, "logger"):
                logger = self.logger
            elif hasattr(self, "client"):
                logger = self.client.api.logger
            else:
                return function(self, *args, **kwargs)

            message = "Invoking "

            if "." in function.__qualname__:
                message += f"method "
            else:
                message += f"function "

            message += f"{function.__module__}.{function.__qualname__} "
            logger.info(message)

            if logger.getEffectiveLevel() == 10:  # check for debug or info
                pass

            if args or kwargs:
                if args and not kwargs:
                    message += f"with args {args}"
                if not args and kwargs:
                    message += f"with kwargs {kwargs}"
                if args and kwargs:
                    message += f"with args {args} and kwargs {kwargs}"

                logger.debug(message)
            logger.debug(function.__doc__) if function.__doc__ else None

            result = function(self, *args, **kwargs)
            return result
        return wrapper
    return decorator

def _extract_logger(self):
    if hasattr(self, "logger"):
        return self.logger
    elif hasattr(self, "client"):
        return self.client.api.logger
    else:
        return

def _log_message_metadata(method, args, kwargs) -> str:
    message = "Invoking "
    if "." in method.__qualname__:
        message += f"method "
    else:
        message += f"function "
    message += f"{method.__module__}.{method.__qualname__} "

    if args or kwargs:
        if args and not kwargs:
            message += f"with args {args}"
        if not args and kwargs:
            message += f"with kwargs {kwargs}"
        if args and kwargs:
            message += f"with args {args} and kwargs {kwargs}"
        return message
    return message

class ExtraMeta(type):
    def __new__(cls, future_class_name, future_class_parent, future_class_attr):
        for attr, v in future_class_attr.items():
            if callable(v) and not attr.startswith("_") and attr != "model":
                future_class_attr[attr] = cls.log_wrapper(attr, v)

        return super().__new__(cls, future_class_name, future_class_parent, future_class_attr)

    @staticmethod
    def log_wrapper(method_name, method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            logger = _extract_logger(self) if _extract_logger(self) else None
            if not logger:
                return method(self, *args, **kwargs)

            message = _log_message_metadata(method, args, kwargs)
            logger.info(message)
            logger.debug(method.__doc__) if method.__doc__ else None

            return method(self, *args, **kwargs)
        return wrapper



def container_dict(image, command=None, hostname=None, user=None, ports=None) -> dict:

    docker_config = dict(image = image)

    if hostname:
        docker_config['Hostname'] = hostname
    if user:
        docker_config['User'] = user
    if command:
        if isinstance(command, str):
            docker_config['Cmd'] = split(command)
        elif isinstance(command, list):
            docker_config['Cmd'] = command

    return docker_config
