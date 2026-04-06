from pydantic import ValidationError
import json
import re
from typing import Any

from ..logger import Logger
from .model import ConfigModel


class ConfigLoader:
    @staticmethod
    def _loadfile(file_path: str) -> Any:
        try:
            with open(file_path, "r") as f:
                content = f.read()
        except Exception as e:
            Logger.warning(Logger.remove_errno(str(e)))
            return {}

        content = re.sub(r"(\/\/.*|\/\*[\s\S]*?\*\/)", "", content)

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            Logger.warning(f"Error decoding JSON from {file_path}: {e}")
            return {}

    @staticmethod
    def load_config(file_path: str | None) -> ConfigModel:
        if file_path:
            content = ConfigLoader._loadfile(file_path)
        else:
            content = {}

        Logger.debug(f"Config loaded: {json.dumps(content, indent=2)}")

        try:
            return ConfigModel(**content)
        except ValidationError as etc:
            error = etc.errors()[0]
            Logger.warning(f"Invalid config: {error['msg']}")
            return ConfigModel()
