import numpy as np
import pygame
from Tower_Anim import *
from Tiles import *

WINDOW = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)

selectedTower = None
selectedTowerField = None

towerfields = []
towerplace_bool = False


# Texturen:
start_map = pygame.transform.scale(pygame.image.load('anfang.png'), (140, 140))
end_map = pygame.transform.scale(pygame.image.load('ende.png'), (140, 140))
way_horizontal = pygame.transform.scale(pygame.image.load("assets/tiles/Gerade.JPG"), (140, 140))
way_vertical = pygame.transform.scale(pygame.transform.rotate(way_horizontal, 90), (140, 140))
clickable_field = pygame.transform.scale(pygame.image.load('bauen.png'), (140, 140))
obstacle_map = pygame.transform.scale(pygame.image.load('hindernis.png'), (140, 140))
curve1 = pygame.transform.scale(pygame.image.load('assets/tiles/Kurve.JPG'), (140, 140))
curve1 = pygame.transform.scale(curve1, (140, 140))
curve2 = pygame.transform.rotate(curve1, 90)
curve3 = pygame.transform.rotate(curve1, 180)
curve4 = pygame.transform.rotate(curve1, 270)

tower_1 = []
tower_2 = []
tower_3 = []
for x in range(1,9):
    tower_1.append(pygame.image.load(f'assets/tower/tower 1 ({x}).png'))
    tower_2.append(pygame.image.load(f'assets/tower/tower 2 ({x}).png'))
    tower_3.append(pygame.image.load(f'assets/tower/tower 3 ({x}).png'))


# Erkennt den Weg auf unserem NumpyArray (Spielfeld)
def LookAhead(way, map, pos_x, pos_y):
    map[pos_y, pos_x] = 0
    if pos_x < 12 and map[pos_y, pos_x + 1] == 8:  # rechts
        way.append(("rechts", pos_x + 1, pos_y))
        LookAhead(way, map, pos_x + 1, pos_y)
    elif pos_x > 0 and map[pos_y, pos_x - 1] == 8:  # links
        way.append(("links", pos_x - 1, pos_y))
        LookAhead(way, map, pos_x - 1, pos_y)
    elif pos_y > 0 and map[pos_y - 1, pos_x] == 8:  # oben
        way.append(("oben", pos_x, pos_y - 1))
        LookAhead(way, map, pos_x, pos_y - 1)
    elif pos_y < 5 and map[pos_y + 1, pos_x] == 8:  # unten
        way.append(("unten", pos_x, pos_y + 1))
        LookAhead(way, map, pos_x, pos_y + 1)
    elif pos_x < 12 and map[pos_y, pos_x + 1] == 2:  # rechts
        way.append(("rechts", pos_x + 1, pos_y))
    elif pos_x > 0 and map[pos_y, pos_x - 1] == 2:  # links
        way.append(("links", pos_x - 1, pos_y))
    elif pos_y > 0 and map[pos_y - 1, pos_x] == 2:  # oben
        way.append(("oben", pos_x, pos_y - 1))
    elif pos_y < 5 and map[pos_y + 1, pos_x] == 2:  # unten
        way.append(("unten", pos_x, pos_y + 1))
    return way


# Wegtextur wird gezeichnet
def DrawPath(path_pos):
    global WINDOW
    current_pos = PATH[path_pos][0]
    next_pos = PATH[path_pos + 1][0]
    pos_x = 50 + (PATH[path_pos][1] * 140)
    pos_y = (PATH[path_pos][2]) * 140
    if current_pos == 'oben' and next_pos == 'rechts' or current_pos == 'links' and next_pos == 'unten':
        WINDOW.blit(curve2, (pos_x, pos_y))
    elif current_pos == 'oben' and next_pos == 'links' or current_pos == 'rechts' and next_pos == 'unten':
        WINDOW.blit(curve1, (pos_x, pos_y))
    elif current_pos == 'unten' and next_pos == 'rechts' or current_pos == 'links' and next_pos == 'oben':
        WINDOW.blit(curve3, (pos_x, pos_y))
    elif current_pos == 'unten' and next_pos == 'unten' or current_pos == 'oben' and next_pos == 'oben':
        WINDOW.blit(way_vertical, (pos_x, pos_y))
    elif current_pos == 'rechts' and next_pos == 'rechts' or current_pos == 'links' and next_pos == 'links':
        WINDOW.blit(way_horizontal, (pos_x, pos_y))
    elif current_pos == 'rechts' and next_pos == 'oben' or current_pos == 'unten' and next_pos == 'links':
        WINDOW.blit(curve4, (pos_x, pos_y))


