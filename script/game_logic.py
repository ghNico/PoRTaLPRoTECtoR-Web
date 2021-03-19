from Tiles import *
import numpy as np
import time
startzeit = time.time()

WINDOW = None
MAP = None
PFAD = None
FPS = 60
rot = (255, 0, 0)
knoepfe = []
gedrückt = False
actionlist = []
running = True
turmfelder = []
turmfelder_gesetzt = False

anfang = pygame.image.load('anfang.png')
ende = pygame.image.load('ende.png')
weghor = pygame.image.load('weg_gerade.png')
wegver = pygame.transform.rotate(weghor, 90)
bauen = pygame.image.load('bauen.png')
hindernis = pygame.image.load('hindernis.png')
knick_links_unten = pygame.image.load('weg_knick.png')
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


def guckeweiter(weg, map, altx, alty):
    map[alty, altx] = 0
    if altx < 12 and map[alty, altx + 1] == 8:  # rechts
        weg.append(("rechts", altx + 1, alty))
        guckeweiter(weg, map, altx + 1, alty)
    elif altx > 0 and map[alty, altx - 1] == 8:  # links
        weg.append(("links", altx - 1, alty))
        guckeweiter(weg, map, altx - 1, alty)
    elif alty > 0 and map[alty - 1, altx] == 8:  # oben
        weg.append(("oben", altx, alty - 1))
        guckeweiter(weg, map, altx, alty - 1)
    elif alty < 5 and map[alty + 1, altx] == 8:  # unten
        weg.append(("unten", altx, alty + 1))
        guckeweiter(weg, map, altx, alty + 1)
    elif altx < 12 and map[alty, altx + 1] == 2:  # rechts
        weg.append(("rechts", altx + 1, alty))
    elif altx > 0 and map[alty, altx - 1] == 2:  # links
        weg.append(("links", altx - 1, alty))
    elif alty > 0 and map[alty - 1, altx] == 2:  # oben
        weg.append(("oben", altx, alty - 1))
    elif alty < 5 and map[alty + 1, altx] == 2:  # unten
        weg.append(("unten", altx, alty + 1))
    return weg


def startup(width, height):
    global WINDOW
    pygame.init()
    WINDOW = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    pygame.display.set_caption("Tower Defense")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    mapladen('schwer', np.random.randint(1, 20000))
    knoepfeladen()


def richtungsEntscheid(sum):
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
        WINDOW.blit(wegver, (px, py))
    elif akt == 'rechts' and naechst == 'rechts' or akt == 'links' and naechst == 'links':
        WINDOW.blit(weghor, (px, py))
    elif akt == 'rechts' and naechst == 'unten':
        WINDOW.blit(knick_links_unten, (px, py))
    elif akt == 'rechts' and naechst == 'oben' or akt == 'unten' and naechst == 'links':
        WINDOW.blit(knick_links_oben, (px, py))


def abstandzuweg(map, posx, posy):
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


def generiereHindernisse(map):
    k = map
    sum = 0
    while sum < 12:
        for y in range(6):
            for x in range(13):
                if k[y, x] == 0:
                    abstand = abstandzuweg(map, x, y)
                    value = np.random.randint(0, 100)
                    if abstand == 1 and value < 5 or abstand == 2 and value < 20 or abstand == 3 and value < 50 or abstand == 4:
                        k[y, x] = 5
                        sum += 1
    return k


def mapladen(mode, zahl):
    global MAP, PFAD
    MAP = generiereHindernisse(np.load(f'maps/{mode}/map ({zahl}).npy'))
    PFAD = guckeweiter([], np.load(f'maps/{mode}/map ({zahl}).npy'), 0, 0)


