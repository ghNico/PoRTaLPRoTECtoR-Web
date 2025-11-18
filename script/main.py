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
import random
from idlelib.run import exit_now
from typing import Any
from pygame_menu._scrollarea import ScrollArea

from Tiles import *
from Main_Screen import LoadMainScreen
from Drawing import *
from Helper import *
import numpy as np
import time
import pygame_menu


GAME_DEFAULT_CURSOR = pygame.SYSTEM_CURSOR_CROSSHAIR

SPECIAL_EFFECT_BONUS_GOLD = 1000

X_COORDINATE_RESTART_BUTTON = 910
Y_COORDINATE_RESTART_BUTTON = 690
Y_COORDINATE_GAME_OVER_BUTTON = 400
Y_COORDINATE_FINAL_SCORE = 700

MAX_AMOUNT_OF_MAPS = 4

SPECIAL_POWER_IMAGE_HEIGHT = 200
SPECIAL_POWER_IMAGE_WIDTH = 200
COLLECTED_PRESENTS=0
EXISTING_PRESENT=0
MAX_NUMBER_OF_PRESENTS=4

LIKELIHOOD_PRESENT_CREATED = 0.1

# Player Values
Gold = 1000
UserHealth = 100

# Game Values
WINDOW = pygame.display.set_mode((1920, 1080));
MAP = None
MAP_Y_SIZE=5
MAP_X_SIZE=12
PATH = None
starttime = None
frames = 0
game_state = 0
pressed = False
maps = []
wayfields = []
towerfields = []
buttons = []
exit_button:Button
special_power_button:Button
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
restart = pygame.transform.scale(pygame.image.load("assets/environment/restart.jpg"),(140,140))
exit_image = pygame.transform.scale(pygame.image.load("assets/environment/exit.jpg"), (140, 140))
special_effect_image= pygame.transform.scale(pygame.image.load("assets/environment/specialPower/0_presents_special_power.png"), (
    SPECIAL_POWER_IMAGE_WIDTH, SPECIAL_POWER_IMAGE_HEIGHT))
special_effect_image1= pygame.transform.scale(pygame.image.load("assets/environment/specialPower/1_presents_special_power.png"), (
    SPECIAL_POWER_IMAGE_WIDTH, SPECIAL_POWER_IMAGE_HEIGHT))
special_effect_image2= pygame.transform.scale(pygame.image.load("assets/environment/specialPower/2_presents_special_power.png"), (
    SPECIAL_POWER_IMAGE_WIDTH, SPECIAL_POWER_IMAGE_HEIGHT))
special_effect_image3= pygame.transform.scale(pygame.image.load("assets/environment/specialPower/3_presents_special_power.png"), (
    SPECIAL_POWER_IMAGE_WIDTH, SPECIAL_POWER_IMAGE_HEIGHT))
special_effect_image4= pygame.transform.scale(pygame.image.load("assets/environment/specialPower/4_presents_special_power.png"), (
    SPECIAL_POWER_IMAGE_WIDTH, SPECIAL_POWER_IMAGE_HEIGHT))
start_map = pygame.transform.scale(pygame.image.load('assets/environment/portal.jpg'), (140, 140))
end_map = pygame.transform.scale(pygame.image.load('assets/environment/portal_red.jpg'), (140, 140))
way_horizontal = pygame.transform.scale(pygame.image.load("assets/tiles/Gerade.JPG"), (140, 140))
way_vertical = pygame.transform.scale(pygame.transform.rotate(way_horizontal, 90), (140, 140))
clickable_field = pygame.transform.scale(pygame.image.load('assets/environment/bauen.png'), (140, 140))
obstacle_map = pygame.transform.scale(pygame.image.load('assets/environment/hindernis.png'), (140, 140))
christmas_tree_obstacle_map = pygame.transform.scale(pygame.image.load('assets/environment/christmas_tree.png'), (140, 140))
christmas_wreath_obstacle_map = pygame.transform.scale(pygame.image.load('assets/environment/christmas_wreath.png'), (140, 140))
present_obstacle_map = pygame.transform.scale(pygame.image.load('assets/environment/present.png'), (140, 140))
curve1 = pygame.transform.scale(pygame.image.load('assets/tiles/Kurve.JPG'), (140, 140))
curve2 = pygame.transform.rotate(curve1, 90)
curve3 = pygame.transform.rotate(curve1, 180)
curve4 = pygame.transform.rotate(curve1, 270)
field_mini = pygame.image.load("assets/mini_map/empty_field.png")
way_mini = pygame.image.load("assets/mini_map/way_field.png")
background = pygame.image.load("assets/environment/Galaxy.jpg")
background = pygame.transform.scale(background, (1920, 1080))
menu = None
frame = None

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
        tower_image[y - 1][x - 1] = (pygame.image.load(f'assets/tower/tower {y} ({x}).png'))

