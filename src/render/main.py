from mazegenerator import MazeGenerator
from ursina import Ursina, Sky, mouse, DirectionalLight, AmbientLight, Vec3, color
from .maze_3d import Maze_3d
from .input import InputHandler
from .minimap import MiniMap
from .player_controller import PlayerController

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

    player = PlayerController(
        speed=10,
        collider_size=Vec3(0.34, 2, 0.34),
        eye_height=2.0,
        fov=90,
    )

    DirectionalLight().look_at(Vec3(1, -1, -1))
    AmbientLight(color=color.rgba32(100, 100, 100, 255))

    scale_maze = 4
    maze_3d = Maze_3d(maze, scale_maze)

    mini_map = MiniMap(maze_3d.walls, size, 0.4)
    InputHandler(player, mini_map.get_ui_map())
    app.run()



