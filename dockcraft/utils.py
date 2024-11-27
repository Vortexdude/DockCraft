from functools import wraps
import logging

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

    custom_format = "%(logger_namespace)s %(asctime)s %(levelname)6s %(filename)10s:%(lineno)s - %(message)s"
    time_format = "%d/%m/%Y %H:%M:%S"

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


def logging_dec(level="debug"):
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            try:
                self.logger = self.logger
            except AttributeError:
                self.logger = self.client.api.logger

            # self.logger = self.client.api.logger.debug("from the api itself")

            if level == "debug":
                self.logger.debug(f"Invoking function '{function.__name__}' with args {kwargs}")
                if function.__doc__:
                    self.logger.debug(function.__doc__)

            elif level == "info":
                self.logger.info(f"Invoking function '{function.__name__}' with args {kwargs}")
                if function.__doc__:
                    self.logger.info(function.__doc__)

            elif level == "warning":
                self.logger.warning(f"Invoking function '{function.__name__}' with args {kwargs}")
                if function.__doc__:
                    self.logger.warning(function.__doc__)

            result = function(self, *args, **kwargs)
            return result
        return wrapper
    return decorator
