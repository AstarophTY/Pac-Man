from typing import Callable
from ursina import Entity, Text, camera, color, mouse, window

from ..components.button import MenuButton


class CheatsMenu:
    def __init__(self):
        self._cheats = []
        self.panel = None
        self.scroll_area = None
        self.content = None
        self.scroll_offset = 0.0
        self.content_height = 0.0
        self.visible_height = 0.0
        self._button_height = 0.0
        self._row_spacing = 0.0

    def add_button(self, on_click: Callable[[], None], label: str):
        self._cheats.append(MenuButton(text=label, on_click=on_click, y=0.2))

    def display_cheats(self):
        if self.panel:
            self.panel.disable()

        aspect = max(window.aspect_ratio, 1.0)
        panel_width = min(1.15, max(0.62, 0.42 * aspect))
        panel_height = 0.86
        button_width = 0.62
        button_height = 0.15
        row_spacing = 0.20
        self._button_height = button_height
        self._row_spacing = row_spacing

        self.panel = Entity(
            parent=camera.ui,
            model='quad',
            color=color.black66,
            scale=(panel_width, panel_height),
            enabled=True,
            collider='box',
        )

        Text(
            "Cheat",
            parent=self.panel,
            y=0.36,
            scale=1.8,
            origin=(0, 0),
        )

        self.scroll_area = Entity(
            parent=self.panel,
            y=0.14,
            scale=(0.94, 0.72),
            collider='box',
        )
        self.content = Entity(parent=self.scroll_area)

        for i, button in enumerate(self._cheats):
            button.parent = self.content
            button.y = -i * row_spacing
            button.scale = (button_width, button_height)

            if hasattr(button, "_base_y"):
                button._base_y = button.y
                button._pressed_y = button.y - 0.008
            if hasattr(button, "_base_width"):
                button._base_width = button_width
                button._base_height = button_height
                button._hover_width = button_width * 1.03
                button._hover_height = button_height * 1.03

        self.scroll_offset = 0
        if self._cheats:
            self.content_height = (
                (len(self._cheats) - 1) * row_spacing
                + button_height
            )
        else:
            self.content_height = 0
        self.visible_height = self.scroll_area.scale_y
        self._update_buttons_visibility()

        self.panel.input = self.handle_scroll

    def _update_buttons_visibility(self) -> None:
        if not self.scroll_area or not self.content:
            return

        half_visible_height = self.scroll_area.scale_y / 2
        half_button_height = self._button_height / 2

        for button in self._cheats:
            local_y = self.content.y + button.y
            is_visible = (
                -half_visible_height - half_button_height
                <= local_y
                <= half_visible_height + half_button_height
            )
            button.visible = is_visible
            button.enabled = is_visible

    def handle_scroll(self, key):
        hovered = mouse.hovered_entity
        is_menu_hovered = False
        while hovered is not None:
            if hovered in [self.panel, self.scroll_area, self.content]:
                is_menu_hovered = True
                break
            hovered = hovered.parent

        is_button_hovered = any(
            mouse.hovered_entity == btn for btn in self._cheats
        )
        if is_menu_hovered or is_button_hovered:
            max_scroll = max(
                0,
                self.content_height - self.visible_height,
            )

            if key == 'scroll up':
                self.scroll_offset = max(0, self.scroll_offset - 0.1)
                self.content.y = self.scroll_offset
                self._update_buttons_visibility()
            elif key == 'scroll down':
                self.scroll_offset = min(max_scroll, self.scroll_offset + 0.1)
                self.content.y = self.scroll_offset
                self._update_buttons_visibility()


if __name__ == "__main__":
    from ursina import Ursina
    app = Ursina()
    cheats = CheatsMenu()
    cheats.add_button(on_click=lambda: print("test"), label="Salut1")
    cheats.add_button(on_click=lambda: print("test"), label="Salut2")
    cheats.add_button(on_click=lambda: print("test"), label="Salut3")
    cheats.add_button(on_click=lambda: print("test"), label="Salut4")
    cheats.add_button(on_click=lambda: print("test"), label="Salut5")
    cheats.add_button(on_click=lambda: print("test"), label="Salut6")
    cheats.add_button(on_click=lambda: print("test"), label="Salut7")
    cheats.add_button(on_click=lambda: print("test"), label="Salut8")
    cheats.add_button(on_click=lambda: print("test"), label="Salut9")
    cheats.add_button(on_click=lambda: print("test"), label="Salut10")
    cheats.add_button(on_click=lambda: print("test"), label="Salut11")
    cheats.add_button(on_click=lambda: print("test"), label="Salut12")
    cheats.display_cheats()
    app.run()
