import os
import random
import pygame
from colors import BLACK
from grid import Grid


class InvalidMazeError(Exception):
    pass


class Maze:
    CHARS = 'oxif'

    def __init__(self, maze, width, height):
        self.grid = Grid(maze)
        self.width = width
        self.height = height

    @property
    def wts(self):
        return self.width / len(self.grid.tiles[0])

    @property
    def hts(self):
        return self.height / len(self.grid.tiles)

    def draw(self, surface):
        x, y = 0, 0
        for row in self.grid.tiles:
            for tile in row:
                color = self.grid.tile_color(tile)
                x1 = x*self.wts
                x2 = x1 + self.wts
                y1 = y*self.hts
                y2 = y1 + self.hts
                pygame.draw.rect(surface, color, pygame.Rect(x1, y1, x2, y2))
                x += 1
            x = 0
            y += 1

        for i in range(len(self.grid.tiles[0])):
            x1 = self.wts*i
            x2 = x1+self.wts-1
            pygame.draw.line(surface, BLACK, (x1, 0), (x1, self.height))
            pygame.draw.line(surface, BLACK, (x2, 0), (x2, self.height))

        for i in range(len(self.grid.tiles)):
            y1 = self.hts*i
            y2 = y1+self.hts-1
            pygame.draw.line(surface, BLACK, (0, y1), (self.width, y1))
            pygame.draw.line(surface, BLACK, (0, y2), (self.width, y2))

    def a_star(self):
        self.grid.a_star()

    @classmethod
    def load(cls, width, height, filename="maze.txt", random=True):
        if not os.path.exists(filename):
            if not random:
                raise FileNotFoundError(f'{filename} does not exist')
            return cls.random(10, 10, width, height)
        with open(filename, 'r', encoding='utf-8') as f:
            columns = None
            maze = []
            for line in f.readlines():
                line = line.lower()
                line = line.replace("\n", "")
                if columns == None:
                    columns = len(line)
                elif len(line) != columns:
                    raise InvalidMazeError("Inconsistent columns")
                for char in line:
                    if char not in cls.CHARS:
                        raise InvalidMazeError(
                            f"'{char}' is an invalid character, must be one of {cls.CHARS}")
                maze.append(line)
            maze = "\n".join(maze)
            start_count = maze.count('i')
            if start_count == 0:
                raise InvalidMazeError(f"the maze must have a beginning")
            elif start_count > 1:
                raise InvalidMazeError(
                    f"the maze must have no more than one beginning")
            end_count = maze.count('f')
            if end_count == 0:
                raise InvalidMazeError(f"the maze must have an end")
            elif end_count > 1:
                raise InvalidMazeError(
                    f"the labyrinth must not have more than one end")
            return cls(maze, width, height)

    @staticmethod
    def _random(x_tiles, y_tiles, ratio=30):
        maze = []
        for _ in range(y_tiles):
            row = ""
            for _ in range(x_tiles):
                if random.randint(0, 100) <= ratio:
                    row += "x"
                else:
                    row += "o"
            maze.append(row)
        maze = "\n".join(maze)
        maze = f"i{maze[1:]}"
        maze = f"{maze[:-1]}f"
        return maze

    def generate_random(self, x_tiles, y_tiles, ratio=30):
        self.grid.maze = self._random(x_tiles, y_tiles, ratio)

    @classmethod
    def random(cls, x_tiles, y_tiles, width, height, ratio=30):
        return cls(cls._random(x_tiles, y_tiles, ratio), width, height)