# Guns:
tower_image2 = [[0 for x in range(8)] for y in range(3)]
for x in range(1, 9):
    for y in range(1, 4):
        tower_image2[y - 1][x - 1] = (pygame.image.load(f'assets/tower/gun {y} ({x}).png'))

# Enemys:
picture = pygame.transform.scale(pygame.image.load(f"assets/enemys/destroyer ({2 - (wave % 2)}).png"), (140, 140))

for i in range(10):
    spawn_offset.append(i * 25)
    enemys.append(Enemy(0, 0, 140, 140, 100, 100, 10, 0,
                        [picture, pygame.transform.rotate(picture, 90), pygame.transform.rotate(picture, 180),
                         pygame.transform.rotate(picture, 270)], None))


def startup():
    """
    Initialization of pygame

    """
    global WINDOW, font, font_headline, font_basic, shootSound, backgroundMusic, frame, menu
    pygame.init()
    shootSound = pygame.mixer.Sound("assets/sounds/pew.wav")
    shootSound.set_volume(0.05)
    pygame.mixer.music.load("assets/sounds/music.mp3")
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play(-1)
    pygame.mouse.set_cursor(GAME_DEFAULT_CURSOR)
    pygame.display.set_caption("PoRTaL PRoTECtoR")
    pygame.display.set_icon(pygame.image.load('assets/icon.png'))
    font = pygame.font.SysFont('comicsans', 20)
    font_headline = pygame.font.SysFont('comicsans', 50, True, True)
    font_basic = pygame.font.SysFont('comicsans', 30, True)
    menu = pygame_menu.Menu('Shop', 300, 400, theme=pygame_menu.themes.THEME_BLUE)
    frame = menu.add.frame_v(300, 400, max_height=200, max_width=200)
    frame.set_scrollarea(True)  # Enables scrolling




