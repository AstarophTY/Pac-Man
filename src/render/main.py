from mazegenerator import MazeGenerator
from ursina import Ursina, Sky, mouse, DirectionalLight, AmbientLight, Vec3, color, Entity
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import BoxCollider, Vec3
from .maze_3d import Maze_3d
from .input import InputHandler
from .minimap import MiniMap

def run_main_maze():
    size = (15, 20)
    maze_gen = MazeGenerator(
        size=size,
        perfect=False
    )
    maze = maze_gen.maze
    app = Ursina()
    
    Sky()
    mouse.locked = True

    player = FirstPersonController()
    player.collider = BoxCollider(player, center=Vec3(0, 1, 0), size=Vec3(0.5, 2, 0.5))
    

    DirectionalLight().look_at(Vec3(1, -1, -1))
    AmbientLight(color=color.rgba32(100, 100, 100, 255))

    scale_maze = 4
    maze_3d = Maze_3d(maze, scale_maze)
    mini_map = MiniMap(maze_3d.walls, size, 0.4)
    InputHandler(player, mini_map.get_ui_map())
    app.run()



