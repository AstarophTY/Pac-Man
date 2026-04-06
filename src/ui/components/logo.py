from ursina import Entity, Sprite


class MenuLogo(Entity):
    def __init__(self, y: float = 0.32) -> None:
        super().__init__()

        logo_path = "assets/logo/pacman.png"

        Sprite(
            parent=self,
            texture=str(logo_path),
            y=y,
            z=-0.5,
            scale=(0.15, 0.15),
        )
