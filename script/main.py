"""
PoRTaLPRoTECtoR
Infinite Tower Defense Game
Attributes:
    Author: Niclas Hörber (NiclasHoerber) and Nico Fischer (ghNico)
    Version: 1.0.0
    license: free but tell us about your usage so we know under niroma2000@gmail.com
    Available via Github: https://github.com/NiclasHoerber/PoRTaLPRoTECtoR
"""
import asyncio

from Tiles import *
from Main_Screen import LoadMainScreen
from Drawing import *
from Helper import *
import numpy as np
import time

# Player Values
Gold = 1000
UserHealth = 100

# Game Values
WINDOW = pygame.display.set_mode((1440, 1440));
MAP = None
PATH = None
starttime = None
frames = 0
game_state = 0
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
wave = 1
enemys = []
spawn_offset = []

# Text-Font
font = None
font_headline = None
font_basic = None

# Textures:
restart = pygame.transform.scale(pygame.image.load("assets/environment/restart.jpg"),(160,160))
exitimage = pygame.transform.scale(pygame.image.load("assets/environment/exit.jpg"),(160,160))
start_map = pygame.transform.scale(pygame.image.load('assets/environment/portal.png'), (160, 160))
end_map = pygame.transform.scale(pygame.image.load('assets/environment/portal_red.png'), (160, 160))
way_horizontal = pygame.transform.scale(pygame.image.load("assets/tiles/Gerade.png"), (160, 160))
way_vertical = pygame.transform.scale(pygame.transform.rotate(way_horizontal, 90), (160, 160))
clickable_field = pygame.transform.scale(pygame.image.load('assets/environment/bauen.png'), (160, 160))
obstacle_map = pygame.transform.scale(pygame.image.load('assets/environment/hindernis.png'), (160, 160))
curve1 = pygame.transform.scale(pygame.image.load('assets/tiles/Kurve.png'), (160, 160))
curve2 = pygame.transform.rotate(curve1, 90)
curve3 = pygame.transform.rotate(curve1, 180)
curve4 = pygame.transform.rotate(curve1, 270)
field_mini = pygame.image.load("assets/mini_map/empty_field.png")
way_mini = pygame.image.load("assets/mini_map/way_field.png")
background = pygame.image.load("assets/environment/Galaxy.png")
background = pygame.transform.scale(background, (1440, 1440))

# Sound:
shootSound = None
backgroundMusic = None

# Bullets:
bullet_image = [0 for x in range(8)]
for x in range(1, 9):
    bullet_image[x - 1] = (pygame.image.load(f'assets/bullet/bullet {x}.png'))

# Tower:
tower_image = [[0 for x in range(8)] for y in range(3)]
for x in range(1, 9):
    for y in range(1, 4):
        tower_image[y - 1][x - 1] = (pygame.image.load(f'assets/tower/tower 1 (1).png'))

# Guns:
tower_image2 = [[0 for x in range(8)] for y in range(3)]
for x in range(1, 9):
    for y in range(1, 4):
        tower_image2[y - 1][x - 1] = (pygame.image.load(f'assets/tower/gun {y} ({x}).png'))

# Enemys:
picture = pygame.transform.scale(pygame.image.load(f"assets/enemys/destroyer ({2 - (wave % 2)}).png"), (160, 160))

for i in range(10):
    spawn_offset.append(i * 25)
    enemys.append(Enemy(0, 0, 160, 160, 100, 100, 5, 0,
                        [picture, pygame.transform.rotate(picture, 90), pygame.transform.rotate(picture, 180),
                         pygame.transform.rotate(picture, 270)], None))


def startup():
    """
    Initialization of pygame

    """
    global WINDOW, font, font_headline, font_basic, shootSound, backgroundMusic
    pygame.init()
    shootSound = pygame.mixer.Sound("assets/sounds/pew.ogg")
    shootSound.set_volume(0.05)
    pygame.mixer.music.load("assets/sounds/music.ogg")
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play(-1)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    pygame.display.set_caption("PoRTaL PRoTECtoR")
    pygame.display.set_icon(pygame.image.load('assets/icon.png'))
    font = pygame.font.SysFont('comicsans', 20)
    font_headline = pygame.font.SysFont('comicsans', 50, True, True)
    font_basic = pygame.font.SysFont('comicsans', 30, True)


