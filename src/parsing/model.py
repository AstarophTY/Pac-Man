from pydantic import BaseModel, Field, ValidationError, model_serializer, field_validator, ConfigDict
from pathlib import Path


class LevelModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    highscore_filename: str = Field(min_length=1)
    level: list[LevelModel]
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seed: int
    level_max_time: int = Field(gt=0)

    def __str__(self):
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