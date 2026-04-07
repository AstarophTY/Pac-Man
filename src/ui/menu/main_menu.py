from ursina import (
    Entity,
    Text,
    Ursina,
    camera,
    color as colors,
    destroy,
    window,
)

from ...logger import Logger
from ..components import MenuButton, MenuLogo, PacmanBackground, VHSEffect


def run_main_menu(highscore: list[dict[str, int | str]]) -> None:
    app = Ursina(
        borderless=False,
        title="Pac-Man",
        color=colors.rgb(0.110, 0.133, 0.227),
    )

    window.exit_button.visible = False
    window.fps_counter.enabled = False

    _build_menu_ui(app, highscore)
    app.run()


def _build_menu_ui(app: Ursina, highscore: list[dict[str, int | str]]) -> None:
    PacmanBackground()
    _build_retro_frame()
    MenuLogo(y=0.300)
    VHSEffect(intensity=0.50)

    menu_buttons: list[MenuButton] = []
    overlay_entities: list[Entity] = []

    font_path = "assets/fonts/PressStart2P-vaV7.ttf"

    def _clear_overlay() -> None:
        for entity in overlay_entities:
            destroy(entity)
        overlay_entities.clear()

        for button in menu_buttons:
            button.enabled = True
            button.visible = True

    def _show_overlay(title: str, rows: list[str]) -> None:
        _clear_overlay()
        for button in menu_buttons:
            button.enabled = False
            button.visible = False

        max_visible_rows = 7
        start_index = 0

        title_text = Text(
            parent=camera.ui,
            text=title,
            y=0.1,
            z=-0.10,
            origin=(0, 0),
            font=font_path,
            scale=1.15,
            color=colors.rgb(0.729, 0.980, 1.000),
        )
        overlay_entities.append(title_text)

        row_start_y = 0.05
        row_step_y = 0.05
        visible_row_entities: list[Text] = []

        if len(rows) > max_visible_rows:
            scroll_hint = Text(
                parent=camera.ui,
                text="SCROLL: WHEEL / UP / DOWN",
                y=-0.28,
                z=-0.10,
                origin=(0, 0),
                font=font_path,
                scale=0.45,
                color=colors.rgb(0.729, 0.980, 1.000),
            )
            overlay_entities.append(scroll_hint)

        def _refresh_visible_rows() -> None:
            for index, row_text in enumerate(visible_row_entities):
                row_index = start_index + index
                if row_index < len(rows):
                    row_text.text = rows[row_index]
                else:
                    row_text.text = ""

        rows_to_create = min(len(rows), max_visible_rows)
        for index in range(rows_to_create):
            row_text = Text(
                parent=camera.ui,
                text="",
                y=row_start_y - (index * row_step_y),
                z=-0.10,
                origin=(0, 0),
                font=font_path,
                scale=0.62,
                color=colors.rgb(1.000, 0.961, 0.620),
            )
            visible_row_entities.append(row_text)
            overlay_entities.append(row_text)

        _refresh_visible_rows()

        if len(rows) > max_visible_rows:
            class _OverlayScroller(Entity):
                def input(self, key: str) -> None:
                    nonlocal start_index

                    if key in ("scroll down", "down arrow"):
                        if start_index < len(rows) - max_visible_rows:
                            start_index += 1
                            _refresh_visible_rows()
                    elif key in ("scroll up", "up arrow"):
                        if start_index > 0:
                            start_index -= 1
                            _refresh_visible_rows()

            scroller = _OverlayScroller(parent=camera.ui)
            overlay_entities.append(scroller)

        back_button = MenuButton(
            text="BACK",
            on_click=_clear_overlay,
            y=-0.350,
        )
        back_button.z = -0.08
        overlay_entities.append(back_button)

    def _play() -> None:
        Logger.debug("Start game clicked from main menu")

    def _highscores() -> None:
        rows: list[str] = []
        try:
            sorted_scores = sorted(
                highscore,
                key=lambda item: int(item.get("score", 0)),
                reverse=True,
            )[:10]
            rows = [
                (
                    f"{index + 1}. "
                    f"{item.get('name', 'UNKNOWN')}  "
                    f"{item.get('score', 0)}"
                )
                for index, item in enumerate(sorted_scores)
            ]
        except Exception as error:
            Logger.warning(f"Failed to load highscores: {error}")

        if not rows:
            rows = ["No high score available."]

        _show_overlay("HIGH SCORES", rows)
        Logger.debug("High scores opened from main menu")

    def _instructions() -> None:
        _show_overlay(
            "INSTRUCTIONS",
            [
                "- Move with W, A, S, D",
                "- Eat pac-gums to score",
                "- Avoid ghosts",
                "- Grab power pellets",
                "- Clear level to win",
            ],
        )
        Logger.debug("Instructions opened from main menu")

    def _quit() -> None:
        Logger.debug("Exit clicked from main menu")
        destroy(camera.ui)
        app.userExit()

    menu_buttons.append(MenuButton(text="START GAME", on_click=_play, y=0.025))
    menu_buttons.append(
        MenuButton(
            text="VIEW HIGH SCORES",
            on_click=_highscores,
            y=-0.085,
        )
    )
    menu_buttons.append(
        MenuButton(
            text="INSTRUCTIONS",
            on_click=_instructions,
            y=-0.195,
        )
    )
    menu_buttons.append(MenuButton(text="EXIT", on_click=_quit, y=-0.305))


def _build_retro_frame() -> None:
    Entity(
        parent=camera.ui,
        model="quad",
        y=-0.10,
        z=0.04,
        scale=(0.78, 0.70),
        color=colors.rgba(0.051, 0.078, 0.141, 0.745),
    )

    Entity(
        parent=camera.ui,
        model="quad",
        y=-0.10,
        z=0.03,
        scale=(0.756, 0.676),
        color=colors.rgba(0.020, 0.031, 0.063, 0.608),
    )

    Entity(
        parent=camera.ui,
        model="quad",
        y=0.17,
        z=0.02,
        scale=(0.70, 0.008),
        color=colors.rgba(0.322, 0.824, 1.000, 0.569),
    )


if __name__ == "__main__":
    run_main_menu([
        {"name": "Player1", "score": 1000},
        {"name": "Player2", "score": 800},
        {"name": "Player3", "score": 600}
    ])
