from game_logic import *

startup(1920, 1080)
clock = pygame.time.Clock()
running = True



while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_window()

pygame.quit()
