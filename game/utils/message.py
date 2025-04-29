import logging
from dataclasses import dataclass

from utils.logger import logger


@dataclass
class Message:
    level: int
    msg: str

    def print(self):
        logger.log(self.level, self.msg)


class MessageLevel:
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
