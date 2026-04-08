from mazegenerator import MazeGenerator
from ursina import (
    Ursina,
    Sky,
    mouse,
    DirectionalLight,
    AmbientLight,
    Vec3,
    color,
)
from ursina.prefabs.first_person_controller import FirstPersonController
from .maze_3d import Maze_3d
from .input import InputHandler
from .hud import InGameHUD


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
    InputHandler(player)
    InGameHUD(score=0, lives=3, level=1, remaining_time=120)

    DirectionalLight().look_at(Vec3(1, -1, -1))
    AmbientLight(color=color.rgba32(100, 100, 100, 255))

    scale_maze = 4
    Maze_3d(maze, scale_maze)
    app.run()
