from ursina import (
    Entity,
    Ursina,
    camera,
    color as colors,
    destroy,
    window,
)

from ...logger import Logger
from ..components import MenuButton, MenuLogo, PacmanBackground, VHSEffect


def run_main_menu() -> None:
    app = Ursina(
        borderless=False,
        title="Pac-Man",
        color=colors.rgb(0.110, 0.133, 0.227),
    )

    window.exit_button.visible = False
    window.fps_counter.enabled = False

    _build_menu_ui(app)
    app.run()


def _build_menu_ui(app: Ursina) -> None:
    PacmanBackground()
    _build_retro_frame()
    MenuLogo(y=0.255)
    VHSEffect(intensity=0.50)

    def _play() -> None:
        Logger.debug("Start game clicked from main menu")

    def _highscores() -> None:
        Logger.debug("High scores clicked from main menu")

    def _instructions() -> None:
        Logger.debug("Instructions clicked from main menu")

    def _quit() -> None:
        Logger.debug("Exit clicked from main menu")
        destroy(camera.ui)
        app.userExit()

    MenuButton(text="START GAME", on_click=_play, y=0.025)
    MenuButton(text="VIEW HIGH SCORES", on_click=_highscores, y=-0.085)
    MenuButton(text="INSTRUCTIONS", on_click=_instructions, y=-0.195)
    MenuButton(text="EXIT", on_click=_quit, y=-0.305)


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
    run_main_menu()
