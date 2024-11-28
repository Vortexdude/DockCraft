import logging
from functools import wraps
from shlex import split


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
            try:
                logger = self.logger
            except AttributeError:
                logger = self.client.api.logger

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
