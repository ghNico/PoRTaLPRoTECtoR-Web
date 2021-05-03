import pygame

from Tiles import *
from Main_Screen import LoadMainScreen
#from Tower_Anim import *
import numpy as np
import time

# Player Values
Gold = 1000
UserHealth = 100

# Game Values
WINDOW = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
MAP = None
PATH = None
starttime = None
#FPS = 120
frames = 0
game_state = 1
pressed = False
maps = []
wayfields = []
towerfields = []
buttons = []
endscreenButtons = []
sideinfo = None
running = True
enemy_path = 0
selectedTowerToBuild = None
selectedPosition = None
towerplace_bool = False
offset = 0

# Text-Font
font = None
font_headline = None
font_basic = None

# Texturen:
start_map = pygame.transform.scale(pygame.image.load('portal.jpg'), (190, 140))
end_map = pygame.transform.scale(pygame.image.load('portal_red.jpg'), (190, 140))
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
background = pygame.image.load("Galaxy.jpg")
background = pygame.transform.scale(background, (1920, 1080))

# Bullets:
bullet_image = [0 for x in range(8)]
for x in range(1, 9):
    bullet_image[x-1] = (pygame.image.load(f'assets/bullet/bullet {x}.png'))


# wussten nicht wie einfacher geht lul:
tower_image = [[0 for x in range(8)] for y in range(3)]
for x in range(1, 9):
    for y in range(1, 4):
        print((y,x))
        tower_image[y-1][x-1] = (pygame.image.load(f'assets/tower/tower {y} ({x}).png'))

tower_image2 = [[0 for x in range(8)] for y in range(3)]
for x in range(1, 9):
    for y in range(1, 4):
        print((y,x))
        tower_image2[y-1][x-1] = (pygame.image.load(f'assets/tower/gun {y} ({x}).png'))


enemys = []
picture = pygame.image.load(f"assets/enemys/destroyer (1).png")
spawn_offset = []
for i in range(10):
    spawn_offset.append(i*100)
    enemys.append(Enemy(0, 0, 140, 140, 100, 100, 10, 0,
                        [picture, pygame.transform.rotate(picture, 90), pygame.transform.rotate(picture, 180),
                         pygame.transform.rotate(picture, 270)], None))


def create_movement():
    """create_movement
    was tut es

    Arguments:

    Test:
        -wie kann man es testen?

    """
    global PATH
    for e in enemys:
        enemy_movement = []
        for k in range(len(PATH)):
            for i in range(0, round(100 / e.velocity)):
                try:
                    diffposx = PATH[k + 1][1] - PATH[k][1]
                    diffposy = PATH[k + 1][2] - PATH[k][2]
                    direction = enemyRotation(PATH[k+1][0])
                except IndexError:
                    break
                enemy_movement.append((diffposx * (i / round(100 / e.velocity)) + PATH[k][1],
                                       diffposy * (i / round(100 / e.velocity)) + PATH[k][2], direction))
        e.path = enemy_movement


def startup():
    global WINDOW, font, font_headline, font_basic
    pygame.init()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    pygame.display.set_caption("Tower Defense")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    font = pygame.font.SysFont('comicsans', 20)
    font_headline = pygame.font.SysFont('comicsans', 50, True, True)
    font_basic = pygame.font.SysFont('comicsans', 30, True)


