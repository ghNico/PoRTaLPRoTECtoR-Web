from Button import *
from colour import Color
import numpy as np

WINDOW = None
MAP = None
PFAD = None
FPS = 60
rot = Color("red")

anfang = pygame.image.load('anfang.png')
ende = pygame.image.load('ende.png')
weghor = pygame.image.load('weg_gerade.png')
wegver = pygame.transform.rotate(weghor,90)
bauen = pygame.image.load('bauen.png')
hindernis = pygame.image.load('hindernis.png')
knick_links_unten = pygame.image.load('weg_knick.png')
knick_rechts_unten = pygame.transform.rotate(knick_links_unten,90)
knick_rechts_oben = pygame.transform.rotate(knick_links_unten,180)
knick_links_oben = pygame.transform.rotate(knick_links_unten,270)

def guckeweiter(weg,map, altx, alty):
    map[alty, altx] = 0
    if altx < 12 and map[alty, altx + 1] == 8:#rechts
        weg.append(("rechts",altx + 1,alty))
        guckeweiter(weg,map,altx + 1,alty)
    elif altx > 0 and map[alty, altx - 1] == 8:#links
        weg.append(("links",altx - 1,alty))
        guckeweiter(weg,map, altx - 1, alty)
    elif alty > 0 and map[alty - 1, altx] == 8:#oben
        weg.append(("oben",altx,alty - 1))
        guckeweiter(weg,map, altx, alty - 1)
    elif alty < 5 and map[alty + 1, altx] == 8:#unten
        weg.append(("unten",altx,alty + 1))
        guckeweiter(weg,map, altx, alty + 1)
    elif altx < 12 and map[alty, altx + 1] == 2:#rechts
        weg.append(("rechts",altx + 1,alty))
    elif altx > 0 and map[alty, altx - 1] == 2:#links
        weg.append(("links",altx - 1,alty))
    elif alty > 0 and map[alty - 1, altx] == 2:#oben
        weg.append(("oben",altx,alty - 1))
    elif alty < 5 and map[alty + 1, altx] == 2:#unten
        weg.append(("unten",altx,alty + 1))
    return weg



def startup(width, height):
    global WINDOW
    pygame.init()
    WINDOW = pygame.display.set_mode((width, height))
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    pygame.display.set_caption("Tower Defense")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    mapladen('schwer',np.random.randint(1,20000))


def richtungsEntscheid(pfad,sum):
    global WINDOW
    akt = pfad[sum][0]
    naechst = pfad[sum+1][0]
    px = 50+(pfad[sum][1]*140)
    py = (pfad[sum][2])*140
    if akt == 'oben' and naechst == 'rechts' or akt == 'links' and naechst == 'unten':
        WINDOW.blit(knick_rechts_unten, (px, py))
    elif akt == 'oben' and naechst == 'links':
        WINDOW.blit(knick_links_unten, (px, py))
    elif akt == 'unten' and naechst == 'rechts' or akt == 'links' and naechst == 'oben':
        WINDOW.blit(knick_rechts_oben, (px, py))
    elif akt == 'unten' and naechst == 'unten' or akt == 'oben' and naechst == 'oben':
        WINDOW.blit(wegver, (px, py))
    elif akt == 'rechts' and naechst == 'rechts' or akt == 'links' and naechst == 'links':
        WINDOW.blit(weghor, (px, py))
    elif akt == 'rechts' and naechst == 'unten':
        WINDOW.blit(knick_links_unten, (px, py))
    elif akt == 'rechts' and naechst == 'oben' or akt == 'unten' and naechst == 'links':
        WINDOW.blit(knick_links_oben, (px, py))

def abstandzuweg(map,posx,posy):
    if posx < 12 and map[posy, posx + 1] == 8 or posx > 0 and map[posy, posx - 1] == 8 or posy > 0 and map[posy - 1, posx] == 8 or posy < 5 and map[posy + 1, posx] == 8:
        return 1
    elif posx < 11 and map[posy, posx + 2] == 8 or posx > 0 and map[posy, posx - 2] == 8 or posy > 0 and map[posy - 2, posx] == 8 or posy < 4 and map[posy + 2, posx] == 8:
        return 2
    elif posx < 10 and map[posy, posx + 3] == 8 or posx > 0 and map[posy, posx - 3] == 8 or posy > 0 and map[posy - 3, posx] == 8 or posy < 3 and map[posy + 3, posx] == 8:
        return 3
    else:
        return 4
def generiereHindernisse(map):
    k = map
    sum = 0
    while sum <12:
        for y in range(6):
            for x in range(13):
                if k[y,x] == 0:
                    abstand = abstandzuweg(map,x,y)
                    if abstand == 1:
                        value = np.random.randint(0, 100)
                        if value < 5:
                            k[y, x] = 5
                            sum +=1
                    elif abstand == 2:
                        value = np.random.randint(0,100)
                        if value < 20:
                            k[y,x] = 5
                            sum += 1
                    elif abstand == 3:
                        value = np.random.randint(0, 100)
                        if value < 50:
                            k[y, x] = 5
                            sum += 1
                    elif abstand == 4:
                        k[y, x] = 5
                        sum += 1
    return k


def mapladen(mode,zahl):
    global MAP,PFAD
    MAP = generiereHindernisse(np.load(f'maps/{mode}/map ({zahl}).npy'))
    PFAD = guckeweiter([], np.load(f'maps/{mode}/map ({zahl}).npy'), 0, 0)


def mapzeichnen():
    sum = 0
    ty = 0
    for y in range(6):
        tx = 0
        if y > 0:
            tx = 40
        for x in range(13):
            wert = MAP[y, x]
            if wert == 0:
                WINDOW.blit(bauen, (tx, ty))
                tx += 140
            elif wert == 5:
                WINDOW.blit(hindernis, (tx, ty))
                tx += 140
            elif wert == 8:
                richtungsEntscheid(PFAD, sum)
                sum += 1
                tx += 140
            elif wert == 1:
                WINDOW.blit(anfang, (tx, ty))
                tx += 190
            else:
                WINDOW.blit(ende, (tx, ty))
                tx += 140
        ty += 140

def draw_window():
    global WINDOW
    WINDOW.fill((255, 255, 255))
    mapzeichnen()
    pygame.display.update()


def movement(bild, keys_pressed):
    if keys_pressed[pygame.K_LEFT]:
        bild.x -= 1
    if keys_pressed[pygame.K_RIGHT]:
        bild.x += 1
    if keys_pressed[pygame.K_DOWN]:
        bild.y += 1
    if keys_pressed[pygame.K_UP]:
        bild.y -= 1
