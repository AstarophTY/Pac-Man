from ursina import Ursina, Sky, Entity, color, DirectionalLight, AmbientLight, mouse, camera, clamp, held_keys, time, Vec3, application

def get_walls(val: int) -> None:
    bits = f"{int(val):04b}"
    return {
        "NORTH": bits[3] == '1',
        "EAST": bits[2] == '1',
        "SOUTH": bits[1] == '1',
        "WEST": bits[0] == '1',
    }

def create_walls(y, x, walls: dict):

    if walls.get('NORTH') is True:
        Entity(model='cube', position=(x,0,y-0.45), color=color.gray, scale=(1,1,0.1))
    if walls.get('SOUTH') is True:
        Entity(model='cube', position=(x,0,y+0.45), color=color.gray, scale=(1,1,0.1))
    if walls.get('EAST') is True:
        Entity(model='cube', position=(x+0.45,0,y), color=color.gray, scale=(0.1,1,1))
    if walls.get('WEST') is True:
        Entity(model='cube', position=(x-0.45,0,y), color=color.gray, scale=(0.1,1,1))

def render(maze: list, width, height):
    app = Ursina()
    Sky()
    mouse.locked = True
    camera.fov = 120
    camera.position = Vec3(0, 5, -10)

    DirectionalLight().look_at(Vec3(1, -1, -1))
    AmbientLight(color=color.rgba32(100, 100, 100, 255))


    for y in range(len(maze)):
        for x in range(len(maze[y])):
            create_walls(y,x, get_walls(maze[y][x]))
    return app


def input(key):
    if key == 'escape':
        application.quit()



def update():

    speed = 10
    camera.rotation_y += mouse.velocity[0] * 40
    camera.rotation_x -= mouse.velocity[1] * 40
    camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    if held_keys['z'] or held_keys['w']:
        camera.position += camera.forward * speed * time.dt
    if held_keys['s']:
        camera.position -= camera.forward * speed * time.dt
    if held_keys['q'] or held_keys['a']:
        camera.position -= camera.right * speed * time.dt
    if held_keys['d']:
        camera.position += camera.right * speed * time.dt
    if held_keys['space']:
        camera.y += speed * time.dt
    if held_keys['shift']:
        camera.y -= speed * time.dt
