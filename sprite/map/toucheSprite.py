import pygame
import time
from pygame.locals import *

class ToucheSprite():
    """ class affichant une image du joueur quand il dash pour une courte duree"""
    def __init__(self, x, y ,id, directory, zoom):
        self.id = id
        self.image1 = pygame.image.load(f'{directory}\\assets\\text\\{id}.png')
        self.image1=pygame.transform.scale(self.image1, (self.image1.get_width()*zoom, self.image1.get_height()*zoom))
        self.image1.set_colorkey(self.image1.get_at((0,0)))
        self.image2 = pygame.image.load(f'{directory}\\assets\\text\\{id}2.png')
        self.image2=pygame.transform.scale(self.image2, (self.image2.get_width()*zoom, self.image2.get_height()*zoom))
        self.image2.set_colorkey(self.image2.get_at((0,0)))
        self.image = self.image1
        self.image_str = "image1"
        self.position = [x,y]
        self.rect = self.image.get_rect()
        self.t1 = time.time()
        self.cooldown = 1
      
    def update_timers(self, dt):
        self.t1 += dt

    def update(self):
        """alternance des 2 images pour creer une animation"""
        if time.time() - self.t1 > self.cooldown:
            self.t1 = time.time()
            if self.image_str == "image1":
                self.image = self.image2
                self.image_str = "image2"
            elif self.image_str == "image2":
                self.image = self.image1
                self.image_str = "image1"
        self.rect.topleft = self.position