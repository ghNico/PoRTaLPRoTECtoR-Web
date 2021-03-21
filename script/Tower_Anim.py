import pygame, sys

class Tower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height, tower_image, angle):
        super().__init__()
        self.sprites = []
        self.groesse = []

        #for i in range(0, 360, 2):
            # rotieren und in einem neuen "surface" speichern
            #rotiert = pygame.transform.rotate(tower_image, i)

            # Bestimmen der neuen Abmessungen (nach Rotation ändern sich diese!)
            #groesse = rotiert.get_rect()
            #self.groesse.append(groesse)

            #self.sprites.append(pygame.transform.rotate(tower_image, i))

        self.pos_x = pos_x
        self.pos_y = pos_y


        #self.current_sprite = 0
        #self.image = self.sprites[self.current_sprite]
        #self.currentGroesse = self.groesse[self.current_sprite]

        self.image = tower_image
        self.angle = angle

        #self.rect = self.image.get_rect()
        #self.rect.topleft = [pos_x, pos_y]
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

    def incrementangle(self):
        self.angle+=1
    def draw(self, win):
        pass
        #win.blit(self.image, (self.pos_x+70 - self.currentGroesse.center[0], self.pos_y+70-self.currentGroesse.center[1]))

    def update(self):
        self.current_sprite += 1

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.currentGroesse = self.groesse[self.current_sprite]

        print(self.pos_x, self.pos_y)