def load_buttons():
    """
    Set the list of buttons with all values of the towers and generate the objects

    Test:
        -screen resolution 1920x1080
        -all values have to be balanced for the game

    """
    global buttons

    buttons.append(
        Informations(x=260, y=870, width=140, height=140, image=pygame.transform.scale(tower_image[0][0], (140, 140)),
                     image2=pygame.transform.scale(tower_image2[0][0], (140, 140)), costs=250, towerRange=200,
                     damage=30, value=11, headline="Ice Boy", name="Tower 1", description="Out of the Iceage"))
    buttons.append(
        Informations(x=440, y=870, width=140, height=140, image=pygame.transform.scale(tower_image[0][1], (140, 140)),
                     image2=pygame.transform.scale(tower_image2[0][1], (140, 140)), costs=300, towerRange=225, damage=35,
                     value=12, headline="Rocket Inferno", name="Tower 2", description="Iron Dome (Israel)"))
    buttons.append(
        Informations(620, 870, 140, 140, pygame.transform.scale(tower_image[0][2], (140, 140)),
                     pygame.transform.scale(tower_image2[0][2], (140, 140)), 325, 250, 40, 13, "Blaster", "Tower 3",
                     "Fat Gun"))
    buttons.append(
        Informations(800, 870, 140, 140, pygame.transform.scale(tower_image[0][3], (140, 140)),
                     pygame.transform.scale(tower_image2[0][3], (140, 140)), 350, 275, 45, 14, "Red Sparrow", "Tower 4",
                     "Not a real sparrow"))
    buttons.append(
        Informations(980, 870, 140, 140, pygame.transform.scale(tower_image[0][4], (140, 140)),
                     pygame.transform.scale(tower_image2[0][4], (140, 140)), 375, 300, 50, 15, "Alfi Deluxe", "Tower 5",
                     "mit 1.0 bestanden ;)"))
    buttons.append(
        Informations(1160, 870, 140, 140, pygame.transform.scale(tower_image[0][5], (140, 140)),
                     pygame.transform.scale(tower_image2[0][5], (140, 140)), 400, 325, 55, 16, "Mega Blizzard", "Tower 6",
                     "Really Cold"))
    buttons.append(
        Informations(1340, 870, 140, 140, pygame.transform.scale(tower_image[0][6], (140, 140)),
                     pygame.transform.scale(tower_image2[0][6], (140, 140)), 425, 350, 60, 17, "Yellow Trinket", "Tower 7",
                     "Gives no Vision"))
    buttons.append(
        Informations(1520, 870, 140, 140, pygame.transform.scale(tower_image[0][7], (140, 140)),
                     pygame.transform.scale(tower_image2[0][7], (140, 140)), 450, 375, 65, 18, "RIGHT Tower", "Tower 8",
                     "Not Left"))


def load_exit_button():
    global exit_button
    exit_button=Button((255, 0, 0), 1755, 1000, 50, 50, pygame.transform.scale(exit_image, (50, 50)), "game stop")


def load_special_power_button():
    global special_power_button
    special_power_button=Button((255, 255, 255), 10, 870, 200, 200, pygame.transform.scale(special_effect_image, (200, 200)), "use special power")





