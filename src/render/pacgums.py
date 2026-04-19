from ursina import Entity, Vec3, color, scene
from random import shuffle

class Pacgums():
    def __init__(self, scale_maze, config, pacgums_zone):
        self.height = config.height
        self.width = config.width
        self.scale = scale_maze
        self.pacgums_zone = pacgums_zone
        self.nb_pacgum = config.pacgum
        self.pacgums = {
            "normal": [],
            "super": []
        }
        self.gen_super_pacgum(Vec3(0,0.25,0))
        self.gen_super_pacgum(Vec3(0,0.25,-self.height+1))
        self.gen_super_pacgum(Vec3(self.width-1,0.25,0))
        self.gen_super_pacgum(Vec3(self.width-1,0.25,-self.height+1))
        shuffle(self.pacgums_zone)
        for i in range(self.nb_pacgum):  
            pos = self.pacgums_zone[i]
            self.gen_pacgum((pos[0],0.15,pos[1]))
        

    
    def gen_super_pacgum(self, pos):
        super_pacgum = Entity(
            model="sphere",
            scale=2,
            position=pos*self.scale
        )
        if (pos[0], pos[2]) in self.pacgums_zone:
            self.pacgums_zone.remove((pos[0], pos[2]))
        self.pacgums.get('super').append(super_pacgum)
        
    def gen_pacgum(self, pos):
        pacgum = Entity(
            model="sphere",
            scale=1,
            add_to_scene_entities=False,
            collider=None,
            position=pos*self.scale
        )
        self.pacgums.get('normal').append(pacgum)
        
        
    
    
    