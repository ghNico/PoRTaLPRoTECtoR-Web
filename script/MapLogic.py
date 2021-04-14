from Tiles import *
from Tower_Anim import *
import numpy as np
import time

WINDOW = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
MAP = None
PATH = None
starttime = None
FPS = 60
frames = 0
factor = 0
buttons = []
sideinfo = None
pressed = False
running = True
enemy_path = 0
game_state = 1
maps = []


selectedTower = None
selectedTowerField = None

towerfields = []
towerplace_bool = False



# Texturen:
start_map = pygame.transform.scale(pygame.image.load('anfang.png'), (190, 140))
end_map = pygame.transform.scale(pygame.image.load('ende.png'), (190, 140))
way_horizontal = pygame.transform.scale(pygame.image.load("assets/tiles/Gerade.JPG"), (140, 140))
way_vertical = pygame.transform.scale(pygame.transform.rotate(way_horizontal, 90), (140, 140))
clickable_field = pygame.transform.scale(pygame.image.load('bauen.png'), (140, 140))
obstacle_map = pygame.transform.scale(pygame.image.load('hindernis.png'), (140, 140))
curve1 = pygame.transform.scale(pygame.image.load('assets/tiles/Kurve.JPG'), (140, 140))
curve1 = pygame.transform.scale(curve1, (140, 140))
curve2 = pygame.transform.rotate(curve1, 90)
curve3 = pygame.transform.rotate(curve1, 180)
curve4 = pygame.transform.rotate(curve1, 270)

field_mini = pygame.image.load("assets/mini_map/empty_field.png")
way_mini = pygame.image.load("assets/mini_map/way_field.png")

tower_1 = []
tower_2 = []
tower_3 = []
for x in range(1,9):
    tower_1.append(pygame.image.load(f'assets/tower/tower 1 ({x}).png'))
    tower_2.append(pygame.image.load(f'assets/tower/tower 2 ({x}).png'))
    tower_3.append(pygame.image.load(f'assets/tower/tower 3 ({x}).png'))
enemys = []
for x in range(1,2):
    enemys.append(Enemy(0,0,140,140,1,1,0,[pygame.image.load(f"assets/enemys/destroyer ({x}).png")],None))





def create_movement():
    global PATH
    for e in enemys:
        enemy_movement = []
        for k in range(len(PATH)):
            for i in range(0, round(100 / e.velocity)):
                try:
                    diffposx = PATH[k + 1][1] - PATH[k][1]
                    diffposy = PATH[k + 1][2] - PATH[k][2]
                    direction = enemyRotation(PATH[k][0])
                except IndexError:
                    break
                enemy_movement.append((diffposx * (i / round(100 / e.velocity)) + PATH[k][1],
                                       diffposy * (i / round(100 / e.velocity)) + PATH[k][2]))
        e.path = enemy_movement


def startup():
    global WINDOW
    pygame.init()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    pygame.display.set_caption("Tower Defense")
    pygame.display.set_icon(pygame.image.load('icon.png'))


def load_buttons():
    global buttons
    buttons.append(
        Button((255, 0, 0), 1755, 1000, 50, 50, pygame.transform.scale(start_map, (50, 50)), "Spiel beenden"))
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
    global frames, WINDOW
    for e in enemys:
        if frames >= 600:
            try:
                pos = frames - 600
                e.x = 50 + e.path[pos][0] * 140
                e.y = e.path[pos][1] * 140
                e.draw(WINDOW)
            except IndexError:
                print(frames)
                print("Indexerror")
                frames = 0


def draw_mini_map(map, pos_x, pos_y):
    ty = pos_y
    for y in range(6):
        tx = pos_x
        for x in range(13):
            value = map[y, x]
            if value == 0:
                WINDOW.blit(field_mini, (tx, ty))
            elif value == 8 or value == 1 or value == 2:
                WINDOW.blit(way_mini, (tx, ty))
            tx += 45
        ty += 45


def draw_menue():
    global maps, WINDOW
    leicht = [np.random.randint(1, 22661), np.random.randint(1, 22661), np.random.randint(1, 22661)]
    mittel = [np.random.randint(1, 40557), np.random.randint(1, 40557), np.random.randint(1, 40557)]
    schwer = [np.random.randint(1, 24198), np.random.randint(1, 24198), np.random.randint(1, 24198)]
    WINDOW.fill((192, 192, 192))
    pos_y = 200
    for key in leicht:
        map = np.load(f'maps/{"leicht"}/map ({key}).npy')
        draw_mini_map(map, 30, pos_y)
        maps.append(Maps(30, pos_y, 585, 270, key, "leicht"))
        pos_y += 305
    pos_y = 200
    for key in mittel:
        map = np.load(f'maps/{"mittel"}/map ({key}).npy')
        draw_mini_map(map, 670, pos_y)
        maps.append(Maps(670, pos_y, 585, 270, key, "mittel"))
        pos_y += 305
    pos_y = 200
    for key in schwer:
        map = np.load(f'maps/{"schwer"}/map ({key}).npy')
        draw_mini_map(map, 1310, pos_y)
        maps.append(Maps(1310, pos_y, 585, 270, key, "schwer"))
        pos_y += 305





def map_selection():
    global pressed, maps, MAP, PATH, game_state, starttime
    state = pygame.mouse.get_pressed()[0]
    if state and not pressed:
        pressed = True
        for m in maps:
            if m.isOver():
                MAP = GenerateObstacles(np.load(f'maps/{m.difficulty}/map ({m.value}).npy'))
                print("hier")
                PATH = LookAhead([], np.load(f'maps/{m.difficulty}/map ({m.value}).npy'), 0, 0)
                game_state = 0
                load_buttons()
                create_movement()
                starttime = time.time()
    elif not state:
        pressed = False


def display_state():
    if game_state == 0:
        upgrade_Listener()
        draw_window()
        on_action()
        handle_input()
        draw_enemys()
    elif game_state == 1:
        map_selection()
        pass
    else:
        pass



"""
    Für Transparenz:
    ---------------
    tower1 = pygame.image.load('assets/tower/tower (1).png').convert()
    tower1.set_alpha(50)
    von 0-255
"""

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

def enemyRotation(current_pos):
    if current_pos == 'oben':
        return 3
    elif current_pos == 'unten':
        return 1
    elif current_pos == 'rechts':
        return 0
    elif current_pos == 'links':
        return 2


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
    global towerplace_bool, angle, MAP, WINDOW
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


startup()
clock = pygame.time.Clock()
print(PATH)
draw_menue()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display_state()
    pygame.display.update()
    frames += 1
pygame.quit()

