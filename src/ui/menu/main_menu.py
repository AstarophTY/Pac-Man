from ursina import Ursina, camera, color, destroy, window

from ...logger import Logger
from ..components import MenuButton, MenuLogo, PacmanBackground


def run_main_menu() -> None:
    app = Ursina(
        borderless=False,
        title="Pac-Man",
        color=color.rgb(20, 23, 40),
    )

    window.exit_button.visible = False
    window.fps_counter.enabled = False

    _build_menu_ui(app)
    app.run()


def _build_menu_ui(app: Ursina) -> None:
    PacmanBackground()
    MenuLogo(y=2.0)

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

    MenuButton(text="START GAME", on_click=_play, y=0.05)
    MenuButton(text="VIEW HIGH SCORES", on_click=_highscores, y=-0.07)
    MenuButton(text="INSTRUCTIONS", on_click=_instructions, y=-0.19)
    MenuButton(text="EXIT", on_click=_quit, y=-0.31)


if __name__ == "__main__":
    run_main_menu()
