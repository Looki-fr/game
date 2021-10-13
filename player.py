import pygame
import time

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, directory, zoom):
        """parametres : 
                - x : coordonne en x du joueur
                - y : coordonne en y du joueur
                - directory : chemin absolu vers le dossier du jeu"""
        # initialisation de la classe mere permettant de faire de cette classe un sprite
        super().__init__()
        
        self.id = "player"
        self.zoom = zoom
        self.dt = 17
        self.speed_dt=17/self.dt
        self.action = "idle"
        
        self.images = {}
        # enregistrement des images dans un dictionnaire :     
        # idle
        self.images["idle"] = {
            "nbr_image":6,
            "compteur_image_max":5,
            "right":{},
            "left":{}
        }
        for i in range(1,7):
            self.images["idle"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\idle_right\\Warrior_Idle_{i}.png').convert_alpha()
            self.images["idle"]["right"][str(i)] = pygame.transform.scale(self.images["idle"]["right"][str(i)], (self.images["idle"]["right"][str(i)].get_width()*self.zoom, self.images["idle"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["idle"]["left"][str(i)] = pygame.transform.flip(self.images["idle"]["right"][str(i)], True, False).convert_alpha()
    
        # run
        self.origin_compteur_image_run = 8
        self.images["run"] = {
            "nbr_image":8,
            "compteur_image_max":self.origin_compteur_image_run,
            "right":{},
            "left":{}
        }
        
        for i in range(1,9):
            self.images["run"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Run_right\\Warrior_Run_{i}.png').convert_alpha()
            self.images["run"]["right"][str(i)] = pygame.transform.scale(self.images["run"]["right"][str(i)], (self.images["run"]["right"][str(i)].get_width()*self.zoom, self.images["run"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["run"]["left"][str(i)] = pygame.transform.flip(self.images["run"]["right"][str(i)], True, False).convert_alpha()
        
        # fall
        self.origin_compteur_image_fall = 6
        self.images["fall"] = {
            "nbr_image":3,
            "compteur_image_max":self.origin_compteur_image_fall,
            "right":{},
            "left":{}
        }
        
        for i in range(1,4):
            self.images["fall"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Fall_right\\Warrior_Fall_{i}.png').convert_alpha()
            self.images["fall"]["right"][str(i)] = pygame.transform.scale(self.images["fall"]["right"][str(i)], (self.images["fall"]["right"][str(i)].get_width()*self.zoom, self.images["fall"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["fall"]["left"][str(i)] = pygame.transform.flip(self.images["fall"]["right"][str(i)], True, False).convert_alpha()
            
        # Uptofall
        self.images["up_to_fall"] = {
            "nbr_image":2,
            "compteur_image_max":4,
            "right":{},
            "left":{}
        }
        
        for i in range(1,3):
            self.images["up_to_fall"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\UptoFall_right\\Warrior_UptoFall_{i}.png').convert_alpha()
            self.images["up_to_fall"]["right"][str(i)] = pygame.transform.scale(self.images["up_to_fall"]["right"][str(i)], (self.images["up_to_fall"]["right"][str(i)].get_width()*self.zoom, self.images["up_to_fall"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["up_to_fall"]["left"][str(i)] = pygame.transform.flip(self.images["up_to_fall"]["right"][str(i)], True, False).convert_alpha()
        
        # Jump
        self.images["jump"] = {
            "nbr_image":3,
            "compteur_image_max":4,
            "right":{},
            "left":{}
        }
        
        for i in range(1,4):
            self.images["jump"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Jump_right\\Warrior_Jump_{i}.png').convert_alpha()
            self.images["jump"]["right"][str(i)] = pygame.transform.scale(self.images["jump"]["right"][str(i)], (self.images["jump"]["right"][str(i)].get_width()*self.zoom, self.images["jump"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["jump"]["left"][str(i)] = pygame.transform.flip(self.images["jump"]["right"][str(i)], True, False).convert_alpha()

        # Edge grab idle
        self.images["Edge_Idle"] = {
            "nbr_image":6,
            "compteur_image_max":4,
            "right":{},
            "left":{}
        }
        
        for i in range(1,7):
            self.images["Edge_Idle"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Edge-Idle_right\\Warrior_Edge-Idle_{i}.png').convert_alpha()
            self.images["Edge_Idle"]["right"][str(i)] = pygame.transform.scale(self.images["Edge_Idle"]["right"][str(i)], (self.images["Edge_Idle"]["right"][str(i)].get_width()*self.zoom, self.images["Edge_Idle"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["Edge_Idle"]["left"][str(i)] = pygame.transform.flip(self.images["Edge_Idle"]["right"][str(i)], True, False).convert_alpha()
    
        # Edge grab
        self.images["Edge_grab"] = {
            "nbr_image":5,
            "compteur_image_max":4,
            "right":{},
            "left":{}
        }
        
        for i in range(1,6):
            self.images["Edge_grab"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\EdgeGrab_right\\Warrior_Edge-Grab_{i}.png').convert_alpha()
            self.images["Edge_grab"]["right"][str(i)] = pygame.transform.scale(self.images["Edge_grab"]["right"][str(i)], (self.images["Edge_grab"]["right"][str(i)].get_width()*self.zoom, self.images["Edge_grab"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["Edge_grab"]["left"][str(i)] = pygame.transform.flip(self.images["Edge_grab"]["right"][str(i)], True, False).convert_alpha()

         # Wall slide
        self.images["Wall_slide"] = {
            "nbr_image":3,
            "compteur_image_max":4,
            "right":{},
            "left":{}
        }
        
        for i in range(1,4):
            self.images["Wall_slide"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\WallSlide_right\\Warrior_WallSlide_{i}.png').convert_alpha()
            self.images["Wall_slide"]["right"][str(i)] = pygame.transform.scale(self.images["Wall_slide"]["right"][str(i)], (self.images["Wall_slide"]["right"][str(i)].get_width()*self.zoom, self.images["Wall_slide"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["Wall_slide"]["left"][str(i)] = pygame.transform.flip(self.images["Wall_slide"]["right"][str(i)], True, False).convert_alpha()

         # ground_slide slide
        self.images["ground_slide"] = {
            "nbr_image":5,
            "compteur_image_max":3,
            "right":{},
            "left":{}
        }
        
        for i in range(1,6):
            self.images["ground_slide"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Slide_right\\Warrior-SlideNoEffect_{i}.png').convert_alpha()
            self.images["ground_slide"]["right"][str(i)] = pygame.transform.scale(self.images["ground_slide"]["right"][str(i)], (self.images["ground_slide"]["right"][str(i)].get_width()*self.zoom, self.images["ground_slide"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["ground_slide"]["left"][str(i)] = pygame.transform.flip(self.images["ground_slide"]["right"][str(i)], True, False).convert_alpha()
        
        # crouch
        self.images["crouch"] = {
            "nbr_image":5,
            "compteur_image_max":1,
            "right":{},
            "left":{}
        }
        
        for i in range(1,6):
            self.images["crouch"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Crouch_right\\Warrior_Crouch_{i}.png').convert_alpha()
            self.images["crouch"]["right"][str(i)] = pygame.transform.scale(self.images["crouch"]["right"][str(i)], (self.images["crouch"]["right"][str(i)].get_width()*self.zoom, self.images["crouch"]["right"][str(i)].get_height()*self.zoom)).convert_alpha()
            self.images["crouch"]["left"][str(i)] = pygame.transform.flip(self.images["crouch"]["right"][str(i)], True, False).convert_alpha()
        
        self.image = self.images["idle"]["right"]["1"]
        
        self.position = [x,y - self.image.get_height()]
        self.rect = self.image.get_rect()
        
        # images
        self.time_cooldown_ralentissement = 0
        self.action_image = "idle"
        self.direction = "right"
        self.compteur_image = 0
        self.current_image = 1
        
        # creation d'un rect pour les pieds et le corps
        self.feet = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.1)
        self.head = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.1)
        self.body = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.8)
        
        # enregistrement de l'ancienne position pour que si on entre en collision avec un element du terrain la position soit permutte avec l'anciene
        self.old_position = self.position.copy()
        
        # course
        self.origin_speed_run = 2.5
        self.max_speed_run = 4.5
        self.speed = self.origin_speed_run
        self.is_mouving_x = False
        
        # ralentissement
        self.cooldown_ralentissement = 0.2
        self.ralentit_bool = False
        self.doit_ralentir = True
        self.compteur_ralentissement = 0
        
        # chute
        self.original_speed_gravity = 5
        self.is_falling = False
        self.t1_passage_a_travers_plateforme = 0
        self.cooldown_passage_a_travers_plateforme = 0.1
        self.speed_gravity = self.original_speed_gravity
        self.max_speed_gravity = 9
        
        # jump
        self.a_sauter = True
        self.is_jumping = False
        self.compteur_jump_min = -4.5
        self.compteur_jump = self.compteur_jump_min
        self.compteur_jump_max = 0
        self.speed_jump = 0
        self.cooldown_able_to_jump = 0.1
        self.timer_cooldown_able_to_jump = 0
        self.cooldown_next_jump = 0.2
        self.timer_cooldown_next_jump = 0
        self.coord_debut_jump = [-999,-999]
        self.increment_jump = 0.25
        
        # jump edge
        self.is_jumping_edge = False
        self.compteur_jump_edge_min = -5
        self.compteur_jump_edge = self.compteur_jump_edge_min
        self.original_compteur_jump_edge_max = -0.5
        self.compteur_jump_edge_max = self.original_compteur_jump_edge_max
        self.speed_jump_edge = 0
        self.coord_debut_jump_edge = [-999,-999]
        self.direction_jump_edge = ''
        self.increment_jump_edge = 0.25
        self.jump_edge_pieds = False
        
        # edge grab / idle
        self.timer_slide = 0
        self.cooldown_slide = 0.25
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
        self.compteur_slide_ground_max = self.compteur_slide_ground_min + self.compteur_slide_ground_increment*self.images["ground_slide"]["compteur_image_max"]*self.images["ground_slide"]["nbr_image"]
        self.speed_slide_ground = 0
        self.slide_ground_direction_x = ""
        self.cooldown_slide_ground = 0.4
        self.timer_cooldown_slide_ground = 0
  
    def update_tick(self, dt):
        """i created a multiplicator for the mouvements that based on 60 fps (clock.tick() = 17) because the original
        frame rate is 60, and so the mouvements are speeder when the game is lagging so when
        the game has a lower frame rate, same for animations but it doesnt work perfectly for animations"""
        self.dt = dt
        self.speed_dt = round(self.dt/17)
  
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
        elif self.is_grabing_edge:
            if time.time() - self.timer_slide > self.cooldown_slide:
                self.is_sliding = True
                self.change_direction("Wall_slide", self.direction)
        
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

    def update_speed(self):
        """appeler quand le joueur avance"""
        self.doit_ralentir = True
        # le speed augmente tant quil est plus petit que 3.5
        if self.speed < self.max_speed_run:
            # aumentation du speed
            self.speed += self.speed*0.002 + self.origin_speed_run*0.01
            if self.speed > self.max_speed_run*0.6:
                if self.action_image != "idle":
                    self.images[self.action_image]["compteur_image_max"] = 6
        # vitesse maximal du defilement des images
        if self.action_image != "idle":
            self.images[self.action_image]["compteur_image_max"] = 4                    
        
    def move_right(self, pieds_sur_sol = False): 
        self.is_mouving_x = True
        self.update_speed()
        self.position[0] += self.speed * self.zoom * self.speed_dt
        if pieds_sur_sol:
            if self.action_image != "run" and self.action_image != "jump" and self.action_image != "crouch":
                self.change_direction("run","right") 
        if self.direction != "right":
            if self.action_image == "crouch":
                # we dont want the crouch animation du re start from the biggining
                self.change_direction(self.action_image,"right",compteur_image=self.compteur_image, current_image=self.current_image)
            else:
                self.change_direction(self.action_image,"right")        

    def move_left(self, pieds_sur_sol = False): 
        self.is_mouving_x = True
        self.update_speed()
        self.position[0] -= self.speed * self.zoom * self.speed_dt
        if pieds_sur_sol:
            if self.action_image != "run" and self.action_image != "jump" and self.action_image != "crouch":
                self.change_direction("run","left") 
        if self.direction != "left":
            if self.action_image == "crouch":
                # we dont want the crouch animation du re start from the biggining
                self.change_direction(self.action_image,"left",compteur_image=self.compteur_image, current_image=self.current_image)
            else:
                self.change_direction(self.action_image,"left")  

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
                    self.position[0] -= 5*self.zoom
                elif self.direction_wall == "left":
                    self.position[0] += 5*self.zoom
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
                self.position[0] += self.speed_jump_edge*1.2
            elif self.direction_jump_edge == "left":
                self.position[0] -= self.speed_jump_edge*1.2
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
        self.speed_jump_edge = (self.compteur_jump_edge**2) * 0.6 *self.zoom * self.speed_dt
    
    def debut_saut(self):
        #penser à bien utiliser .copy() parce que sinon la valeur est la meme que self.position tous le temps
        self.coord_debut_jump = self.position.copy()
        self.timer_cooldown_next_jump = time.time()
        self.is_jumping = True
        self.change_direction('jump', self.direction)

    def saut(self):
        # utilisation de la fonction carre avec un compteur qui commence en negatif et finis à 0
        # => le mouvement est RALLENTIT        
        if self.compteur_jump < self.compteur_jump_max:
            self.update_speed_jump()
            self.position[1] -= self.speed_jump
            self.compteur_jump += self.increment_jump*self.speed_dt
        else:
            self.fin_saut()
    
    def fin_saut(self):
        """reinitialisation des vvariables du saut"""
        self.is_jumping = False
        self.compteur_jump = self.compteur_jump_min        
        self.a_sauter = True
        self.coord_debut_jump = [-999,-999]

    def update_speed_jump(self):
        self.speed_jump = (self.compteur_jump**2) * 0.7 *self.zoom * self.speed_dt
    
    def debut_chute(self):
        if self.a_dash == False:
            self.timer_cooldown_able_to_jump = time.time()
        self.is_falling = True
        self.change_direction('up_to_fall', self.direction)
        
    def chute(self):
        self.update_speed_gravity()
        self.position[1] += self.speed_gravity * self.zoom * self.speed_dt
    
    def fin_chute(self, jump_or_dash = False):
        self.is_falling = False
        self.speed_gravity = self.original_speed_gravity
        if not jump_or_dash:
            self.debut_crouch()
    
    def update_speed_gravity(self):
        if self.speed_gravity < self.max_speed_gravity:
            # self.speed_gravity augmente de plus en plus vite au file des ticks 
            self.speed_gravity += self.speed_gravity*0.005 + self.original_speed_gravity*0.005
            # reduction de la vitesse de defilement des images quand la vitesse augmente
            if self.speed_gravity > 5:
                self.images[self.action_image]["compteur_image_max"] = 4
            elif self.speed_gravity > 6.5:
                self.images[self.action_image]["compteur_image_max"] = 3
        # vitesse maximal du defilement des images
        elif self.images[self.action_image]["compteur_image_max"] != 2:
            self.images[self.action_image]["compteur_image_max"] = 2  

    def debut_ralentissement(self):
        """methode appele quand je joueur arretes de courir"""
        # self.doit ralentir est mis sur true a chaque fois que le joueur avance et mis sur false quand il est en collision avec un mur
        if self.doit_ralentir:
            self.doit_ralentir = False
            self.ralentit_bool = True
            self.compteur_ralentissement = 0
            # augmentation du compteur pour que le ralentissement soit visible
            self.images[self.action_image]["compteur_image_max"] = 6
        else:
            # si le joueur arrete davancer mais est contre un mur
            if self.action_image == "run":
                self.change_direction("idle", self.direction)

    def ralentissement(self):
        """methode appele quand le joueur bouge pas"""
        if self.ralentit_bool:
            tab = [4, 8]
            if self.compteur_ralentissement in tab:
                # la vitesse diminue 3 fois tous les 4 frames + on fait avancer le joueur
                self.speed = self.speed*0.7*self.zoom * self.speed_dt
                if self.action_image == "run":
                    if self.direction == "right":
                        self.position[0] += self.speed  * self.zoom
                    elif self.direction == "left":
                        self.position[0] -= self.speed  * self.zoom
                       
            self.compteur_ralentissement += 1
                
            # arret du ralentissement au bout de 8 frames
            if self.compteur_ralentissement > 8 + 1:
                self.ralentit_bool = False
                if self.action_image == "run":
                    if self.direction == "right":
                        self.change_direction("idle", "right")
                    elif self.direction == "left":
                        self.change_direction("idle", "left")
                
    def save_location(self): 
        """enregistrement de la position dans 'old_position'"""
        self.old_position = self.position.copy()
    
    def move_back(self):
        """retour aux coordonees de la frame davant"""
        self.position = self.old_position
        self.doit_ralentir = False

    def update_animation(self):
        """change les animations du joueurs, appelé toutes les frames"""
        # changement de l'image tout les X ticks
        if self.compteur_image < self.images[self.action_image]["compteur_image_max"]:
            self.compteur_image += 1*self.speed_dt
        else:
            # temp sert a faire en sorte que l'image ne soit pas update si on passe de 'uptofall' à 'fall'
            temp = False
            # changement de l'image
            self.compteur_image = 0
            # si l'image en cours est la derniere on re passe a la 1ere, sinon on passe a la suivante
            if self.current_image < self.images[self.action_image]["nbr_image"]:
                self.current_image += 1
            else:
                # pour ces actions on passe a une autre animation quand l'animation respeective est finis
                if self.action_image == "up_to_fall":
                    temp = True
                    self.change_direction("fall", self.direction)
                elif self.action_image == "crouch":
                    temp = True
                    if self.is_mouving_x:
                        self.change_direction("run", self.direction)
                    else:
                        self.change_direction("idle", self.direction)
                elif self.action_image == "Edge_grab":
                    temp = True
                    self.change_direction("Edge_Idle", self.direction)
                else:
                    self.current_image = 1
            
            if not temp:
                self.image = self.images[self.action_image][self.direction][str(self.current_image)]
                transColor = self.image.get_at((0,0))
                self.image.set_colorkey(transColor)
        
    def change_direction(self, action, direction, compteur_image=0, current_image=0):
        """change la direction et / ou l'action en cours"""
        # ralentissement si le joueur cours et continue de courir dans lautre sens
        if self.action_image == "run" and action == "run":
            self.speed *= 0.7
        # reset du compteur d'image si le joueur ne va pas chuter, sion il garde sa vitesse
        if self.action_image == "run" and action != "fall" and action != "up_to_fall":
            self.images["run"]["compteur_image_max"] = self.origin_compteur_image_run
        elif self.action_image == "fall":
            self.images["fall"]["compteur_image_max"] = self.origin_compteur_image_fall
        self.action_image = action
        self.direction = direction
        self.compteur_image = compteur_image
        self.current_image = current_image
        self.image = self.images[self.action_image][self.direction]["1"]
        transColor = self.image.get_at((0,0))
        self.image.set_colorkey(transColor)
        
    def update(self):
        """methode appele a chaque tick"""
        if self.speed > self.max_speed_run:
            self.speed = self.max_speed_run
            
        self.update_animation()
        
        # update des coordonees des rect
        self.rect.topleft = self.position
        self.body.midbottom = self.rect.midbottom
        self.feet.midbottom = self.rect.midbottom
        self.head.midtop = self.body.midtop
        
        # la vitesse de course du joueur ne ralentit pas tant qu'il coure ou chute
        if self.action_image == "run" or self.action_image == "fall" or self.action_image == "up_to_fall" or self.action_image == "jump":
            self.time_cooldown_ralentissement = time.time()
        
        if self.action_image == "idle" and time.time() - self.time_cooldown_ralentissement > self.cooldown_ralentissement:
            self.speed = self.origin_speed_run
        
    def update_action(self):
        """sometimes actions and actions image are differents :
        when the player dash self.action = 'dash' and self.action_image = 'jump'
        because its has the same image, so we update it here"""
        if self.action_image in ["run", "idle", "fall","up_to_fall","Edge_Idle","Edge_grab","Wall_slide","ground_slide","crouch"]:
            self.action = self.action_image
        elif self.action_image == "jump":
            if self.is_dashing:
                self.action = "dash"
            elif self.is_jumping_edge:
                self.action = "jump_edge"   
            elif self.is_jumping:
                self.action = "jump"   