def load_buttons():
    """
    Set the list of buttons with all values of the towers and generate the objects

    Test:
        -screen resolution 1920x1080
        -all values have to be balanced for the game

    """
    global buttons
    buttons.append(
        Informations(x=400, y=1300, width=160, height=160, image=pygame.transform.scale(tower_image[0][0], (160, 160)),
                     image2=pygame.transform.scale(tower_image2[0][0], (160, 160)), costs=250, towerRange=200,
                     damage=30, value=11, headline="Frost", name="Tower 1", description="Out of the Iceage"))
    buttons.append(
        Informations(x=560, y=1300, width=160, height=160, image=pygame.transform.scale(tower_image[0][1], (160, 160)),
                     image2=pygame.transform.scale(tower_image2[0][1], (160, 160)), costs=300, towerRange=225, damage=35,
                     value=12, headline="Inferno", name="Tower 2", description="Iron Dome (Israel)"))
    buttons.append(
        Informations(720, 1300, 160, 160, pygame.transform.scale(tower_image[0][3], (160, 160)),
                     pygame.transform.scale(tower_image2[0][3], (160, 160)), 350, 275, 45, 14, "Devil", "Tower 4",
                     "Not a real sparrow"))
    buttons.append(
        Informations(880, 1300, 160, 160, pygame.transform.scale(tower_image[0][4], (160, 160)),
                     pygame.transform.scale(tower_image2[0][4], (160, 160)), 375, 300, 50, 15, "Alfi Deluxe", "Tower 5",
                     "mit 1.0 bestanden ;)"))
    buttons.append(
        Informations(1040, 1300, 160, 160, pygame.transform.scale(tower_image[0][5], (160, 160)),
                     pygame.transform.scale(tower_image2[0][5], (160, 160)), 400, 325, 55, 16, "Mega Blizzard", "Tower 6",
                     "Really Cold"))


