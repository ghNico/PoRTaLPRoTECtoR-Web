import math
from Bullet import *

allBullets = []


def PerfectRotated(x, y, image, angle):
    """
    Rotates the given image by angle and corrects the offset

    Arguments: position, image, angle to rotate

    Returns: rotated picture and the new rect

    Source: https://python-code-snippet.blogspot.com/2021/03/Rotate-Image-In-PyGame.html
    """
    picture_rotated = pygame.transform.rotozoom(image, angle, 1)
    picture_rotated_rect = picture_rotated.get_rect(center=(x, y))
    return picture_rotated, picture_rotated_rect


class Tiles:
    """
    Tiles class for objects needed in game
    During object creation it needs a position, width, height and the image which will displayed on the pygame windows
    """
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def isOver(self):
        """
        Check if the mouse is over an object

        Returns: Boolean if the mouse is over an object

        Test:
            -check if the function always detects if the mouse is over the button
            -check if return is always correct

        """
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


    def showRange(self, win):
        pass

    def findEnemys(self, enemy_lst, image):
        pass

    def checkCollide(self):
        pass

    def getTowerLst(self):
        return None

    def getValue(self):
        return None


class Button(Tiles):
    """
    Button class for all buttons, like the close-button
    During object creation it needs a color, position, width, height and the image also a name is possible
    """
    def __init__(self, color, x, y, width, height, image=None, name=''):
        super().__init__(x, y, width, height, image)
        self.color = color
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        """
        Draws the image of the button object (if it is not None)

        Arguments: pygame window

        Test:
            -check if all images are drawn

        """
        if self.image != '':
            win.blit(self.image, (self.x, self.y))



class Enemy(Tiles):
    """
    Enemy class for all enemys
    During object creation it needs position, width, height, health, maxhealth, velocity, direction, images, and the path
    """
    def __init__(self, x, y, width, height, health, maxHealth, velocity, direction, images, path):
        super().__init__(x, y, width, height, images)
        self.health = health
        self.maxHealth = maxHealth
        self.velocity = velocity
        self.direction = direction
        self.images = images
        self.path = path
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        """
        Draws the image and the healthbar of the enemy object (if it is not None)
        The healthbar contains the actualHealth and the MaxHealth of the enemy

        Arguments: pygame window

        Test:
            -check if all images are drawn
            -check if the healthbar is shown correctly
        """
        if self.image != None:
            win.blit(self.images[self.direction], (self.x, self.y))
            actualHealth = (self.health/self.maxHealth)*100
            pygame.draw.rect(win, (255, 0, 0), (self.x+20, self.y-20, 100, 15))
            pygame.draw.rect(win, (0, 255, 0), (self.x+20, self.y-20, actualHealth, 15))

    def rotate(self, direction):
        """
        In order to rotate the enemy we have 4 states top, down, left and right.
        The enemy has to manipulate his image based on rotation state so if he rotate in a corner on map (direction ==1)
        The next Image has to be selected so we increase the objects direction variable which is been used
        to select the displayed image on the pygame window

        Arguments: direction where the enemy moves

        """
        if direction == 1:
            if self.direction == 3:
                self.direction = 0
            else:
                self.direction += 1
        elif direction == -1:
            if self.direction == 0:
                self.direction = 3
            else:
                self.direction -= 1

    def getDamage(self, damage):
        """
        Changes the enemy's health when hit by a tower bullet. The damage is variable, so each tower has a different damage.
        After the health is changed it checks if the enemy is dead (health <=0). If this is true the image of it will be set to none and also health and maxHealth is set to 0.

        Arguments: damage which is applied to the enemy

        Test:
            -check if damage is the same as the damage which is set at the tower class
            -check if image of enemy always gets set to none
        """
        self.health -= damage
        if self.health<=0:
            self.image = None
            self.health = 0
            self.maxHealth = 0
        else:
            pass

    def checkCollide(self, towerBullets):
        global allBullets
        """
        Iterates over the list of all currently spawned bullets and checks if one of those bullets collided with the current enemy. 
        If they collide with the enemy, the function getDamage get triggered with the damage of the bullet. 
        After that the bullet gets destroyed.

        Arguments: list of all towerBullets

        Test:
            -check if collide works
            -check if the right damage gets applied to the enemy and if the bullet gets deleted after that
            
        """
        if towerBullets != None:
            for b in towerBullets:
                if self.rect.colliderect(b.rect):
                    self.getDamage(b.damage)
                    towerBullets.remove(b)
                else:
                    pass

    def updateRect(self):
        """
        Updates the position and the width/height of the rect of the enemy.

        Test:
            -check if rect changes the right way
            -check if the rect moves correctly with enemy
        """
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)



