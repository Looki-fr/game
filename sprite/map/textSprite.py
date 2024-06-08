import pygame
from pygame.locals import *
import os

class TextSprite():
    def __init__(self, x, y ,id, directory, zoom):
        self.id = id
        self.image = pygame.image.load(os.path.join(directory,"assets","text",f"{id}.png"))
        self.image = pygame.transform.scale(self.image, (round(self.image.get_width()*0.6*zoom), round(self.image.get_height()*0.6*zoom)))
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.position = [x,y]
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.topleft = self.position