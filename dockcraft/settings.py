import os, sys
from dotenv import load_dotenv
import logging
from rich.logging import RichHandler

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


load_dotenv()

project_home_path = os.path.dirname(os.path.realpath(sys.argv[0]))
log_level = os.environ.get("LOG_LEVEL", "warning")

def is_debug():
    return log_level.lower() == "debug"


if is_debug():
    from rich.traceback import install
    install()

project_name = os.environ.get("PROJECT_NAME", "dockercraft")

FORMAT = "%(message)s"
logging.basicConfig(
    level=log_level.upper(), format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True, enable_link_path=True)]
)

logger = logging.getLogger("rich")

print(banner)
logger.info("\U0001F680 logger initialize")
logger.info(f"{project_name=}")
