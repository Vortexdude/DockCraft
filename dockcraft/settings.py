from utils import CustomLogger
import os

project_name = "dockcraft"

logger_init = CustomLogger("debug", os.path.basename(project_name))
logger = logger_init.get_logger()

logger.debug("logger initialize")
logger.debug(f"{project_name=}")