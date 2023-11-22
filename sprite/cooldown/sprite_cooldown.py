import pygame
import time
from pygame.locals import *

class Sprite_cooldown(pygame.sprite.Sprite):
    def __init__(self, image, x, y, timers, key, cooldown):
        super().__init__()
        self.id = "image_dash"
        self.img = image 
        self.image=self.img.copy()
        self.position = [x, y]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.timers=timers
        self.key=key
        self.cooldown=cooldown
        # start / end etc

        
    def update(self):
        timer=self.timers[self.key]
        a=(time.time()-timer)/self.cooldown
        self.image=self.img.copy()
        x=(self.image.get_width() * min(1, a))
        pygame.draw.line(self.image, (200,50,50), (0, self.image.get_height()-3), (x, self.image.get_height()-3), 2)