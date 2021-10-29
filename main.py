import sys
import pygame
from colors import BLACK
from puzzle import Maze
pygame.init()

pygame.display.set_caption('A* algorithm')

size = width, height = 700, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

maze = Maze.load(width, height)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            maze.grid.allow_diagonals = True
            maze.a_star()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            maze.grid.allow_diagonals = False
            maze.a_star()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            maze.generate_random(25, 25)
    screen.fill(BLACK)
    maze.draw(screen)
    pygame.display.flip()
    clock.tick(10)
