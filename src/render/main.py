from mazegenerator import MazeGenerator
from ursina import Ursina, Sky, mouse, DirectionalLight, AmbientLight, Vec3, color, Entity
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import BoxCollider, Vec3
from .maze_3d import Maze_3d
from .input import InputHandler
from .minimap import MiniMap
<<<<<<< HEAD
=======
from .player_controller import PlayerController
from .pacgums import Pacgums
>>>>>>> 4da2e00 (pacgums display, map and 3d + pacman inb the map)

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

<<<<<<< HEAD
    player = FirstPersonController()
    player.collider = BoxCollider(player, center=Vec3(0, 1, 0), size=Vec3(0.5, 2, 0.5))
    
=======
>>>>>>> 4da2e00 (pacgums display, map and 3d + pacman inb the map)

    DirectionalLight().look_at(Vec3(1, -1, -1))
    AmbientLight(color=color.rgba32(100, 100, 100, 255))

    scale_maze = 4
    maze_3d = Maze_3d(maze, scale_maze)
<<<<<<< HEAD
    mini_map = MiniMap(maze_3d.walls, size, 0.4)
    InputHandler(player, mini_map.get_ui_map())
=======
    
    
    player = PlayerController(
        position=maze_3d.player_spawn,
        speed=10,
        collider_size=Vec3(0.34, 2, 0.34),
        eye_height=2.0,
        fov=90,
    )

    pacgums = Pacgums(scale_maze, config, maze_3d.pacgums_zone)
    mini_map = MiniMap(maze_3d.walls, size, 0.4, pacgums)
    InputHandler(player, mini_map.get_ui_map(), pacgums)
>>>>>>> 4da2e00 (pacgums display, map and 3d + pacman inb the map)
    app.run()



