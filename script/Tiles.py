import pygame


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
    def __init__(self, x, y, width, height, health, velocity, direction, images, path):
        super().__init__(x, y, width, height, images)
        self.health = health
        self.velocity = velocity
        self.direction = direction
        self.images = images
        self.path = path

    def draw(self, win):
        win.blit(self.images[self.direction], (self.x, self.y))

    # Hier noch rotate funktion

class Maps(Tiles):
    def __init__(self, x, y, width, height, value, difficulty, image=None):
        super().__init__(x, y, width, height, image)
        self.value = value
        self.difficulty = difficulty


class Tower(Tiles):
    def __init__(self, x, y, width, height, image, towerRange, damage, value, costs=0):
        super().__init__(x, y, width, height, image)
        self.costs = costs
        self.value = value
        self.towerRange = towerRange
        self.damage = damage
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def upgrade(self):
        return self


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
        if self.headline == '':
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height) + 10))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))
        else:
            win.blit(headline, (self.x + (self.width / 2 - headline.get_width() / 2), self.y - 20))
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height) - 10))
            win.blit(description,
                     (self.x + (self.width / 2 - description.get_width() / 2), self.y + (self.height) + 10))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))