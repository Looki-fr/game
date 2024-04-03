import pygame
import time
from pygame.locals import *

class Counter(pygame.sprite.Sprite):
    def __init__(self, x, y ,dir,img_name, nbr_image, player, key, coefficient, compteur_max):
        super().__init__()
        self.id = "profile_picture"
        self.images=[]
        for i in range(nbr_image):
            self.images.append(pygame.image.load(dir+img_name+str(i+1)+".png").convert_alpha())
            self.images[i]=pygame.transform.scale(self.images[i], (int(self.images[i].get_width()*coefficient), int(self.images[i].get_height()*coefficient)))
        self.i=0
        self.img=self.images[self.i]
        self.image=self.img.copy()
        # l'image devient transparente
        self.position = [x,y]
        self.rect = self.img.get_rect()
        self.compteur_img=0
        self.compteur_max=compteur_max
        self.player=player
        self.key=key

    def change_img(self):
        if self.compteur_img==self.compteur_max:
            self.compteur_img=0
            self.i+=1
            if self.i==len(self.images):
                self.i=0
            self.img=self.images[self.i]
        else:
            self.compteur_img+=1

    def update(self):
        self.change_img()
        self.image=pygame.Surface((self.img.get_width(), self.img.get_height()+30), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        self.image.blit(self.img, (0,0))
        font = pygame.font.SysFont('courier', 30, bold=True)
        img = font.render(str(self.player.inventory[self.key]), True, (0, 0, 0))
        self.image.blit(img, (self.image.get_width()/2-img.get_width()/2, self.image.get_height()-img.get_height()))
        self.rect.topleft = self.position