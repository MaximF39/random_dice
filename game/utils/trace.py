import inspect
import os
from datetime import datetime

from loguru import logger

# ANSI коды цветов
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"  # Сброс цвета

# Настраиваем логгер
logger.remove()
logger.add(lambda msg: print(msg, end=""), format="{message}", level="DEBUG")


def trace(msg=""):
    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)
    args, _, _, values = inspect.getargvalues(frame)

    timestamp = datetime.now().strftime("%H:%M:%S")
    file_name = os.path.basename(info.filename)  # Только имя файла
    function_name = frame.f_code.co_name  # Название функции
    class_name = None

    # Проверяем, вызывается ли функция в методе класса
    if "self" in values:
        class_name = values["self"].__class__.__name__
    elif "cls" in values:
        class_name = values["cls"].__name__

    args_str = ", ".join(f"{arg}={values[arg]}" for arg in args if arg not in ("self", "cls"))

    # Форматируем лог с ANSI цветами
    log_msg = (
        f"{COLOR_CYAN}{timestamp}{COLOR_RESET} | "
        f"{COLOR_YELLOW}DEBUG{COLOR_RESET} | "
        f"{COLOR_GREEN}{file_name}{COLOR_RESET}, "
        f"{COLOR_BLUE}{(class_name + '.' if class_name else '') + function_name}{COLOR_RESET}, "
        f"{COLOR_MAGENTA}Args: {args_str}{COLOR_RESET}, "
        f"{COLOR_RED}Line: {info.lineno}{COLOR_RESET}, "
        f"{COLOR_CYAN}Msg: {msg}{COLOR_RESET}"
    )

    logger.debug(log_msg)
