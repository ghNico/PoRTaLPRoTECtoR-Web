from Tiles import *
import pygame

# texture load for start screen:
background = pygame.image.load("assets/environment/Galaxy.png")
background = pygame.transform.scale(background, (1440, 1540))
button1 = pygame.image.load("assets/environment/Button_Start (1).png")
button1 = pygame.transform.scale(button1, (300,300))
button2 = pygame.image.load("assets/environment/Button_Start (2).png")
button2 = pygame.transform.scale(button2, (300,300))

tower = pygame.image.load("assets/tower/towerStart1.png")
tower = pygame.transform.scale(tower, (160, 160))
towerGround = pygame.image.load("assets/tower/towerStart2.png")
towerGround = pygame.transform.scale(towerGround, (160, 160))
bullet = pygame.image.load("assets/bullet/bullet 1.png")

logo = pygame.image.load("assets/icon.png")
logo = pygame.transform.scale(logo, (1702/3,846/3))

# Tower placement in corners of 1920x1080 screen:
tower_lst = []
tower_lst.append(
    Tower(x=50, y=1230, width=160, height=160, image1=tower, image2=towerGround, towerRange=200, damage=15,
          value=11))
tower_lst.append(
    Tower(x=50, y=50, width=160, height=160, image1=tower, image2=towerGround, towerRange=200, damage=15,
          value=11))
tower_lst.append(
    Tower(x=1230, y=1230, width=160, height=160, image1=tower, image2=towerGround, towerRange=200, damage=15,
          value=11))
tower_lst.append(
    Tower(x=1230, y=50, width=160, height=160, image1=tower, image2=towerGround, towerRange=200, damage=15,
          value=11))

# Position of mouse click init:
AimX = 0
AimY = 0

def LoadMainScreen(win, sound):
    #TODO hier noch schauen wegen dem exit button
    """
    Draws the launch screen at the startup, tower animation and mouse follow, shoot animation, and start game when pressing the start button

    Arguments: pygame window

    Test:
        -return values need to be same as the gamestate in main.py
        -collide of bullets are needed for game startup so the draw function has to work properly

    Returns: gamestate 0 or 1 if start is pressed and the bullets collide with the button

    """
    global pressed, font, font_headline, font_headline, AimX, AimY

    font = pygame.font.SysFont('comicsans', 20)
    font_headline = pygame.font.SysFont('comicsans', 80, True, True)
    win.blit(background, (0, 0))
    win.blit(logo, (720 - (logo.get_width() // 2), 50))
    btn1 = Button((255, 0, 0), x=(720 - button1.get_width()//2), y=550, width=300, height=300, image=button1, name="game start")
    btn2 = Button((255, 0, 0), x=(720 - button2.get_width()//2), y=550, width=300, height=300, image=button2, name="game start")
    btn_rect = pygame.Rect(btn1.x, btn1.y, btn1.width, btn1.height)
    pos = pygame.mouse.get_pos()

    for t in tower_lst:
        towerBullets = t.getTowerLst()
        t.rotate(pos[0], pos[1])
        t.draw(win)

        for b in towerBullets:
            if b.x > 1440 or b.x < 0 or b.y < 0 or b.y > 1440 or b.x == AimX or b.y == AimY:
                towerBullets.remove(b)

            if btn_rect.colliderect(b.rect) and (btn1.x < AimX < btn1.x + button1.get_width()) and (btn1.y < AimY < btn1.y + button1.get_height()):
                return 1
            else:
                pass

    if btn1.isOver():
        btn2.draw(win)
    else:
        btn1.draw(win)

    state = pygame.mouse.get_pressed()[0]
    if state and not pressed:
        for t in tower_lst:
                t.spawnBullet(pos[0], pos[1], pygame.transform.rotate(bullet, t.angle), sound)
                AimX = pos[0]
                AimY = pos[1]
                t.draw(win)
        pressed = True
    elif not state:
        pressed = False

    return 0


