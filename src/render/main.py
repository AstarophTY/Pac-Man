from mazegenerator import MazeGenerator
from ursina import Ursina, Sky, mouse, DirectionalLight, AmbientLight, Vec3, color, Entity, time, raycast, held_keys, clamp
from ursina.prefabs.first_person_controller import FirstPersonController
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
    
    # Custom update function to prevent FirstPersonController from sticking to walls
    def custom_update():
        player.rotation_y += mouse.velocity[0] * player.mouse_sensitivity[1]
        player.camera_pivot.rotation_x -= mouse.velocity[1] * player.mouse_sensitivity[0]
        player.camera_pivot.rotation_x = clamp(player.camera_pivot.rotation_x, -90, 90)

        player.direction = Vec3(
            player.forward * (held_keys['w'] - held_keys['s'])
            + player.right * (held_keys['d'] - held_keys['a'])
        ).normalized()

        move_amount = player.direction * time.dt * player.speed

        # Raycast for X axis movement
        if raycast(player.position + Vec3(0, 0.5, 0), Vec3(1, 0, 0), distance=.5 + max(0, move_amount[0]), traverse_target=player.traverse_target, ignore=player.ignore_list).hit:
            move_amount[0] = min(move_amount[0], 0)
        elif raycast(player.position + Vec3(0, 0.5, 0), Vec3(-1, 0, 0), distance=.5 - min(0, move_amount[0]), traverse_target=player.traverse_target, ignore=player.ignore_list).hit:
            move_amount[0] = max(move_amount[0], 0)

        # Raycast for Z axis movement
        if raycast(player.position + Vec3(0, 0.5, 0), Vec3(0, 0, 1), distance=.5 + max(0, move_amount[2]), traverse_target=player.traverse_target, ignore=player.ignore_list).hit:
            move_amount[2] = min(move_amount[2], 0)
        elif raycast(player.position + Vec3(0, 0.5, 0), Vec3(0, 0, -1), distance=.5 - min(0, move_amount[2]), traverse_target=player.traverse_target, ignore=player.ignore_list).hit:
            move_amount[2] = max(move_amount[2], 0)

        player.position += move_amount

    player.update = custom_update
    

    DirectionalLight().look_at(Vec3(1, -1, -1))
    AmbientLight(color=color.rgba32(100, 100, 100, 255))

    scale_maze = 4
    maze_3d = Maze_3d(maze, scale_maze)
    mini_map = MiniMap(maze_3d.walls, size, 0.4)
    InputHandler(player, mini_map.get_ui_map())
    app.run()