class Maps(Tiles):
    """
    Maps class for selecting maps
    During object creation it needs position, width, height, value, difficulty, image (default no image)
    """
    def __init__(self, x, y, width, height, value, difficulty, image=None):
        super().__init__(x, y, width, height, image)
        self.value = value
        self.difficulty = difficulty



class Tower(Tiles):
    """
    Tower class for all Tower placed on the map
    During object creation it needs position, width, height, 2 images (ground & rotated Tower), Range, damage, value, costs and a boolean which checks if the Range should be shown
    """
    def __init__(self, x, y, width, height, image1, image2, towerRange, damage, value, costs=0, ShowRangeBoolean=False):
        super().__init__(x, y, width, height, image1)
        self.costs = costs
        self.value = value
        self.towerRange = towerRange
        self.damage = damage
        self.rect = pygame.Rect(x, y, width, height)
        self.ShowRangeBoolean = ShowRangeBoolean
        self.image2 = image2
        self.angle = 0
        self.TowerBullets = []

    def draw(self, win):
        """
        Draws the image of the ground of the tower (image) after that it draws the rotated Tower on top of it.
        It also controls the bullets of its list of bullets.

        Arguments: pygame window

        Test:
            -check if all images are drawn
            -check if the bullet trajectory is created right
        """

        win.blit(self.image, (self.x, self.y))

        image_rotated, image_rotated_rect = PerfectRotated(self.x+self.width//2, self.y+self.height//2, self.image2, self.angle)
        win.blit(image_rotated, image_rotated_rect)

        for b in self.TowerBullets:
            b.trajectoryCreation()
            b.move(win)

    def upgrade(self, tower_image, tower_image2):
        """
        Upgrade of Tower is calculated and set

        Arguments: old Tower image, new Tower image

        Test:
            -new calculated Tower is balanced for the game

        """
        self.value += 10
        self.costs = int(int(self.costs)*(1.5))
        self.damage = int(int(self.damage)*(1.5))
        self.towerRange = int(int(self.towerRange)*(1.2))
        first_place = (self.value % 10)-1
        second_place = (self.value // 10) - 1
        self.image = pygame.transform.scale(tower_image[second_place][first_place], (160, 160))
        self.image2 = pygame.transform.scale(tower_image2[second_place][first_place], (160, 160))
        return self

    def showRange(self, win):
        """
        Transparent overlay for range indicator

        Arguments: pygame window

        Test:
            -resolution of pygame window matches the surface resolution

        """
        Range = pygame.Surface((1440, 1440), pygame.SRCALPHA, 32)
        pygame.draw.circle(Range, (255,0, 0, 80), (self.x+self.width//2, self.y+self.height//2), self.towerRange)
        win.blit(Range, (0,0))

    def spawnBullet(self, aimPosX, aimPosY, image, sound):
        """
        Create bullet object and append it to render queue

        Arguments: aim position and bullet image and sound

        Test:
            -Bullet image size 50x50

        """

        tempObject = Bullet(self.x, self.y, 50, 50, image, self.damage, aimPosX, aimPosY)
        sound.play()
        self.TowerBullets.append(tempObject)
        allBullets.append(tempObject)

    def rotate(self, aimX, aimY):
        """
        Rotates the tower around itself so the angle of tower is changed (Rotate to the Enemy/Aim)

        Arguments: aim position

        Test:
            -correct angle calculation
            -handling zerodivisionerror

        """
        try:
            angle2 = math.degrees(math.atan((self.y - aimY) / (self.x - aimX)))
        except ZeroDivisionError:
            return
        if (self.x - aimX) < 0 and (self.y - aimY) >= 0:
            angle2 += 180
        elif (self.x - aimX) < 0 and (self.y - aimY) < 0:
            angle2 += 180
        if angle2 < 0:
            angle2 += 360
        angle2 = 0 - angle2
        self.angle = angle2

    def findEnemys(self, enemy_lst, image, sound):
        """
        Tower search enemy + some math for positioning and the according bullet is spawned to kill the enemy

        Arguments: list of enemys and the bullet image and sound of shooting

        Test:
            -check if always find the nearest enemy
            -check if the position of nearest enemy is right (important for rotation and spawn bullet)
        """
        nearestEnemy = None
        lowestDistance = 0
        for e in enemy_lst:
            enemyX = e.x + e.width // 2
            enemyY = e.y + e.height // 2
            distance = math.sqrt((self.x + self.width // 2 - enemyX) ** 2 + (self.y + self.height // 2 - enemyY) ** 2)

            if distance < self.towerRange:
                if lowestDistance > distance or lowestDistance ==0:
                    lowestDistance = distance
                    nearestEnemy = e

        if nearestEnemy != None:
            if nearestEnemy.image != None:
                if nearestEnemy.direction == 1:
                    additionX = 0
                    additionY = 1
                elif nearestEnemy.direction == 3:
                    additionX = 0
                    additionY = -1
                elif nearestEnemy.direction == 0:
                    additionX = 1
                    additionY = 0
                elif nearestEnemy.direction == 2:
                    additionX = -1
                    additionY = 0

                enemyX = nearestEnemy.x + e.width // 2 + additionX * 10
                enemyY = nearestEnemy.y + e.height // 2 + additionY * 10
                self.rotate(enemyX, enemyY)
                self.spawnBullet(enemyX, enemyY, pygame.transform.rotate(image, self.angle), sound)



    def getValue(self):
        return self.value

    def getTowerLst(self):
        return self.TowerBullets


class Informations(Tower):
    """
    Informations class is used to store and hold the tower selection in the lower center of the screen

    Based on Tower object based on Tiles object
    """
    def __init__(self, x, y, width, height, image, image2, costs, towerRange, damage, value, headline='', name='', description='', sizeMenu=0):
        super().__init__(x, y, width, height, image, image2, towerRange, damage, value, costs)
        self.headline = headline
        self.name = name
        self.description = description
        self.rect = pygame.Rect(x, y, width, height)
        self.sizeMenu = sizeMenu

    def draw(self, win):
        """
        Draws the object with all information below and a headline

        Arguments: pygame window

        Test:
            -resolution of pygame window 1920x1080
            -correct display of text on screen
        """
        if self.sizeMenu == 0:
            win.blit(self.image, (self.x, self.y))
            win.blit(self.image2, (self.x, self.y))
        else:
            twq = pygame.transform.scale(self.image, (self.sizeMenu, self.sizeMenu))
            u = pygame.transform.scale(self.image2, (self.sizeMenu, self.sizeMenu))

            win.blit(twq, (self.x, self.y))
            win.blit(u, (self.x, self.y))


        font = pygame.font.SysFont('comicsans', 20)
        font_headline = pygame.font.SysFont('comicsans', 20, True, True)
        headline = font_headline.render(self.headline, True, (250, 250, 250))
        name = font.render(self.name, True, (250, 250, 250))
        description = font.render(self.description, True, (250, 250, 250))
        costs = font.render(str(self.costs), True, (250, 250, 250))
        towerRange = font.render("Additional Range: " + str(self.towerRange), True, (250, 250, 250))
        damage = font.render("Additional Damage: " + str(self.damage), True, (250, 250, 250))
        if self.headline == '':
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height)))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))
        elif self.headline == 'Upgrade':
            win.blit(headline, (self.x + (self.width / 2 - headline.get_width() / 2), self.y - 20))
            win.blit(towerRange, (self.x + (self.width / 2 - towerRange.get_width() / 2), self.y + (self.height) - 10))
            win.blit(damage,
                     (self.x + (self.width / 2 - damage.get_width() / 2), self.y + (self.height) + 10))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))
        elif self.sizeMenu:
            win.blit(headline, (self.x + (self.sizeMenu / 2 - headline.get_width() / 2), self.y - 20))
            win.blit(name, (self.x + (self.sizeMenu / 2 - name.get_width() / 2), self.y + (self.sizeMenu)))
            win.blit(description,
                     (self.x + (self.sizeMenu / 2 - description.get_width() / 2), self.y + (self.sizeMenu) + 20))
            win.blit(costs, (self.x + (self.sizeMenu / 2 - costs.get_width() / 2), self.y + (self.sizeMenu) + 40))
        else:
            win.blit(headline, (self.x + (self.width / 2 - headline.get_width() / 2), self.y - 20))
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height)))
            win.blit(description,
                     (self.x + (self.width / 2 - description.get_width() / 2), self.y + (self.height) + 20))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 40))

    # TODO wieso geht nicht
    def get_hover_state(self, gold: int,  mouse_pos: tuple[int, int]):
        if self.rect.collidepoint(mouse_pos):
            if gold > self.costs:
                return pygame.SYSTEM_CURSOR_HAND
            else:
                return pygame.SYSTEM_CURSOR_NO
        return None