def load_buttons():
    global buttons
    buttons.append(
        Button((255, 0, 0), 1755, 1000, 50, 50, pygame.transform.scale(start_map, (50, 50)), "Spiel beenden"))
    print( pygame.transform.scale(tower_image[0][0], (140, 140)))
    print( pygame.transform.scale(tower_image2[0][0], (140, 140)))
    buttons.append(
        Informations(x=260, y=870, width=140, height=140, image=pygame.transform.scale(tower_image[0][0], (140, 140)), image2=pygame.transform.scale(tower_image2[0][0], (140, 140)), costs=450, towerRange=200, damage=15, value=11, headline="Headline", name="Tower 1", description="Description"))
    buttons.append(
        Informations(x=440, y=870, width=140, height=140, image=pygame.transform.scale(tower_image[0][1], (140, 140)), image2=pygame.transform.scale(tower_image2[0][1], (140, 140)), costs=550, towerRange=300, damage=5, value=12, headline="Headline", name="Tower 2", description="Description"))
    buttons.append(
        Informations(620, 870, 140, 140, pygame.transform.scale(tower_image[0][2], (140, 140)), pygame.transform.scale(tower_image2[0][2], (140, 140)), 450, 300, 80, 13, "Headline", "Tower 3", "Description", "schaden"))
    buttons.append(
        Informations(800, 870, 140, 140, pygame.transform.scale(tower_image[0][3], (140, 140)), pygame.transform.scale(tower_image2[0][3], (140, 140)), 450, 200, 80, 14, "Headline", "Tower 4", "Description", "schaden"))
    buttons.append(
        Informations(980, 870, 140, 140, pygame.transform.scale(tower_image[0][4], (140, 140)), pygame.transform.scale(tower_image2[0][4], (140, 140)), 450, 100, 80, 15, "Headline", "Tower 5", "Description", "schaden"))
    buttons.append(
        Informations(1160, 870, 140, 140, pygame.transform.scale(tower_image[0][5], (140, 140)), pygame.transform.scale(tower_image2[0][5], (140, 140)), 450, 100, 80, 16, "Headline", "Tower 6", "Description", "schaden"))
    buttons.append(
        Informations(1340, 870, 140, 140, pygame.transform.scale(tower_image[0][6], (140, 140)), pygame.transform.scale(tower_image2[0][6], (140, 140)), 450, 100, 80, 17, "Headline", "Tower 7", "Description", "schaden"))
    buttons.append(
        Informations(1520, 870, 140, 140, pygame.transform.scale(tower_image[0][7], (140, 140)), pygame.transform.scale(tower_image2[0][7], (140, 140)), 450, 100, 80, 18, "Headline", "Tower 8", "Description", "schaden"))


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
    global WINDOW, UserHealth

    WINDOW.fill((192, 192, 192))
    WINDOW.blit(background, (0,0))
    draw_buttons()
    timetext = pygame.font.SysFont('comicsans', 20).render(str(int(time.time() - starttime)), True, (0, 0, 0))
    WINDOW.blit(timetext, (1800, 1000))
    # Show gold:
    # ------------
    goldText = pygame.font.SysFont('comicsans', 20).render("Gold: ", True, (0, 0, 0))
    goldValue = pygame.font.SysFont('comicsans', 20).render(str(int(Gold)), True, (0, 0, 0))
    WINDOW.blit(goldText, (1750, 900))
    WINDOW.blit(goldValue, (1800, 900))
    # Show Health:
    # ------------
    HealthText = pygame.font.SysFont('comicsans', 20).render("Health: ", True, (0, 0, 0))
    WINDOW.blit(HealthText, (1750, 970))
    actualHealth = 50*UserHealth/100
    pygame.draw.rect(WINDOW, (255, 0, 0), (1800, 970, 50, 15))
    pygame.draw.rect(WINDOW, (0, 255, 0), (1800, 970, actualHealth, 15))




