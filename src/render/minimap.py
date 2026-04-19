<<<<<<< HEAD
from ursina import color, Entity, camera, duplicate

class MiniMap():
    def __init__(self, walls, size, scale):
        self.minimap_walls = duplicate(walls)
        self.minimap_walls.parent = camera.ui
=======
from ursina import Entity, camera, color, duplicate


class MiniMap(Entity):
    def __init__(self, walls, size, scale, pacgums_all):
        super().__init__(parent=camera.ui)
        self.display_minimap(walls, scale)
        self.display_pacgums(pacgums_all.pacgums)

    def display_pacgum(self, model):
        pacgum = Entity(
            parent=self.minimap_walls,
            model='sphere',
            color=color.white,
            scale=(1, 0, 1),
            position=model.position
        )

    def display_super_pacgums(self, model):
        super = Entity(
            parent=self.minimap_walls,
            model='sphere',
            color=color.white,
            scale=(2, 0, 2),
            position=model.position
        )
            
    
    def display_pacgums(self, dict):
        for gum in dict.get("normal"):
            self.display_pacgum(gum)
        for super in dict.get("super"):
            self.display_super_pacgums(super)

    def display_minimap(self, walls, scale):
        self.minimap_walls = duplicate(walls)
        self.minimap_walls.parent = self
        self._panel_center_x = 0.7
        self._panel_center_y = 0.3

>>>>>>> 4da2e00 (pacgums display, map and 3d + pacman inb the map)
        min_bound, max_bound = self.minimap_walls.getTightBounds()
        model_size = max_bound - min_bound
        center_x = (max_bound.x + min_bound.x) / 2
        center_z = (max_bound.z + min_bound.z) / 2
        
        max_dim = max(model_size.x, model_size.z)
        scale_factor = scale / max_dim
        
        self.minimap_walls.scale = (scale_factor, 0.1, scale_factor)
        
        self.minimap_walls.texture = None
<<<<<<< HEAD
        self.minimap_walls.color = color.black
=======
        self.minimap_walls.color = color.rgb(0.729, 0.980, 1.000)
>>>>>>> 4da2e00 (pacgums display, map and 3d + pacman inb the map)
        self.minimap_walls.collider = None
        self.minimap_walls.rotation_x = -90


        self.minimap_walls.position = (
            0.7 - (center_x * scale_factor),
            0.3 - (center_z * scale_factor),
            -0.1
        )

        bg_width = model_size.x * scale_factor
        bg_height = model_size.z * scale_factor
<<<<<<< HEAD
=======
 
 
        frame_h = bg_height + 0.08
        inner_w = bg_width + 0.04
        inner_h = bg_height + 0.04

        Entity(
            parent=self,
            model='quad',
            color=color.rgba(0.020, 0.031, 0.063, 0.74),
            scale=(inner_w, inner_h),
            position=(self._panel_center_x, self._panel_center_y),
            z=0.03,
        )

        Entity(
            parent=self,
            model='quad',
            color=color.rgba(0.322, 0.824, 1.000, 0.36),
            scale=(inner_w, 0.005),
            position=(
                self._panel_center_x,
                self._panel_center_y + (inner_h * 0.5) - 0.01,
            ),
            z=0.02,
        )
>>>>>>> 4da2e00 (pacgums display, map and 3d + pacman inb the map)

        self.bg = Entity(
            parent=camera.ui,
            model='quad',
<<<<<<< HEAD
            color=color.white,
=======
            color=color.rgba(0.071, 0.098, 0.169, 0.84),
>>>>>>> 4da2e00 (pacgums display, map and 3d + pacman inb the map)
            scale=(bg_width, bg_height),
            position=(0.7, 0.3),
            z=0
        )
<<<<<<< HEAD
    
=======

        self._title = Entity(
            parent=self,
            model='quad',
            color=color.rgba(0.110, 0.161, 0.251, 0.82),
            scale=(bg_width * 0.56, 0.03),
            position=(
                self._panel_center_x,
                self._panel_center_y + (frame_h / 2) + 0.022,
            ),
            z=0.03,
        )

>>>>>>> 4da2e00 (pacgums display, map and 3d + pacman inb the map)
    def get_ui_map(self):
        return self.minimap_walls