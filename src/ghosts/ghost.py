from ursina import Entity, Vec3, color


class Ghost(Entity):
    def __init__(
        self,
        spawn_coords: tuple[int, int],
        tile_size: float = 1,
        ghost_color=color.red
    ):

        self.spawn_coords = spawn_coords
        self.tile_size = tile_size

        super().__init__(
            model="cube",
            color=ghost_color,
            scale=(1, 2, 1),
            position=self._grid_to_world(*spawn_coords),
            collider="box",
        )

        self.collider.trigger = True

    def _grid_to_world(self, x: int, y: int) -> Vec3:
        return Vec3(
            x * self.tile_size,
            1.2,
            -y * self.tile_size
        )

    def update(self):
        pass


class Blinky(Ghost):
    def __init__(self, spawn_coords: tuple[int, int], tile_size: float):
        super().__init__(
            spawn_coords,
            tile_size,
            ghost_color=color.red
        )
