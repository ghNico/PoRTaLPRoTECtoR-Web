import pygame

class Tiles:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def isOver(self):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

class Button(Tiles):
    def __init__(self, color, x, y, width, height, image, name=''):
        super().__init__(x, y, width, height)
        self.color = color
        self.name = name
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
    def draw(self, win):
        # Call this method to draw the button on the screen
        pygame.draw.rect(win, self.color, self.rect, 0)
        if self.image != '':
            win.blit(self.image, (self.x , self.y))
        if self.name != '':
            font = pygame.font.SysFont('comicsans', 20)
            name = font.render(self.name, True, (0, 0, 0))
            win.blit(name, (
                self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height / 2 - name.get_height() / 2)))

class Informations(Tiles):
    def __init__(self, x, y, width, height, image, headline='', name='', description='', spm='', costs=''):
        super().__init__(x, y, width, height)
        self.headline = headline
        self.name = name
        self.costs = costs
        self.description = description
        self.spm = spm
        self.costs = costs
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        font = pygame.font.SysFont('comicsans', 20)
        font_headline = pygame.font.SysFont('comicsans', 20, True, True)
        headline = font_headline.render(self.headline, True, (0, 0, 0))
        name = font.render(self.name, True, (0, 0, 0))
        description = font.render(self.description, True, (0, 0, 0))
        costs = font.render(self.costs, True, (0, 0, 0))
        if self.headline == '':
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height) + 10))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))
        else:
            win.blit(headline, (self.x + (self.width / 2 - headline.get_width() / 2), self.y - 20 ))
            win.blit(name, (self.x + (self.width / 2 - name.get_width() / 2), self.y + (self.height) - 10))
            win.blit(description, (self.x + (self.width / 2 - description.get_width() / 2), self.y + (self.height) + 10))
            win.blit(costs, (self.x + (self.width / 2 - costs.get_width() / 2), self.y + (self.height) + 30))