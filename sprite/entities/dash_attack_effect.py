import pygame
import time
from pygame.locals import *

class Dash_attack_image(pygame.sprite.Sprite):
    def __init__(self, x, y ,image1,image2,image3, play_random_sound):
        super().__init__()
        self.id = "dash_attack_effect"
        self.images=[image1, image2, image3]
        self.i=0
        for img in self.images:
            transColor = img.get_at((0,0))
            img.set_colorkey(transColor)
        self.image=self.images[self.i]
        # l'image devient transparente
        self.position = [x,y]
        self.rect = self.image.get_rect()
        self.body = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.8)
        self.t1 = time.time()
        self.compteur_img=0
        self.finish=False
        play_random_sound("dash_attack_sprite", 2)
        
    def update_timers(self, dt):
        self.t1 += dt

    def update(self):
        if self.compteur_img==3 and self.i!=2:
            self.compteur_img=0
            self.i+=1
            self.image=self.images[self.i]
        elif self.compteur_img==4 and self.i==2:
            self.finish=True
        self.compteur_img+=1


        self.rect.topleft = self.position
        self.body.center = self.rect.center