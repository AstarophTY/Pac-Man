from pydantic import BaseModel, Field, field_validator, ConfigDict

from ..logger import Logger


class LevelModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = Field(min_length=1)


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    highscore_filename: str = Field(min_length=1, default="highscore.json")
    level: list[LevelModel] = Field(default=[
        LevelModel(name="easy"),
        LevelModel(name="medium"),
        LevelModel(name="hard"),
    ])
    width: int = Field(gt=0, default=50)
    height: int = Field(gt=0, default=50)
    lives: int = Field(gt=0, default=3)
    pacgum: int = Field(gt=0, default=42)
    points_per_pacgum: int = Field(gt=0, default=10)
    points_per_super_pacgum: int = Field(gt=0, default=50)
    points_per_ghost: int = Field(gt=0, default=200)
    seed: int = Field(default=42)
    level_max_time: int = Field(gt=0, default=90)

    def __str__(self) -> str:
        return (
            "Config Object: {\n"
            f"\tHighscore filename: {self.highscore_filename}\n"
            f"\tLevel: {self.level}\n"
            f"\tWidth: {self.width}\n"
            f"\tHeight: {self.height}\n"
            f"\tLives: {self.lives}\n"
            f"\tPacgum: {self.pacgum}\n"
            f"\tPoints per Pacgum: {self.points_per_pacgum}\n"
            f"\tPoints per Super Pacgum: {self.points_per_super_pacgum}\n"
            f"\tPoints per Ghost: {self.points_per_ghost}\n"
            f"\tSeed: {self.seed}\n"
            f"\tLevel max time: {self.level_max_time}\n"
            "}\n"
        )

    @field_validator(
        "width", "height", "lives", "pacgum",
        "points_per_pacgum", "points_per_super_pacgum",
        "points_per_ghost", "level_max_time",
        mode="before"
    )
    @classmethod
    def _validate_positive(cls, v, info):
        field_name = info.field_name

        try:
            v = int(v)
        except Exception:
            Logger.warning(f"'{field_name}' invalid, using default")
            return cls.model_fields[field_name].default

        if v <= 0:
            Logger.warning(f"'{field_name}' must be > 0, using default")
            return cls.model_fields[field_name].default

        return v

    @field_validator("seed", mode="before")
    @classmethod
    def _seed_validator(cls, v):
        if v is None:
            Logger.warning("'seed' not provided, using default (42)")
            return 42

        try:
            return int(v)
        except Exception:
            Logger.warning("'seed' invalid, using default (42)")
            return 42

    @field_validator("level", mode="before")
    @classmethod
    def _validate_levels(cls, v):
        if not isinstance(v, list) or len(v) == 0:
            Logger.warning("'level' invalid, using default levels")
            return cls.model_fields["level"].default
        return v

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def _validate_string(cls, v):
        if not isinstance(v, str):
            Logger.warning("'highscore_filename' invalid, using default")
            return cls.model_fields["highscore_filename"].default
        return v