def on_action():
    """

    When mouse is pressed over tower or sideinfo or buttons, checks and prepare the ingame values for the handle_input function

    Test:
        -objects need isOver function
        -every element is 160x160 and the map need to contain the value of tower to level up

    """
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
            if MAP[selectedPosition.y // 160, (selectedPosition.x - 50) // 160] < 30:
                if Gold >= int(sideinfo.costs):
                    MAP[(selectedPosition.y // 160, (selectedPosition.x - 50) // 160)] += 10
                    #logger.info("Towerupgrade")
                    selectedPosition.upgrade(tower_image, tower_image2)
                    Gold -= int(sideinfo.costs)
                selectedTowerToBuild = None
                selectedPosition = None
    elif not state:
        pressed = False


def handle_input():
    """
    Based on the User clicks and the preparation of the on_action function the User interact with the game

    Game could be closed

    A Tower is selected and placed if enough gold is in the wallet

    Test:
        -to handle 2 clicks 4 different cases can raise errors
        -all is based on 160x160 Tiles so test the Tiles size for correct selection

    """
    global running, selectedTowerToBuild, selectedPosition, MAP, Gold

    if selectedTowerToBuild is not None and selectedPosition is None:
        if selectedTowerToBuild.name == "game stop":
            running = False
            #logger.info("End Game")
            selectedTowerToBuild = None
            selectedPosition = None
    elif selectedTowerToBuild is not None and selectedPosition is not None and MAP[
        selectedPosition.y // 160, (selectedPosition.x - 50) // 160] == 0:
        if MAP[selectedPosition.y // 160, (selectedPosition.x - 50) // 160] < 30:
            if Gold >= int(selectedTowerToBuild.costs):
                value = 10 + int(selectedTowerToBuild.name[6:])
                MAP[selectedPosition.y // 160, (selectedPosition.x - 50) // 160] = value
                for f in range(len(towerfields)):
                    if towerfields[f] == selectedPosition:
                        towerfields[f] = Tower(selectedPosition.x, selectedPosition.y, selectedPosition.width,
                                               selectedPosition.height, selectedTowerToBuild.image,
                                               selectedTowerToBuild.image2, selectedTowerToBuild.towerRange,
                                               selectedTowerToBuild.damage, value, selectedTowerToBuild.costs)
                Gold -= int(selectedTowerToBuild.costs)
                #logger.info(f"Tower build {selectedTowerToBuild.name}")
            selectedTowerToBuild = None
            selectedPosition = None
    elif selectedTowerToBuild is not None and selectedPosition is not None and MAP[selectedPosition.y // 160, (selectedPosition.x - 50) // 160] != 0 or selectedTowerToBuild is None and selectedPosition is not None and MAP[selectedPosition.y // 160, (selectedPosition.x - 50) // 160] == 0:
        selectedPosition = None
    elif selectedTowerToBuild is None and selectedPosition is not None and MAP[
        selectedPosition.y // 160, (selectedPosition.x - 50) // 160] != 0:
        selectedTowerToBuild = None


def upgrade_Listener():
    """

    The sideinfo contains new information based on which element is selected based on the clicks of User

    Test:
        -All needed information has to be in button object or tower object
        -sideinfo object has to contain and store the information of two different objects

    """
    global selectedTowerToBuild, selectedPosition, sideinfo, MAP

    if selectedTowerToBuild is not None:
        if "Tower" in selectedTowerToBuild.name:
            sideinfo = Informations(80, 1300, 100, 100, pygame.transform.scale(selectedTowerToBuild.image, (80, 80)),
                                    pygame.transform.scale(selectedTowerToBuild.image2, (80, 80)),
                                    selectedTowerToBuild.costs, selectedTowerToBuild.towerRange,
                                    selectedTowerToBuild.damage, selectedTowerToBuild.value,
                                    selectedTowerToBuild.headline, selectedTowerToBuild.name,
                                    selectedTowerToBuild.description)
    elif selectedTowerToBuild is None and selectedPosition is not None:
        nextstage = MAP[selectedPosition.y // 160, (selectedPosition.x - 50) // 160] + 10
        if 20 < nextstage < 40:
            dummie = Tower(selectedPosition.x, selectedPosition.y, selectedPosition.width, selectedPosition.height,
                           selectedPosition.image, selectedPosition.image2, selectedPosition.towerRange,
                           selectedPosition.damage, selectedPosition.value, selectedPosition.costs)
            UpgradeTower = dummie.upgrade(tower_image, tower_image2)
            sideinfo = Informations(80, 1300, 100, 100, pygame.transform.scale(UpgradeTower.image, (80, 80)),
                                    pygame.transform.scale(UpgradeTower.image2, (80, 80)),
                                    UpgradeTower.costs, UpgradeTower.towerRange - selectedPosition.towerRange,
                                    UpgradeTower.damage - selectedPosition.damage, UpgradeTower.value,
                                    "Upgrade", "UpgradeTower.name", "UpgradeTower.description")
        else:
            sideinfo = Informations(80, 1300, 100, 100, pygame.transform.scale(tower_image[1][0], (0, 0)),
                                    pygame.transform.scale(tower_image2[1][0], (0, 0)), "",
                                    "nothing to upgrade", "", "", "")
    else:
        sideinfo = Informations(80, 1300, 100, 100, pygame.transform.scale(tower_image[1][0], (0, 0)),
                                pygame.transform.scale(tower_image2[1][0], (0, 0)), "",
                                "nothing selected", "", "", "")



def draw_path(path_pos):
    """
    Generate and store the position of a wayfield on the map at a position with the correct image based on the rotation

    Arguments: postion on path

    Test:
        -Path has to be ready
        -screen has to be 1920x1080 and all Tiles 160x160
        -Test if the end is reached or a position not on the path

    """
    global wayfields
    print(PATH)
    current_pos = PATH[path_pos][0]
    next_pos = PATH[path_pos + 1][0]
    pos_x = 50 + (PATH[path_pos][1] * 160)
    pos_y = (PATH[path_pos][2]) * 160
    if current_pos == 'up' and next_pos == 'right' or current_pos == 'left' and next_pos == 'down':
        wayfields.append(Tiles(pos_x, pos_y, 160, 160, curve2))
    elif current_pos == 'up' and next_pos == 'left' or current_pos == 'right' and next_pos == 'down':
        wayfields.append(Tiles(pos_x, pos_y, 160, 160, curve1))
    elif current_pos == 'down' and next_pos == 'right' or current_pos == 'left' and next_pos == 'up':
        wayfields.append(Tiles(pos_x, pos_y, 160, 160, curve3))
    elif current_pos == 'down' and next_pos == 'down' or current_pos == 'up' and next_pos == 'up':
        wayfields.append(Tiles(pos_x, pos_y, 160, 160, way_vertical))
    elif current_pos == 'right' and next_pos == 'right' or current_pos == 'left' and next_pos == 'left':
        wayfields.append(Tiles(pos_x, pos_y, 160, 160, way_horizontal))
    elif current_pos == 'right' and next_pos == 'up' or current_pos == 'down' and next_pos == 'left':
        wayfields.append(Tiles(pos_x, pos_y, 160, 160, curve4))



def creation_map_objects():
    """
    Generate based on the numpy array all fields

    Test:
        -check if map format is 6x13 and tiles are 160x160
        -test if the is exact one start and exact one end
        -test the path is without holes and has no loops

    """
    global towerplace_bool, MAP, towerfields
    count_ways = 0
    ty = 0
    for y in range(8):
        tx = 0
        if y > 0:
            tx = 50
        for x in range(8):
            value = MAP[y, x]
            if value == 0:
                if not towerplace_bool:
                    towerfields.append(Tiles(tx, ty, 160, 160, clickable_field))
            elif value == 5:
                towerfields.append(Tiles(tx, ty, 160, 160, obstacle_map))
            elif value == 8:
                draw_path(count_ways)
                count_ways += 1
            elif value == 1:
                tx += 50
                towerfields.append(Tiles(tx, ty, 160, 160, start_map))
            elif value == 2:
                towerfields.append(Tiles(tx, ty, 160, 160, end_map))
            elif 10 < value < 39:
                first_place = value % 10
                second_place = value // 10
                towerfields.append(Tiles(tx, ty, 160, 160, tower_image[second_place - 1][first_place - 1]))
            tx += 160
        ty += 160
    towerplace_bool = True


def draw_enemys():
    """

    Enemy Movement and check if they need to be removed.

    When    -they are dead
            -they reached the end

    If whole wave is dead generate the new wave

    Test:
        -All "old" enemys have to be removed before the new wave is spawned
        -Correct Health decrease if Enemy dies at the end

    """
    global frames, WINDOW, UserHealth, enemys, spawn_offset, offset, wave
    i = 0
    while i < (len(enemys)):
        if frames >= spawn_offset[i + offset]:
            pos = frames - spawn_offset[i + offset]
            e = enemys[i]
            if pos > len(e.path):
                enemys.remove(e)
            elif pos == len(e.path):
                if e.health > 0:
                    UserHealth -= 10
                enemys.remove(e)
                offset += 1
            else:
                e.direction = e.path[pos][2]
                e.x = 50 + e.path[pos][0] * 160
                e.y = e.path[pos][1] * 160
                e.updateRect()
                e.draw(WINDOW)
        i += 1
    if len(enemys) == 0:
        frames = 0
        wave += 1
        #logger.info(f"Current wave is {wave}")
        picture = pygame.transform.scale(pygame.image.load(f"assets/enemys/destroyer ({2 - (wave % 2)}).png"),
                                         (160, 160))
        offset = 0
        spawn_offset = []
        enemys = []
        for i in range(10):
            spawn_offset.append(i * 25)
            enemys.append(Enemy(0, 0, 160, 160, 100 * wave, 100 * wave, 5+wave, 0,
                                [picture, pygame.transform.rotate(picture, 90), pygame.transform.rotate(picture, 180),
                                 pygame.transform.rotate(picture, 270)], None))
        create_movement(PATH, enemys)



def draw_menue():
    """

    Draws the map selection at startup and generate 9 random maps out of the 30.000

    Test:
        -The maps have to be generated with mapgen.py
        -maps must have 6x13 format and resolution 1920x1080

    """
    global maps, WINDOW, font_headline, font_basic

    easy = [0, 1, 2]
    hard = [8, 9, 10]
    medium = [30, 31, 32]
    WINDOW.blit(background, (0, 0))
    headline = font_headline.render("Select a Map", True, (250, 250, 250))
    WINDOW.blit(headline, (700 - (headline.get_width() // 2), 0))
    pos_y = 157
    for key in easy:
        map = np.load(f'maps/{"easy"}/map{key}.npz')['arr_0']
        draw_mini_map(WINDOW, field_mini, way_mini, map, 78, pos_y)
        maps.append(Maps(78, pos_y, 270, 270, key, "easy"))
        pos_y += 400
    pos_y = 157
    for key in medium:
        map = np.load(f'maps/{"medium"}/map{key}.npz')['arr_0']
        draw_mini_map(WINDOW, field_mini, way_mini, map, 585-41, pos_y)
        maps.append(Maps(585-41, pos_y, 270, 270, key, "medium"))
        pos_y += 400
    pos_y = 157
    for key in hard:
        map = np.load(f'maps/{"hard"}/map{key}.npz')['arr_0']
        draw_mini_map(WINDOW, field_mini, way_mini, map, 1012, pos_y)
        maps.append(Maps(1012, pos_y, 270, 270, key, "hard"))
        pos_y += 400


def map_selection():
    """

    When User selects a map its been saved and path is generated, gamestate is changed into the main game loop

    Test:
        -game state 2 has to be main game loop
        -every function call must work since there is no error handling

    """
    global pressed, maps, MAP, PATH, game_state, starttime
    state = pygame.mouse.get_pressed()[0]
    if state and not pressed:
        pressed = True
        for m in maps:
            if m.isOver():
                #logger.add("file.log", level="DEBUG")
                #logger.info(f"Map selected {m.difficulty} {m.value}")
                MAP = generate_obstacles(np.load(f'maps/{m.difficulty}/map{m.value}.npz')['arr_0'])
                PATH = build_path([], np.load(f'maps/{m.difficulty}/map{m.value}.npz')['arr_0'], 0, 0)
                game_state = 2
                load_buttons()
                create_movement(PATH, enemys)
                creation_map_objects()
                starttime = time.time()
    elif not state:
        pressed = False


def draw_endscreen():
    """

    Draws the Game Over screen

    """
    global WINDOW, endscreenButtons

    WINDOW.blit(background, (0, 0))
    GameOverText = pygame.font.SysFont('comicsans', 100, True, True).render("Game Over", True, (0, 0, 0))
    WINDOW.blit(GameOverText, (720 - GameOverText.get_width() // 2, 600 - GameOverText.get_height() // 2))

    if endscreenButtons == []:
        endscreenButtons.append(
            Button((255, 0, 0), 650, 640, 100, 100, restart))
    for btn in endscreenButtons:
        btn.draw(WINDOW)


def display_endscreen():
    """

    When Game is Over, restart or end game

    """
    global pressed

    draw_endscreen()
    state = pygame.mouse.get_pressed()[0]
    if state and not pressed:
        pressed = True
        for btn in endscreenButtons:
            if btn.isOver():
                #logger.info("New Game")
                ReInit()


    elif not state:
        pressed = False


def ReInit():
    """

    Resets all Game Values which have changed during game loop

    Test:
        -Values have to be the same as at the beginning
        -Only Call when Restart not during gaming
    """
    global Gold, MAP, PATH, starttime, frames, game_state, pressed, maps, wayfields, towerfields, buttons, endscreenButtons, sideinfo, running, enemy_path, selectedEnemy, selectedTowerToBuild, selectedPosition, towerplace_bool, UserHealth, wave, offset, enemys, spawn_offset

    # Player Values
    Gold = 1000
    UserHealth = 100

    # Game Values
    MAP = None
    PATH = None
    starttime = None
    frames = 0
    game_state = 0
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
    wave = 0
    enemys = []
    spawn_offset = []


def display_state():
    """

    Switch for different game states
    Game state 2 is Main game loop

    Test:
        -Drawing of objects have to be ground up care about correct sequence
        -Test for enough frames per second
    """
    global frames, Gold, game_state, WINDOW, pressed

    if game_state == 0:
        game_state = LoadMainScreen(win=WINDOW, sound= shootSound)
        if game_state == 1:
            pressed = True
            draw_menue()
    elif game_state == 1:
        map_selection()
    elif game_state == 2:
        upgrade_Listener()
        handle_input()
        draw_window(WINDOW, UserHealth, background, sideinfo, buttons, wave, starttime, Gold)
        draw_map(WINDOW, wayfields, towerfields)
        on_action()
        draw_enemys()
        draw_tower_bullets(frames, towerfields, enemys, bullet_image, shootSound)
        frames += 1
        Gold += 0.8
        if UserHealth <= 0:
            game_state = 3
        draw_tower_range(WINDOW, towerfields)
    elif game_state == 3:
        display_endscreen()
    else:
        pass


# Main Loop to call States with 60fps and update the pygame window
pygame.init()
WINDOW= pygame.display.set_mode((1440, 1440))
clock = pygame.time.Clock()
shootSound = pygame.mixer.Sound("assets/sounds/pew.ogg")
shootSound.set_volume(0.05)
pygame.mixer.music.load("assets/sounds/music.ogg")
pygame.mixer.music.set_volume(0.02)
pygame.mixer.music.play(-1)
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
pygame.display.set_caption("PoRTaL PRoTECtoR")
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
font = pygame.font.SysFont('comicsans', 20)
font_headline = pygame.font.SysFont('comicsans', 50, True, True)
font_basic = pygame.font.SysFont('comicsans', 30, True)

async def main():
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        display_state()
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())