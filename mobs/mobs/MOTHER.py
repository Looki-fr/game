import pygame
import time
import random

class MOB(pygame.sprite.Sprite):

    def __init__(self, zoom, id, checkpoint, Particule, update_particle, directory, directory_assets):
        super().__init__()
        self.directory=directory
        self.directory_assets=directory_assets
        
        self.actions = ["run", "fall", "jump", "idle", "dying", "hurt"]
        
        self.coord_map=[0,0]
        
        self.checkpoint=checkpoint
        
        self.increment_foot=1
        self.increment_x_body=0
        
        self.id = id
        self.zoom = zoom
        self.dt = 17
        self.speed_dt=17/self.dt
        
        if "player" in id :
            self.images = {
                "shotgun":{},
                "gun":{},
                "crossbow":{},
                "effect":{}
            }
        elif "crab" in id:
            self.images = {
                "default":{}
            }
        
        self.weapon="default"

        # all timers in a dict so that we can increase all of them at once when the game is paused

        self.timers= {
            "time_cooldown_ralentissement":0,
            "t1_passage_a_travers_plateforme":0,
            "timer_cooldown_able_to_jump":0,
            "timer_cooldown_next_jump":0,
        }

        # images
        self.action_image = "idle"
        self.action = "idle"
        self.direction = "right"
        self.compteur_image = 0
        self.current_image = 1
        
        # course
        self.speed_coeff=1
        self.origin_speed_run = 2.5
        self.max_speed_run = 4.5
        self.speed = self.origin_speed_run
        self.is_mouving_x = False
        self.max_distance_collide=15
        self.increment_left_right=25
        
        # ralentissement
        self.cooldown_ralentissement = 0.2
        self.ralentit_bool = False
        self.doit_ralentir = True
        self.compteur_ralentissement = 0
        
        # chute
        self.original_speed_gravity = 5
        self.is_falling = False
        self.cooldown_passage_a_travers_plateforme = 0.2
        self.speed_gravity = self.original_speed_gravity
        self.max_speed_gravity = 9
        
        # jump
        self.a_sauter = True
        self.is_jumping = False
        self.compteur_jump_min = -4.5
        self.compteur_jump = self.compteur_jump_min
        self.compteur_jump_max = 0
        self.speed_jump = 0
        # allow to jump when in air for a cooldown
        self.cooldown_able_to_jump = 0
        # cooldown pour jump edge, 2x plus long pour saut normal
        self.cooldown_next_jump = 0.16
        self.coord_debut_jump = [-999,-999]
        self.increment_jump = 0.25   
        
        # autre booleen
        self.is_jumping_edge = False 
        self.is_sliding = False
        self.is_grabing_edge = False
        self.a_dash = False
        self.is_dashing = False    
        self.is_sliding_ground = False
        self.is_attacking=False
        self.is_dashing_attacking=False
        self.is_parying=False
        self.has_air_attack = False
        self.can_attack_while_jump=False
        self.is_rolling=False
        self.is_dashing_ground = False
        self.rect_attack_update_pos=""
        
        self.max_health=100
        self.health=self.max_health
        self.is_dead=False
        self.is_mob=True
        self.is_friendly=False
        
        self.bot=None
        
        self.motion=[1,1]
        
        self.particule=Particule(directory, self, self.zoom, update_particle)

    
    def _random_choice(self, liste):
        choice=random.randint(0, sum([e[1] for e in liste]))
        liste=sorted(liste, key=lambda l:l[1])
        c=0
        for i in liste:
            c+=i[1]
            if c >= choice:
                return i[0]
    
    def _get_images(self, action, nbr_image, compteur_image_max, directory_name, image_name, weapon="default", coefficient=1, reverse=False):

        self.images[weapon][action] = {
            "nbr_image":nbr_image,
            "compteur_image_max":compteur_image_max,
            "right":{},
            "left":{}
        }
        s="\\"
        for i in range(1,nbr_image+1):
            self.images[weapon][action]["right"][str(i)] = pygame.image.load(f'{self.directory}\\{self.directory_assets}{s+weapon if weapon != "default" else ""}\\{directory_name}\\{image_name}{i}.png').convert_alpha()
            self.images[weapon][action]["right"][str(i)] = pygame.transform.scale(self.images[weapon][action]["right"][str(i)], (round(self.images[weapon][action]["right"][str(i)].get_width()*self.zoom*coefficient), round(self.images[weapon][action]["right"][str(i)].get_height()*self.zoom*coefficient))).convert_alpha()
            self.images[weapon][action]["left"][str(i)] = pygame.transform.flip(self.images[weapon][action]["right"][str(i)], True, False).convert_alpha()
            if reverse: self.images[weapon][action]["right"][str(i)], self.images[weapon][action]["left"][str(i)] = self.images[weapon][action]["left"][str(i)], self.images[weapon][action]["right"][str(i)]

    def update_timers(self, dt):
        for i in self.timers.keys():
            self.timers[i]+=dt

    def start_dying(self, ground):
        self.reset_actions(ground)
        if ground or not "air_dying" in self.images[self.weapon].keys() : self.change_direction("dying", self.direction)
        else : self.change_direction("air_dying", self.direction)
        self.update_action()
        self.health=self.max_health
      
    def reset_actions(self, ground,chute=False):
        """reset all actions except the fall"""
        if self.is_dashing:
            self.fin_dash()
        if self.is_dashing_attacking:
            self.fin_dash_attack()
        if self.is_jumping:
            self.fin_saut(ground=ground)
        if self.is_jumping_edge:
            self.fin_saut_edge()
        if self.is_attacking:
            self.is_attacking=False
        if self.is_sliding_ground:
            self.fin_slide_ground()
        if self.is_sliding_ground:
            self.fin_slide_ground()
        if self.is_parying:
            self.is_parying=False
        if self.is_grabing_edge:
            self.fin_grab_edge()
        if self.is_rolling:
            self.fin_roll()
        if self.is_dashing_attacking:
            self.fin_dash_attack()
        if chute:
            self.fin_chute()
        if not self.is_falling:
            self.action="idle"
        
    def take_damage(self):
        if self.is_falling and "air_hurt" in self.actions: 
            self.reset_actions(False,chute=False)
            self.change_direction("air_hurt", self.direction)
        elif (self.is_jumping or self.is_jumping_edge or self.is_dashing or (self.is_dashing_attacking and self.is_falling)) and "air_hurt" in self.actions:
            self.reset_actions(False)
            self.debut_chute(attack=True)
            self.change_direction("air_hurt", self.direction)
        else:
            self.reset_actions(True)
            self.change_direction("hurt", self.direction)
  
    def update_tick(self, dt):
        """i created a multiplicator for the mouvements that based on 60 fps (clock.tick() = 17) because the original
        frame rate is 60, and so the mouvements are speeder when the game is lagging so when
        the game has a lower frame rate, same for animations but it doesnt work perfectly for animations"""
        self.dt = dt
        self.speed_dt = round(self.dt/17)
        self.particule.update_tick(dt)

    def update_speed(self):
        """appeler quand le joueur avance"""
        self.doit_ralentir = True
        # le speed augmente tant quil est plus petit que 3.5
        if self.speed < self.max_speed_run*abs(self.motion[0]):
            # aumentation du speed
            self.speed += (self.speed*0.002 + self.origin_speed_run*0.01)*abs(self.motion[0])
            if self.speed > self.max_speed_run*0.6*abs(self.motion[0]):
                if self.action_image != "idle" and self.action_image != "attack1" and self.action_image != "attack2":
                    self.images[self.weapon][self.action_image]["compteur_image_max"] = 6
        # vitesse maximal du defilement des images
        if self.action_image != "idle" and self.action_image != "attack1" and self.action_image != "attack2":
            self.images[self.weapon][self.action_image]["compteur_image_max"] = 4                    
        
    def move_right(self, pieds_sur_sol = False): 
        self.is_mouving_x = True
        if (not "player" in self.id and not self.is_attacking) or ("player" in self.id and not self.is_attacking and not self.is_parying or not pieds_sur_sol):
            self.position[0] += self.speed_coeff*self.speed * self.zoom * self.speed_dt *abs(self.motion[0])
            self.update_speed()
        elif not "player" in self.id:
            self.position[0] += self.speed_coeff*self.speed * self.zoom * self.speed_dt *abs(self.motion[0])*0.7
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
            if self.action_image in ["crouch", "run", "idle"] and self.direction == "left":
                self.position[0]+=self.increment_left_right*self.zoom

            if not self.is_rolling and self.action_image != "run" and self.action_image != "jump" and self.action_image != "crouch" and not self.is_attacking and not self.is_parying:
                self.change_direction("run","right") 

        if self.direction != "right" and not self.is_rolling:
            if self.action_image == "crouch":
                # we dont want the crouch animation du re start from the biggining
                self.change_direction(self.action_image,"right",compteur_image=self.compteur_image, current_image=self.current_image)
            elif not self.is_attacking and not self.is_parying:
                self.change_direction(self.action_image,"right")       
            else:
                self.direction="right"  

    def move_left(self, pieds_sur_sol = False): 
        self.is_mouving_x = True
        if (not "player" in self.id and not self.is_attacking) or ("player" in self.id and not self.is_attacking and not self.is_parying or not pieds_sur_sol):
            self.position[0] -= self.speed_coeff*self.speed * self.zoom * self.speed_dt *abs(self.motion[0])
            self.update_speed()
        elif not "player" in self.id:
            self.position[0] -= self.speed_coeff*self.speed * self.zoom * self.speed_dt *abs(self.motion[0])*0.7
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
            if self.action_image in ["crouch", "run", "idle"] and self.direction == "right":
                self.position[0]-=self.increment_left_right*self.zoom
            if not self.is_rolling and self.action_image != "run" and self.action_image != "jump" and self.action_image != "crouch" and not self.is_attacking and not self.is_parying:
                self.change_direction("run","left") 

        if self.direction != "left" and not self.is_rolling:
            if self.action_image == "crouch":
                # we dont want the crouch animation du re start from the biggining
                self.change_direction(self.action_image,"left",compteur_image=self.compteur_image, current_image=self.current_image)
            elif not self.is_attacking and not self.is_parying:
                self.change_direction(self.action_image,"left")       
            else:
                self.direction="left" 
  
    def debut_saut(self):
        #penser à bien utiliser .copy() parce que sinon la valeur est la meme que self.position tous le temps
        self.coord_debut_jump = self.position.copy()
        self.is_jumping = True
        self.change_direction('jump', self.direction)

    def saut(self):
        # utilisation de la fonction carre avec un compteur qui commence en negatif et finis à 0
        # => le mouvement est RALLENTIT       
        if not self.is_attacking or self.can_attack_while_jump:
            if self.compteur_jump < self.compteur_jump_max:
                self.update_speed_jump()
                self.position[1] -= self.speed_jump
                self.compteur_jump += self.increment_jump*self.speed_dt
            else:
                self.fin_saut(False)
        
    def fin_saut(self, ground=True, no_change=False, cogne=False):
        """reinitialisation des vvariables du saut"""
        if cogne and "jump_edge" in self.actions: self.timers["timer_jump_edge_cogne"] = time.time()
        self.is_jumping = False
        self.compteur_jump = self.compteur_jump_min        
        self.a_sauter = True
        self.coord_debut_jump = [-999,-999]
        self.timers["timer_cooldown_next_jump"] = time.time()
        if not no_change and ground and self.action_image=="jump": self.change_direction("idle", self.direction)
        elif not no_change and not ground and self.action_image=="jump": self.debut_chute()
        self.update_action()

    def update_speed_jump(self):
        self.speed_jump = (self.compteur_jump**2) * 0.7 *self.zoom * self.speed_dt
    
    def debut_chute(self, attack=False):
        if self.a_dash == False:
            self.timers["timer_cooldown_able_to_jump"] = time.time()
        self.is_falling = True
        if not attack and not self.is_parying and not self.is_dashing_attacking:
            if "up_to_fall" in self.actions:  self.change_direction('up_to_fall', self.direction)
            else: self.change_direction('fall', self.direction)
        elif not self.is_rolling and not self.is_dashing_attacking and not self.is_sliding_ground and not self.is_dashing_ground:
            if "up_to_fall" in self.actions: self.action="up_to_fall"
            else: self.action="fall"
        
    def chute(self):
        self.update_speed_gravity()
        if self.action_image != "air attack" : self.position[1] += self.speed_gravity * self.zoom * self.speed_dt
        else : self.position[1] += self.speed_gravity * self.zoom * self.speed_dt * 0.5
    
    def fin_chute(self, jump_or_dash = False):
        self.is_falling = False
        self.speed_gravity = self.original_speed_gravity
        if not self.is_dashing_attacking and not self.is_sliding_ground and not self.is_rolling and not jump_or_dash and not self.is_parying and not self.is_dashing_ground:
            self.debut_crouch()
        self.update_action()
    
    def update_speed_gravity(self):
        if self.action_image!="air_dying" and self.action_image!="air_hurt":
            if self.speed_gravity < self.max_speed_gravity:
                # self.speed_gravity augmente de plus en plus vite au file des ticks 
                self.speed_gravity += self.speed_gravity*0.005 + self.original_speed_gravity*0.005
                # reduction de la vitesse de defilement des images quand la vitesse augmente
                if self.speed_gravity > 5:
                    if not self.is_attacking and not self.is_dashing_attacking:
                        self.images[self.weapon][self.action_image]["compteur_image_max"] = 4
                elif self.speed_gravity > 6.5:
                    if not self.is_attacking and not self.is_dashing_attacking:
                        self.images[self.weapon][self.action_image]["compteur_image_max"] = 3
            # vitesse maximal du defilement des images
            elif self.images[self.weapon][self.action_image]["compteur_image_max"] != 2 and not self.is_attacking and not self.is_dashing_attacking:
                self.images[self.weapon][self.action_image]["compteur_image_max"] = 2  

    def debut_ralentissement(self):
        """methode appele quand je joueur arretes de courir"""
        # self.doit ralentir est mis sur true a chaque fois que le joueur avance et mis sur false quand il est en collision avec un mur
        if self.doit_ralentir:
            self.doit_ralentir = False
            self.ralentit_bool = True
            self.compteur_ralentissement = 0
            # augmentation du compteur pour que le ralentissement soit visible
            if not self.is_attacking:
                self.images[self.weapon][self.action_image]["compteur_image_max"] = 6
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
                    self.change_direction("idle", self.direction)
                
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
        if not self.is_attacking:
            dir = self.direction
        else:
            dir=self.direction_attack
        if self.compteur_image < self.images[self.weapon][self.action_image]["compteur_image_max"]:
            if self.action_image == "run":
                self.compteur_image += 1*self.speed_dt * abs(self.motion[0])
            else:
                self.compteur_image += 1*self.speed_dt
        else:
            # temp sert a faire en sorte que l'image ne soit pas update si on passe de 'uptofall' à 'fall'
            temp = False
            # changement de l'image
            self.compteur_image = 0
            # si l'image en cours est la derniere on re passe a la 1ere, sinon on passe a la suivante
            if self.current_image < self.images[self.weapon][self.action_image]["nbr_image"]:
                self.current_image += 1
            else:
                temp=True
                # pour ces actions on passe a une autre animation quand l'animation respeective est finis
                # it doesnt matter if the mob doesnt have these actions
                if self.action_image == "up_to_fall": self.change_direction("fall", dir)
                elif self.action_image == "up_to_attack": self.change_direction("attack1", dir)
                elif self.action_image == "crouch":
                    if self.is_mouving_x:
                        self.change_direction("run", dir)
                    else:
                        self.change_direction("idle", dir)
                elif self.action_image == "Edge_grab":
                    self.debut_wallslide()
                elif self.action_image == "attack1" or self.action_image == "attack2" or self.action_image=="hurt" or self.action_image=="pary":
                    self.is_attacking=False
                    self.is_parying=False
                    if not self.is_falling:
                        self.change_direction("idle", dir)
                    else:
                        if "up_to_fall" in self.actions :self.change_direction("up_to_fall", dir)
                        else: self.change_direction("fall", dir)
                elif self.action_image=="air attack":
                    self.is_attacking=False
                    if "up_to_fall" in self.actions :self.change_direction("up_to_fall", dir)
                    else: self.change_direction("fall", dir)
                elif self.action_image == "dash_attack":   
                    self.fin_dash_attack()
                elif "dying" in self.action_image:
                    self.position=[self.checkpoint[0], self.checkpoint[1]-self.image.get_height()]
                    self.fin_chute()
                    self.change_direction("idle", dir)
                elif self.action_image=="Edge_climb":
                    self.change_direction("idle", dir)
                    self.position[1]+=2*self.zoom
                elif self.action_image=="jump" and not self.is_dashing:
                    self.fin_saut(ground=False)
                    self.change_direction("fall", dir)
                elif self.action_image=="air_hurt":
                    self.action_image="fall"
                else:
                    temp=False
                    self.current_image = 1
                self.update_action()
            if not temp:
                self.image = self.images[self.weapon][self.action_image][dir][str(self.current_image)]
                transColor = self.image.get_at((0,0))
                self.image.set_colorkey(transColor)
                

        
    def change_direction(self, action, direction, compteur_image=0, current_image=1):
        """change la direction et / ou l'action en cours"""
        if "player" in self.id:
            if action =="Wall_slide" and not self.dict_sounds["slide"] :
                self.play_long_sounds("slide")
                self.dict_sounds["slide"]=True
            elif action !="Wall_slide" and self.dict_sounds["slide"]:
                self.stop_long_sounds("slide")
                self.dict_sounds["slide"]=False

            if self.action_image!="dash_attack" and self.dict_sounds["slide_speed"]:
                self.stop_long_sounds("slide_speed")
                self.dict_sounds["slide_speed"]=False

            if action=="run" and not self.dict_sounds["run"]:
                self.play_long_sounds("run")
                self.dict_sounds["run"]=True
            elif action!="run" and self.dict_sounds["run"]:
                self.stop_long_sounds("run")
                self.dict_sounds["run"]=False

            

        
        
        if action != "attack1" and action != "attack2" and action != "up_to_attack" and action != "air attack":
            self.is_attacking=False
        elif self.action == "attack2":
            self.a_attaquer2=False
            
        # ralentissement si le joueur cours et continue de courir dans lautre sens
        if self.action_image == "run" and action == "run":
            self.speed *= 0.9
        # reset du compteur d'image si le joueur ne va pas chuter, sion il garde sa vitesse
        if self.action_image == "run" and action != "fall" and action != "up_to_fall":
            self.images[self.weapon]["run"]["compteur_image_max"] = self.origin_compteur_image_run
        elif self.action_image == "fall":
            self.images[self.weapon]["fall"]["compteur_image_max"] = self.origin_compteur_image_fall
        self.action_image = action
        self.direction = direction
        self.compteur_image = compteur_image
        self.current_image = current_image
        self.image = self.images[self.weapon][self.action_image][self.direction]["1"]
        transColor = self.image.get_at((0,0))
        self.image.set_colorkey(transColor)
        self.update_action()
        
    def update_rect(self):
        self.rect.topleft = self.position
        self.body.midbottom = self.rect.midbottom
        if self.direction=="right": self.body.x-=self.increment_x_body*self.zoom
        else: self.body.x+=self.increment_x_body*self.zoom
        if 'Wall_slide' in self.actions:
            self.body_wallslide.midbottom = self.body.midbottom
            if self.direction=="right": self.body_wallslide.x+=self.wall_slide_increment_body*self.zoom
            else: self.body_wallslide.x-=self.wall_slide_increment_body*self.zoom
        self.feet.midbottom = (self.body.midbottom[0], self.body.midbottom[1]-self.increment_foot)
        self.head.midtop = self.body.midtop
        if "Edge_climb" in self.actions : self.big_head.midtop = self.body.midtop
        if "dash" in self.actions: self.chest.midtop=self.head.midtop

    def update(self):
        """methode appele a chaque tick"""
        if self.speed > self.max_speed_run:
            if self.action != "jump_edge" and self.action != "chute":
                self.speed = self.max_speed_run
            else:
                self.speed *= 0.97
            
        self.update_animation()
        
        # update des coordonees des rect
        self.update_rect()
        if self.is_attacking and self.rect_attack_update_pos=="mid":
            self.rect_attack.center = self.rect.center
        elif self.is_attacking and self.rect_attack_update_pos=="left_right":
            if self.direction_attack == "right":
                self.rect_attack.topleft=self.body.topleft
                self.rect_air_attack.topleft=self.body.topleft
            else:
                self.rect_attack.topright=self.body.topright
                self.rect_air_attack.topright=self.body.topright
        
        # la vitesse de course du joueur ne ralentit pas tant qu'il coure ou chute
        if self.action_image == "run" or self.action_image == "fall" or self.action_image == "up_to_fall" or self.action_image == "jump" or self.action == "jump_edge" or self.is_attacking:
            self.timers["time_cooldown_ralentissement"] = time.time()
        
        if self.action_image == "idle" and time.time() - self.timers["time_cooldown_ralentissement"] > self.cooldown_ralentissement:
            self.speed = self.origin_speed_run
        
    def update_action(self):
        """sometimes actions and actions image are differents :
        when the player dash self.action = 'dash' and self.action_image = 'jump'
        because its has the same image, so we update it here"""
        if self.action_image in ["dash_ground", "roll","Edge_climb", "run", "idle", "fall","up_to_fall","Edge_Idle","Edge_grab","Wall_slide","ground_slide","crouch", "dying", "air_hurt", "dash_attack", "air_dying"]:
            self.action = self.action_image
        elif self.action_image == "jump":
            if self.is_dashing:
                self.action = "dash"
            elif self.is_jumping_edge:
                self.action = "jump_edge"   
            elif self.is_jumping:
                self.action = "jump"   