def knoepfeladen():
    global knoepfe
    knoepfe.append(Button(rot, 1755, 1000, 50, 50, pygame.transform.scale(anfang, (50,50)), "Spiel beenden"))
    knoepfe.append(Informations(260, 870, 140, 140, pygame.transform.scale(tower1, (140, 140)), "", "Tower 1", "450G"))
    knoepfe.append(Informations(440, 870, 140, 140, pygame.transform.scale(tower2, (140, 140)), "", "Tower 2", "450G"))
    knoepfe.append(Informations(620, 870, 140, 140, pygame.transform.scale(tower3, (140, 140)), "", "Tower 3", "450G"))
    knoepfe.append(Informations(800, 870, 140, 140, pygame.transform.scale(tower4, (140, 140)), "", "Tower 4", "450G"))
    knoepfe.append(Informations(980, 870, 140, 140, pygame.transform.scale(tower5, (140, 140)), "", "Tower 5", "450G"))
    knoepfe.append(Informations(1160, 870, 140, 140, pygame.transform.scale(tower6, (140, 140)), "", "Tower 6", "450G"))
    knoepfe.append(Informations(1340, 870, 140, 140, pygame.transform.scale(tower7, (140, 140)), "", "Tower 7", "450G"))
    knoepfe.append(Informations(1520, 870, 140, 140, pygame.transform.scale(tower8, (140, 140)), "", "Tower 8", "450G"))
    knoepfe.append(Informations(70, 900, 100, 100, pygame.transform.scale(tower1, (100,100)), "Upgrades", "test", "test"))


def mapzeichnen():
    global turmfelder_gesetzt
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
                richtungsEntscheid(sum)
                sum += 1
            elif wert == 1:
                WINDOW.blit(anfang, (tx, ty))
                tx += 50
            elif wert == 2:
                WINDOW.blit(ende, (tx, ty))
            elif wert == 11:
                WINDOW.blit(tower1, (tx, ty))
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
            tx += 140
        ty += 140
    turmfelder_gesetzt = True


def knoepfezeichnen():
    global WINDOW

    for k in knoepfe:
        k.draw(WINDOW)


def begrenzungzeichnen():
    global WINDOW
    pygame.draw.line(WINDOW, (0, 0, 0), (0, 845), (1920, 845), 5)


def draw_window():
    global WINDOW
    WINDOW.fill((192, 192, 192))
    mapzeichnen()
    begrenzungzeichnen()
    knoepfezeichnen()
    timetext = pygame.font.SysFont('comicsans', 20).render(str(int(time.time()-startzeit)), True, (0, 0, 0))
    WINDOW.blit(timetext, (1800,1000))
    pygame.display.update()


def on_action():
    global knoepfe, gedrückt, actionlist
    state = pygame.mouse.get_pressed()[0]
    if state and not gedrückt:
        gedrückt = True
        for k in knoepfe:
            if k.isOver():
                actionlist.append(k.text1)
        for t in turmfelder:
            if t.isOver():
                actionlist.append(("Turmfeld",t.x,t.y))
    elif not state:
        gedrückt = False


def handle_input():
    global actionlist, running
    if len(actionlist) == 1:
        if actionlist[0] == "Spiel beenden":
            running = False
            actionlist.remove(actionlist[0])
    elif len(actionlist) == 2:
        if "Tower" in actionlist[0] and "Tower" in actionlist[1]:
            actionlist.remove(actionlist[0])
        elif actionlist[1] == "Spiel beenden":
            print("SPIEEEL BEEENDEN")
            running = False
        elif "Tower" in actionlist[1]:
            print("JA HIER")
            actionlist.remove(actionlist[0])
        elif "Turmfeld" in actionlist[1][0] and "Tower" in actionlist[0]:
            MAP[actionlist[1][2]//140,(actionlist[1][1]-50)//140] = 10 + int(actionlist[0][6:])
            print(MAP)
            actionlist.remove(actionlist[1])
            actionlist.remove(actionlist[0])
        else:
            pass


startup(1920, 1080)
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_window()
    on_action()
    handle_input()
pygame.quit()
