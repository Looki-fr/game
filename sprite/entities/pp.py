import pygame
import time
from pygame.locals import *

class Profile_picture(pygame.sprite.Sprite):
    def __init__(self, x, y ,image1,image2, play_random_sound, player):
        super().__init__()
        self.id = "profile_picture"
        self.images=[image1, image2]
        self.i=0
        self.img=self.images[self.i]
        self.image=self.img.copy()
        # l'image devient transparente
        self.position = [x,y]
        self.rect = self.img.get_rect()
        self.compteur_img=0
        self.player=player

    def update(self):
        if self.compteur_img==20:
            self.compteur_img=0
            self.i+=1
            if self.i==len(self.images):
                self.i=0
            self.img=self.images[self.i]
        else:
            self.compteur_img+=1

        a=(self.player.max_health-(self.player.max_health-self.player.health))/self.player.max_health
        self.image=self.img.copy()
        x=(self.image.get_width() * a)
        self.image=self.img.copy()
        pygame.draw.line(self.image, (200,50,50), (0, self.image.get_height()-3), (x, self.image.get_height()-3), 2)
        self.rect.topleft = self.position