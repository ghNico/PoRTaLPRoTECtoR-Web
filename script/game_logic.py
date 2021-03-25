from Tiles import *
from Tower_Anim import *
from MapLogic import *
import numpy as np
import time

starttime = time.time()

FPS = 60

buttons = []
sideinfo = None
pressed = False
running = True


def startup():
    global WINDOW
    pygame.init()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    pygame.display.set_caption("Tower Defense")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    load_buttons()


def load_buttons():
    global buttons
    buttons.append(Button((255,0,0), 1755, 1000, 50, 50, pygame.transform.scale(start_map, (50, 50)), "Spiel beenden"))
    buttons.append(
        Informations(260, 870, 140, 140, pygame.transform.scale(tower_1[0], (140, 140)), "", "Tower 1",
                     "Shoots bullets",
                     "10 shots per minute", "450G"))
    buttons.append(
        Informations(440, 870, 140, 140, pygame.transform.scale(tower_1[1], (140, 140)), "", "Tower 2", "450G"))
    buttons.append(
        Informations(620, 870, 140, 140, pygame.transform.scale(tower_1[2], (140, 140)), "", "Tower 3", "450G"))
    buttons.append(
        Informations(800, 870, 140, 140, pygame.transform.scale(tower_1[3], (140, 140)), "", "Tower 4", "450G"))
    buttons.append(
        Informations(980, 870, 140, 140, pygame.transform.scale(tower_1[4], (140, 140)), "", "Tower 5", "450G"))
    buttons.append(
        Informations(1160, 870, 140, 140, pygame.transform.scale(tower_1[5], (140, 140)), "", "Tower 6", "450G"))
    buttons.append(
        Informations(1340, 870, 140, 140, pygame.transform.scale(tower_1[6], (140, 140)), "", "Tower 7", "450G"))
    buttons.append(
        Informations(1520, 870, 140, 140, pygame.transform.scale(tower_1[7], (140, 140)), "", "Tower 8", "450G"))


def animate():
    global moving_sprites, WINDOW

    # tower = Tower(100, 300, 140, 140, pygame.transform.scale(tower1, (140, 140)))

    # tower.draw(WINDOW)


def draw_buttons():
    global WINDOW, sideinfo

    for k in buttons:
        k.draw(WINDOW)

    sideinfo.draw(WINDOW)



def draw_window():
    global WINDOW

    WINDOW.fill((192, 192, 192))
    DrawMap()
    draw_buttons()
    timetext = pygame.font.SysFont('comicsans', 20).render(str(int(time.time() - starttime)), True, (0, 0, 0))
    WINDOW.blit(timetext, (1800, 1000))

    # moving_sprites.update()


def on_action():
    global buttons, selectedTower, selectedTowerField, pressed, sideinfo
    state = pygame.mouse.get_pressed()[0]
    if state and not pressed:
        pressed = True
        for k in buttons:
            if k.isOver():
                selectedTower = k
        for t in towerfields:
            if t.isOver():
                selectedTowerField = t
        if sideinfo.isOver() and selectedTowerField != None:
            print("upgrade")
            print(selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140)
            if MAP[selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] < 30:
                MAP[(selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140)] += 10
                selectedTower = None
                selectedTowerField = None
    elif not state:
        pressed = False


def handle_input():
    global running, selectedTower, selectedTowerField, MAP

    if selectedTower is not None and selectedTowerField is None:
        if selectedTower.name == "Spiel beenden":
            running = False
            selectedTower = None
            selectedTowerField = None
            print("Tower und kein Feld")
    elif selectedTower is not None and selectedTowerField is not None and MAP[
        selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] == 0:
        if MAP[selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] < 30:
            MAP[selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] = 10 + int(selectedTower.name[6:])
            selectedTower = None
            selectedTowerField = None
        print("Tower und leeres Feld")
    elif selectedTower is not None and selectedTowerField is not None and MAP[selectedTowerField.y // 140, (
            selectedTowerField.x - 50) // 140] != 0 or selectedTower is None and selectedTowerField is not None and \
            MAP[selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] == 0:
        selectedTowerField = None
        print("Tower und volles Feld")
    elif selectedTower is None and selectedTowerField is not None and MAP[
        selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] != 0:
        selectedTower = None
        print("kein Tower und volles Feld")
        print(MAP)


def upgrade_Listener():
    global selectedTower, selectedTowerField, sideinfo, MAP

    if selectedTower is not None and selectedTowerField is None or selectedTower is not None and selectedTowerField is not None:
        if "Tower" in selectedTower.name:
            sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(selectedTower.image, (80, 80)),
                                        "Information", selectedTower.name, selectedTower.description, selectedTower.spm,
                                    selectedTower.costs)
    elif selectedTower is None and selectedTowerField is not None:
        nextstage = MAP[selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] + 10
        if 20 < nextstage < 30:
            sideinfo = Informations(80, 900, 100, 100,
                                    pygame.transform.scale(tower_2[(nextstage - 1) % 10], (80, 80)), "Upgrade",
                                        "Tower 2", "Upgrades Range", "+10", "500")
        elif 30 < nextstage < 40:
            sideinfo = Informations(80, 900, 100, 100,
                                    pygame.transform.scale(tower_3[(nextstage - 1) % 10], (80, 80)), "Upgrade",
                                        "Tower 3", "Upgrades Range", "+20", "1000")
        else:
            sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(tower_1[0], (0, 0)), "Upgrades",
                                        "nothing to upgrade")
    else:
        sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(tower_1[0], (0, 0)), "Upgrades",
                                    "nothing selected")


def draw_enemys():
    pass


startup()
clock = pygame.time.Clock()
print(PATH)
# animate()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    upgrade_Listener()
    draw_window()
    on_action()
    handle_input()
    draw_enemys()
    pygame.display.update()
pygame.quit()

"""
    Für Transparenz:
    ---------------
    tower1 = pygame.image.load('assets/tower/tower (1).png').convert()
    tower1.set_alpha(50)
    von 0-255
"""