def on_action():
    """

    When mouse is pressed over tower or sideinfo or buttons, checks and prepare the ingame values for the handle_input function

    Test:
        -objects need isOver function
        -every element is 140x140 and the map need to contain the value of tower to level up

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
            if MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] < 30:
                if Gold >= int(sideinfo.costs):
                    MAP[(selectedPosition.y // 140, (selectedPosition.x - 50) // 140)] += 10
                    #logger.info("Towerupgrade")
                    selectedPosition.upgrade(tower_image, tower_image2)
                    Gold -= int(sideinfo.costs)
                selectedTowerToBuild = None
                selectedPosition = None
        handle_press_present(towerfields)
        handle_press_exit_button()
        handle_press_special_power_button()
    elif not state:
        pressed = False

def handle_press_special_power_button():
    global special_power_button, Gold, COLLECTED_PRESENTS
    if special_power_button.isOver() and COLLECTED_PRESENTS==MAX_NUMBER_OF_PRESENTS:
        Gold+= SPECIAL_EFFECT_BONUS_GOLD
        COLLECTED_PRESENTS = 0
        update_special_power_button()

def handle_press_present(towerfields):
    global COLLECTED_PRESENTS, EXISTING_PRESENT
    for t in towerfields:
        if t.isOver():
            selectedPosition = t
            value = MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140]
            if value == 7 and MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] < 30:
                MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] = 0
                update_map()
                COLLECTED_PRESENTS += 1
                EXISTING_PRESENT -= 1
                update_special_power_button()


def handle_press_exit_button():
    global game_state
    global exit_button
    if exit_button.isOver():
        game_state = 3


def handle_input():
    """
    Based on the User clicks and the preparation of the on_action function the User interact with the game

    Game could be closed

    A Tower is selected and placed if enough gold is in the wallet

    Test:
        -to handle 2 clicks 4 different cases can raise errors
        -all is based on 140x140 Tiles so test the Tiles size for correct selection

    """
    global running, selectedTowerToBuild, selectedPosition, MAP, Gold

    if selectedTowerToBuild is not None and selectedPosition is None:
        if selectedTowerToBuild.name == "game stop":
            running = False
            #logger.info("End Game")
            selectedTowerToBuild = None
            selectedPosition = None
    elif selectedTowerToBuild is not None and selectedPosition is not None and MAP[
        selectedPosition.y // 140, (selectedPosition.x - 50) // 140] == 0:
        if MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] < 30:
            if Gold >= int(selectedTowerToBuild.costs):
                value = 10 + int(selectedTowerToBuild.name[6:])
                MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] = value
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
    elif selectedTowerToBuild is not None and selectedPosition is not None and MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] != 0 or selectedTowerToBuild is None and selectedPosition is not None and MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] == 0:
        selectedPosition = None
    elif selectedTowerToBuild is None and selectedPosition is not None and MAP[
        selectedPosition.y // 140, (selectedPosition.x - 50) // 140] != 0:
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
            sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(selectedTowerToBuild.image, (80, 80)),
                                    pygame.transform.scale(selectedTowerToBuild.image2, (80, 80)),
                                    selectedTowerToBuild.costs, selectedTowerToBuild.towerRange,
                                    selectedTowerToBuild.damage, selectedTowerToBuild.value,
                                    selectedTowerToBuild.headline, selectedTowerToBuild.name,
                                    selectedTowerToBuild.description)
    elif selectedTowerToBuild is None and selectedPosition is not None:
        nextstage = MAP[selectedPosition.y // 140, (selectedPosition.x - 50) // 140] + 10
        if 20 < nextstage < 40:
            dummie = Tower(selectedPosition.x, selectedPosition.y, selectedPosition.width, selectedPosition.height,
                           selectedPosition.image, selectedPosition.image2, selectedPosition.towerRange,
                           selectedPosition.damage, selectedPosition.value, selectedPosition.costs)
            UpgradeTower = dummie.upgrade(tower_image, tower_image2)
            sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(UpgradeTower.image, (80, 80)),
                                    pygame.transform.scale(UpgradeTower.image2, (80, 80)),
                                    UpgradeTower.costs, UpgradeTower.towerRange - selectedPosition.towerRange,
                                    UpgradeTower.damage - selectedPosition.damage, UpgradeTower.value,
                                    "Upgrade", "UpgradeTower.name", "UpgradeTower.description")
        else:
            sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(tower_image[1][0], (0, 0)),
                                    pygame.transform.scale(tower_image2[1][0], (0, 0)), "",
                                    "nothing to upgrade", "", "", "")
    else:
        sideinfo = Informations(80, 900, 100, 100, pygame.transform.scale(tower_image[1][0], (0, 0)),
                                pygame.transform.scale(tower_image2[1][0], (0, 0)), "",
                                "nothing selected", "", "", "")



def draw_path(path_pos):
    """
    Generate and store the position of a wayfield on the map at a position with the correct image based on the rotation

    Arguments: postion on path

    Test:
        -Path has to be ready
        -screen has to be 1920x1080 and all Tiles 140x140
        -Test if the end is reached or a position not on the path

    """
    global wayfields

    current_pos = PATH[path_pos][0]
    next_pos = PATH[path_pos + 1][0]
    pos_x = 50 + (PATH[path_pos][1] * 140)
    pos_y = (PATH[path_pos][2]) * 140
    if current_pos == 'up' and next_pos == 'right' or current_pos == 'left' and next_pos == 'down':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, curve2))
    elif current_pos == 'up' and next_pos == 'left' or current_pos == 'right' and next_pos == 'down':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, curve1))
    elif current_pos == 'down' and next_pos == 'right' or current_pos == 'left' and next_pos == 'up':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, curve3))
    elif current_pos == 'down' and next_pos == 'down' or current_pos == 'up' and next_pos == 'up':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, way_vertical))
    elif current_pos == 'right' and next_pos == 'right' or current_pos == 'left' and next_pos == 'left':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, way_horizontal))
    elif current_pos == 'right' and next_pos == 'up' or current_pos == 'down' and next_pos == 'left':
        wayfields.append(Tiles(pos_x, pos_y, 140, 140, curve4))


def update_map():
    global towerplace_bool, MAP, towerfields
    count_ways = 0
    ty = 0
    for y in range(6):
        tx = 0
        if y > 0:
            tx = 50
        for x in range(13):
            value = MAP[y, x]
            if value == 0:
                towerfields.append(Tiles(tx, ty, 140, 140, clickable_field))
            if value == 7:
                append_presents(towerfields, tx, ty)
            tx += 140
        ty += 140
    towerplace_bool = True

def creation_map_objects():
    """
    Generate based on the numpy array all fields

    Test:
        -check if map format is 6x13 and tiles are 140x140
        -test if the is exact one start and exact one end
        -test the path is without holes and has no loops

    """
    global towerplace_bool, MAP, towerfields
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
                append_random_obstacles(towerfields, tx, ty)
            elif value == 7:
                append_presents(towerfields, tx, ty)
            elif value == 8:
                draw_path(count_ways)
                count_ways += 1
            elif value == 1:
                tx += 50
                towerfields.append(Tiles(tx, ty, 140, 140, start_map))
            elif value == 2:
                towerfields.append(Tiles(tx, ty, 140, 140, end_map))
            elif 10 < value < 39:
                first_place = value % 10
                second_place = value // 10
                towerfields.append(Tiles(tx, ty, 140, 140, tower_image[second_place - 1][first_place - 1]))
            tx += 140
        ty += 140
    towerplace_bool = True


def append_random_obstacles(towerfields: list[Any], tx: int | Any, ty: int):
    random_value = random.random()
    if random_value<0.33:
        towerfields.append(Tiles(tx, ty, 140, 140, obstacle_map))
    elif random_value<0.66:
        towerfields.append(Tiles(tx, ty, 140, 140, christmas_tree_obstacle_map))
    else:
        towerfields.append(Tiles(tx, ty, 140, 140, christmas_wreath_obstacle_map))

def append_presents(towerfields, tx, ty):
    towerfields.append(Tiles(tx, ty, 140, 140, present_obstacle_map))

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
                e.x = 50 + e.path[pos][0] * 140
                e.y = e.path[pos][1] * 140
                e.updateRect()
                e.draw(WINDOW)
        i += 1
    if len(enemys) == 0:
        frames = 0
        wave += 1
        #logger.info(f"Current wave is {wave}")
        picture = pygame.transform.scale(pygame.image.load(f"assets/enemys/destroyer ({2 - (wave % 2)}).png"),
                                         (140, 140))
        offset = 0
        spawn_offset = []
        enemys = []
        for i in range(10):
            spawn_offset.append(i * 25)
            enemys.append(Enemy(0, 0, 140, 140, 100 * wave, 100 * wave, 10, 0,
                                [picture, pygame.transform.rotate(picture, 90), pygame.transform.rotate(picture, 180),
                                 pygame.transform.rotate(picture, 270)], None))
        create_movement(PATH, enemys)





def draw_present():
    global MAP, COLLECTED_PRESENTS, EXISTING_PRESENT
    add_present_zo_map = LIKELIHOOD_PRESENT_CREATED > random.random()
    if add_present_zo_map and EXISTING_PRESENT+COLLECTED_PRESENTS < MAX_NUMBER_OF_PRESENTS:
        present_y_coordinate=random.randint(0, MAP_Y_SIZE)
        present_x_coordinate=random.randint(0, MAP_X_SIZE)
        if MAP[present_y_coordinate, present_x_coordinate] == 0:
            MAP[present_y_coordinate, present_x_coordinate] = 7
            EXISTING_PRESENT += 1
            #TODO nicht sicher ob gebraucht wird
            update_map()



def update_special_power_button():
    global special_power_button, COLLECTED_PRESENTS
    if COLLECTED_PRESENTS ==0:
        special_power_button = Button((255, 255, 255), 10, 870, 200, 200, pygame.transform.scale(special_effect_image, (200, 200)))
    elif COLLECTED_PRESENTS ==1:
        special_power_button = Button((255, 255, 255), 10, 870, 200, 200, pygame.transform.scale(special_effect_image1, (200, 200)))
    elif COLLECTED_PRESENTS ==2:
        special_power_button = Button((255, 255, 255), 10, 870, 200, 200, pygame.transform.scale(special_effect_image2, (200, 200)))
    elif COLLECTED_PRESENTS ==3:
        special_power_button = Button((255, 255, 255), 10, 870, 200, 200, pygame.transform.scale(special_effect_image3, (200, 200)))
    elif COLLECTED_PRESENTS ==4:
        special_power_button = Button((255, 255, 255), 10, 870, 200, 200, pygame.transform.scale(special_effect_image4, (200, 200)))

def draw_menue():
    """

    Draws the map selection at startup and generate 9 random maps out of the 30.000

    Test:
        -The maps have to be generated with mapgen.py
        -maps must have 6x13 format and resolution 1920x1080

    """
    global maps, WINDOW, font_headline, font_basic

    easy = [np.random.randint(1, MAX_AMOUNT_OF_MAPS), np.random.randint(1, MAX_AMOUNT_OF_MAPS), np.random.randint(1, MAX_AMOUNT_OF_MAPS)]
    medium = [np.random.randint(1, MAX_AMOUNT_OF_MAPS), np.random.randint(1, MAX_AMOUNT_OF_MAPS), np.random.randint(1, MAX_AMOUNT_OF_MAPS)]
    hard = [np.random.randint(1, MAX_AMOUNT_OF_MAPS), np.random.randint(1, MAX_AMOUNT_OF_MAPS), np.random.randint(1, MAX_AMOUNT_OF_MAPS)]
    WINDOW.blit(background, (0, 0))
    headline = font_headline.render("Select a Map", True, (250, 250, 250))
    WINDOW.blit(headline, (960 - (headline.get_width() // 2), 50))
    pos_y = 175
    basic = font_basic.render("Easy", True, (250, 250, 250))
    WINDOW.blit(basic, (300 - (basic.get_width() // 2), 125))
    for key in easy:
        map = np.load(f'maps/{"easy"}/map ({key}).npz')['data']
        draw_mini_map(WINDOW, field_mini, way_mini, map, 30, pos_y)
        maps.append(Maps(30, pos_y, 585, 270, key, "easy"))
        pos_y += 305
    pos_y = 175
    basic = font_basic.render("Medium", True, (250, 250, 250))
    WINDOW.blit(basic, (950 - (basic.get_width() // 2), 125))
    for key in medium:
        map = np.load(f'maps/{"medium"}/map ({key}).npz')['data']
        draw_mini_map(WINDOW, field_mini, way_mini, map, 670, pos_y)
        maps.append(Maps(670, pos_y, 585, 270, key, "medium"))
        pos_y += 305
    pos_y = 175
    basic = font_basic.render("Hard", True, (250, 250, 250))
    WINDOW.blit(basic, (1600 - (basic.get_width() // 2), 125))
    for key in hard:
        map = np.load(f'maps/{"hard"}/map ({key}).npz')['data']
        draw_mini_map(WINDOW, field_mini, way_mini, map, 1310, pos_y)
        maps.append(Maps(1310, pos_y, 585, 270, key, "hard"))
        pos_y += 305





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
                MAP = generate_obstacles(np.load(f'maps/{m.difficulty}/map ({m.value}).npz')['data'])
                PATH = build_path([], np.load(f'maps/{m.difficulty}/map ({m.value}).npz')['data'], 0, 0)
                game_state = 2
                load_buttons()
                load_exit_button()
                load_special_power_button()
                create_movement(PATH, enemys)
                creation_map_objects()
                starttime = time.time()
    elif not state:
        pressed = False


def draw_endscreen():
    """

    Draws the Game Over screen

    """
    global WINDOW, endscreenButtons, wave

    WINDOW.blit(background, (0, 0))
    GameOverText = pygame.font.SysFont('comicsans', 100, True, True).render("Game Over", True, (0, 0, 0))
    WINDOW.blit(GameOverText, (960 - GameOverText.get_width() // 2, Y_COORDINATE_GAME_OVER_BUTTON - GameOverText.get_height() // 2))
    final_score = pygame.font.SysFont('comicsans', 30, True, True).render("You made it to wave: "+str(wave), True, (0, 0, 0))
    WINDOW.blit(final_score, (960 - final_score.get_width() // 2, Y_COORDINATE_FINAL_SCORE - final_score.get_width() // 2))



    if endscreenButtons == []:
        endscreenButtons.append(
            Button((255, 0, 0), X_COORDINATE_RESTART_BUTTON, Y_COORDINATE_RESTART_BUTTON, 100, 100, restart))
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
    global Gold, MAP, PATH, starttime, frames, game_state, pressed, maps, wayfields, towerfields, buttons, endscreenButtons, sideinfo, running, enemy_path, selectedEnemy, selectedTowerToBuild, selectedPosition, towerplace_bool, UserHealth, wave, offset, enemys, spawn_offset, COLLECTED_PRESENTS, EXISTING_PRESENT

    # Player Values
    Gold = 1000
    UserHealth = 100
    COLLECTED_PRESENTS=0
    EXISTING_PRESENT=0

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

def handle_hover_events():
    mouse_pos = pygame.mouse.get_pos()
    hovering = special_power_button.rect.collidepoint(mouse_pos)

    if hovering and COLLECTED_PRESENTS==MAX_NUMBER_OF_PRESENTS:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(GAME_DEFAULT_CURSOR)




def display_state():
    """

    Switch for different game states
    Game state 2 is Main game loop

    Test:
        -Drawing of objects have to be ground up care about correct sequence
        -Test for enough frames per second
    """
    global frames, Gold, game_state, WINDOW, pressed, special_power_button

    if game_state == 0:
        game_state = LoadMainScreen(win=WINDOW, sound= shootSound)
        if game_state == 1:
            pressed = True
            draw_menue()
    elif game_state == 1:
        map_selection()
    elif game_state == 2:
        menu.enable()
        upgrade_Listener()
        handle_input()
        draw_window(WINDOW, UserHealth, background, sideinfo, buttons, wave, starttime, Gold, exit_button, special_power_button)
        draw_map(WINDOW, wayfields, towerfields)
        on_action()
        handle_hover_events()
        draw_enemys()
        draw_present()
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
WINDOW= pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
shootSound = pygame.mixer.Sound("assets/sounds/pew.wav")
shootSound.set_volume(0.05)
pygame.mixer.music.load("assets/sounds/music.mp3")
pygame.mixer.music.set_volume(0.02)
pygame.mixer.music.play(-1)
pygame.mouse.set_cursor(GAME_DEFAULT_CURSOR)
pygame.display.set_caption("PoRTaL PRoTECtoR")
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
font = pygame.font.SysFont('comicsans', 20)
font_headline = pygame.font.SysFont('comicsans', 50, True, True)
font_basic = pygame.font.SysFont('comicsans', 30, True)

menu = pygame_menu.Menu('Shop', 300, 400, theme=pygame_menu.themes.THEME_BLUE)
menu.set_absolute_position(500,700)
frame = menu.add.frame_v(300, 400, max_height=200, max_width=200)
scroll = ScrollArea(
    area_width=250,
    area_height=300,
    scrollbar_thick=12,
    scrollbars='position-south'  # correct
)
frame.set_scrollarea(scroll)  # Enables scrolling

for i in range(5):
    frame.pack(menu.add.button(f'Tower {i+1}', lambda x=i: print(f"Selected tower {x}")))

async def main():
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if menu.is_enabled():
            menu.draw(WINDOW)
        display_state()
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())