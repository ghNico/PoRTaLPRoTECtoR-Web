import math
from Bullet import *

allBullets = []

"""
    Quelle:
        https://python-code-snippet.blogspot.com/2021/03/how-to-rotate-image-in-pygame.html
"""
def PerfectRotated(x, y, image, angle):
    picture_rotated = pygame.transform.rotozoom(image, angle, 1)
    picture_rotated_rect = picture_rotated.get_rect(center=(x, y))
    return picture_rotated, picture_rotated_rect


class Tiles:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def isOver(self):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    # Hier bitte noch andere Lösung finden
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
    def __init__(self, color, x, y, width, height, image=None, name=''):
        super().__init__(x, y, width, height, image)
        self.color = color
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        # Call this method to draw the button on the screen
        #pygame.draw.rect(win, self.color, self.rect, 0)
        if self.image != '':
            win.blit(self.image, (self.x, self.y))
        #if self.name != '':
            #font = pygame.font.SysFont('comicsans', 20)
            #name = font.render(self.name, True, (0, 0, 0))
            #win.blit(name, (
                #self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height / 2 - name.get_height() / 2)))



class Enemy(Tiles):
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
        if self.image != None:
            win.blit(self.images[self.direction], (self.x, self.y))
            actualHealth = (self.health/self.maxHealth)*100
            pygame.draw.rect(win, (255, 0, 0), (self.x+20, self.y-20, 100, 15))
            pygame.draw.rect(win, (0, 255, 0), (self.x+20, self.y-20, actualHealth, 15))

    def rotate(self, direction):
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
        self.health -= damage
        if self.health<=0:
            self.image = None
            self.health = 0
            self.maxHealth = 0
        else:
            pass

    def checkCollide(self, towerBullets):
        global allBullets

        # Check auf Bullet versuchen
        if towerBullets != None:
            for b in towerBullets:
                if self.rect.colliderect(b.rect):
                    self.getDamage(b.damage)
                    towerBullets.remove(b)
                else:
                    pass

    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)



class Maps(Tiles):
    def __init__(self, x, y, width, height, value, difficulty, image=None):
        super().__init__(x, y, width, height, image)
        self.value = value
        self.difficulty = difficulty



class Tower(Tiles):
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
        win.blit(self.image, (self.x, self.y))

        image_rotated, image_rotated_rect = PerfectRotated(self.x+self.width//2, self.y+self.height//2, self.image2, self.angle)
        win.blit(image_rotated, image_rotated_rect)

        for b in self.TowerBullets:
            b.trajectoryCreation()
            b.move(win)

    def upgrade(self, tower_image, tower_image2):
        self.value += 10
        self.costs = int(int(self.costs)*(1.5))
        self.damage = int(int(self.damage)*(1.5))
        self.towerRange = int(int(self.towerRange)*(1.2))
        # Bilder:
        # -------
        first_place = (self.value % 10)-1
        second_place = (self.value // 10) - 1
        self.image = pygame.transform.scale(tower_image[second_place][first_place], (140, 140))
        self.image2 = pygame.transform.scale(tower_image2[second_place][first_place], (140, 140))
        return self

    def showRange(self, win):
        # Surface((width, height), flags=0, depth=0, masks=None)
        Range = pygame.Surface((1920, 1080), pygame.SRCALPHA, 32)
        # circle(surface, color, center, radius, width=0, draw_top_right=None, draw_top_left=None, draw_bottom_left=None, draw_bottom_right=None)
        pygame.draw.circle(Range, (255,0, 0, 80), (self.x+self.width//2, self.y+self.height//2), self.towerRange)
        win.blit(Range, (0,0))

    def spawnBullet(self, aimPosX, aimPosY, image):
        tempObject = Bullet(self.x, self.y, 50, 50, image, self.damage, aimPosX, aimPosY)
        self.TowerBullets.append(tempObject)
        allBullets.append(tempObject)

    # For Rotate
    def rotate(self, aimX, aimY):
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

    def findEnemys(self, enemy_lst, image):

        # Hier sucht den nähesten Gegner:
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
            # Check ob enemy noch am Leben ist
            if nearestEnemy.image != None:
                if nearestEnemy.direction == 1:
                    # Nach oben
                    additionX = 0
                    additionY = 1
                elif nearestEnemy.direction == 3:
                    # Nach unten
                    additionX = 0
                    additionY = -1
                elif nearestEnemy.direction == 0:
                    # Nach rechts
                    additionX = 1
                    additionY = 0
                elif nearestEnemy.direction == 2:
                    # Nach unten
                    additionX = -1
                    additionY = 0

                enemyX = nearestEnemy.x + e.width // 2 + additionX * 10
                enemyY = nearestEnemy.y + e.height // 2 + additionY * 10
                self.rotate(enemyX, enemyY)
                self.spawnBullet(enemyX, enemyY, pygame.transform.rotate(image, self.angle))



    def getValue(self):
        return self.value

    def getTowerLst(self):
        return self.TowerBullets


class Informations(Tower):
    def __init__(self, x, y, width, height, image, image2, costs, towerRange, damage, value, headline='', name='', description='', spm=''):
        super().__init__(x, y, width, height, image, image2, towerRange, damage, value, costs)
        self.headline = headline
        self.name = name
        self.description = description
        self.spm = spm
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        win.blit(self.image2, (self.x, self.y))
        font = pygame.font.SysFont('comicsans', 20)
        font_headline = pygame.font.SysFont('comicsans', 20, True, True)
        headline = font_headline.render(self.headline, True, (250, 250, 250))
        name = font.render(self.name, True, (250, 250, 250))
        description = font.render(self.description, True, (250, 250, 250))
        costs = font.render(str(self.costs), True, (250, 250, 250))
        towerRange = font.render("Additional Range: " + str(self.towerRange), True, (250, 250, 250))
        damage = font.render("Additional Damage: " + str(self.damage), True, (250, 250, 250))
        if self.headline == '':
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height) + 20))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))
        elif self.headline == 'Upgrade':
            win.blit(headline, (self.x + (self.width / 2 - headline.get_width() / 2), self.y - 20))
            win.blit(towerRange, (self.x + (self.width / 2 - towerRange.get_width() / 2), self.y + (self.height) - 10))
            win.blit(damage,
                     (self.x + (self.width / 2 - damage.get_width() / 2), self.y + (self.height) + 10))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))
        else:
            win.blit(headline, (self.x + (self.width / 2 - headline.get_width() / 2), self.y - 20))
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height)))
            win.blit(description,
                     (self.x + (self.width / 2 - description.get_width() / 2), self.y + (self.height) + 20))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 40))

