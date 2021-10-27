import math
from colors import BLUE, GREEN, ORANGE, RED
from tile import Tile


class Grid:
    def __init__(self, maze):
        self._start = None
        self._end = None
        self._tiles: list[list[Tile]] = []
        self._open: list[Tile] = []
        self._close: list[Tile] = []
        self._trace = []
        self.maze = maze

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def tiles(self):
        return self._tiles

    @property
    def open(self):
        return self._open

    @property
    def close(self):
        return self._close

    @property
    def trace(self):
        return self._trace

    @property
    def maze(self):
        return self.maze

    @maze.setter
    def maze(self, new_maze):
        if isinstance(new_maze, str):
            new_maze = new_maze.splitlines()
        self._maze = new_maze
        self._start = None
        self._end = None
        self._open = []
        self._close = []
        self._trace = []
        self._load()
        for row in self._tiles:
            for node in row:
                node.init(self._end, self)
        self._start.g = 0

    def _load(self):
        self._tiles = []
        for i in range(len(self._maze)):
            tmp = []
            for j in range(len(self._maze[i])):
                if self._maze[i][j] == 'i':
                    self._start = Tile(i, j, False)
                    cur = self._start
                elif self._maze[i][j] == 'f':
                    self._end = Tile(i, j, False)
                    cur = self._end
                else:
                    cur = Tile(i, j, self._maze[i][j] == 'x')
                tmp.append(cur)
            self._tiles.append(tmp)

    def get_min(self):
        m = math.inf
        _i = 0
        for i in range(len(self._open)):
            if self._open[i].f < m:
                m = self._open[i].f
                _i = i
        return self._open.pop(_i)

    def a_star(self, func=None):
        self._open.append(self._start)
        while len(self._open) > 0:
            if self._a_star_step():
                break
            if func:
                func(self.open)

        cur = self._end
        self._trace = []
        while cur != None:
            self._trace.append(cur)
            cur = cur.parent
        return self._trace

    def _a_star_step(self):
        actual = self.get_min()
        self._close.append(actual)
        if actual == self._end:
            return True
        for ns, cost in actual.neighbors.items():
            if ns not in self._close:
                if ns not in self._open:
                    self._open.append(ns)
                if actual.g + cost < ns.g:
                    ns.g = actual.g + cost
                    ns.parent = actual
        return False

    def print_puzzle(self):
        for row in self._tiles:
            for node in row:
                if node in self._trace:
                    print('-', end="   ")
                else:
                    print('x' if node.is_obtacle else 'o', end="   ")
            print()

    def tile_color(self, tile):
        # print(self.start, self.end, self.trace, self.close)
        if tile == self.start:
            return GREEN
        if tile == self.end:
            return RED
        if tile in self.trace:
            return BLUE
        if tile in self.close:
            return ORANGE
        return tile.color
