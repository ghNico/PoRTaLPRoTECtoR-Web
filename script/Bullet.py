import pygame

class Bullet:
    """
        Bullet class for all bullets
        During object creation it needs position, width, height, image, damage, aim (where the bullets should hit)
    """
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
        """
        Draws the image of the bullet

        Arguments: pygame window

        Test:
            -correct display of the bullet during movement
            -check if it will always get drawn
        """
        win.blit(self.image, (self.x, self.y))

    def trajectoryCreation(self):

        #60 Frames
        stepX = -(self.x - self.aimPosX)
        stepY = -(self.y - self.aimPosY)

        for i in range(0, round(10/ self.speed)):
            self.path.append((stepX * (i / round(10/self.speed)), stepY * (i / round(10/self.speed))))

    def move(self, win):
        """
        Moves through the path of the bullet and calls the draw methode

        Arguments: pygame window

        Test:
            -correct path that will hit the enemy
            -check if it is a fluent movement (enough steps till enemy)
        """

        i = self.positionMarker

        self.x += self.path[i][0]
        self.y += self.path[i][1]
        self.draw(win)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.positionMarker += 1
