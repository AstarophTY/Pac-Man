from mazegenerator import MazeGenerator
from ursina import (Ursina, Sky, mouse, DirectionalLight,
                    AmbientLight, Vec3, color)
from .maze_3d import Maze_3d
from .input import InputHandler
from .minimap import MiniMap
from .player_controller import PlayerController
from .pacgums import Pacgums_Manager


def run_main_maze(config):
    size = (config.width, config.height)
    maze_gen = MazeGenerator(
        size=size,
        perfect=False,
        seed=config.seed
    )
    maze = maze_gen.maze
    app = Ursina()

    Sky()
    mouse.locked = True

    DirectionalLight().look_at(Vec3(1, -1, -1))
    AmbientLight(color=color.rgba32(100, 100, 100, 255))

    scale_maze = 4
    maze_3d = Maze_3d(maze, scale_maze)
    player = PlayerController(
        position=maze_3d.player_spawn,
        speed=10,
        collider_size=Vec3(0.34, 2, 0.34),
        eye_height=2.0,
        fov=90,
    )
    mini_map = MiniMap(maze_3d.walls, size, 0.4)
    pacgums = Pacgums_Manager(scale_maze, config,
                              maze_3d.pacgums_zone, mini_map)

    InputHandler(player, mini_map, pacgums)
    app.run()
