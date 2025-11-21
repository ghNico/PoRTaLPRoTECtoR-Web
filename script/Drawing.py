import time
import pygame


def draw_buttons(WINDOW,sideinfo, buttons, exit_button, special_power_button):
    """
    Draws the button list and the side info for tower upgrades

    Arguments: pygame window, sideinfo, list of buttons

    Test:
        -check if the objects have a draw function
        -check if sideinfo is shown correctly

    """
    # todo hier werden die Türme gezeichnet
    for k in buttons:
        k.draw(WINDOW)

    sideinfo.draw(WINDOW)
    exit_button.draw(WINDOW)
    special_power_button.draw(WINDOW)

def draw_window(WINDOW, UserHealth, sideinfo, buttons, wave, starttime, Gold, exit_button, special_power_button):
    """
    Draws the game window with background and game stats on the left-down corner and draw buttons on top of background

    Arguments: pygame window, all stats

    Test:
        -user health calculation is not dynamic
        -check if the window resolution is 1920x1080

    """
    WINDOW.fill((27, 36, 53))
    draw_buttons(WINDOW,sideinfo, buttons, exit_button, special_power_button)
    # Show Wave
    waveValue = pygame.font.SysFont('comicsans', 20).render(str(wave), True, (255, 255, 255))
    waveText = pygame.font.SysFont('comicsans', 20).render("Wave: ", True, (255, 255, 255))
    WINDOW.blit(waveText, (1250, 1300))
    WINDOW.blit(waveValue, (1300, 1300))
    # Show Time
    timeValue = pygame.font.SysFont('comicsans', 20).render(str(int(time.time() - starttime)), True, (255, 255, 255))
    timeText = pygame.font.SysFont('comicsans', 20).render("Time: ", True, (255, 255, 255))
    WINDOW.blit(timeText, (1250, 1340))
    WINDOW.blit(timeValue, (1300, 1340))
    # Show Gold:
    goldText = pygame.font.SysFont('comicsans', 20).render("Gold: ", True, (255, 255, 255))
    goldValue = pygame.font.SysFont('comicsans', 20).render(str(int(Gold)), True, (255, 255, 255))
    WINDOW.blit(goldText, (1250, 1380))
    WINDOW.blit(goldValue, (1300, 1380))
    # Show Health:
    HealthText = pygame.font.SysFont('comicsans', 20).render("Health: ", True, (255, 255, 255))
    WINDOW.blit(HealthText, (1250, 1420))
    actualHealth = 50 * UserHealth / 100
    pygame.draw.rect(WINDOW, (255, 0, 0), (1300, 1420, 50, 15))
    pygame.draw.rect(WINDOW, (0, 255, 0), (1300, 1420, actualHealth, 15))

def draw_map(WINDOW, wayfields, towerfields):
    """
    Draws the way and tower

    Arguments: pygame window, list of way, list of tower

    Test:
        -Error handling if no way or tower is given
        -check if the objects have a draw function
    """
    for way in wayfields:
        way.draw(WINDOW)

    for tower in towerfields.values():
        tower.draw(WINDOW)

def draw_mini_map(WINDOW, field_mini, way_mini, map, pos_x, pos_y):
    """
    Draws the mini map seen at start of game

    Arguments: pygame window, textures, map and start position

    Test:
        -start position values require the 1920x1080 resolution
        -check if the map is in 6x13 format
    """
    ty = pos_y
    for y in range(8):
        tx = pos_x
        for x in range(8):
            value = map[y, x]
            if value == 0:
                WINDOW.blit(field_mini, (tx, ty))
            elif value == 8 or value == 1 or value == 2:
                WINDOW.blit(way_mini, (tx, ty))
            tx += 45
        ty += 45

def draw_tower_range(WINDOW, towerfields):
    """
    Call of range indicator draw function if mouse is over tower

    Arguments: pygame window, list of tower

    Test:
        -isOver function needs to deliver true when mouse is over tower position
        -showRange function of tower draws the range indicator
    """

    for t in towerfields.values():
        if t.isOver():
            t.showRange(WINDOW)

def draw_tower_bullets(frames, towerfields, enemys, bullet_image, sound):
    """
    Draws tower bullets, check for collide with enemys or window frame limits

    Arguments: frames, list of tower, list of enemys and the bullet image

    Test:
        -require the 1920x1080 resolution
        -check if frames are 60 so the animation looks fine
    """

    if frames%8 == 0:
        for t in towerfields.values():
            if t.getValue() != None:
                bulletValue = t.getValue()%10 - 1
                t.findEnemys(enemys, bullet_image[bulletValue], sound)

    for t in towerfields.values():
        towerBullets = t.getTowerLst()
        if towerBullets != None and towerBullets != []:
            for e in enemys:
                if e.image != None:
                    e.checkCollide(towerBullets)

            for t in towerBullets:
                if t.x > 1440 or t.x<0 or t.y<0 or t.y>1440:
                    towerBullets.remove(t)