def on_action():
    global buttons, selectedTowerToBuild, selectedPosition, pressed, sideinfo, Gold, tower_image

    state = pygame.mouse.get_pressed()[0]
    if state and not pressed:
        pressed = True
        for k in buttons:
            if k.isOver():
                selectedTowerToBuild = k
        for t in towerfields:
            if t.isOver():
                selectedPosition = t
        if sideinfo.isOver() and selectedPosition is not None:
            if MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] < 30:
                if Gold >= int(sideinfo.costs):
                    MAP[(selectedPosition.y // 140, (selectedPosition.x - 50) // 140)] += 10
                    #[Tower(selectedPosition.x, selectedPosition.y, selectedPosition.width, selectedPosition.height, selectedTowerToBuild.image, selectedTowerToBuild.towerRange, selectedTowerToBuild.damage, selectedTowerToBuild.costs) if value==selectedPosition else value for value in towerfields]
                    selectedPosition.upgrade(tower_image, tower_image2)
                    Gold -= int(sideinfo.costs)
                else:
                    print("Zu wenig Geld")
                selectedTowerToBuild = None
                selectedPosition = None
    elif not state:
        pressed = False


def handle_input():
    global running, selectedTowerToBuild, selectedPosition, MAP, Gold

    if selectedTowerToBuild is not None and selectedPosition is None:
        if selectedTowerToBuild.name == "Spiel beenden":
            running = False
            selectedTowerToBuild = None
            selectedPosition = None
            print("Tower und kein Feld")
    elif selectedTowerToBuild is not None and selectedPosition is not None and MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] == 0:
        if MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] < 30:
            if Gold >= int(selectedTowerToBuild.costs):
                value = 10 + int(selectedTowerToBuild.name[6:])
                #print(selectedTowerToBuild.name)
                print("hier")
                print(selectedTowerToBuild.towerRange)
                MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] = value
                for f in range(len(towerfields)):
                    if towerfields[f] == selectedPosition:
                        print(selectedTowerToBuild.damage)
                        towerfields[f]= Tower(selectedPosition.x, selectedPosition.y, selectedPosition.width, selectedPosition.height,selectedTowerToBuild.image, selectedTowerToBuild.image2,  selectedTowerToBuild.towerRange, selectedTowerToBuild.damage,  value, selectedTowerToBuild.costs)
                        print(towerfields[f].towerRange)
                Gold -= int(selectedTowerToBuild.costs)
            else:
                print("Zu wenig Geld")
            selectedTowerToBuild = None
            selectedPosition = None
        print("Tower und leeres Feld")
    elif selectedTowerToBuild is not None and selectedPosition is not None and MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] != 0 or selectedTowerToBuild is None and selectedPosition is not None and \
            MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] == 0:
        selectedPosition = None
        print("Tower und volles Feld")
    elif selectedTowerToBuild is None and selectedPosition is not None and MAP[
        selectedPosition.y // 140, (selectedPosition.x - 50) // 140] != 0:
        selectedTowerToBuild = None
        print("kein Tower und volles Feld")


def upgrade_Listener():
    global selectedTowerToBuild, selectedPosition, sideinfo, MAP

    if selectedTowerToBuild is not None:
        if "Tower" in selectedTowerToBuild.name:
            sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(selectedTowerToBuild.image, (80, 80)), pygame.transform.scale(selectedTowerToBuild.image2, (80, 80)),
                                    selectedTowerToBuild.costs, selectedTowerToBuild.towerRange, selectedTowerToBuild.damage, selectedTowerToBuild.value,
                                    selectedTowerToBuild.headline, selectedTowerToBuild.name, selectedTowerToBuild.description, selectedTowerToBuild.spm)
    elif selectedTowerToBuild is None and selectedPosition is not None:
        nextstage = MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] + 10
        if 20 < nextstage < 40:
            #print(selectedPosition.value)
            dummie = Tower(selectedPosition.x, selectedPosition.y, selectedPosition.width, selectedPosition.height, selectedPosition.image, selectedPosition.image2, selectedPosition.towerRange, selectedPosition.damage, selectedPosition.value, selectedPosition.costs)
            UpgradeTower = dummie.upgrade(tower_image, tower_image2)
            sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(UpgradeTower.image, (80, 80)), pygame.transform.scale(UpgradeTower.image2, (80, 80)),
                                    UpgradeTower.costs, UpgradeTower.towerRange-selectedPosition.towerRange, UpgradeTower.damage-selectedPosition.damage, UpgradeTower.value,
                                    "Upgrade", "UpgradeTower.name", "UpgradeTower.description", "UpgradeTower.spm")
            #hier auch range
        else:
            sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(tower_image[1][0], (0, 0)), pygame.transform.scale(tower_image2[1][0], (0, 0)), "Upgrades",
                                    "nothing to upgrade", "", "", "", "")
    else:
        sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(tower_image[1][0], (0, 0)), pygame.transform.scale(tower_image2[1][0], (0, 0)), "Upgrades",
                                "nothing selected", "", "", "test", "")



"""
    Für Transparenz:
    ---------------
    tower1 = pygame.image.load('assets/tower/tower (1).png').convert()
    tower1.set_alpha(50)
    von 0-255
"""




# ------------------------------------------------------------------------------------------------------------
# -----------------------------------------Angepasst----------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------

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
        return 1
    elif current_pos == 'unten':
        return 3
    elif current_pos == 'rechts':
        return 0
    elif current_pos == 'links':
        return 2


