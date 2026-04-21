from ursina import application, Entity, time, held_keys, color, mouse


class InputHandler(Entity):
    def __init__(self, player, minimap, pacgums):
        super().__init__()
        player.speed = 10
        player.gravity = 0
        self.minimap = minimap
        self.player = player
        self.pacgums = pacgums.pacgums
        self.point = Entity(
            parent=minimap.get_ui_map(),
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

        for gum in self.pacgums.get('normal'):
            gum_pos = gum.model.position
            if (self.player.x <= gum_pos.x + 1 and
               self.player.x >= gum_pos.x - 1 and
               self.player.z <= gum_pos.z + 1 and
               self.player.z >= gum_pos.z - 1):
                gum.hide()

        for gum in self.pacgums.get('super'):
            gum_pos = gum.model.position
            if (self.player.x <= gum_pos.x + 2 and
               self.player.x >= gum_pos.x - 2 and
               self.player.z <= gum_pos.z + 2 and
               self.player.z >= gum_pos.z - 2):
                gum.hide()

        self.point.x = self.player.x
        self.point.z = self.player.z
