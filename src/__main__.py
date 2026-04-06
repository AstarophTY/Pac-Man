from sys import argv
from pathlib import Path

from .logger import Logger
from .parsing import ConfigLoader


def _get_path() -> Path:
    if len(argv) > 2:
        Logger.warning("Too many arguments provided. Using the first one.")

    try:
        path = Path(argv[1])
    except Exception as e:
        Logger.warning(f"Invalid path provided: {Logger.remove_errno(str(e))}")

    return path


def main() -> None:
    if len(argv) > 2:
        Logger.warning("Too many arguments provided. Using the first one.")
    elif len(argv) < 2:
        Logger.warning("No argument provided.")
        file = ""
    else:
        file = argv[1]

    if len(file) > 0:
        Logger.info(f"Path provided: {file}")

    try:
        config = ConfigLoader.load_config(str(file))
    except Exception as e:
        Logger.error(f"Error loading config: {e}")
        return

    Logger.debug(str(config))


if __name__ == "__main__":
    main()
