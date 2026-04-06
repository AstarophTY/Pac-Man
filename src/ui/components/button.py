from collections.abc import Callable

from ursina import Button, Entity, Text, color as colors, invoke
from ursina.curve import linear


class MenuButton(Button):
    def __init__(
        self,
        text: str,
        on_click: Callable[[], None],
        y: float,
        width: float = 0.38,
        height: float = 0.080,
    ) -> None:
        self._base_width = width
        self._base_height = height
        self._aspect_compensation = width / max(height, 0.001)
        self._hover_width = width * 1.03
        self._hover_height = height * 1.03
        self._font_path = "assets/fonts/PressStart2P-vaV7.ttf"

        self._base_text_color = colors.rgb(1.000, 0.961, 0.620)
        self._hover_text_color = colors.rgb(0.729, 0.980, 1.000)
        self._base_color = colors.rgb(0.071, 0.098, 0.169)
        self._hover_color = colors.rgb(0.110, 0.161, 0.251)
        self._pressed_color = colors.rgb(0.051, 0.078, 0.141)
        self._base_frame_color = colors.rgb(0.290, 0.545, 0.800)
        self._hover_frame_color = colors.rgb(0.420, 0.725, 1.000)

        self._base_z = 0.0
        self._pressed_z = 0.012
        self._base_y = y
        self._pressed_y = y - 0.008

        super().__init__(
            text=text,
            y=y,
            scale=(width, height),
            color=self._base_color,
            highlight_color=self._hover_color,
            pressed_color=self._pressed_color,
            text_color=self._base_text_color,
            model="quad",
            on_click=self._handle_click,
        )

        self._on_click_callback = on_click
        self._is_pressed = False

        self.model = "quad"

        self.text_entity.font = self._font_path
        self.text_entity.color = self._base_text_color
        self.text_entity.origin = (0, 0)
        self.text_entity.x = 0
        self.text_entity.y = 0.002
        self.text_entity.scale = (1.85, 1.85 * self._aspect_compensation)
        self.text_entity.z = -0.1

        self._frame = Entity(
            parent=self,
            model="quad",
            x=0, y=0, z=0.03,
            scale=(1.04, 1.16),
            color=self._base_frame_color,
            ignore=True,
        )

        self._depth = Entity(
            parent=self,
            model="quad",
            x=0, y=-0.065, z=0.015,
            scale=(0.98, 0.16),
            color=colors.rgb(0.027, 0.039, 0.063),
            ignore=True,
        )

        self._scanlines: list[Entity] = []
        num_lines = 6
        for i in range(num_lines):
            ypos = -0.38 + i * (0.76 / (num_lines - 1))
            line = Entity(
                parent=self,
                model="quad",
                x=0,
                y=ypos,
                z=-0.02,
                scale=(0.96, 0.045),
                color=colors.rgba(0, 0, 0, 0.12),
                ignore=True,
            )
            self._scanlines.append(line)

        self._top_glow = Entity(
            parent=self,
            model="quad",
            x=0, y=0.28, z=0.02,
            scale=(0.72, 0.10),
            color=colors.rgba(0.729, 0.980, 1.000, 0.18),
            ignore=True,
        )

        self._indicator = Text(
            parent=self,
            text=">>",
            x=-0.42, y=0, z=-0.05,
            origin=(0, 0),
            font=self._font_path,
            scale=(0.85, 0.85 * self._aspect_compensation),
            color=self._hover_text_color,
            enabled=False,
            ignore=True,
        )

    def _handle_click(self) -> None:
        if self._is_pressed:
            return
        self._is_pressed = True
        self._animate_press()

    def _animate_press(self) -> None:
        self.animate_y(self._pressed_y, duration=0.07, curve=linear)
        self.animate_z(self._pressed_z, duration=0.07, curve=linear)
        self._depth.animate_color(
            colors.rgb(0.020, 0.027, 0.047), duration=0.07)
        invoke(self._animate_release, delay=0.13)

    def _animate_release(self) -> None:
        self.animate_y(self._base_y, duration=0.10, curve=linear)
        self.animate_z(self._base_z, duration=0.10, curve=linear)
        self._depth.animate_color(
            colors.rgb(0.027, 0.039, 0.063), duration=0.10)
        invoke(self._finish_press, delay=0.12)

    def _finish_press(self) -> None:
        self._is_pressed = False
        self._on_click_callback()

    def on_mouse_enter(self) -> None:
        self.text_entity.color = self._hover_text_color
        self.color = self._hover_color
        self._frame.color = self._hover_frame_color
        self.scale = (self._hover_width, self._hover_height)
        self._indicator.enabled = True

    def on_mouse_exit(self) -> None:
        self.text_entity.color = self._base_text_color
        self.color = self._base_color
        self._frame.color = self._base_frame_color
        self.scale = (self._base_width, self._base_height)
        self._indicator.enabled = False
