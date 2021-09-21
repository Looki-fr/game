import pygame
import time

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, directory):
        """parametres : 
                - x : coordonne en x du joueur
                - y : coordonne en y du joueur
                - directory : chemin absolu vers le dossier du jeu"""
        # initialisation de la classe mere permettant de faire de cette classe un sprite
        super().__init__()
        
        # creation de l'image du joueur
        # la couleur du 1er pixel sera la couleur transparente
        self.image = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\idle_right\\Warrior_Idle_1.png')
        transColor = self.image.get_at((0,0))
        self.image.set_colorkey(transColor)
        
        # le jeu a été creer avec 60 fps, faut change cette variable quand on change le nombre de fps
        self.fast_variable = 1
        
        self.id = "player"
        
        self.position = [x,y - self.image.get_height()]
        self.rect = self.image.get_rect()
        
        # images
        self.time_cooldown_ralentissement = 0
        self.action = "idle"
        self.direction = "right"
        self.compteur_image = 0
        self.current_image = 1
        
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
            self.images["idle"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\idle_right\\Warrior_Idle_{i}.png')
            self.images["idle"]["left"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\idle_left\\Warrior_Idle_{i}.png')
    
        # run
        self.origin_compteur_image_run = 10
        self.images["run"] = {
            "nbr_image":8,
            "compteur_image_max":self.origin_compteur_image_run,
            "right":{},
            "left":{}
        }
        
        for i in range(1,9):
            self.images["run"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Run_right\\Warrior_Run_{i}.png')
            self.images["run"]["left"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Run_left\\Warrior_Run_{i}.png')
        
        # fall
        self.images["fall"] = {
            "nbr_image":3,
            "compteur_image_max":6,
            "right":{},
            "left":{}
        }
        
        for i in range(1,4):
            self.images["fall"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Fall_right\\Warrior_Fall_{i}.png')
            self.images["fall"]["left"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Fall_left\\Warrior_Fall_{i}.png')
        
        # Uptofall
        self.images["up_to_fall"] = {
            "nbr_image":2,
            "compteur_image_max":6,
            "right":{},
            "left":{}
        }
        
        for i in range(1,3):
            self.images["up_to_fall"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\UptoFall_right\\Warrior_UptoFall_{i}.png')
            self.images["up_to_fall"]["left"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\UptoFall_left\\Warrior_UptoFall_{i}.png')
        
        # Jump
        self.jump = 6
        self.images["jump"] = {
            "nbr_image":3,
            "compteur_image_max":6,
            "right":{},
            "left":{}
        }
        
        for i in range(1,4):
            self.images["jump"]["right"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Jump_right\\Warrior_Jump_{i}.png')
            self.images["jump"]["left"][str(i)] = pygame.image.load(f'{directory}\\assets\\character\\Individual_Sprite\\Jump_left\\Warrior_Jump_{i}.png')

        # creation d'un rect pour les pieds et le corps
        self.feet = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.1)
        self.head = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height*0.1)
        self.body = pygame.Rect(0,0,self.rect.width * 0.3, self.rect.height)
        
        # enregistrement de l'ancienne position pour que si on entre en collision avec un element du terrain la position soit permutte avec l'anciene
        self.old_position = self.position.copy()
        
        # course
        self.origin_speed = 2.5
        self.speed = self.origin_speed
        
        # gravite
        self.original_speed_gravity = 5
        
        # ralentissement
        self.cooldown_ralentissement = 0.2
        self.ralentit_bool = False
        self.doit_ralentir = True
        self.compteur_ralentissement = 0
        
        # chute
        self.is_falling = False
        self.t1_passage_a_travers_plateforme = 0
        self.cooldown_passage_a_travers_plateforme = 0.3
        self.speed_gravity = self.original_speed_gravity
        
        # jump
        self.a_sauter = True
        self.is_jumping = False
        self.compteur_jump = -5
        self.compteur_jump_max = 0
        self.speed_jump = 0
        self.cooldown_able_to_jump = 0.1
        self.timer_cooldown_able_to_jump = 0
        self.cooldown_next_jump = 0.2
        self.timer_cooldown_next_jump = 0
        self.coord_debut_jump = [-999,-999]
        
        # dash
        self.a_dash = False
        self.is_dashing = False
        self.image1_dash = False
        self.image2_dash = False
        self.image3_dash = False
        self.image4_dash = False
        self.compteur_dash = -9
        self.compteur_dash_max = 0
        self.compteur_dash_increment = 0.4
        self.compteur_dash_immobile = 0
        self.compteur_dash_immobile_max = 10
        self.speed_dash = 0
        self.dash_direction_x = ""
        self.dash_direction_y = "" 
        # [x,y, image_modifié]
        self.images_dash = []
        self.dash_cooldown_image = 0.15
        self.coord_debut_dash = [-999,-999]

    def debut_dash(self, dash_direction_x, dash_direction_y):
        #penser à bien utiliser .copy() parce que sinon la valeur est la meme que self.position tous le temps
        self.coord_debut_dash = self.position.copy()
        self.is_dashing = True
        self.change_direction('jump', self.direction)
        self.dash_direction_x = dash_direction_x
        self.dash_direction_y = dash_direction_y
    
    def dash(self):
        if self.is_dashing :
            #enregistrement des images transparentes lors su dash
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
            
            # sinon le joueur va sauter immediatement en arrivant sur une plateforme apres un dash
            self.timer_cooldown_next_jump = time.time()
            
            # le dash commence par un "mouvement immobile"
            if self.compteur_dash_immobile < self.compteur_dash_immobile_max:
                self.compteur_dash_immobile += 1
            else:
                # utilisation de la fonction carre avec un compteur qui commence en negatif et finis à 0
                # => le mouvement est RALLENTIT
                if self.compteur_dash < self.compteur_dash_max:
                    self.update_speed_dash()
                    speed_dash = self.speed_dash
                    if self.dash_direction_y != "" and self.dash_direction_x != "":
                        speed_dash *= 1
                    elif self.dash_direction_x == 'up' or self.dash_direction_x == "right" or self.dash_direction_x == "left":
                        speed_dash *= 1.1
                    if self.dash_direction_x == "right":
                        self.position[0] += speed_dash
                    elif self.dash_direction_x == "left":
                        self.position[0] -= speed_dash
                    if self.dash_direction_y == "down":
                        self.position[1] += speed_dash
                    elif self.dash_direction_y == "up":
                        self.position[1] -= speed_dash
                    self.compteur_dash += self.compteur_dash_increment
                else:
                    self.fin_dash()
    
    def fin_dash(self):
        """reinitialisation des vvariables du dash"""
        self.coord_debut_dash = [-999,-999]
        self.a_dash = True
        self.is_dashing = False
        self.compteur_dash_immobile = 0
        self.compteur_dash_immobile_max = 10
        self.compteur_dash = -8
        self.speed_dash = 0
        self.dash_direction_x = ""
        self.dash_direction_y = "" 
        self.images_dash = []
        self.image1_dash = False
        self.image2_dash = False
        self.image3_dash = False
        self.image4_dash = False

    def update_speed_dash(self):
        self.speed_dash = (self.compteur_dash**2) * 0.3 * self.fast_variable

    def debut_saut(self):
        #penser à bien utiliser .copy() parce que sinon la valeur est la meme que self.position tous le temps
        self.coord_debut_jump = self.position.copy()
        self.timer_cooldown_next_jump = time.time()
        self.is_jumping = True
        self.change_direction('jump', self.direction)

    def saut(self):
        # utilisation de la fonction carre avec un compteur qui commence en negatif et finis à 0
        # => le mouvement est RALLENTIT        
        if self.is_jumping :
            if self.compteur_jump < self.compteur_jump_max:
                self.update_speed_jump()
                self.position[1] -= self.speed_jump
                self.compteur_jump += 0.25
            else:
                self.fin_saut()
    
    def fin_saut(self):
        """reinitialisation des vvariables du saut"""
        self.is_jumping = False
        self.compteur_jump = -5        
        self.a_sauter = True
        self.coord_debut_jump = [-999,-999]

    def update_speed_jump(self):
        self.speed_jump = (self.compteur_jump**2) * 0.5 * self.fast_variable
    
    def debut_chute(self):
        if self.a_dash == False:
            # le joueur peut sauter sans avoir les pieds au sol pendant un cours instant
            self.timer_cooldown_able_to_jump = time.time()
        self.is_falling = True
        self.change_direction('up_to_fall', self.direction)
        
    def chute(self):
        if self.is_falling:
            self.update_speed_gravity()
            self.position[1] += self.speed_gravity
    
    def fin_chute(self, jump_or_dash = False):
        self.is_falling = False
        if not jump_or_dash:
            self.change_direction("idle", self.direction)
    
    def update_speed_gravity(self):
        if self.speed_gravity < 8 * self.fast_variable:
            # self.speed_gravity augmente de plus en plus vite au file des ticks
            self.speed_gravity += self.speed_gravity*0.005 + self.origin_speed*0.025 * self.fast_variable
            # reduction de la vitesse de defilement des images quand la vitesse augmente
            if self.speed_gravity > 5 * self.fast_variable:
                self.images[self.action]["compteur_image_max"] = 6
            elif self.speed_gravity > 7 * self.fast_variable:
                self.images[self.action]["compteur_image_max"] = 4
        # vitesse maximal du defilement des images
        elif self.images[self.action]["compteur_image_max"] != 2:
            self.images[self.action]["compteur_image_max"] = 2  
    
    def move_right_fall(self):
        self.position[0] += self.speed_gravity/2 
        if self.direction != "right":
            self.change_direction(self.action,"right")
            
    def move_left_fall(self):
        self.position[0] -= self.speed_gravity/2
        if self.direction != "left":
            self.change_direction(self.action,"left")

    def debut_ralentissement(self):
        """methode appele quand je joueur arretes de courir"""
        # self.doit ralentir est mis sur true a chaque fois que le joueur avance et mis sur false quand il est en collision avec un mur
        if self.doit_ralentir:
            self.doit_ralentir = False
            self.ralentit_bool = True
            self.compteur_ralentissement = 0
            # augmentation du compteur pour que le ralentissement soit visible
            self.images[self.action]["compteur_image_max"] = 10
        else:
            # si le joueur arrete davancer mais est contre un mur
            if self.action == "run":
                self.change_direction("idle", self.direction)

    def ralentissement(self):
        """methode appele quand le joueur bouge pas"""
        tab = [4, 8]
        if self.ralentit_bool:
            if self.compteur_ralentissement in tab:
                # la vitesse diminue 3 fois tous les 4 frames + on fait avancer le joueur
                self.speed = self.speed*0.7
                if self.action == "run":
                    if self.direction == "right":
                        self.position[0] += self.speed
                    elif self.direction == "left":
                        self.position[0] -= self.speed
                       
            self.compteur_ralentissement += 1
                
            # arret du ralentissement au bout de 8 frames
            if self.compteur_ralentissement > 8 + 1:
                self.ralentit_bool = False
                if self.action == "run":
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
        temp = False
        if self.compteur_image / self.fast_variable < self.images[self.action]["compteur_image_max"] / self.fast_variable:
            self.compteur_image += 1
        else:
            # changement de l'image
            self.compteur_image = 0
            # si l'image en cours est la derniere on re passe a la 1ere, sinon on passe a la suivante
            if self.current_image < self.images[self.action]["nbr_image"]:
                self.current_image += 1
            else:
                if self.action == "up_to_fall":
                    temp = True
                    self.change_direction("fall", self.direction)
                else:
                    self.current_image = 1
            
            if not temp:
                self.image = self.images[self.action][self.direction][str(self.current_image)]
                
                # la couleur du 1er pixel sera la couleur transparente
                transColor = self.image.get_at((0,0))
                self.image.set_colorkey(transColor)
        
    def change_direction(self, action, direction):
        """change la direction et / ou l'action en cours"""
        # ralentissement si le joueur cours et continue de courir dans lautre sens
        if self.action == "run" and action == "run":
            self.speed *= 0.6
        # reset du compteur d'image
        if self.action == "run" and action != "fall" and action != "up_to_fall":
            self.images["run"]["compteur_image_max"] = self.origin_compteur_image_run
        self.speed_gravity = self.original_speed_gravity
        self.action = action
        self.direction = direction
        self.compteur_image = 0
        self.current_image = 0
        self.image = self.images[self.action][self.direction]["1"]
        
        # la couleur du 1er pixel sera la couleur transparente
        transColor = self.image.get_at((0,0))
        self.image.set_colorkey(transColor)
        
        self.rect = self.image.get_rect()
        
    def update_speed(self):
        """appeler quand le joueur avance"""
        self.doit_ralentir = True
        # le speed augmente tant quil est plus petit que 5
        if self.speed < 3.5 * self.fast_variable:
            # aumentation du speed
            self.speed += self.speed*0.002 + self.origin_speed*0.015 * self.fast_variable
            #if self.action == "run":
                # augementation du defilement d'image quand le speed passe à 3
            if self.speed > 2.5 * self.fast_variable:
                self.images[self.action]["compteur_image_max"] = 8
        # vitesse maximal du defilement des images
        elif self.images[self.action]["compteur_image_max"] != 6:
            self.images[self.action]["compteur_image_max"] = 6                    
        
    def move_right(self, pieds_sur_sol = False): 
        self.update_speed()
        self.position[0] += self.speed
        if pieds_sur_sol:
            if self.action != "run":
                self.change_direction("run","right") 
        if self.direction != "right":
            self.change_direction(self.action,"right")       

    def move_left(self, pieds_sur_sol = False): 
        self.update_speed()
        self.position[0] -= self.speed
        if pieds_sur_sol:
            if self.action != "run":
                self.change_direction("run","left") 
        if self.direction != "left":
            self.change_direction(self.action,"left")  

    def update(self):
        """methode appele a chaque tick"""
        self.update_animation()
        self.rect.topleft = self.position
        self.body.midbottom = self.rect.midbottom
        self.feet.midbottom = self.rect.midbottom
        self.head.midtop = self.rect.midtop
        
        if self.action == "run" or self.action == "fall" or self.action == "up_to_fall":
            self.time_cooldown_ralentissement = time.time()
        
        if self.action == "idle" and time.time() - self.time_cooldown_ralentissement > self.cooldown_ralentissement:
            self.speed = self.origin_speed
        