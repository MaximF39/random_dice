import logging
import os

import colorlog
from config import Config

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
logger = logging.getLogger()
console_handler = logging.StreamHandler()

log_dir = os.path.dirname(Config.path_log)
os.makedirs(log_dir, exist_ok=True)

file_handler = logging.FileHandler(Config.path_log, mode="w")

logger.setLevel(logging.DEBUG)

console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
