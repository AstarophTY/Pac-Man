from mazegenerator import MazeGenerator
from ursina import Ursina
from .render import render, input, update

def main():
    print("Hello from pac-man!")
    size = (15, 20)
    width = size[0]
    height = size[1]
    maze_gen = MazeGenerator(
        size=size,
        perfect=False
    )
    maze = maze_gen.maze
    app = render(maze, width, height)
    app.run()



if __name__ == "__main__":
    main()
