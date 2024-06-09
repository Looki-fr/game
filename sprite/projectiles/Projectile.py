import pygame
import os
import math
import time
import random

class Projectile(pygame.sprite.Sprite):
    n=0
    @staticmethod
    def get_id():
        Projectile.n+=1
        return str(Projectile.n)
    def __init__(self, x, y, img_dict, angle, sender, need_to_stick):
        """
        
        img_dict: {
            "dir_path": str,
            "img_name": str,
            "nbr_image": int,
            "coefficient": int,
            "cpt_img_max": int,
            "id":str,
        }
        
        """
        super().__init__()
        self.sender=sender
        self.id=img_dict["id"]+Projectile.get_id()
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
        self.damage = img_dict["damage"]
        self.angle = math.radians(angle+random.uniform(-img_dict["angle_diff"],img_dict["angle_diff"]))
        self.speed = img_dict["speed"]
        self.need_to_stick=need_to_stick
        self.sticked=False
        self.mob_sticked=None
        self.mob_sticked_d=[0,0]

    def change_img(self):
        if self.compteur_img>=self.compteur_max:
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

    def stay_put(self):
        self.sticked=True

    def stick_to_mob(self, mob, handle_take_damage, collision,group_projectile):
        if self.need_to_stick:
            self.sticked=True
            self.mob_sticked=mob
            self.mob_sticked_d[0]=self.position[0]-mob.position[0]
            self.mob_sticked_d[1]=self.position[1]-mob.position[1]
            mob.projectile_sticked.append(self)

        mob.health-=self.damage
        handle_take_damage(mob, collision, group_projectile)
        
    def update_timers(self, dt):
        pass    

    def update(self):
        if not self.sticked:
            self.parabole_function()
            self.rect.topleft = self.position
        elif self.mob_sticked:
            self.position[0]=self.mob_sticked.position[0]+self.mob_sticked_d[0]
            self.position[1]=self.mob_sticked.position[1]+self.mob_sticked_d[1]
            self.rect.topleft = self.position
        self.change_img()