# Hindernisse: Abstand von Feld zu Weg (return Abstand)
def DistanceToPath(map, pos_x, pos_y):
    if pos_x < 12 and map[pos_y, pos_x + 1] == 8 or pos_x > 0 and map[pos_y, pos_x - 1] == 8 or pos_y > 0 and map[
        pos_y - 1, pos_x] == 8 or pos_y < 5 and map[pos_y + 1, pos_x] == 8:
        return 1
    elif pos_x < 11 and map[pos_y, pos_x + 2] == 8 or pos_x > 0 and map[pos_y, pos_x - 2] == 8 or pos_y > 0 and map[
        pos_y - 2, pos_x] == 8 or pos_y < 4 and map[pos_y + 2, pos_x] == 8:
        return 2
    elif pos_x < 10 and map[pos_y, pos_x + 3] == 8 or pos_x > 0 and map[pos_y, pos_x - 3] == 8 or pos_y > 0 and map[
        pos_y - 3, pos_x] == 8 or pos_y < 3 and map[pos_y + 3, pos_x] == 8:
        return 3
    else:
        return 4


# Hindernisse: Je weiter entfernt ein Feld vom Weg ist, umso wahrscheinlicher ist das auftreten eines Hindernisses (return k = manipulierte MAP)
def GenerateObstacles(map):
    k = map
    sum_obstacles = 0
    while sum_obstacles < 12:
        for y in range(6):
            for x in range(13):
                if k[y, x] == 0:
                    distance = DistanceToPath(map, x, y)
                    value = np.random.randint(0, 100)
                    if distance == 1 and value < 5 or distance == 2 and value < 20 or distance == 3 and value < 50 or distance == 4:
                        k[y, x] = 5
                        sum_obstacles += 1
    return k


# NumpyArray wird ausgewertet => Texturen werden gezeichnet
def DrawMap():
    global towerplace_bool, angle
    count_ways = 0
    ty = 0
    for y in range(6):
        tx = 0
        if y > 0:
            tx = 50
        for x in range(13):
            value = MAP[y, x]
            if value == 0:
                WINDOW.blit(clickable_field, (tx, ty))
                if not towerplace_bool:
                    towerfields.append(Tiles(tx, ty, 140, 140))
            elif value == 5:
                WINDOW.blit(obstacle_map, (tx, ty))
            elif value == 8:
                DrawPath(count_ways)
                count_ways += 1
            elif value == 1:
                WINDOW.blit(start_map, (tx, ty))
                tx += 50
            elif value == 2:
                WINDOW.blit(end_map, (tx, ty))
            elif value == 11:
                WINDOW.blit(tower_1[0], (tx, ty))
            elif value == 12:
                WINDOW.blit(tower_1[1], (tx, ty))
            elif value == 13:
                WINDOW.blit(tower_1[2], (tx, ty))
            elif value == 14:
                WINDOW.blit(tower_1[3], (tx, ty))
            elif value == 15:
                WINDOW.blit(tower_1[4], (tx, ty))
            elif value == 16:
                WINDOW.blit(tower_1[5], (tx, ty))
            elif value == 17:
                WINDOW.blit(tower_1[6], (tx, ty))
            elif value == 18:
                WINDOW.blit(tower_1[7], (tx, ty))
            elif value == 21:
                WINDOW.blit(tower_2[0], (tx, ty))
            elif value == 22:
                WINDOW.blit(tower_2[1], (tx, ty))
            elif value == 23:
                WINDOW.blit(tower_2[2], (tx, ty))
            elif value == 24:
                WINDOW.blit(tower_2[3], (tx, ty))
            elif value == 25:
                WINDOW.blit(tower_2[4], (tx, ty))
            elif value == 26:
                WINDOW.blit(tower_2[5], (tx, ty))
            elif value == 27:
                WINDOW.blit(tower_2[6], (tx, ty))
            elif value == 28:
                WINDOW.blit(tower_2[7], (tx, ty))
            elif value == 31:
                WINDOW.blit(tower_3[0], (tx, ty))
            elif value == 32:
                WINDOW.blit(tower_3[1], (tx, ty))
            elif value == 33:
                WINDOW.blit(tower_3[2], (tx, ty))
            elif value == 34:
                WINDOW.blit(tower_3[3], (tx, ty))
            elif value == 35:
                WINDOW.blit(tower_3[4], (tx, ty))
            elif value == 36:
                WINDOW.blit(tower_3[5], (tx, ty))
            elif value == 37:
                WINDOW.blit(tower_3[6], (tx, ty))
            elif value == 38:
                WINDOW.blit(tower_3[7], (tx, ty))
            tx += 140
        ty += 140
    towerplace_bool = True


# Rotates Images
#def Rotate(tower):
#    global WINDOW
#    print(tower.angle)
#    tower.incrementangle()
#    print(tower.angle)
#    # rotieren und in einem neuen "surface" speichern
#    image_rotation = pygame.transform.rotate(tower.image, tower.angle)

    # Bestimmen der neuen Abmessungen (nach Rotation ändern sich diese!)
#    image_size = image_rotation.get_rect()

    # Ausgabe
#    WINDOW.blit(image_rotation, (tower.pos_x + 70 - image_size.center[0], tower.pos_y + 70 - image_size.center[1]))

    # pygame.draw.rect(WINDOW, (255, 255, 255), (x - groesse.center[0], y - groesse.center[1], groesse.width, groesse.height), 1)


MAP = GenerateObstacles(np.load(f'maps/{"leicht"}/map ({10}).npy'))
PATH = LookAhead([], np.load(f'maps/{"leicht"}/map ({10}).npy'), 0, 0)
