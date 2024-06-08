import pygame
import os
import math
import time

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, img_dict, angle, speed, damage):
        """
        
        img_dict: {
            "dir_path": str,
            "img_name": str,
            "nbr_image": int,
            "coefficient": int,
            "cpt_img_max": int,
            "id":str
        }
        
        """
        super().__init__()
        self.id=img_dict["id"]
        self.images = []
        for i in range(img_dict["nbr_image"]):
            self.images.append(pygame.image.load(os.path.join(img_dict["dir_path"], img_dict["img_name"]+str(i+1)+".png")).convert_alpha())
            self.images[i] = pygame.transform.scale(self.images[i], (int(self.images[i].get_width()*img_dict["coefficient"]), int(self.images[i].get_height()*img_dict["coefficient"])))
            self.images[i] = pygame.transform.rotate(self.images[i], angle)
        self.image=self.images[0]
        self.i=0
        self.position = [x,y]
        self.rect = self.image.get_rect()
        self.compteur_img=0
        self.compteur_max=img_dict["cpt_img_max"]
        self.damage = damage
        self.angle = math.radians(angle)
        self.speed = speed

    def change_img(self):
        if self.compteur_img==self.compteur_max:
            self.compteur_img=0
            self.i+=1
            if self.i==len(self.images):
                self.i=0
            self.image=self.images[self.i]
        else:
            self.compteur_img+=1

    def parabole_function(self):
        self.position[0] += self.speed * math.cos(self.angle)
        self.position[1] += self.speed * math.sin(self.angle)

    def update(self):
        self.parabole_function()
        self.rect.topleft = self.position
        self.change_img()
