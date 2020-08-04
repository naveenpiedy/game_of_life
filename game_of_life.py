import random
import pygame
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HEIGHT = 300
WIDTH = 300


def game_of_life_rules(screen, x, y):
    dead = []
    live = []
    x_values = [x - 1, x, x + 1]
    y_values = [y - 1, y, y + 1]
    live_neighbours = 0
    for i in x_values:
        for j in y_values:
            if 0 <= i < HEIGHT and 0 <= j < WIDTH and (i, j) != (x, y):
                if screen.get_at((i, j)) == WHITE:
                    live_neighbours += 1

    if screen.get_at((x, y)) == WHITE and not 1 < live_neighbours < 4:
        dead.append((x, y))
    elif screen.get_at((x, y)) == BLACK and live_neighbours == 3:
        live.append((x, y))

    return live, dead


def init_screen(screen):
    i = screen
    i[120][120] = WHITE
    i[121][120] = WHITE
    i[120][121] = WHITE
    i[121][121] = WHITE

    i[122][119] = WHITE
    i[123][119] = WHITE
    i[123][118] = WHITE
    i[122][118] = WHITE


def game_loop():
    screen = pygame.Surface((WIDTH, HEIGHT))
    win = pygame.display.set_mode((WIDTH*6, HEIGHT*6))
    pygame.display.set_caption("Game of Life")
    screen.fill(BLACK)
    pixAr = pygame.PixelArray(screen)
    init_screen(pixAr)
    win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
    pygame.display.update()
    carry_on = True
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
                pixAr[i[0]][i[1]] = WHITE

        if dead:
            for i in dead:
                pixAr[i[0]][i[1]] = BLACK


        win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game_loop()
