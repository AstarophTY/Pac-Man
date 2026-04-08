from ursina import color, Entity, camera, duplicate

class MiniMap():
    def __init__(self, walls, size, scale):
        self.minimap_walls = duplicate(walls)
        self.minimap_walls.parent = camera.ui
        min_bound, max_bound = self.minimap_walls.getTightBounds()
        model_size = max_bound - min_bound
        center_x = (max_bound.x + min_bound.x) / 2
        center_z = (max_bound.z + min_bound.z) / 2
        
        max_dim = max(model_size.x, model_size.z)
        scale_factor = scale / max_dim
        
        self.minimap_walls.scale = (scale_factor, 0.1, scale_factor)
        
        self.minimap_walls.texture = None
        self.minimap_walls.color = color.black
        self.minimap_walls.collider = None
        self.minimap_walls.rotation_x = -90


        self.minimap_walls.position = (
            0.7 - (center_x * scale_factor),
            0.3 - (center_z * scale_factor),
            -0.1
        )

        bg_width = model_size.x * scale_factor
        bg_height = model_size.z * scale_factor

        self.bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.white,
            scale=(bg_width, bg_height),
            position=(0.7, 0.3),
            z=0
        )
    
    def get_ui_map(self):
        return self.minimap_walls