from ursina import color, Entity, camera, duplicate

class MiniMap():
    def __init__(self, walls, size):
        self.size = size
        self.bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.red,
            scale=(size[0]*0.02, size[1]*0.02),
            position=(0.7, 0.3),
        )
         
        self.minimap_walls = duplicate(walls)
        self.minimap_walls.parent = self.bg
        self.minimap_walls.texture = None
        self.minimap_walls.color = color.black
        self.minimap_walls.collider = None
        self.minimap_walls.scale = (0.02, 0.01, 0.02)
        self.minimap_walls.position = (-0.5, 0.4, -0.1) 
        self.minimap_walls.rotation_x = -90