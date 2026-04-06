from sys import argv
from pathlib import Path

from .logger import Logger
from .parsing import ConfigLoader


def _get_path() -> Path:
    if len(argv) < 2:
        raise ValueError("No path provided")
    elif len(argv) > 2:
        raise ValueError("Too many arguments provided")

    try:
        path = Path(argv[1])
    except Exception as e:
        raise ValueError(f"Invalid path provided: {e}")

    if not path.exists():
        raise ValueError("Provided path does not exist")

    return path


def main():
    try:
        path = _get_path()
    except ValueError as e:
        Logger.error(e)
        return

    Logger.info(f"Path provided: {path}")

    try:
        config = ConfigLoader.load_config(path)
    except Exception as e:
        Logger.error(f"Error loading config: {e}")
        return

    Logger.debug(config)


if __name__ == "__main__":
    main()
