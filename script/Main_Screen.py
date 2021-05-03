import pygame


# Texturen:
background = pygame.image.load("Galaxy.jpg")
background = pygame.transform.scale(background, (1920, 1080))


def LoadMainScreen(win):

    # Initialize
    font = pygame.font.SysFont('comicsans', 20)
    font_headline = pygame.font.SysFont('comicsans', 80, True, True)
    font_basic = pygame.font.SysFont('comicsans', 30, True)

    win.blit(background, (0, 0))
    headline = font_headline.render("Tower Defense", True, (250, 250, 250))
    win.blit(headline, (960 - (headline.get_width() // 2), 150))

