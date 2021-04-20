import pygame
import math


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



class Button(Tiles):
    def __init__(self, color, x, y, width, height, image=None, name=''):
        super().__init__(x, y, width, height, image)
        self.color = color
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        # Call this method to draw the button on the screen
        pygame.draw.rect(win, self.color, self.rect, 0)
        if self.image != '':
            win.blit(self.image, (self.x, self.y))
        if self.name != '':
            font = pygame.font.SysFont('comicsans', 20)
            name = font.render(self.name, True, (0, 0, 0))
            win.blit(name, (
                self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height / 2 - name.get_height() / 2)))



class Enemy(Tiles):
    def __init__(self, x, y, width, height, health, maxHealth, velocity, direction, images, path):
        super().__init__(x, y, width, height, images)
        self.health = health
        self.maxHealth = maxHealth
        self.velocity = velocity
        self.direction = direction
        self.images = images
        self.path = path

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
        if self.health<=0:
            self.image = None
            self.health = 0
            self.maxHealth = 0
        else:
            self.health -= damage

    def moveThroughPath(self):
        pass


class Maps(Tiles):
    def __init__(self, x, y, width, height, value, difficulty, image=None):
        super().__init__(x, y, width, height, image)
        self.value = value
        self.difficulty = difficulty


class Tower(Tiles):
    def __init__(self, x, y, width, height, image, towerRange, damage, value, costs=0, ShowRangeBoolean=False):
        super().__init__(x, y, width, height, image)
        self.costs = costs
        self.value = value
        self.towerRange = towerRange
        self.damage = damage
        self.rect = pygame.Rect(x, y, width, height)
        self.ShowRangeBoolean = ShowRangeBoolean

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def upgrade(self, tower_image):
        self.value += 10
        print(self.value)
        self.costs = int(int(self.costs)*(1.5))
        self.damage = int(int(self.damage)*(1.5))
        self.towerRange += 30
        first_place = (self.value % 10)-1
        second_place = (self.value // 10) - 1
        self.image = pygame.transform.scale(tower_image[second_place][first_place], (140, 140))
        return self

    def showRange(self, win):
        # Surface((width, height), flags=0, depth=0, masks=None)
        Range = pygame.Surface((self.towerRange*2, self.towerRange*2), pygame.SRCALPHA, 32)
        # circle(surface, color, center, radius, width=0, draw_top_right=None, draw_top_left=None, draw_bottom_left=None, draw_bottom_right=None)
        pygame.draw.circle(Range, (255,0, 0, 120), (self.width//2+self.towerRange//math.pi, self.height//2+self.towerRange//math.pi), self.towerRange)
        win.blit(Range, (self.x+self.width//2-self.towerRange, self.y+self.height//2-self.towerRange))


class Informations(Tower):
    def __init__(self, x, y, width, height, image, costs, towerRange, damage, value, headline='', name='', description='', spm=''):
        super().__init__(x, y, width, height, image, towerRange, damage, value, costs)
        self.headline = headline
        self.name = name
        self.description = description
        self.spm = spm
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        font = pygame.font.SysFont('comicsans', 20)
        font_headline = pygame.font.SysFont('comicsans', 20, True, True)
        headline = font_headline.render(self.headline, True, (0, 0, 0))
        name = font.render(self.name, True, (0, 0, 0))
        description = font.render(self.description, True, (0, 0, 0))
        costs = font.render(str(self.costs), True, (0, 0, 0))
        towerRange = font.render("Additional Range: " + str(self.towerRange), True, (0, 0, 0))
        damage = font.render("Additional Damage: " + str(self.damage), True, (0, 0, 0))
        if self.headline == '':
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height) + 10))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))
        elif self.headline == 'Upgrade':
            win.blit(headline, (self.x + (self.width / 2 - headline.get_width() / 2), self.y - 20))
            win.blit(towerRange, (self.x + (self.width / 2 - towerRange.get_width() / 2), self.y + (self.height) - 10))
            win.blit(damage,
                     (self.x + (self.width / 2 - damage.get_width() / 2), self.y + (self.height) + 10))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))
        else:
            win.blit(headline, (self.x + (self.width / 2 - headline.get_width() / 2), self.y - 20))
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height) - 10))
            win.blit(description,
                     (self.x + (self.width / 2 - description.get_width() / 2), self.y + (self.height) + 10))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))

