import random
import pygame
import numpy as np
import pixel_array_manipulation

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HEIGHT = 300
WIDTH = 300
RUNNING = 1
PAUSE = 0


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


def python_pixel_manipulator(screen, pixAr):
    alive = []
    dead = []
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

    return pixAr


def init_screen(screen):
    i = screen
    pass
    # i[120][120] = WHITE
    # i[121][120] = WHITE
    # i[120][121] = WHITE
    # i[121][121] = WHITE
    #
    # i[122][119] = WHITE
    # i[123][119] = WHITE
    # i[123][118] = WHITE
    # i[122][118] = WHITE

    # i[122][120] = WHITE
    # i[122][121] = WHITE
    # i[122][122] = WHITE


def game_loop():
    screen = pygame.Surface((WIDTH, HEIGHT))
    win = pygame.display.set_mode((WIDTH*3, HEIGHT*3))
    pygame.display.set_caption("Game of Life")
    screen.fill(BLACK)
    state = PAUSE
    pixAr = pygame.PixelArray(screen)
    pygame.draw.line(screen, WHITE, (1, 299), (299, 1), 1)
    pygame.draw.line(screen, WHITE, (150, 1), (150, 299), 1)
    pygame.draw.line(screen, WHITE, (1, 1), (299, 299), 1)
    pygame.draw.circle(screen, WHITE, (150, 150), 60, 1)
    pygame.draw.circle(screen, WHITE, (150, 150), 80, 1)
    init_screen(pixAr)
    win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
    pygame.display.update()
    carry_on = True
    while carry_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carry_on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state = PAUSE
                if event.key == pygame.K_u:
                    state = RUNNING
        # --- Game logic should go here
        if state == RUNNING:
            # pygame.surfarray.blit_array(screen, python_pixel_manipulator(screen, pixAr))
            pixAr = pixel_array_manipulation.pixel_array_manipulator(pixAr, HEIGHT, WIDTH)
            pygame.surfarray.blit_array(screen, np.array(pixAr))
        win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game_loop()
