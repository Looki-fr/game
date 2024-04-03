import pygame
import time
from .MOTHER import MOB
from mobs.bot.botStar import Bot
import random

class Star(MOB):

    def __init__(self, x, y, directory, zoom, id, checkpoint, Particule, update_particle, player, audio):
        """parametres : 
                - x : coordonne en x du joueur
                - y : coordonne en y du joueur
                - directory : chemin absolu vers le dossier du jeu"""
        # initialisation de la classe mere permettant de faire de cette classe un sprite
        MOB.__init__(self, zoom, f"star{id}", checkpoint, Particule,update_particle, directory, "assets\\Pink Star", audio)
        
        action=["attack", "crouch"]
        for a in action:
            self.actions.append(a)
            
        self.coefficient=1.5
            
        self._get_images("idle", 8, 5, "01-Idle", "Idle 0", reverse=True, coefficient=self.coefficient)
        self.origin_compteur_image_run=8
        self._get_images('run', 6, self.origin_compteur_image_run, "02-Run","Run 0", reverse=True, coefficient=self.coefficient)
        self.origin_compteur_image_fall = 1
        self._get_images("fall", 1, self.origin_compteur_image_fall, "04-Fall", "Fall 0", reverse=True, coefficient=self.coefficient)
        self._get_images("jump", 3, 4, "03-Jump", "Jump 0", reverse=True, coefficient=self.coefficient)  
        self._get_images("crouch", 2, 1, "05-Ground", "Ground 0", reverse=True, coefficient=self.coefficient) 
        self._get_images("up_to_attack", 3, 5, "06-Anticipation", "Anticipation 0", reverse=True, coefficient=self.coefficient) 
        self._get_images("attack1", 4, 3, "07-Attack", "Attack 0", reverse=True, coefficient=self.coefficient) 
        self._get_images("hurt", 4, 4, "08-Hit", "Hit 0", reverse=True, coefficient=self.coefficient) 
        self._get_images("dying", 4, 5, "09-Dead Hit", "Dead Hit 0", reverse=True, coefficient=self.coefficient) 
        self._get_images("air_hurt", 4, 4, "08-Hit", "Hit 0", reverse=True, coefficient=self.coefficient) 
        
        self.image = self.images[self.weapon]["idle"]["right"]["1"]
        
        self.position = [x,y - self.image.get_height()]
        self.rect = self.image.get_rect()
        
        # creation d'un rect pour les pieds et le corps
        self.feet = pygame.Rect(0,0,self.rect.width * 0.7, self.rect.height*0.1)
        self.head = pygame.Rect(0,0,self.rect.width * 0.7, self.rect.height*0.1)
        self.body = pygame.Rect(0,0,self.rect.width * 0.7, self.rect.height*0.8)
        self.rect_attack = self.body
        self.rect_attack_update_pos="mid"
        self.complement_collide_wall_right = self.body.w
        self.complement_collide_wall_left = self.body.w
        self.increment_left_right=0
        
        # enregistrement de l'ancienne position pour que si on entre en collision avec un element du terrain la position soit permutte avec l'anciene
        self.old_position = self.position.copy()
        
        # self.speed_coeff=self._random_choice([(0.65, 2), (0.68, 3), (0.71, 3),(0.74, 5),(0.77, 10),(0.80, 10),(0.83, 5),(0.86, 3), (0.89, 3), (0.92, 2)])
        self.speed_coeff=random.random() * 0.3 + 0.65

        #attack
        self.can_attack_while_jump=True
        self.attack_damage={}
        self.attack_damage["attack1"]=([1,2,3,4], self._random_choice([(1, 2), (1.2, 3), (1.4, 5),(1.6, 10),(1.8, 5),(2, 3),(2.2, 2)]))
        self.is_attacking = False
        self.timers["timer_attack"] = 0
        self.cooldown_attack=2
        self.timers["fin_attack"] = 0
        self.cooldown_fin_attack=1
        self.direction_attack=""
        
        self.compteur_jump_min = -5
        
        self.dico_action_functions = {
            "fall":self.chute,
            "jump":self.saut,
            "attack1":self.attack,
            "air_hurt":self.air_hurt,
        }       
        
        self.range_attack=self.rect_attack.w * 10
        self.bot=Bot(self, player)
    
    def update_timers(self, dt):
        super().update_timers(dt)
        self.bot.update_timers(dt)

    def debut_crouch(self):
        """very simple"""
        if not self.is_attacking:
            self.change_direction("crouch", self.direction)
    
    def debut_attack(self):
        self.compteur_attack=0
        self.is_attacking = True
        self.change_direction("up_to_attack", self.direction)
        self.timers["timer_attack"]=time.time()
        self.direction_attack=self.direction
        self.max_speed_run = self.max_speed_run * 2
    
    def attack(self):
        if self.is_falling:
            self.chute()
        if self.is_jumping:
            self.saut()
        if self.direction_attack=="left":
            self.move_left(change_image=False, just_run=True)
        elif self.direction_attack=="right":
            self.move_right(change_image=False, just_run=True)

    def fin_attack(self, ground=True):
        self.is_attacking = False
        if ground:
            self.change_direction("hurt", self.direction)
            self.action="idle"
        else:
            self.change_direction("air_hurt", self.direction)
        self.max_speed_run = self.max_speed_run / 2
        self.timers["fin_attack"]=time.time()

    def air_hurt(self):
        if self.is_falling:self.chute()

    def debut_saut(self):
        if self.is_attacking:
            super().debut_saut(change_image=False)
        else:
            super().debut_saut()

    def fin_saut(self, ground=False, cogne=False):
        if self.is_attacking:
            super().fin_saut(no_change=True, ground=ground, cogne=cogne)
        else:
            super().fin_saut(ground=ground, cogne=cogne)

    def update_action(self):
        super().update_action(["attack1"])