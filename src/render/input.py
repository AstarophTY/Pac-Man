from ursina import application, Entity, time, held_keys, color, mouse


class InputHandler(Entity):
    def __init__(self, player, ui_map, pacgums):
        super().__init__()
        player.speed = 10
        player.gravity = 0
        self.player = player
        self.pacgums = pacgums.pacgums
        self.point = Entity(
            parent=ui_map,
            model='pacman.obj',
            color=color.yellow,
            scale=(0.125, 0, 0.125),
            position=(0, 1, 0),
            rotation_y=90
        )

    def input(self, key):
        if key == 'escape':
            application.quit()

    def update(self):
        speed = 10
        self.point.rotation_y += mouse.velocity[0] * 40

        if held_keys['c']:
            self.player.y += speed * time.dt
        if held_keys['v']:
            self.player.y -= speed * time.dt

        self.point.x = self.player.x
        self.point.z = self.player.z
