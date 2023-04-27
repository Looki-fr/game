import pygame
import time
from .MOTHER import MOB

class Player(MOB):
    def __init__(self, x, y, directory, zoom, id, checkpoint, Particule, update_particle, Dash_attack_image):
        """parametres : 
                - x : coordonne en x du joueur
                - y : coordonne en y du joueur
                - directory : chemin absolu vers le dossier du jeu"""
        # initialisation de la classe mere permettant de faire de cette classe un sprite
        MOB.__init__(self, zoom, f"player{id}", checkpoint, Particule,update_particle, directory, "assets\\Bounty Hunter\\Individual Sprite")

        #"up_to_fall", 
        action=["air_hurt","roll","Edge_climb", "Edge_Idle", "Edge_grab", "Wall_slide", "ground_slide", "crouch", "jump_edge", "dash", "attack", "dash_attack"]
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
            self._get_images("air_hurt", 3, 4, "Air Hurt", "Air-Hurt_", w, coefficient=coefficient) 
            self._get_images("dying", 7, 4, "Death", "Death_", w, coefficient=coefficient) 
            self._get_images("air_dying", 3, 5, "Death Fall", "Death-Fall_", w, coefficient=coefficient) 
            self._get_images("ground_slide", 4, 3, "Slide", "Slide_", w, coefficient=coefficient) 
            self._get_images("dash_attack", 10, 3, "Dash Attack", "Dash-Attack_", w, coefficient=coefficient)
            self._get_images("crouch", 5, 2, "Croush", "Croush_", w, coefficient=coefficient) 
            self._get_images("Edge_climb", 3, 5, "Edge Climb", "Edge-Climb_", w, coefficient=coefficient) 
            self._get_images("Edge_grab", 4, 5, "Edge Grab", "Edge-Grab_", w, coefficient=coefficient) 
            self._get_images("Wall_slide", 3, 4, "WallSlide", "WallSlide_", w, coefficient=coefficient, reverse=True) 
            self._get_images("air attack", 5, 3, "Air Attack", "Air-Attack_", w, coefficient=coefficient) 
            self._get_images("attack1", 8, 2, "Attack", "Attack_", w, coefficient=coefficient) 
            self._get_images("attack2", 6, 2, "Attack2", "Attack_", w, coefficient=coefficient)
            self._get_images("roll", 7, 3, "Roll", "Roll_", w, coefficient=coefficient)

        self._get_images("dash_attack_effect", 3, 0, "Dash-Attack-Effect", "Dash-Attack-Effect", weapon="effect", coefficient=2)
        
        self.image_pp=pygame.image.load(f'{self.directory}\\assets\\pp.png').convert_alpha()

        self.image = self.images[self.weapon]["idle"]["right"]["1"]
        
        self.position = [x,y - self.image.get_height()]
        self.position_wave_map=[0,0]
        self.rect = self.image.get_rect()
        self.increment_foot=0
        self.increment_x_body=17
        
        # creation d'un rect pour les pieds et le corps
        self.feet = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.1)
        self.head = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.2)
        self.big_head = pygame.Rect(0,0,self.rect.width * 1, self.rect.height*0.2)
        self.body = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.7)
        self.body_wallslide = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.7)
        self.rect_attack = pygame.Rect(0,0,self.rect.width * 1, self.rect.height*1)
        self.rect_air_attack = pygame.Rect(0,0,self.rect.width * 1, self.rect.height*1)
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
        self.timer_jump_edge_cogne=0
        self.cooldown_jump_edge_cogne=0.5
        
        # edge grab / idle
        self.is_sliding = False
        self.is_grabing_edge = False
        self.direction_wall = ""
        self.speed_sliding = 3.5
        self.wall_slide_increment_body=15

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
        self.timer_debut_dash_grabedge=0
        self.cooldown_not_collide_dash=0.1
    
        # ground slide
        self.is_sliding_ground = False
        self.compteur_slide_ground_min = -5
        self.compteur_slide_ground = self.compteur_slide_ground_min
        self.compteur_slide_ground_increment = 0.25
        # le mouvement doit durer exactement le temps necessaire à passer toutes les images de wall slide
        self.compteur_slide_ground_max = self.compteur_slide_ground_min + self.compteur_slide_ground_increment*self.images[self.weapon]["ground_slide"]["compteur_image_max"]*self.images[self.weapon]["ground_slide"]["nbr_image"]
        self.speed_slide_ground = 0
        self.slide_ground_direction_x = ""
        self.cooldown_slide_ground = 0.4
        self.timer_cooldown_slide_ground = 0

        # roll
        self.is_rolling = False
        self.compteur_roll_min = -5
        self.compteur_roll = self.compteur_roll_min
        self.compteur_roll_increment = 0.25
        # le mouvement doit durer exactement le temps necessaire à passer toutes les images de wall slide
        self.compteur_roll_max = self.compteur_roll_min + self.compteur_roll_increment*self.images[self.weapon]["roll"]["compteur_image_max"]*self.images[self.weapon]["roll"]["nbr_image"]
        self.speed_roll = 0
        self.roll_direction_x = ""
        self.cooldown_roll = 1
        self.timer_roll = 0
        
        #attack
        self.attack_damage={}
        self.attack_damage["attack1"]=([6,7,8], 100)
        self.attack_damage["attack2"]=([2,3,4],100)
        self.dash_attack_damage=100
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
    

        # dash attack
        self.is_dashing_attacking = False
        self.timer_dash_attack=0
        self.cooldown_dash_attack=2
        self.compteur_dash_attack_min=-5
        self.compteur_dash_attack=self.compteur_dash_attack_min
        self.increment_dash_attack=0.082
        self.dash_attack_image=None
        self.Dash_attack_image=Dash_attack_image
        self.dash_attack_image_added=False
        self.timer_debut_dash_attack_grabedge=0
        self.cooldown_not_collide_dash_attack=0.1
    
        
        # edge climb
        self.additionnal_compeur=0
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
            "ground_slide":self.slide_ground,
            "Edge_climb":self.edge_climb,
            "roll":self.roll,
            "air_hurt":self.air_hurt,
            "dash_attack":self.dash_attack
        }       

    def debut_edge_climb(self):
        if self.direction=="right":
            self.position[0]+=self.body.width + 10*self.zoom
        else:
            self.position[0]-=self.body.width + 10*self.zoom
        self.position[1]-=77*self.zoom
        self.change_direction("Edge_climb", self.direction)

    def edge_climb(self):
        if self.current_image==2 and self.compteur_image==0:
            self.position[1]-=31*self.zoom
            self.save_location()
        elif self.current_image==2:
            if (self.additionnal_compeur<=5):
                self.compteur_image=1
            self.additionnal_compeur+=1

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
        
    def debut_dash_attack(self, direct):
        self.compteur_dash_attack=self.compteur_dash_attack_min
        self.is_dashing_attacking = True
        if direct=="":
            self.change_direction("dash_attack", self.direction)
        else:
            self.change_direction("dash_attack", direct)
    
    def dash_attack(self):
        if self.is_falling:self.chute()
        c=0.7

        self.is_mouving_x=True

        self.compteur_dash_attack+=self.increment_dash_attack* self.speed_dt

        if self.direction=="right":
            x, y=self.body.topright[0]-self.images["effect"]["dash_attack_effect"][self.direction]["1"].get_width(), self.position[1]+20*self.zoom
            self.position[0] += self.compteur_dash_attack**2 *c* self.zoom * self.speed_dt
        elif self.direction=="left":
            x, y=self.body.topleft[0], self.position[1]+20*self.zoom
            self.position[0] -= self.compteur_dash_attack**2 *c* self.zoom * self.speed_dt

        if self.current_image==2 and self.compteur_image==1:
            self.dash_attack_image=self.Dash_attack_image(x,y, self.images["effect"]["dash_attack_effect"][self.direction]["1"], self.images["effect"]["dash_attack_effect"][self.direction]["2"], self.images["effect"]["dash_attack_effect"][self.direction]["3"])
        self.compteur_debut_dash_attack=time.time()

    def distance_dash_attack(self):
        if self.is_falling:c=0.7
        else:c=0.7
        if self.direction=="right":
            return self.compteur_dash_attack**2 *c* self.zoom * self.speed_dt
        elif self.direction=="left":
            return self.compteur_dash_attack**2 *c* self.zoom * self.speed_dt
        return 0

    def fin_dash_attack(self):
        self.is_dashing_attacking = False
        if not self.is_falling:
            self.change_direction("idle", self.direction)
        elif "up_to_fall" in self.actions:
            self.change_direction("up_to_fall", self.direction)  
        else:
            self.change_direction("fall", self.direction)  
        self.timer_dash_attack=time.time()
        if self.current_image==self.images[self.weapon]["dash_attack"]["nbr_image"]:
            self.speed=self.max_speed_run
            self.is_mouving_x=True
        if not self.is_falling:
            self.change_direction("run",self.direction)
        else:
            self.change_direction("fall",self.direction)
        # on soccupe de reset dash_attack_image dans game
  
    def debut_crouch(self):
        """very simple"""
        self.change_direction("crouch", self.direction)
  
    def air_hurt(self):
        if self.is_falling:self.chute()
    
    def debut_roll(self, direction_x):
        self.is_rolling = True
        self.change_direction('roll', direction_x)
        self.roll_direction_x = direction_x
    
    def roll(self):
        if self.is_falling:self.chute()
        if self.compteur_roll < self.compteur_roll_max:
            self.update_speed_slide_ground()
            if self.roll_direction_x == "right":
                self.move_right()
                self.position[0] += (self.speed_roll + self.speed *0.5) * self.zoom * self.speed_dt 
            elif self.roll_direction_x == "left":
                self.move_left()
                self.position[0] -= (self.speed_roll + self.speed *0.5) * self.zoom * self.speed_dt 
            self.compteur_roll += self.compteur_roll_increment* self.speed_dt
        else:
            self.fin_roll()
    
    def update_speed_roll(self):
        self.speed_roll = (self.compteur_roll**2) * 1.5
        # the base speed is also increasing
        if self.speed < self.max_speed_run:
            self.speed += (self.speed*0.003 + self.origin_speed_run*0.010)
    
    def fin_roll(self):
        self.is_rolling = False
        self.roll_direction_x = ""
        self.compteur_roll = self.compteur_roll_min
        # the player was running before the slide so he should run after
        self.change_direction("run", self.direction)
        self.timer_roll = time.time()

        if self.is_falling:
                if "up_to_fall" in self.actions :self.change_direction("up_to_fall", self.direction)
                else: self.change_direction("fall", self.direction)

    def debut_slide_ground(self, slide_ground_direction_x):
        #penser à bien utiliser .copy() parce que sinon la valeur est la meme que self.position tous le temps
        self.is_sliding_ground = True
        self.change_direction('ground_slide', slide_ground_direction_x)
        self.slide_ground_direction_x = slide_ground_direction_x

    def slide_ground(self):
        if self.is_falling:self.chute()
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
        self.speed_slide_ground = (self.compteur_slide_ground**2) * 0.55
        # the base speed is also increasing
        if self.speed < self.max_speed_run:
            self.speed += (self.speed*0.003 + self.origin_speed_run*0.010)
    
    def fin_slide_ground(self):
        self.is_sliding_ground = False
        self.slide_ground_direction_x = ""
        self.compteur_slide_ground = self.compteur_slide_ground_min
        # the player was running before the slide so he should run after 
        if not self.is_falling:self.change_direction("run", self.direction)
        else: self.change_direction("fall", self.direction)
            
        self.timer_cooldown_slide_ground = time.time()
        
    def debut_grab_edge(self, head_only=False):
        # if only the head collide with the wall
        self.head_only_edge = head_only
        self.timer_slide = time.time()
        self.is_grabing_edge = True
        self.direction_wall = self.direction
        self.change_direction('Edge_grab', self.direction)
   
    def debut_wallslide(self):
        #if self.is_grabing_edge: self.fin_grab_edge(mouvement=False)
        self.is_sliding = True
        self.change_direction("Wall_slide", self.direction)

    def sliding(self):
        if time.time() - self.timer_jump_edge_cogne < self.cooldown_jump_edge_cogne:
            self.debut_wallslide()
        if self.is_sliding:
            self.position[1] += self.speed_sliding * self.zoom * self.speed_dt
        
    def fin_grab_edge(self, mouvement = True):
        """
        ne pas appeler quand on veut wallslide
        """
        self.is_grabing_edge = False
        self.is_sliding = False
        self.additionnal_compeur=0
        if mouvement:
            # petit decalage necessaires pour eviter des bug a causes des images d'animations ou des collision
            if self.direction == "right":
                self.position[0] -= 15*self.zoom
            elif self.direction == "left":
                self.position[0] += 15*self.zoom
        self.speed_gravity = self.original_speed_gravity 

    def debut_dash(self, dash_direction_x, dash_direction_y, skip_immobile=False):
        #penser à bien utiliser .copy() parce que sinon la valeur est la meme que self.position tous le temps
        self.coord_debut_dash = self.position.copy()
        self.is_dashing = True
        # used when dashing from a wallslide
        if skip_immobile and dash_direction_x!="": self.change_direction('jump', dash_direction_x)
        else :self.change_direction('jump', self.direction)
        self.dash_direction_x = dash_direction_x
        self.dash_direction_y = dash_direction_y
        self.compteur_dash_immobile = self.compteur_dash_immobile_max
    
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
                elif (self.dash_direction_y == 'up' and self.dash_direction_x=="") or (self.dash_direction_x == "right" or self.dash_direction_x == "left") and self.dash_direction_y=="":
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

    def distance_dash_y(self):
        speed_dash=(self.compteur_dash**2) * 0.3 * self.zoom * self.speed_dt
        if self.dash_direction_y != "" and self.dash_direction_x != "":
            speed_dash *= 1
        elif (self.dash_direction_y == 'up' and self.dash_direction_x=="") or (self.dash_direction_x == "right" or self.dash_direction_x == "left") and self.dash_direction_y=="":
            speed_dash *= 1.3
        if self.dash_direction_x == "down":
            return speed_dash
        elif self.dash_direction_x == "up":
            return - speed_dash
        return 0

    def distance_dash(self):
        speed_dash=(self.compteur_dash**2) * 0.3 * self.zoom * self.speed_dt
        if self.dash_direction_y != "" and self.dash_direction_x != "":
                    speed_dash *= 1
        elif (self.dash_direction_y == 'up' and self.dash_direction_x=="") or (self.dash_direction_x == "right" or self.dash_direction_x == "left") and self.dash_direction_y=="":
            speed_dash *= 1.3
        if self.dash_direction_x == "right":
            return speed_dash
        elif self.dash_direction_x == "left":
            return speed_dash
        return 0

    def update_speed_dash(self):
        self.speed_dash = (self.compteur_dash**2) * 0.6 * self.zoom * self.speed_dt

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
                self.position[0] += 5*self.zoom
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
    
    def fin_saut_edge(self, cogne=False):
        """reinitialisation des vvariables du saut"""
        # sinon le joueur va sauter immediatement en arrivant sur une plateforme ou sur le sol apres un saut
        if cogne : self.timer_jump_edge_cogne = time.time()
        self.jump_edge_pieds = False
        self.a_sauter = True
        self.is_jumping_edge = False
        self.compteur_jump_edge = self.compteur_jump_edge_min     
        self.coord_debut_jump = [-999,-999]
        self.direction_jump_edge = ''
        self.compteur_jump_edge_max = self.original_compteur_jump_edge_max
        self.timer_cooldown_next_jump=time.time()
    
    def update_speed_jump_edge(self):
        self.speed_jump_edge = (self.compteur_jump_edge**2) * 0.4 *self.zoom * self.speed_dt
        if self.direction_jump_edge != "":
            self.speed *= 1.05