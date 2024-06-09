import pygame
import time
import os

class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, img_dict, group, mob_sticked, reverse, angle=None):
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
        self.images = []
        for i in range(img_dict["nbr_image"]):
            self.images.append(pygame.image.load(os.path.join(img_dict["dir_path"], img_dict["img_name"]+str(i+1)+".png")).convert_alpha())
            self.images[i] = pygame.transform.scale(self.images[i], (int(self.images[i].get_width()*img_dict["coefficient"]), int(self.images[i].get_height()*img_dict["coefficient"])))
            if angle != None:
                self.images[i] = pygame.transform.rotate(self.images[i], angle)
            elif reverse:
                self.images[i] = pygame.transform.flip(self.images[i], True, False)

        self.image=self.images[0]
        self.i=0
        self.position = [x,y]
        self.rect = self.image.get_rect()
        self.compteur_img=0
        self.compteur_max=img_dict["cpt_img_max"]
        self.id=img_dict["id"]
        self.group=group
        self.group.add(self)
        self.mob_sticked=mob_sticked
        if mob_sticked:
            self.mob_sticked_d = (self.position[0] - mob_sticked.position[0], self.position[1] - mob_sticked.position[1])
    
    def change_img(self):
        if self.compteur_img>=self.compteur_max:
            self.compteur_img=0
            self.i+=1
            if self.i==len(self.images):
                self.group.remove(self)
                self.group=None
                return
            self.image=self.images[self.i]
        else:
            self.compteur_img+=1

    def update(self):
        self.change_img()
        if self.mob_sticked:
            self.position[0]=self.mob_sticked.position[0]+self.mob_sticked_d[0]
            self.position[1]=self.mob_sticked.position[1]+self.mob_sticked_d[1]
        self.rect.topleft = self.position