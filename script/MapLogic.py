import numpy as np
import pygame
from Tower_Anim import *
from Tiles import *

WINDOW = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)



selectedTower = None
selectedTowerField = None

turmfelder = []
turmfelder_gesetzt = False

angle = 0


# Texturen:
anfang = pygame.image.load('anfang.png')
ende = pygame.image.load('ende.png')
weghor = pygame.image.load('weg_gerade.png')
wegver = pygame.transform.rotate(weghor, 90)
bauen = pygame.image.load('bauen.png')
hindernis = pygame.image.load('hindernis.png')
weggerade = pygame.image.load("assets/tiles/Gerade.JPG")
weggerade = pygame.transform.scale(weggerade, (140, 140))
wegver2 = pygame.transform.rotate(weggerade, 90)
knick_links_unten = pygame.image.load('assets/tiles/Kurve.JPG')
knick_links_unten = pygame.transform.scale(knick_links_unten, (140, 140))
knick_rechts_unten = pygame.transform.rotate(knick_links_unten, 90)
knick_rechts_oben = pygame.transform.rotate(knick_links_unten, 180)
knick_links_oben = pygame.transform.rotate(knick_links_unten, 270)


tower1 = pygame.image.load('assets/tower/tower (1).png')
tower2 = pygame.image.load('assets/tower/tower (2).png')
tower3 = pygame.image.load('assets/tower/tower (3).png')
tower4 = pygame.image.load('assets/tower/tower (4).png')
tower5 = pygame.image.load('assets/tower/tower (5).png')
tower6 = pygame.image.load('assets/tower/tower (6).png')
tower7 = pygame.image.load('assets/tower/tower (7).png')
tower8 = pygame.image.load('assets/tower/tower (8).png')


tower1 = pygame.image.load('assets/tower/Tower1.1_Ground.png')
tower1_rotate = pygame.transform.scale(tower1, (120,120))
tower1 = pygame.transform.scale(tower1, (140, 140))

tower1_2 = pygame.image.load('assets/tower/Chess.png')

tower = Tower(100, 300, 140, 140, pygame.transform.scale(tower1, (140, 140)),0)



# Erkennt den Weg auf unserem NumpyArray (Spielfeld)
def LookAhead(weg, map, altx, alty):
    map[alty, altx] = 0
    if altx < 12 and map[alty, altx + 1] == 8:  # rechts
        weg.append(("rechts", altx + 1, alty))
        LookAhead(weg, map, altx + 1, alty)
    elif altx > 0 and map[alty, altx - 1] == 8:  # links
        weg.append(("links", altx - 1, alty))
        LookAhead(weg, map, altx - 1, alty)
    elif alty > 0 and map[alty - 1, altx] == 8:  # oben
        weg.append(("oben", altx, alty - 1))
        LookAhead(weg, map, altx, alty - 1)
    elif alty < 5 and map[alty + 1, altx] == 8:  # unten
        weg.append(("unten", altx, alty + 1))
        LookAhead(weg, map, altx, alty + 1)
    elif altx < 12 and map[alty, altx + 1] == 2:  # rechts
        weg.append(("rechts", altx + 1, alty))
    elif altx > 0 and map[alty, altx - 1] == 2:  # links
        weg.append(("links", altx - 1, alty))
    elif alty > 0 and map[alty - 1, altx] == 2:  # oben
        weg.append(("oben", altx, alty - 1))
    elif alty < 5 and map[alty + 1, altx] == 2:  # unten
        weg.append(("unten", altx, alty + 1))
    return weg

# Wegtextur wird gezeichnet
def DrawPath(sum):
    global WINDOW
    akt = PFAD[sum][0]
    naechst = PFAD[sum + 1][0]
    px = 50 + (PFAD[sum][1] * 140)
    py = (PFAD[sum][2]) * 140
    if akt == 'oben' and naechst == 'rechts' or akt == 'links' and naechst == 'unten':
        WINDOW.blit(knick_rechts_unten, (px, py))
    elif akt == 'oben' and naechst == 'links':
        WINDOW.blit(knick_links_unten, (px, py))
    elif akt == 'unten' and naechst == 'rechts' or akt == 'links' and naechst == 'oben':
        WINDOW.blit(knick_rechts_oben, (px, py))
    elif akt == 'unten' and naechst == 'unten' or akt == 'oben' and naechst == 'oben':
        WINDOW.blit(wegver2, (px, py))
    elif akt == 'rechts' and naechst == 'rechts' or akt == 'links' and naechst == 'links':
        WINDOW.blit(weggerade, (px, py))
    elif akt == 'rechts' and naechst == 'unten':
        WINDOW.blit(knick_links_unten, (px, py))
    elif akt == 'rechts' and naechst == 'oben' or akt == 'unten' and naechst == 'links':
        WINDOW.blit(knick_links_oben, (px, py))