# Wegtextur wird gezeichnet
def DrawPath(path_pos):
    global WINDOW, wayfields

    current_pos = PATH[path_pos][0]
    next_pos = PATH[path_pos + 1][0]
    pos_x = 50 + (PATH[path_pos][1] * 140)
    pos_y = (PATH[path_pos][2]) * 140
    if current_pos == 'oben' and next_pos == 'rechts' or current_pos == 'links' and next_pos == 'unten':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, curve2))
        # WINDOW.blit(curve2, (pos_x, pos_y))
    elif current_pos == 'oben' and next_pos == 'links' or current_pos == 'rechts' and next_pos == 'unten':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, curve1))
        # WINDOW.blit(curve1, (pos_x, pos_y))
    elif current_pos == 'unten' and next_pos == 'rechts' or current_pos == 'links' and next_pos == 'oben':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, curve3))
        # WINDOW.blit(curve3, (pos_x, pos_y))
    elif current_pos == 'unten' and next_pos == 'unten' or current_pos == 'oben' and next_pos == 'oben':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, way_vertical))
        # WINDOW.blit(way_vertical, (pos_x, pos_y))
    elif current_pos == 'rechts' and next_pos == 'rechts' or current_pos == 'links' and next_pos == 'links':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, way_horizontal))
        # WINDOW.blit(way_horizontal, (pos_x, pos_y))
    elif current_pos == 'rechts' and next_pos == 'oben' or current_pos == 'unten' and next_pos == 'links':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, curve4))
        # WINDOW.blit(curve4, (pos_x, pos_y))


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
def CreationMapObjects():
    global towerplace_bool, angle, MAP, WINDOW, towerfields
    count_ways = 0
    ty = 0
    for y in range(6):
        tx = 0
        if y > 0:
            tx = 50
        for x in range(13):
            value = MAP[y, x]
            if value == 0:
                if not towerplace_bool:
                    towerfields.append(Tiles(tx, ty, 140, 140, clickable_field))
            elif value == 5:
                towerfields.append(Tiles(tx, ty, 140, 140, obstacle_map))
            elif value == 8:
                DrawPath(count_ways)
                count_ways += 1
            elif value == 1:
                towerfields.append(Tiles(tx, ty, 140, 140, start_map))
                tx += 50
            elif value == 2:
                towerfields.append(Tiles(tx, ty, 140, 140, end_map))
            elif value > 10 and value < 39:
                first_place = value % 10
                second_place = value // 10
                towerfields.append(Tiles(tx, ty, 140, 140, tower_image[second_place-1][first_place-1]))
            tx += 140
        ty += 140
    towerplace_bool = True


def DrawMap():
    global WINDOW

    for way in wayfields:
        way.draw(WINDOW)

    for tower in towerfields:
        tower.draw(WINDOW)


def draw_enemys():
    global frames, WINDOW, UserHealth, enemys, spawn_offset, Gold, offset

    i = 0
    while i<(len(enemys)):
        i +=offset
        if frames >= spawn_offset[i]:
            pos = frames - spawn_offset[i]
            if len(enemys[i].path) == pos:
                print(enemys[i])
                if enemys[i].health >0:
                    UserHealth -= 10
                e = enemys[i]
                enemys.remove(e)
                offset +=1
            else:
                print(i)
                enemys[i].direction = enemys[i].path[pos][2]
                enemys[i].x = 50 + enemys[i].path[pos][0] * 140
                enemys[i].y = enemys[i].path[pos][1] * 140
                enemys[i].updateRect()
                enemys[i].draw(WINDOW)
        i += 1
    if len(enemys) == 0:
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



