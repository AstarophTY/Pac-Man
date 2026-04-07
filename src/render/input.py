from ursina import application, Entity, time, held_keys

class InputHandler(Entity):
    def __init__(self, player):
        super().__init__()
        player.speed = 10
        player.gravity = 0
        self.player = player
    
    def input(self, key):
        if key == 'escape':
            application.quit()
    
    def update(self):
        speed = 10
        if held_keys['c']:
            self.player.y += speed * time.dt
        if held_keys['v']:
            self.player.y -= speed * time.dt