from .color import Color
from sys import stderr
import os
from dotenv import load_dotenv


load_dotenv()


class Logger:
    LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "SUCCESS": 25,
        "WARNING": 30,
        "ERROR": 40,
        "NONE": 100
    }

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    @classmethod
    def _get_log_level(cls, level: str) -> bool:
        current = cls.LEVELS.get(cls.LOG_LEVEL, 20)
        target = cls.LEVELS.get(level, 20)
        return target >= current

    @classmethod
    def info(cls, message: str) -> None:
        if cls._get_log_level("INFO"):
            print(f"[{Color.BLUE}{Color.BOLD}INFO{Color.RESET}] {message}")

    @classmethod
    def success(cls, message: str) -> None:
        if cls._get_log_level("SUCCESS"):
            print(f"[{Color.GREEN}{Color.BOLD}SUCCESS{Color.RESET}] {message}")

    @classmethod
    def warning(cls, message: str) -> None:
        if cls._get_log_level("WARNING"):
            print(
                f"[{Color.YELLOW}{Color.BOLD}WARNING{Color.RESET}] {message}",
                file=stderr
            )

    @classmethod
    def error(cls, message: str) -> None:
        if cls._get_log_level("ERROR"):
            print(
                f"[{Color.RED}{Color.BOLD}ERROR{Color.RESET}] {message}",
                file=stderr
            )

    @classmethod
    def debug(cls, message: str) -> None:
        if cls._get_log_level("DEBUG"):
            print(
                f"[{Color.MAGENTA}{Color.BOLD}DEBUG{Color.RESET}] {message}",
                file=stderr
            )
