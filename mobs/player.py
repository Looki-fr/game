import pygame
import time
from .MOTHER import MOB


class Player(MOB):

    def __init__(self, x, y, directory, zoom, id, checkpoint, Particule):
        """parametres : 
                - x : coordonne en x du joueur
                - y : coordonne en y du joueur
                - directory : chemin absolu vers le dossier du jeu"""
        # initialisation de la classe mere permettant de faire de cette classe un sprite
        MOB.__init__(self, zoom, f"player{id}", checkpoint, Particule, directory, "assets\\Bounty Hunter\\Individual Sprite")

        #"up_to_fall", 
        action=["Edge_Idle", "Edge_grab", "Wall_slide", "ground_slide", "crouch", "jump_edge", "dash", "attack", "dash_attack", "pary"]
        for a in action:
            self.actions.append(a)
        
        coefficient=2
        self.weapon="shotgun"
        for w in ["shotgun", "crossbow", "gun"]:
            self._get_images("idle", 8, 5, "Idle", "Idle_", w, coefficient=coefficient)
            self.origin_compteur_image_run=8
            self._get_images('run', 8, self.origin_compteur_image_run, "Run","Run_", w, coefficient=coefficient)
            self.origin_compteur_image_fall = 6
            self._get_images("fall", 3, self.origin_compteur_image_fall, "Fall", "Fall_", w, coefficient=coefficient)
            self._get_images("jump", 4, 4, "Jump", "Jump_", w, coefficient=coefficient) 
            self._get_images("hurt", 3, 4, "Hurt", "Hurt_", w, coefficient=coefficient) 
            self._get_images("dying", 7, 4, "Death", "Death_", w, coefficient=coefficient) 
            self._get_images("ground_slide", 4, 3, "Slide", "Slide_", w, coefficient=coefficient) 
            self._get_images("dash_attack", 10, 3, "Dash Attack", "Dash-Attack_", w, coefficient=coefficient)
            self._get_images("crouch", 5, 1, "Croush", "Croush_", w, coefficient=coefficient) 
            self._get_images("Edge_climb", 3, 50, "Edge Climb", "Edge-Climb_", w, coefficient=coefficient) 
            self._get_images("Edge_grab", 4, 5, "Edge Grab", "Edge-Grab_", w, coefficient=coefficient) 
            self._get_images("Wall_slide", 3, 4, "WallSlide", "WallSlide_", w, coefficient=coefficient, reverse=True) 
            self._get_images("air attack", 5, 3, "Air Attack", "Air-Attack_", w, coefficient=coefficient) 
            self._get_images("attack1", 8, 2, "Attack", "Attack_", w, coefficient=coefficient) 
            self._get_images("attack2", 6, 2, "Attack2", "Attack_", w, coefficient=coefficient)
            self._get_images("pary", 7, 6, "Roll", "Roll_", w, coefficient=coefficient)

        # self._get_images("idle", 6, 5, "idle_right", "Warrior_Idle_")
        # self.origin_compteur_image_run=8
        # self._get_images('run', 8, self.origin_compteur_image_run, "Run_right","Warrior_Run_")
        # self.origin_compteur_image_fall = 6
        # self._get_images("fall", 3, self.origin_compteur_image_fall, "Fall_right", "Warrior_Fall_")
        # self._get_images("up_to_fall", 2, 4, "UptoFall_right", "Warrior_UptoFall_")    
        # self._get_images("jump", 3, 4, "Jump_right", "Warrior_Jump_")  
        # self._get_images("Edge_Idle", 6, 4, "Edge-Idle_right", "Warrior_Edge-Idle_")  
        # self._get_images("Edge_grab", 5, 4, "EdgeGrab_right", "Warrior_Edge-Grab_")  
        # self._get_images("Wall_slide", 3, 4, "WallSlide_right", "Warrior_WallSlide_")  
        # self._get_images("ground_slide", 5, 3, "Slide_right", "Warrior-SlideNoEffect_") 
        # self._get_images("crouch", 5, 1, "Crouch_right", "Warrior_Crouch_") 
        # self._get_images("attack1", 8, 2, "Attack1", "Warrior_Attack_") 
        # self._get_images("attack2", 4, 2, "Attack2", "Warrior_Attack_") 
        # self._get_images("dash_attack", 12, 3, "Dash_Attack", "Warrior_Dash-Attack_") 
        # self._get_images("hurt", 4, 4, "HurtnoEffect", "Warrior_hurt_") 
        # self._get_images("dying", 11, 4, "Death-Effect", "Warrior_Death_") 
        # self._get_images("pary", 4, 6, "pary", "pary_")
        
        self.image = self.images[self.weapon]["idle"]["right"]["1"]
        
        self.position = [x,y - self.image.get_height()]
        self.position_wave_map=[0,0]
        self.rect = self.image.get_rect()
        
        # creation d'un rect pour les pieds et le corps
        self.feet = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.1)
        self.head = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.2)
        self.body = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.7)
        self.rect_attack = pygame.Rect(0,0,self.rect.width * 0.8, self.rect.height*1)
        self.rect_air_attack = pygame.Rect(0,0,self.rect.width * 0.8, self.rect.height*0.5)
        self.rect_attack_update_pos="left_right"
        self.complement_collide_wall_right = self.body.w
        self.complement_collide_wall_left = self.body.w
        self.is_mob=False
        
        # enregistrement de l'ancienne position pour que si on entre en collision avec un element du terrain la position soit permutte avec l'anciene
        self.old_position = self.position.copy()
        
        # jump edge
        self.is_jumping_edge = False
        self.compteur_jump_edge_min = -5.5
        self.compteur_jump_edge = self.compteur_jump_edge_min
        self.original_compteur_jump_edge_max = -1.5
        self.compteur_jump_edge_max = self.original_compteur_jump_edge_max
        self.speed_jump_edge = 0
        self.coord_debut_jump_edge = [-999,-999]
        self.direction_jump_edge = ''
        self.increment_jump_edge = 0.25
        self.jump_edge_pieds = False
        
        # edge grab / idle
        self.is_sliding = False
        self.is_grabing_edge = False
        self.direction_wall = ""
        self.speed_sliding = 3.5
        
        # dash
        self.a_dash = False
        self.is_dashing = False
        self.image1_dash = False
        self.image2_dash = False
        self.image3_dash = False
        self.image4_dash = False
        self.compteur_dash_min = -8
        self.compteur_dash = self.compteur_dash_min
        self.compteur_dash_max = 0
        self.compteur_dash_increment = 0.4
        self.compteur_dash_immobile = 0
        self.compteur_dash_immobile_max = 10
        self.speed_dash = 0
        self.dash_direction_x = ""
        self.dash_direction_y = "" 
        # [x,y, image_modifié, cooldown]
        self.images_dash = []
        self.dash_cooldown_image = 0.15
        self.coord_debut_dash = [-999,-999]
    
        # ground slide
        self.is_sliding_ground = False
        self.compteur_slide_ground_min = -5
        self.compteur_slide_ground = self.compteur_slide_ground_min
        self.compteur_slide_ground_increment = 0.25
        # le mouvement doit durer exactement le temps necessaire à passer toutes les images de wall slide
        self.compteur_slide_ground_max = self.compteur_slide_ground_min + self.compteur_slide_ground_increment*self.images["shotgun"]["ground_slide"]["compteur_image_max"]*self.images["shotgun"]["ground_slide"]["nbr_image"]
        self.speed_slide_ground = 0
        self.slide_ground_direction_x = ""
        self.cooldown_slide_ground = 0.4
        self.timer_cooldown_slide_ground = 0
        
        #attack
        self.attack_damage={}
        self.attack_damage["attack1"]=([6,7,8], 100)
        self.attack_damage["attack2"]=([2,3,4],100)
        self.attack_damage["dash_attack"]=([6,7],100)
        self.attack_damage["air attack"]=([3,4,5],100)

        self.has_air_attack = True
        self.is_attacking = False
        self.a_attaquer2=False
        self.timer_attack=0
        self.cooldown_attack=1
        self.compteur_attack=0
        self.increment_attack=1
        self.compteur_attack_max=5
        self.direction_attack=""
        self.timer_attack_aerienne=0
        self.cooldown_attack_aerienne=0.5
    
        # pary
        self.is_parying = False
        self.compteur_pary=0
        self.increment_pary=1
        self.compteur_pary_max=5
        self.direction_pary=""
        self.timer_pary=0
        self.cooldown_pary=0.5
        
        #dash attack
        self.is_dashing_attacking = False
        self.timer_dash_attack=0
        self.cooldown_dash_attack=1
        self.compteur_dash_attack_min=-5
        self.compteur_dash_attack=self.compteur_dash_attack_min
        self.increment_dash_attack=0.1
        self.compteur_dash_attack_max = self.compteur_dash_attack_min + self.increment_dash_attack*self.images["shotgun"]["dash_attack"]["compteur_image_max"]*self.images["shotgun"]["dash_attack"]["nbr_image"] - 8*self.increment_dash_attack
        
        self.is_friendly=True
        
        self.dico_action_functions = {
            "fall":self.chute,
            "up_to_fall":self.chute,
            "jump":self.saut,
            "dash":self.dash,
            "jump_edge":self.saut_edge,
            "Wall_slide":self.sliding,
            "Edge_Idle":self.sliding,
            "Edge_grab":self.sliding,
            "ground_slide":self.slide_ground
        }       
    
    def move_right(self, pieds_sur_sol = False): 
        self.is_mouving_x = True
        if (not self.is_attacking and not self.is_parying) or not pieds_sur_sol  or self.id != "player1":
            self.position[0] += self.speed_coeff*self.speed * self.zoom * self.speed_dt *abs(self.motion[0])
            self.update_speed()
        elif self.is_attacking:
            if self.compteur_attack < self.compteur_attack_max:
                self.compteur_attack+=self.increment_attack
                self.position[0] += self.speed *0.8* (self.compteur_attack_max/self.compteur_attack)* self.zoom * self.speed_dt *abs(self.motion[0])
                if self.compteur_attack == self.compteur_attack_max:
                    self.speed=self.speed*0.7
                    if self.speed < self.origin_speed_run:
                        self.speed=self.origin_speed_run
        elif self.is_parying:
            if self.compteur_pary < self.compteur_pary_max:
                self.compteur_pary+=self.increment_pary
                self.position[0] += self.speed *0.8* (self.compteur_pary_max/self.compteur_pary)* self.zoom * self.speed_dt *abs(self.motion[0])
            
        if pieds_sur_sol:
            if self.action_image != "run" and self.action_image != "jump" and self.action_image != "crouch" and not self.is_attacking and not self.is_parying:
                self.change_direction("run","right") 
        if self.direction != "right":
            if self.action_image == "crouch":
                # we dont want the crouch animation du re start from the biggining
                self.change_direction(self.action_image,"right",compteur_image=self.compteur_image, current_image=self.current_image)
            elif not self.is_attacking and not self.is_parying:
                self.change_direction(self.action_image,"right")       
            else:
                self.direction="right" 

    def move_left(self, pieds_sur_sol = False): 
        self.is_mouving_x = True
        if (not self.is_attacking and not self.is_parying) or not pieds_sur_sol or self.id != "player1":
            self.position[0] -= self.speed_coeff*self.speed * self.zoom * self.speed_dt *abs(self.motion[0])
            self.update_speed()
        elif self.is_attacking:
            if self.compteur_attack < self.compteur_attack_max:
                self.compteur_attack+=self.increment_attack
                self.position[0] -= self.speed *0.8* (self.compteur_attack_max/self.compteur_attack)* self.zoom * self.speed_dt *abs(self.motion[0])
                if self.compteur_attack == self.compteur_attack_max:
                    self.speed=self.speed*0.7
                    if self.speed < self.origin_speed_run:
                        self.speed=self.origin_speed_run
        elif self.is_parying:
            if self.compteur_pary < self.compteur_pary_max:
                self.compteur_pary+=self.increment_pary
                self.position[0] -= self.speed *0.8* (self.compteur_pary_max/self.compteur_pary)* self.zoom * self.speed_dt *abs(self.motion[0])
        if pieds_sur_sol:
            if self.action_image != "run" and self.action_image != "jump" and self.action_image != "crouch" and not self.is_attacking and not self.is_parying:
                self.change_direction("run","left") 
        if self.direction != "left":
            if self.action_image == "crouch":
                # we dont want the crouch animation du re start from the biggining
                self.change_direction(self.action_image,"left",compteur_image=self.compteur_image, current_image=self.current_image)
            elif not self.is_attacking and not self.is_parying:
                self.change_direction(self.action_image,"left")  
            else:
                self.direction="left"
    
    def debut_pary(self):
        self.compteur_pary=0
        self.is_parying = True
        self.change_direction("pary", self.direction)
        self.direction_attack=self.direction
        self.timer_pary=time.time()
        
    def debut_attack(self, air=False):
        self.is_attacking = True
        self.a_attaquer2=False
        self.timer_attack=time.time()
        self.direction_attack=self.direction
        self.compteur_attack=0
        if air:
            self.timer_attack_aerienne=time.time()
            self.change_direction("air attack", self.direction)
        else :
            self.change_direction("attack1", self.direction)
            self.a_attaquer2=False
        
            
    
    def attack2(self):
        self.compteur_attack=0
        self.is_attacking = True
        self.a_attaquer2=True
        self.change_direction("attack2", self.direction)
        self.direction_attack=self.direction
        
    def debut_dash_attack(self):
        self.compteur_dash_attack=self.compteur_dash_attack_min
        self.is_dashing_attacking = True
        self.change_direction("dash_attack", self.direction)
    
    def dash_attack(self):
        if self.is_falling:
            c=0.45
        else:
            c=0.3
        self.compteur_dash_attack+=self.increment_dash_attack
        if self.compteur_dash_attack<=self.compteur_dash_attack_max:
            if self.direction=="right":
                self.position[0] += self.compteur_dash_attack**2 *c* self.zoom * self.speed_dt
            elif self.direction=="left":
                self.position[0] -= self.compteur_dash_attack**2 *c* self.zoom * self.speed_dt
    
    def fin_dash_attack(self):
        self.is_dashing_attacking = False
        if not self.is_falling:
            self.change_direction("idle", self.direction)
        else:
            self.change_direction("up_to_fall", self.direction)  
  
    def debut_crouch(self):
        """very simple"""
        self.change_direction("crouch", self.direction)
  
    def debut_slide_ground(self, slide_ground_direction_x):
        #penser à bien utiliser .copy() parce que sinon la valeur est la meme que self.position tous le temps
        self.is_sliding_ground = True
        self.change_direction('ground_slide', slide_ground_direction_x)
        self.slide_ground_direction_x = slide_ground_direction_x
    
    def slide_ground(self):
        if self.compteur_slide_ground < self.compteur_slide_ground_max:
            self.update_speed_slide_ground()
            if self.slide_ground_direction_x == "right":
                self.position[0] += (self.speed_slide_ground + self.speed *0.5) * self.zoom * self.speed_dt 
            elif self.slide_ground_direction_x == "left":
                self.position[0] -= (self.speed_slide_ground + self.speed *0.5) * self.zoom * self.speed_dt 
            self.compteur_slide_ground += self.compteur_slide_ground_increment* self.speed_dt
        else:
            self.fin_slide_ground()
    
    def update_speed_slide_ground(self):
        self.speed_slide_ground = (self.compteur_slide_ground**2) * 0.5
        # the base speed is also increasing
        if self.speed < self.max_speed_run:
            self.speed += (self.speed*0.003 + self.origin_speed_run*0.010)
    
    def fin_slide_ground(self):
        self.is_sliding_ground = False
        self.slide_ground_direction_x = ""
        self.compteur_slide_ground = self.compteur_slide_ground_min
        # the player was running before the slide so he should run after
        self.change_direction("run", self.direction)
        self.timer_cooldown_slide_ground = time.time()
        
    def debut_grab_edge(self, head_only=False):
        # if only the head collide with the wall
        self.head_only_edge = head_only
        self.timer_slide = time.time()
        self.is_grabing_edge = True
        self.direction_wall = self.direction
        self.change_direction('Edge_grab', self.direction)
   
    def sliding(self):
        if self.is_sliding:
            self.position[1] += self.speed_sliding * self.zoom * self.speed_dt
        
    def fin_grab_edge(self, mouvement = True):
        self.is_grabing_edge = False
        self.is_sliding = False
        if mouvement:
            # petit decalage necessaires pour eviter des bug a causes des images d'animations ou des collision
            if self.direction == "right":
                self.position[0] -= 15*self.zoom
            elif self.direction == "left":
                self.position[0] += 15*self.zoom
        self.speed_gravity = self.original_speed_gravity 

    def debut_dash(self, dash_direction_x, dash_direction_y):
        #penser à bien utiliser .copy() parce que sinon la valeur est la meme que self.position tous le temps
        self.coord_debut_dash = self.position.copy()
        self.is_dashing = True
        self.change_direction('jump', self.direction)
        self.dash_direction_x = dash_direction_x
        self.dash_direction_y = dash_direction_y
    
    def dash(self):
        #enregistrement des images transparentes lors su dash
        #i should have calculated the distance in term of the speed but i got lazy x)
        if self.compteur_dash >-9 and not self.image1_dash:
            self.image1_dash = True
            self.images_dash.append((self.position[0], self.position[1], self.image.copy(), 0))
        elif self.compteur_dash >-7.75 and not self.image2_dash:
            self.image2_dash = True
            self.images_dash.append((self.position[0], self.position[1], self.image.copy(), self.dash_cooldown_image))
        elif self.compteur_dash >-6.25 and not self.image3_dash:
            self.image3_dash = True
            self.images_dash.append((self.position[0], self.position[1], self.image.copy(), self.dash_cooldown_image*2))
        elif self.compteur_dash >-4.25 and not self.image4_dash:
            self.image4_dash = True
            self.images_dash.append((self.position[0], self.position[1], self.image.copy(), self.dash_cooldown_image*3))
        
        # le dash commence par un "mouvement immobile"
        if self.compteur_dash_immobile < self.compteur_dash_immobile_max:
            self.compteur_dash_immobile += 1* self.speed_dt
        else:
            # utilisation de la fonction carre avec un compteur qui commence en negatif et finis à 0
            # => le mouvement est RALLENTIT
            if self.compteur_dash < self.compteur_dash_max:
                self.update_speed_dash()
                speed_dash = self.speed_dash
                if self.dash_direction_y != "" and self.dash_direction_x != "":
                    speed_dash *= 1
                elif self.dash_direction_x == 'up' or self.dash_direction_x == "right" or self.dash_direction_x == "left":
                    speed_dash *= 1.3
                if self.dash_direction_x == "right":
                    self.position[0] += speed_dash
                elif self.dash_direction_x == "left":
                    self.position[0] -= speed_dash
                if self.dash_direction_y == "down":
                    self.position[1] += speed_dash
                elif self.dash_direction_y == "up":
                    self.position[1] -= speed_dash
                self.compteur_dash += self.compteur_dash_increment* self.speed_dt
            else:
                self.fin_dash()
    
    def fin_dash(self):
        """reinitialisation des variables du dash"""
        # sinon le joueur va sauter immediatement en arrivant sur une plateforme apres un dash
        self.timer_cooldown_next_jump = time.time()
        self.coord_debut_dash = [-999,-999]
        self.a_dash = True
        self.is_dashing = False
        self.compteur_dash_immobile = 0
        self.compteur_dash_immobile_max = 10
        self.compteur_dash = self.compteur_dash_min
        self.speed_dash = 0
        self.dash_direction_x = ""
        self.dash_direction_y = "" 
        self.images_dash = []
        self.image1_dash = False
        self.image2_dash = False
        self.image3_dash = False
        self.image4_dash = False

    def update_speed_dash(self):
        self.speed_dash = (self.compteur_dash**2) * 0.3 * self.zoom * self.speed_dt

    def debut_saut_edge(self, pieds = False, direction_x = ""):
        self.jump_edge_pieds = pieds
        self.coord_debut_jump_edge = self.position.copy()
        self.is_jumping_edge = True
        if direction_x != "":
            self.speed = self.max_speed_run
            if self.direction_wall == "right" and direction_x == "left":
                self.direction_jump_edge = "left"
                self.change_direction('jump', "left")
                self.compteur_jump_edge_max -= 2*self.increment_jump_edge
            elif self.direction_wall == "left" and direction_x == "right":
                self.direction_jump_edge = "right"
                self.change_direction('jump', "right")
                self.compteur_jump_edge_max -= 2*self.increment_jump_edge
            else:
                self.direction_jump_edge == ""
                self.change_direction('jump',self.direction)
                if self.direction_wall == "right":
                    self.position[0] += 5*self.zoom
                elif self.direction_wall == "left":
                    self.position[0] -= 5*self.zoom
        else:
            self.direction_jump_edge == ""
            self.change_direction('jump',self.direction)
    
    def saut_edge(self):
        # utilisation de la fonction carre avec un compteur qui commence en negatif et finis à 0
        # => le mouvement est RALLENTIT        
        if self.compteur_jump_edge < self.compteur_jump_edge_max:
            self.update_speed_jump_edge()
            self.position[1] -= self.speed_jump_edge
            if self.direction_jump_edge == "right":
                self.position[0] += self.speed*2.5
            elif self.direction_jump_edge == "left":
                self.position[0] -= self.speed*2.5
            self.compteur_jump_edge += self.increment_jump_edge* self.speed_dt
        else:
            self.fin_saut_edge()
    
    def fin_saut_edge(self):
        """reinitialisation des vvariables du saut"""
        # sinon le joueur va sauter immediatement en arrivant sur une plateforme ou sur le sol apres un saut
        self.timer_cooldown_next_jump = time.time()
        self.a_sauter = True
        self.is_jumping_edge = False
        self.compteur_jump_edge = self.compteur_jump_edge_min     
        self.coord_debut_jump = [-999,-999]
        self.direction_jump_edge = ''
        self.compteur_jump_edge_max = self.original_compteur_jump_edge_max
    
    def update_speed_jump_edge(self):
        self.speed_jump_edge = (self.compteur_jump_edge**2) * 0.4 *self.zoom * self.speed_dt
        if self.direction_jump_edge != "":
            self.speed *= 1.05