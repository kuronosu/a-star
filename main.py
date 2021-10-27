import sys
import pygame
from colors import BLACK
from puzzle import Maze
pygame.init()

size = width, height = 600, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

maze = Maze.load(width, height)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            maze.a_star()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            maze.generate_random(12, 12)
    screen.fill(BLACK)
    maze.draw(screen)
    pygame.display.flip()
    clock.tick(10)
