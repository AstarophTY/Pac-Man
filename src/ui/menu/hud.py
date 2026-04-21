from ursina import Entity, Text, Ursina, Vec2, camera, color, time
from ..components.vhs_effect import VHSEffect


def _fmt_time(total_seconds: float) -> str:
    safe = max(0, int(total_seconds))
    minutes = safe // 60
    seconds = safe % 60
    return f"{minutes:02d}:{seconds:02d}"


class HUDTemplate(Entity):
    def __init__(
        self,
        lives: int = 3,
        battery: float = 100.0,
        level: int = 1,
        remaining_time: float = 120.0,
        countdown: bool = True,
        recording: bool = True,
    ):
        super().__init__(parent=camera.ui)
        self.lives = max(0, int(lives))
        self.battery = max(0.0, min(100.0, float(battery)))
        self.level = max(1, int(level))
        self.remaining_time = max(0.0, float(remaining_time))
        self.countdown = countdown
        self.recording = recording

        font_path = "assets/fonts/PressStart2P-vaV7.ttf"

        self.rec_text = Text(
            parent=self,
            text="",
            position=Vec2(-0.86, 0.46),
            color=color.white,
            scale=1.0,
            font=font_path,
        )
        self.time_text = Text(
            parent=self,
            text="",
            position=Vec2(0.48, 0.46),
            color=color.white,
            scale=1.0,
            font=font_path,
        )
        self.lives_text = Text(
            parent=self,
            text="",
            position=Vec2(-0.86, -0.45),
            color=color.white,
            scale=1.0,
            font=font_path,
        )
        self.level_text = Text(
            parent=self,
            text="",
            position=Vec2(0.70, -0.45),
            color=color.white,
            scale=1.0,
            font=font_path,
        )

        VHSEffect(0.5)

        self.refresh()

    def refresh(self):
        rec_prefix = "TIME" if self.recording else "OVER"
        self.rec_text.text = f"{rec_prefix} {_fmt_time(self.remaining_time)}"
        self.lives_text.text = f"HEALTH {'♥' * self.lives}"
        self.level_text.text = f"LVL {self.level:02d}"

    def set_lives(self, value: int):
        self.lives = max(0, int(value))
        self.refresh()

    def lose_life(self):
        self.set_lives(self.lives - 1)

    def set_level(self, value: int):
        self.level = max(1, int(value))
        self.refresh()

    def set_battery(self, value: float):
        self.battery = max(0.0, min(100.0, float(value)))
        self.refresh()

    def add_battery(self, value: float):
        self.set_battery(self.battery + float(value))

    def set_remaining_time(self, value: float):
        self.remaining_time = max(0.0, float(value))
        self.refresh()

    def add_time(self, value: float):
        self.set_remaining_time(self.remaining_time + float(value))

    def set_recording(self, value: bool):
        self.recording = bool(value)
        self.refresh()

    def update_hud(
        self,
        lives: int | None = None,
        battery: float | None = None,
        level: int | None = None,
        remaining_time: float | None = None,
        rec_time: float | None = None,
        recording: bool | None = None,
    ):
        if lives is not None:
            self.lives = max(0, int(lives))
        if battery is not None:
            self.battery = max(0.0, min(100.0, float(battery)))
        if level is not None:
            self.level = max(1, int(level))
        if remaining_time is not None:
            self.remaining_time = max(0.0, float(remaining_time))
        if recording is not None:
            self.recording = bool(recording)
        self.refresh()

    def update(self):
        if self.countdown and self.remaining_time > 0:
            self.remaining_time = max(0.0, self.remaining_time - time.dt)
        self.refresh()


class _HUDTester(Entity):
    def __init__(self, hud: HUDTemplate):
        super().__init__()
        self.hud = hud

    def input(self, key):
        if key == 'l':
            self.hud.lose_life()
        elif key == 'k':
            self.hud.set_lives(self.hud.lives + 1)
        elif key == 'n':
            self.hud.set_level(self.hud.level + 1)
        elif key == 'm':
            self.hud.set_level(self.hud.level - 1)
        elif key == 'b':
            self.hud.add_battery(-10)
        elif key == 'g':
            self.hud.add_battery(10)
        elif key == 't':
            self.hud.add_time(15)
        elif key == 'y':
            self.hud.add_time(-15)
        elif key == 'f':
            self.hud.set_recording(not self.hud.recording)
        elif key == 'r':
            self.hud.update_hud(
                lives=3,
                battery=100,
                level=1,
                remaining_time=120,
                recording=True,
            )


def main():
    app = Ursina()
    hud = HUDTemplate(
        lives=3,
        battery=100,
        level=1,
        remaining_time=120,
        countdown=True,
        recording=True,
    )
    _HUDTester(hud)
    app.run()


if __name__ == "__main__":
    main()
