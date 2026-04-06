from collections.abc import Callable

from ursina import Button, color


class MenuButton(Button):
    def __init__(
        self,
        text: str,
        on_click: Callable[[], None],
        y: float,
        width: float = 0.42,
        height: float = 0.09,
    ) -> None:
        self._base_width = width
        self._base_height = height
        self._font_path = "assets/fonts/PressStart2P-vaV7.ttf"

        super().__init__(
            text=text,
            y=y,
            scale=(width, height),
            color=color.rgb(0.23, 0.23, 0.30),
            highlight_color=color.rgb(0.45, 0.45, 0.60),
            pressed_color=color.rgb(0.10, 0.10, 0.15),
            text_color=color.rgb(1.0, 0.87, 0.0),
            radius=3,
            model="quad",
            shadow=(0.01, -0.01),
            on_click=on_click,
        )

        self.font_normal = self._font_path
        self.font_hover = self._font_path
        self.font_pressed = self._font_path

        self.text_entity.font = self.font_normal
        self.text_entity.color = color.rgb(1.0, 0.87, 0.0)

    def on_mouse_enter(self) -> None:
        self.text_entity.font = self.font_hover
        self.scale = (self.scale_x * 1.02, self.scale_y * 1.02)

    def on_mouse_exit(self) -> None:
        self.text_entity.font = self.font_normal
        self.scale = (self._base_width, self._base_height)
