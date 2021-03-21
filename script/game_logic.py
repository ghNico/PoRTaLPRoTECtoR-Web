from Tiles import *
from Tower_Anim import *
from MapLogic import *
import numpy as np
import time
startzeit = time.time()



FPS = 60
rot = (255, 0, 0)

moving_sprites = pygame.sprite.Group()





knoepfe = []
UpgradeKnopf = None
gedrückt = False

running = True




def startup():
    global WINDOW
    pygame.init()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    pygame.display.set_caption("Tower Defense")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    knoepfeladen()




def knoepfeladen():
    global knoepfe
    knoepfe.append(Button(rot, 1755, 1000, 50, 50, pygame.transform.scale(anfang, (50,50)), "Spiel beenden"))
    knoepfe.append(Informations(260, 870, 140, 140, pygame.transform.scale(tower1, (140, 140)), "", "Tower 1", "Shoots bullets", "10 shots per minute", "450G"))
    knoepfe.append(Informations(440, 870, 140, 140, pygame.transform.scale(tower2, (140, 140)), "", "Tower 2", "450G"))
    knoepfe.append(Informations(620, 870, 140, 140, pygame.transform.scale(tower3, (140, 140)), "", "Tower 3", "450G"))
    knoepfe.append(Informations(800, 870, 140, 140, pygame.transform.scale(tower4, (140, 140)), "", "Tower 4", "450G"))
    knoepfe.append(Informations(980, 870, 140, 140, pygame.transform.scale(tower5, (140, 140)), "", "Tower 5", "450G"))
    knoepfe.append(Informations(1160, 870, 140, 140, pygame.transform.scale(tower6, (140, 140)), "", "Tower 6", "450G"))
    knoepfe.append(Informations(1340, 870, 140, 140, pygame.transform.scale(tower7, (140, 140)), "", "Tower 7", "450G"))
    knoepfe.append(Informations(1520, 870, 140, 140, pygame.transform.scale(tower8, (140, 140)), "", "Tower 8", "450G"))




def animate():
    global moving_sprites, WINDOW

    #tower = Tower(100, 300, 140, 140, pygame.transform.scale(tower1, (140, 140)))

    #tower.draw(WINDOW)
    #moving_sprites.Tower_Anim.add(tower)


def knoepfezeichnen():
    global WINDOW, UpgradeKnopf

    for k in knoepfe:
        k.draw(WINDOW)

    UpgradeKnopf.draw(WINDOW)


def begrenzungzeichnen():
    global WINDOW
    pygame.draw.line(WINDOW, (0, 0, 0), (0, 845), (1920, 845), 5)


def draw_window():
    global WINDOW

    WINDOW.fill((192, 192, 192))
    DrawMap()
    begrenzungzeichnen()
    knoepfezeichnen()
    timetext = pygame.font.SysFont('comicsans', 20).render(str(int(time.time()-startzeit)), True, (0, 0, 0))
    WINDOW.blit(timetext, (1800,1000))

    #moving_sprites.update()


def on_action():
    global knoepfe, selectedTower, selectedTowerField, gedrückt, UpgradeKnopf
    state = pygame.mouse.get_pressed()[0]
    if state and not gedrückt:
        gedrückt = True
        for k in knoepfe:
            if k.isOver():
                selectedTower = k
        for t in turmfelder:
            if t.isOver():
                selectedTowerField = t
        if UpgradeKnopf.isOver():
                print("upgrade")
                print(selectedTowerField.y//140,(selectedTowerField.x-50)//140)
                MAP[(selectedTowerField.y//140,(selectedTowerField.x-50)//140)] += 10
                selectedTower = None
                selectedTowerField = None
    elif not state:
        gedrückt = False


def handle_input():
    global running, selectedTower, selectedTowerField

    if selectedTower != None and selectedTowerField == None:
        if selectedTower.name == "Spiel beenden":
            running = False
            selectedTower = None
            selectedTowerField = None
            #print("Tower und kein Feld")
    elif selectedTower != None and selectedTowerField != None and MAP[selectedTowerField.y//140, (selectedTowerField.x-50)//140] == 0:
            MAP[selectedTowerField.y//140,(selectedTowerField.x-50)//140] = 10 + int(selectedTower.name[6:])
            selectedTower = None
            selectedTowerField = None
            #print("Tower und leeres Feld")
    elif selectedTower != None and selectedTowerField != None and MAP[selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] != 0:
            selectedTowerField = None
            #print("Tower und volles Feld")
    elif selectedTower == None and selectedTowerField != None and MAP[selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] != 0:
            selectedTower = None
            #print("kein Tower und volles Feld")
    elif selectedTower == None and selectedTowerField != None and MAP[selectedTowerField.y // 140, (selectedTowerField.x - 50) // 140] == 0:
            selectedTowerField = None
            #print("kein Tower und leeres Feld")




def upgrade_Listener():
    global selectedTower, selectedTowerField, UpgradeKnopf

    if selectedTower != None and selectedTowerField == None or selectedTower != None and selectedTowerField != None:
        if "Tower" in selectedTower.name:
            UpgradeKnopf = Informations(80, 900, 100, 100, pygame.transform.scale(selectedTower.image, (80, 80)), "Information", selectedTower.name, selectedTower.description, selectedTower.spm, selectedTower.costs)
    elif selectedTower == None and selectedTowerField != None:
            nextStage = MAP[selectedTowerField.y//140, (selectedTowerField.x-50)//140] + 10
            if (nextStage == 21):
                UpgradeKnopf = Informations(80, 900, 100, 100, pygame.transform.scale(tower1_2, (80, 80)), "Upgrade", "Tower 1", "Upgrades Range", "+10", "500")
    else:
        UpgradeKnopf = Informations(80, 900, 100, 100, pygame.transform.scale(tower1, (0, 0)), "Upgrades", "nothing selected")






startup()
clock = pygame.time.Clock()

animate()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    upgrade_Listener()
    draw_window()
    on_action()
    handle_input()
    pygame.display.update()
pygame.quit()


"""
    Für Transparenz:
    ---------------
    tower1 = pygame.image.load('assets/tower/tower (1).png').convert()
    tower1.set_alpha(50)
    von 0-255
"""
