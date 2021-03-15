import pygame
from Button import *
from colour import Color
import numpy as np
import time

WINDOW = None
FPS = 60
rot = Color("red")

# Knopf = Button("HIER STEHT WAS",Beispielbild,pygame.Rect(50, 50, 100, 80)))
# Knopfe = []
# Knopfe.append(Knopf)
Beispielbild = pygame.image.load('anfang.png')
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


#def bauePfad(map):
 #   mx = 0
  #  my = 0
   # value = map[my,mx]
    #if my > 0 and map[my - 1, mx] == 8:
    #    #geht nicht
    #elif my < spielfeldy - 1 and map[my + 1, mx] == 8:
    #    #unten gucke eins weiter
    #elif mx > 0 and map[my, mx - 1] == 8:
    #    #geht nicht
    #elif mx < spielfeldx - 1 and map[my, mx + 1] == 8:
    #    #rechts gucke eins weiter
    #else:
    #    print("Fehler")
    #return wege


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


def draw_window(zufall):
    global WINDOW
    WINDOW.fill((255, 255, 255))
    sum = 0
    map = np.load(f'maps/leicht/map ({zufall}).npy')
    pfad= guckeweiter([],np.load(f'maps/leicht/map ({zufall}).npy'),0,0)
    print(pfad)
    ty = 0
    for y in range(6):
        tx = 0
        if y > 0:
            tx=40
        for x in range(13):

            wert = map[y, x]
            if wert == 0:
                value = np.random.randint(0,100)
                if value > 20:
                    WINDOW.blit(bauen, (tx, ty))
                else:
                    WINDOW.blit(hindernis, (tx, ty))
                tx += 140
            elif wert == 8:
                richtungsEntscheid(pfad,sum)

                sum+=1
                tx += 140
            elif wert == 1:
                WINDOW.blit(anfang, (tx, ty))
                tx += 190
            else:
                WINDOW.blit(ende, (tx, ty))
                tx += 140
        ty += 140
    print(sum)
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


# def handle_bullets(bullets, bild2):
#    for b in bullets:
#        b.x +=5
#        if bild2.colliderect(b):
#            print("TREEEEFFFEEER")
#           bullets.remove(b)
#       elif b.x > :
#           bullets.remove(b)

def maus_press(event):
    global Knopfe
    if event[0] == True:
        for b in Knopfe:
            if b.isOver(pygame.mouse.get_pos()):
                print(pygame.mouse.get_pos())
