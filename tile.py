import math

from colors import BLACK, WHITE


class Tile:
    def __init__(self, x, y, is_obtacle):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.is_obtacle = is_obtacle
        self.parent = None
        self.neighbors: dict[Tile, int] = {}

    @property
    def f(self):
        return self.g + self.h

    @property
    def color(self):
        return BLACK if self.is_obtacle else WHITE

    def init(self, final, grid, allow_diagonals):
        self.g = math.inf
        self.h = self.cost_h(final)
        self.parent = None
        self.setup_neighbors(grid, allow_diagonals)

    def __neighbour_tile(self, tile):
        if not tile.is_obtacle:
            self.neighbors[tile] = self.cost_g(tile)

    def setup_neighbors(self, grid, allow_diagonals):
        grid = grid.tiles
        columns = len(grid)
        rows = len(grid[0])

        if self.x < columns - 1:
            self.__neighbour_tile(grid[self.x+1][self.y])
        if self.x > 0:
            self.__neighbour_tile(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.__neighbour_tile(grid[self.x][self.y + 1])
        if self.y > 0:
            self.__neighbour_tile(grid[self.x][self.y-1])
        # diagonals
        if allow_diagonals:
            if self.x > 0 and self.y > 0:
                self.__neighbour_tile(grid[self.x-1][self.y-1])
            if self.x < columns - 1 and self.y > 0:
                self.__neighbour_tile(grid[self.x+1][self.y-1])
            if self.x > 0 and self.y < rows - 1:
                self.__neighbour_tile(grid[self.x-1][self.y+1])
            if self.x < columns - 1 and self.y < rows - 1:
                self.__neighbour_tile(grid[self.x+1][self.y+1])

    def cost_h(self, final):
        return abs(final.x - self.x) + abs(final.y - self.y)

    def cost_g(self, other):
        # Si el movimiento es horizontal o vertical el costo es 1, si es diagonal el costo es 1.4
        return 1 if self.x == other.x or self.y == other.y else 1.4

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Tile) and self.x == o.x and self.y == o.y and self.is_obtacle == o.is_obtacle

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.g} {self.h})"

    def __repr__(self) -> str:
        return self.__str__()
