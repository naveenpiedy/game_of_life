import itertools

import pygame
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HEIGHT = 300
WIDTH = 300


def get_neighbour(screen, x, y):
    x_values = [x - 1, x, x + 1]
    y_values = [y - 1, y, y + 1]
    neighbouring_points = list(itertools.product(x_values, y_values))
    neighbouring_points = filter(
        lambda item: not (item[0] >= HEIGHT or item[0] < 0 or item[1] >= WIDTH or item[1] < 0), neighbouring_points)

    return neighbouring_points


def game_of_life_rules(screen, x, y):
    dead = []
    live = []
    neighbouring_points = get_neighbour(screen, x, y)
    live_neighbours = filter(lambda item: screen.get_at(item) == WHITE, neighbouring_points)
    num_live_neighbours = len(list(live_neighbours))

    if screen.get_at((x, y)) == WHITE:
        if not (2 < num_live_neighbours < 4):
            dead.append((x, y))
    else:
        if num_live_neighbours == 3:
            live.append((x, y))

    return live, dead


def init_screen(screen):
    pygame.draw.line(screen, WHITE, (0, 299), (299, 0), 10)
    pygame.draw.line(screen, WHITE, (0, 0), (299, 299), 10)


def game_loop():
    size = (HEIGHT, WIDTH)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game of Life")
    screen.fill(BLACK)
    init_screen(screen)
    carry_on = True
    clock = pygame.time.Clock()
    while carry_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carry_on = False
        alive = list()
        dead = list()
        # --- Game logic should go here
        for x, y in np.ndindex((HEIGHT, WIDTH)):
            l, d = game_of_life_rules(screen, x, y)
            if l:
                alive.extend(l)
            if d:
                dead.extend(d)

        if alive:
            for i in alive:
                pygame.draw.circle(screen, WHITE, i, 1, 1)

        if dead:
            for i in dead:
                pygame.draw.circle(screen, BLACK, i, 1, 1)

        pygame.display.flip()

        clock.tick(120)

    pygame.quit()


if __name__ == '__main__':
    game_loop()
