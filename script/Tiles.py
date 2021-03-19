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
    def __init__(self, color, x, y, width, height, image, text=''):
        super().__init__(x, y, width, height)
        self.color = color
        self.text = text
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
    def draw(self, win):
        # Call this method to draw the button on the screen
        pygame.draw.rect(win, self.color, self.rect, 0)
        if self.image != '':
            win.blit(self.image, (self.x , self.y))
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

class Informations(Tiles):
    def __init__(self, x, y, width, height, image, headline='', text1='', text2='', text3=''):
        super().__init__(x, y, width, height)
        self.headline = headline
        self.text1 = text1
        self.text2 = text2
        self.text3 = text3
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        font = pygame.font.SysFont('comicsans', 20)
        font_headline = pygame.font.SysFont('comicsans', 20, True, True)
        headline = font_headline.render(self.headline, True, (0, 0, 0))
        text1 = font.render(self.text1, True, (0, 0, 0))
        text2 = font.render(self.text2, True, (0, 0, 0))
        text3 = font.render(self.text3, True, (0, 0, 0))
        if headline == '':
            win.blit(text1, (self.x + (self.width / 2 - text1.get_width() / 2), self.y + (self.height) + 10))
            win.blit(text2, (self.x + (self.width / 2 - text2.get_width() / 2), self.y + (self.height) + 30))
        else:
            win.blit(headline, (self.x + (self.width / 2 - headline.get_width() / 2), self.y - 20 ))
            win.blit(text1, (self.x + (self.width / 2 - text1.get_width() / 2), self.y + (self.height) + 10))
            win.blit(text2, (self.x + (self.width / 2 - text2.get_width() / 2), self.y + (self.height) + 30))
            win.blit(text3, (self.x + (self.width / 2 - text2.get_width() / 2), self.y + (self.height) + 40))