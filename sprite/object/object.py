from mobs.mobs.MOTHER import MOB
import pygame
import random
class Object(MOB):
    def __init__(self, zoom, id, checkpoint, directory, directory_assets, audio, dir_name, nbr_image, img_name, coefficient, x, y, animation_speed):
        super().__init__(zoom, id, checkpoint, None, None, directory,  directory_assets, audio)

        self.coefficient=coefficient
        # initialisation de la classe mere permettant de faire de cette classe un sprite
        self._get_images("idle", nbr_image, animation_speed, dir_name, img_name, reverse=True, coefficient=self.coefficient)
        self.origin_compteur_image_fall = animation_speed
        self.images[self.weapon]["fall"] = self.images[self.weapon]["idle"]
        self.images[self.weapon]["jump"] = self.images[self.weapon]["idle"]

        self.one_animation=True
        self.image = self.images[self.weapon]["idle"]["right"]["1"]
        
        self.position = [x,y - self.image.get_height()]
        self.rect = self.image.get_rect()
        
        self.body = pygame.Rect(0,0,self.rect.width * 1, self.rect.height*1)
        self.feet = pygame.Rect(0,0,self.rect.width * 1, self.rect.height*1)
        self.head = pygame.Rect(0,0,self.rect.width * 1, self.rect.height*1)

        # enregistrement de l'ancienne position pour que si on entre en collision avec un element du terrain la position soit permutte avec l'anciene
        self.old_position = self.position.copy()
        
        # self.speed_coeff=self._random_choice([(0.65, 2), (0.68, 3), (0.71, 3),(0.74, 5),(0.77, 10),(0.80, 10),(0.83, 5),(0.86, 3), (0.89, 3), (0.92, 2)])
        self.speed_coeff=random.random() * 0.3 + 0.65

        self.dico_action_functions = {
            "fall":self.chute,
            "jump":self.saut,
        }      

        self.action="parabolic"
        self.action_image="parabolic"

        #parabolic
        self.parabolic=True
        self.direction_parabolic="right"
        if random.randint(0,1)==0:
            self.direction_parabolic="left"
        self.speed_coeff=random.random() * 0.8 + 0.15
        self.speed_coeff_jump=1.25-self.speed_coeff
        self.debut_saut()

    def update(self):
        super().update()
        if self.parabolic:
            if self.direction_parabolic=="right":
                self.move_right(just_run=True)
            else:
                self.move_left(just_run=True)