import pygame
from Tiles import *


# Texturen:
background = pygame.image.load("Galaxy.jpg")
background = pygame.transform.scale(background, (1920, 1080))
button1 = pygame.image.load("Button_Start (1).png")
button1 = pygame.transform.scale(button1, (300,300))
button2 = pygame.image.load("Button_Start (2).png")
button2 = pygame.transform.scale(button2, (300,300))


def LoadMainScreen(win):
    global pressed

    # Initialize
    font = pygame.font.SysFont('comicsans', 20)
    font_headline = pygame.font.SysFont('comicsans', 80, True, True)
    font_basic = pygame.font.SysFont('comicsans', 30, True)

    win.blit(background, (0, 0))
    headline = font_headline.render("Tower Defense", True, (250, 250, 250))
    win.blit(headline, (960 - (headline.get_width() // 2), 150))

    btn1 = Button((255, 0, 0), x=(960 - button1.get_width()//2), y=400, width=300, height=300, image=button1, name="Spiel starten")
    btn2 = Button((255, 0, 0), x=(960 - button2.get_width()//2), y=400, width=300, height=300, image=button2, name="Spiel starten")

    if btn1.isOver():
        btn2.draw(win)
        state = pygame.mouse.get_pressed()[0]
        if state and not pressed:
            return 1
        elif not state:
            pressed = False
    else:
        btn1.draw(win)

    return 0