import pygame

from Button import *
from game_logic import *
import numpy as np
import time

startup(1920, 1080)
clock = pygame.time.Clock()
running = True



while running:
    clock.tick(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # maus_press(pygame.mouse.get_pressed())
    draw_window(np.random.randint(1,22000))

pygame.quit()
