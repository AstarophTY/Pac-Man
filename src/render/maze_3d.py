from ursina import Entity, color, scene


class Maze_3d():
    def __init__(self, maze, scale):
        self.maze = maze
        self.scale = scale
        self.walls_entity = []
        self.walls = Entity(parent=scene)
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                self.create_walls(x, y)
        self.walls.combine()
        self.walls.texture = "assets/textures/wall.jpg"
        self.gen_floor(((x/2)*scale,0,(-y/2)*scale),((x+1)*scale,1,(-y-1)*scale))        

    def get_walls(self, val: int) -> None:
        bits = f"{int(val):04b}"
        return {
            "NORTH": bits[3] == '1',
            "EAST": bits[2] == '1',
            "SOUTH": bits[1] == '1',
            "WEST": bits[0] == '1',
            "NB": val
        }

    def gen_floor(self, position, scale):
        floor_texture_path = "assets/textures/floor.jpg"
        return Entity(model='cube',
                position=position,
                scale=scale,
                collider='box',
                texture=str(floor_texture_path),
                texture_scale = (5, 5)
                )

    def gen_wall(self, position, scale):
        wall_texture_path = "assets/textures/wall.jpg"
        
        # Separate invisible box collider for stable collision
        Entity(model=None,
               position=(position[0]*self.scale, position[1], position[2]*self.scale),
               scale=scale*self.scale,
               collider='box',
               visible=False)

        return Entity(model='cube',
                      position=(position[0]*self.scale, position[1], position[2]*self.scale),
                      color=color.gray,
                      scale=scale*self.scale,
                      texture=str(wall_texture_path),
                      parent=self.walls)


    def create_walls(self, x, y):
        y = -y
        walls = self.get_walls(self.maze[-y][x])
        pos = [model.position for model in self.walls_entity]
        if walls.get('NB') == 15:
            Entity(
                model='cube',
                position=(x*self.scale, 2, y*self.scale),
                color=color.gray,
                scale=(0.8*self.scale, 1*self.scale, 0.8*self.scale)
            )
        if walls.get('NORTH') is True and not (x*self.scale, 2, (y+0.5)*self.scale) in pos:
            self.walls_entity.append(
                self.gen_wall((x, 2, (y+0.5)),(1.2, 1, 0.2))
            )
        if walls.get('SOUTH') is True and not (x*self.scale, 2, (y-0.5)*self.scale) in pos:
            self.walls_entity.append(
                self.gen_wall(
                    (x, 2, (y-0.5)),
                    (1.2, 1, 0.2)
                )
            )
        if walls.get('EAST') is True and not ((x+0.5)*self.scale, 2, y*self.scale) in pos:
            self.walls_entity.append(
                self.gen_wall(
                    ((x+0.5), 2, y),
                    (0.2, 1, 1.2)
                )
            )
        if walls.get('WEST') is True and not ((x-0.5)*self.scale, 2, y*self.scale) in pos:
            self.walls_entity.append(
                self.gen_wall(
                    ((x-0.5), 2, y),
                    (0.2, 1, 1.2)
                )
            )