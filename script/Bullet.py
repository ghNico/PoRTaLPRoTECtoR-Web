import pygame

class Bullet:
    def __init__(self, x, y, width, height, image, damage, aimPosX=None, aimPosY=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.aimPosX = aimPosX
        self.aimPosY = aimPosY
        self.damage = damage
        self.path = []
        self.positionMarker = 1 #Auf eins, dass der schuss nicht hinter der Kanone anfängt
        self.speed = 1
        self.rect = pygame.Rect(self.x, self.y, self.width*1.5, self.height*1.5)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def trajectoryCreation(self):

        #60 Frames
        stepX = -(self.x - self.aimPosX)
        stepY = -(self.y - self.aimPosY)

        for i in range(0, round(10/ self.speed)):
            self.path.append((stepX * (i / round(10/self.speed)), stepY * (i / round(10/self.speed))))

    def move(self, win):
        i = self.positionMarker

        self.x += self.path[i][0]
        self.y += self.path[i][1]
        self.draw(win)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.positionMarker += 1