# Hindernisse: Abstand von Feld zu Weg (return Abstand)
def DistanceToPath(map, posx, posy):
    if posx < 12 and map[posy, posx + 1] == 8 or posx > 0 and map[posy, posx - 1] == 8 or posy > 0 and map[
        posy - 1, posx] == 8 or posy < 5 and map[posy + 1, posx] == 8:
        return 1
    elif posx < 11 and map[posy, posx + 2] == 8 or posx > 0 and map[posy, posx - 2] == 8 or posy > 0 and map[
        posy - 2, posx] == 8 or posy < 4 and map[posy + 2, posx] == 8:
        return 2
    elif posx < 10 and map[posy, posx + 3] == 8 or posx > 0 and map[posy, posx - 3] == 8 or posy > 0 and map[
        posy - 3, posx] == 8 or posy < 3 and map[posy + 3, posx] == 8:
        return 3
    else:
        return 4


# Hindernisse: Je weiter entfernt ein Feld vom Weg ist, umso wahrscheinlicher ist das auftreten eines Hindernisses (return k = manipulierte MAP)
def GenerateObstacles(map):
    k = map
    sum = 0
    while sum < 12:
        for y in range(6):
            for x in range(13):
                if k[y, x] == 0:
                    abstand = DistanceToPath(map, x, y)
                    value = np.random.randint(0, 100)
                    if abstand == 1 and value < 5 or abstand == 2 and value < 20 or abstand == 3 and value < 50 or abstand == 4:
                        k[y, x] = 5
                        sum += 1
    return k






# NumpyArray wird ausgewertet => Texturen werden gezeichnet
def DrawMap():
    global turmfelder_gesetzt, angle
    sum = 0
    ty = 0
    for y in range(6):
        tx = 0
        if y > 0:
            tx = 50
        for x in range(13):
            wert = MAP[y, x]
            if wert == 0:
                WINDOW.blit(bauen, (tx, ty))
                if not turmfelder_gesetzt:
                    turmfelder.append(Tiles(tx,ty,140,140))
            elif wert == 5:
                WINDOW.blit(hindernis, (tx, ty))
            elif wert == 8:
                DrawPath(sum)
                sum += 1
            elif wert == 1:
                WINDOW.blit(anfang, (tx, ty))
                tx += 50
            elif wert == 2:
                WINDOW.blit(ende, (tx, ty))
            elif wert == 11:
                tower_lokal = Tower(tx, ty, 140, 140, pygame.transform.scale(tower1, (140, 140)),0)
                tower_lokal.draw(WINDOW)
                Rotate(tower_lokal)
            elif wert == 12:
                WINDOW.blit(tower2, (tx, ty))
            elif wert == 13:
                WINDOW.blit(tower3, (tx, ty))
            elif wert == 14:
                WINDOW.blit(tower4, (tx, ty))
            elif wert == 15:
                WINDOW.blit(tower5, (tx, ty))
            elif wert == 16:
                WINDOW.blit(tower6, (tx, ty))
            elif wert == 17:
                WINDOW.blit(tower7, (tx, ty))
            elif wert == 18:
                WINDOW.blit(tower8, (tx, ty))
            elif wert == 21:
                WINDOW.blit(pygame.transform.scale(tower1_2, (140, 140)), (tx, ty))
            tx += 140
        ty += 140
    turmfelder_gesetzt = True


# Rotates Images
def Rotate(tower):
    global WINDOW
    print(tower.angle)
    tower.incrementangle()
    print(tower.angle)
    # rotieren und in einem neuen "surface" speichern
    rotiert = pygame.transform.rotate(tower.image, tower.angle)

    # Bestimmen der neuen Abmessungen (nach Rotation ändern sich diese!)
    groesse = rotiert.get_rect()

    # Ausgabe
    WINDOW.blit(rotiert, (tower.pos_x+70 - groesse.center[0], tower.pos_y+70 - groesse.center[1]))

    # pygame.draw.rect(WINDOW, (255, 255, 255), (x - groesse.center[0], y - groesse.center[1], groesse.width, groesse.height), 1)

MAP = GenerateObstacles(np.load(f'maps/{"leicht"}/map ({10}).npy'))
PFAD = LookAhead([], np.load(f'maps/{"leicht"}/map ({10}).npy'), 0, 0)