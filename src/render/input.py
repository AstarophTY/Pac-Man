from ursina import application, Entity, time, held_keys,camera, color

class InputHandler(Entity):
    def __init__(self, player, ui_map):
        super().__init__()
        player.speed = 10
        player.gravity = 0
        self.player = player
        self.point = Entity(
            parent=ui_map,
            model='sphere',
            color=color.red,
            scale=(2, 0, 2),
            position=(0, 1, 0)
        )
    
    def input(self, key):
        if key == 'escape':
            application.quit()
    
    def update(self):
        speed = 10
        if held_keys['c']:
            self.player.y += speed * time.dt
        if held_keys['v']:
            self.player.y -= speed * time.dt

        self.point.x = self.player.x
        self.point.z = self.player.z
        