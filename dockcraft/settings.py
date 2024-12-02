import os, sys
from utils import CustomLogger, banner
from dotenv import load_dotenv

load_dotenv()

project_home_path = os.path.dirname(os.path.realpath(sys.argv[0]))
log_level = os.environ.get("LOG_LEVEL", "warning")

if log_level == "debug":
    from rich.traceback import install
    install()

project_name = os.environ.get("PROJECT_NAME", "dockercraft")

logger_init = CustomLogger(log_level, os.path.basename(project_name))
logger = logger_init.get_logger()

print(banner)
logger.debug("logger initialize")
logger.debug(f"{project_name=}")
