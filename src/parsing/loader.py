from pydantic import ValidationError
import json
import re

from .errors import ParsingError
from ..logger import Logger
from .model import ConfigModel


class ConfigLoader:
    @staticmethod
    def _loadfile(file_path: str):
        with open(file_path, "r") as f:
            content = f.read()

        content = re.sub(r"//.*", "", content)

        return json.loads(content)



    @staticmethod
    def load_config(file_path: str) -> ConfigModel:
        content = ConfigLoader._loadfile(file_path)

        Logger.debug(f"Config loaded: {json.dumps(content, indent=2)}")

        try:
            return ConfigModel(**content)
        except ValidationError as etc:
            error = etc.errors()[0]
            raise ParsingError(f"Invalid config: {error['msg']}")