# Operativen Systeme:
def draw_menue():
    global maps, WINDOW, font_headline, font_basic

    leicht = [np.random.randint(1, 22661), np.random.randint(1, 22661), np.random.randint(1, 22661)]
    mittel = [np.random.randint(1, 40557), np.random.randint(1, 40557), np.random.randint(1, 40557)]
    schwer = [np.random.randint(1, 24198), np.random.randint(1, 24198), np.random.randint(1, 24198)]
    # WINDOW.fill((192, 192, 192))
    WINDOW.blit(background, (0,0))
    # Headline:
    headline = font_headline.render("Select a Map", True, (250, 250, 250))
    WINDOW.blit(headline, (960 - (headline.get_width()//2), 50))
    pos_y = 175
    basic = font_basic.render("Easy", True, (250, 250, 250))
    WINDOW.blit(basic, (300 - (basic.get_width() // 2), 125))
    for key in leicht:
        map = np.load(f'maps/{"leicht"}/map ({key}).npy')
        draw_mini_map(map, 30, pos_y)
        maps.append(Maps(30, pos_y, 585, 270, key, "leicht"))
        pos_y += 305
    pos_y = 175
    basic = font_basic.render("Medium", True, (250, 250, 250))
    WINDOW.blit(basic, (950 - (basic.get_width() // 2), 125))
    for key in mittel:
        map = np.load(f'maps/{"mittel"}/map ({key}).npy')
        draw_mini_map(map, 670, pos_y)
        maps.append(Maps(670, pos_y, 585, 270, key, "mittel"))
        pos_y += 305
    pos_y = 175
    basic = font_basic.render("Hard", True, (250, 250, 250))
    WINDOW.blit(basic, (1600 - (basic.get_width() // 2), 125))
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
                PATH = LookAhead([], np.load(f'maps/{m.difficulty}/map ({m.value}).npy'), 0, 0)
                game_state = 0
                load_buttons()
                create_movement()
                CreationMapObjects()
                starttime = time.time()
        print(MAP)
    elif not state:
        pressed = False


def draw_endscreen():
    global maps, WINDOW

    WINDOW.fill((192, 192, 192))
    GameOverText = pygame.font.SysFont('comicsans', 100, True, True).render("Game Over", True, (0, 0, 0))
    WINDOW.blit(GameOverText, (960-GameOverText.get_width()//2, 540-GameOverText.get_height()//2))

    if endscreenButtons == []:
        endscreenButtons.append(Button((255,0,0), 960 -50, 640, 100, 100 , pygame.transform.scale(start_map, (100, 100))))
    for btn in endscreenButtons:
        btn.draw(WINDOW)


def display_endscreen():
    global pressed, MAP, PATH, game_state, starttime

    draw_endscreen()
    state = pygame.mouse.get_pressed()[0]
    if state and not pressed:
        pressed = True
        for btn in endscreenButtons:
            if btn.isOver():
                ReInit()
                draw_menue()
                game_state = 1
    elif not state:
        pressed = False


def drawTowerRange():
    for t in towerfields:
        if t.isOver():
            t.showRange(WINDOW)



def ReInit():
    global Gold, WINDOW, MAP, PATH, starttime, frames, game_state, pressed, maps, wayfields, towerfields, buttons, endscreenButtons, sideinfo, running, enemy_path, selectedEnemy, selectedTowerToBuild, selectedPosition, towerplace_bool, UserHealth

    # Player Values
    Gold = 1000
    UserHealth = 100

    # Game Values
    WINDOW = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
    MAP = None
    PATH = None
    starttime = None
    # FPS = 120
    frames = 0
    game_state = 1
    pressed = False
    maps = []
    wayfields = []
    towerfields = []
    buttons = []
    endscreenButtons = []
    sideinfo = None
    running = True
    enemy_path = 0
    selectedTowerToBuild = None
    selectedPosition = None
    towerplace_bool = False


def allTowerShootes():
    global towerfields, frames

    if frames%10 == 0:
        for t in towerfields:
            # hier nur wenn Tower (!= NONE)
            if t.getValue() != None:
                bulletValue = t.getValue()%10 - 1
                print("hier")
                print(bulletValue)
                t.findEnemys(enemys, bullet_image[bulletValue])


    for t in towerfields:
        towerBullets = t.getTowerLst()
        if towerBullets != None and towerBullets != []:
            for e in enemys:
                if e.image != None:
                    e.checkCollide(towerBullets)



def display_state():
    global frames, Gold, game_state, WINDOW

    if game_state == 0:
        upgrade_Listener()
        handle_input()
        draw_window()
        DrawMap()
        on_action()
        draw_enemys()
        allTowerShootes()
        frames += 1
        Gold += 0.8
        if UserHealth <= 0:
            game_state = 2
        drawTowerRange()
        #print(1/((time.time()-starttime)/frames))
    elif game_state == 1:
        #,
        # LoadMainScreen(win=WINDOW)
        map_selection()
    elif game_state == 2:
        display_endscreen()
    else:
        pass


startup()
#clock = pygame.time.Clock()
print(PATH)
draw_menue()
while running:
    #clock.tick(FPS)
    #time.sleep(0.0666)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display_state()
    pygame.display.update()
pygame.quit()
