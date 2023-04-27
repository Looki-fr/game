import pygame
import os
import time
from math import ceil
from mobs.player import Player
from mobs.crab import Crab
from mobs.mob_functions import *
from mobs.bot import *
from mobs.collision import Collision
from pygame.locals import *
from entities_sprite.dash_images import Dash_images
from entities_sprite.particule import Particule
from map.render_map_new import RenderMap
from map.object_map import Object_map
from entities_sprite.dash_attack_effect import Dash_attack_image

class Game:
    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(__file__))
        
        info_screen = pygame.display.Info()
        self.screen = pygame.display.set_mode((round(info_screen.current_w*0.7),round(info_screen.current_h*0.7)))
        self.screen.fill((200,100,100))       
        self.bg = pygame.Surface((self.screen.get_width(), self.screen.get_height()), flags=SRCALPHA)
        self.minimap = pygame.Surface((200,200), flags=SRCALPHA)
        self.dt = 1/30
        
        
        self.all_mobs=[]
        self.all_mobs_wave=[]
        self.group = pygame.sprite.Group()
        self.group_particle = pygame.sprite.Group()
        self.group_object=pygame.sprite.Group()
        self.group_wave=pygame.sprite.Group()
        self.all_groups = [self.group_object,self.group, self.group_particle]
        self.all_coords_mobs_screen = []
        self.all_coords_particule = []
        self.tab_particule_dead=[]
        
        self.radiusL=80
        self.radiusLInc=40

        self.render=RenderMap(self.screen.get_width(), self.screen.get_height(), self.directory)
        self.map_height=self.render.get_height()
        self.map_width=self.render.get_width()
        self.first_map=self.render.get_first_map()
        player_position = (500, 500)
        
        self.image_pp=pygame.image.load(f'{self.directory}\\assets\\pp.png').convert_alpha()
        self.checkpoint=[player_position[0], player_position[1]+1] # the plus one is because the checkpoints are 1 pixel above the ground
        self.player=Player(player_position[0], player_position[1]+1, self.directory, self.render.zoom, "1", self.checkpoint.copy(), Particule, self.add_particule_to_group, Dash_attack_image)
        
        self.pressed_up_bool = [False]
        self.last_player_position=self.player.position.copy()
        
        self.scroll=[0,0]
        self.scroll_rect = Rect(self.player.position[0],self.player.position[1],1,1)
        
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        self.motion = [0, 0]
        
        self.total_friendly_mob=0
        self.add_mob_to_game(self.player, "solo_clavier")
        self.add_mob_to_game(self.player, "solo_clavier", group="wave")
        
        self.collision=Collision(self.render.zoom, self.render.matrix_map) 
        i=1  
        # for line in self.render.matrix_map:
        #     for map in line:
        #         if map != None:      
        #             self.add_mob_to_game(Crab(map["spawn_player"][0], map["spawn_player"][1]+1, self.directory, self.render.zoom, i, self.checkpoint.copy(), Particule,self.add_particule_to_group, self.player, handle_input_ralentissement), "bot")
        #             i+=1
        
        self.all_controls={}
        self.all_controls["solo_clavier"]={"perso":[],"touches":[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,pygame.K_DOWN, pygame.K_q, pygame.K_a, pygame.K_d, pygame.K_z, pygame.K_e]}  
    
        for i,line in enumerate(self.render.matrix_map):
            for y, map in enumerate(line):
                self.load_object_map(y, i)
    
    def load_object_map(self, c, d):
        pass
        #if self.render.type_objects_map[d][c]=="wave":
            # coord=self.render.matrix_map[d][c]["object_map"]
            # self.group_object.add(Object_map(self.render.zoom, "wave", coord[0], coord[1], self.directory, 5, 8, "assets\\flag", "flag_", 2, 30, 5, c, d))

    def blit_health_bar(self, bg, all_mobs):
        i=1
        for mob in all_mobs:
            if "player" in mob.id:
                
                new_y = 12.5*self.render.zoom*(i)
                bg.blit(self.image_pp, (15*self.render.zoom, new_y +5*self.render.zoom*i+ self.image_pp.get_height()*(i-1)))
                new_x = 15*self.render.zoom+80/(mob.max_health/(mob.health+1))
                
                pygame.draw.line(bg, (200,50,50), (15*self.render.zoom, new_y), (new_x, new_y), 2*self.render.zoom)
                i+=1
    
    def blit_group(self, bg, all_groups):
        """blit les images des sprites des groupes sur la surface bg"""
        self.all_coords_mobs_screen = []
        self.all_coords_particule = []
        for group in all_groups:
            for sprite in group.sprites():
                if self.scroll_rect.x - (self.screen.get_width()/2) - sprite.image.get_width() <= sprite.position[0] <= self.scroll_rect.x + (self.screen.get_width()/2)  + sprite.image.get_width() and \
                    self.scroll_rect.y - (self.screen.get_height()/2) - sprite.image.get_height() <= sprite.position[1] <= self.scroll_rect.y + (self.screen.get_height()/2)  + sprite.image.get_height():
                        new_x=self.screen.get_width()/2 + sprite.position[0] - self.scroll_rect.x
                        new_y = self.screen.get_height()/2 + sprite.position[1] - self.scroll_rect.y
                        if "particule" not in sprite.id: 
                            if "arbre" in sprite.id :new_x = self.screen.get_width()/2 + sprite.position[0] - self.scroll_rect.x - sprite.image.get_width()/2

                            if "player" in sprite.id: 
                                new_x_=self.screen.get_width()/2 + sprite.body.centerx - self.scroll_rect.x  
                                new_y_ = self.screen.get_height()/2 + sprite.body.centery - self.scroll_rect.y 
                                self.all_coords_mobs_screen.append((new_x_, new_y_, 3))
                            elif "crab" in sprite.id:
                                new_x_ = self.screen.get_width()/2 + sprite.body.centerx - self.scroll_rect.x  
                                new_y_ = self.screen.get_height()/2 + sprite.body.centery - self.scroll_rect.y 
                                nbr = 3
                                for co in self.all_coords_mobs_screen:
                                    if new_x_-(self.radiusL) <= co[0] <= new_x_+(self.radiusL) and new_y_-(self.radiusL) <= co[1] <= new_y_+(self.radiusL) : 
                                        nbr=0
                                        break
                                    elif new_x_-(self.radiusL+self.radiusLInc) <= co[0] <= new_x_+(self.radiusL+self.radiusLInc) and new_y_-(self.radiusL+self.radiusLInc) <= co[1] <= new_y_+(self.radiusL+self.radiusLInc) : nbr=min(nbr, 1)
                                    elif new_x_-(self.radiusL+self.radiusLInc*2) <= co[0] <= new_x_+(self.radiusL+self.radiusLInc*2) and new_y_-(self.radiusL+self.radiusLInc*2) <= co[1] <= new_y_+(self.radiusL+self.radiusLInc*2) : nbr=min(nbr, 2)
                                if nbr>0:
                                    self.all_coords_mobs_screen.append((new_x_, new_y_, nbr))
                        else: 
                            
                            new_x_=self.screen.get_width()/2 + sprite.rect.centerx - self.scroll_rect.x  
                            new_y_ = self.screen.get_height()/2 + sprite.rect.centery - self.scroll_rect.y 
                            bool=False
                            for co in self.all_coords_mobs_screen:
                                if new_x_-5 <= co[0] <= new_x_+5 and new_y_-5 <= co[1] <= new_y_+5 : bool=True
                            if not bool:self.all_coords_particule.append((new_x_, new_y_, sprite.rect.w*2))
                        bg.blit(sprite.image, (new_x,new_y))
                        
    def update_camera(self, playerx, playery, player_speed_dt):
        self.scroll[0] = ((playerx - self.scroll_rect.x) // 15)*self.render.zoom*player_speed_dt
        self.scroll_rect.x += self.scroll[0] 
        self.scroll[1] = ((playery - self.scroll_rect.y) // 15)*self.render.zoom*player_speed_dt
        self.scroll_rect.y += self.scroll[1] 
        # if self.scroll_rect.x < self.screen.get_width()/2 : self.scroll_rect.x = self.screen.get_width()/2
        # if self.scroll_rect.y < self.screen.get_height()/2 : self.scroll_rect.y = self.screen.get_height()/2
        # if self.scroll_rect.x > self.map_width - self.screen.get_width()/2 : self.scroll_rect.x = self.map_width - self.screen.get_width()/2
        # if self.scroll_rect.y > self.map_height - self.screen.get_height()/2 : self.scroll_rect.y = self.map_height - self.screen.get_height()/2 
    
    def add_mob_to_game(self, mob, input, group="base"):
        if group=="base":
            self.all_mobs.append([mob, input])
            self.group.add(mob)
        else:
            self.all_mobs_wave.append([mob, input])
            self.group_wave.add(mob)
        if input=="manette":
            mob.motion=self.motion
      
    def end_wave_map(self):
        self.render.current_map_is_wave=False  
        self.collision.current_map_is_wave=False
        self.player.reset_actions(chute=True)
        self.player.position, self.player.position_wave_map = self.player.position_wave_map, self.player.position
        self.scroll_rect.x=self.player.position[0]
        self.scroll_rect.y=self.player.position[1]
        player_position = self.first_map["spawn_player"]
        self.checkpoint=[player_position[0], player_position[1]]
        self.player.checkpoint=[player_position[0], player_position[1]]
        self.all_groups.remove(self.group_wave)
        self.all_groups.insert(1, self.group)
      
    def interact_object_map(self, id):
        if id =="wave":
            self.render.load_map_wave()
            self.collision.dico_map_wave=self.render.current_map_objects  
            self.collision.current_map_is_wave=True
            self.player.reset_actions(chute=True)
            self.player.checkpoint=[self.collision.dico_map_wave['spawn_player'][0], self.collision.dico_map_wave['spawn_player'][1]]
            self.player.position_wave_map=[self.collision.dico_map_wave['spawn_player'][0], self.collision.dico_map_wave['spawn_player'][1]-self.player.image.get_height()+1]
            self.player.position, self.player.position_wave_map = self.player.position_wave_map, self.player.position
            self.checkpoint=[self.collision.dico_map_wave['spawn_player'][0], self.collision.dico_map_wave['spawn_player'][1]]
            for i, coord in enumerate(self.collision.dico_map_wave["spawn_crab"]):
                self.add_mob_to_game(Crab(coord[0], coord[1]+1, self.directory, self.render.zoom, str(i+1), self.checkpoint.copy(), Particule,self.add_particule_to_group, self.player, handle_input_ralentissement), "bot", group="wave")  
            self.all_groups.remove(self.group)
            self.all_groups.insert(1, self.group_wave)
        
    def handle_input(self):
        """agit en fonction des touches appuye par le joueur"""
             
        pressed = pygame.key.get_pressed()
        self.all_controls["solo_clavier"]["perso"]=[]
        perso_manette=[]
        if pressed:
            for mob in self.get_all_mob():
                if mob[0].action_image!="dying":
                    #le joueur joue au clavier
                    # elif player[1]=="manette":
                    #     perso_manette.append(player[0])
                    if mob[1] in self.all_controls.keys():
                        self.all_controls[mob[1]]["perso"].append(mob[0])
                    elif mob[1]=="manette":
                        perso_manette.append(mob[0])
                    elif mob[1]=="bot":
                        if mob[0].bot.get_distance_target()<750*self.render.zoom:
                            mob[0].bot.make_mouvement(self.collision)
                        else:
                            mob[0].reset_actions()
            
            for control in self.all_controls.values():
                down=pressed[control["touches"][3]]
                left=pressed[control["touches"][0]]
                right=pressed[control["touches"][1]]
                up=pressed[control["touches"][2]]
                if left: pressed_left(control["perso"], self.collision)
                elif right: pressed_right(control["perso"], self.collision)
                if not left and not right:
                    for mob in control["perso"]:
                        handle_input_ralentissement(mob, self.collision)
                if up:pressed_up(control["perso"], down, left, right, self.pressed_up_bool, self.collision, self.render.zoom)
                if down:pressed_down(control["perso"])
                if pressed[control["touches"][4]]:pressed_dash(control["perso"], left, right, pressed[control["touches"][3]], pressed[control["touches"][2]], self.collision.joueur_sur_sol, self.render.zoom, self.collision)
                if pressed[control["touches"][5]]:pressed_attack(control["perso"])
                if pressed[control["touches"][6]]:pressed_heavy_attack(control["perso"], self.collision, left, right)     
                if pressed[control["touches"][7]]:pressed_pary(control["perso"], left, right, self.collision)                                                    
                if pressed[control["touches"][8]]: 
                    id = pressed_interact(control["perso"], self.group_object)
                    if id !=None:
                        self.interact_object_map(id)
                
        # joystick :
            # down : self.motion[1]>0.1:
            # haut : self.motion[1]<-0.1:
            # right : self.motion[0]>0.1:
            # left :  self.motion[0]<-0.1:
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == JOYAXISMOTION:
                if event.axis < 2:
                    self.motion[event.axis] = event.value
                    if abs(self.motion[0]) < 0.01:
                        self.motion[0] = 0
                    if abs(self.motion[1]) < 0.01:
                        self.motion[1] = 0
            if event.type == JOYBUTTONDOWN or event.type==JOYBUTTONUP:
                if event.button == 0:
                    down,left,right=False,False,False
                    if self.motion[0]<-0.2: left=True
                    if self.motion[0]>0.2: right=True
                    if self.motion[1]>0.4: down=True
                    pressed_up(perso_manette, down, left, right, self.pressed_up_bool, self.collision, self.particule, self.render.zoom)

                if event.button == 1:
                    down,up,left,right=False,False,False,False
                    if self.motion[1]>0.4:down=True
                    if self.motion[1]<-0.4:up=True
                    if self.motion[0]>0.4:right=True
                    if self.motion[0]<-0.4:left=True
                    pressed_dash(perso_manette, left, right, down, up, self.collision.joueur_sur_sol, self.particule, self.render.zoom, self.collision)
                if event.button == 2:    
                    pressed_attack(perso_manette)   
                if event.button == 3:
                    pressed_heavy_attack(perso_manette, self.collision, left, right)
                                
        if self.motion[0]<-0.1:
            pressed_left(perso_manette, self.collision)
        elif self.motion[0]>0.1:
            pressed_right(perso_manette, self.collision)
        else:
            for mob in perso_manette:
                handle_input_ralentissement(mob, self.collision)
        
        if self.motion[1]>0.8:
            pressed_down(perso_manette)
    
    def suppr_dash_image(self):
        for sprite in self.group.sprites():      
            # suppression des images dash apres le cooldown
            if sprite.id == "image_dash":
                if time.time() - sprite.t1 > sprite.cooldown:
                    self.group.remove(sprite)
                if sprite.body.collidelist([tuple[0] for tuple in self.get_all_mob()]) > -1 and self.player.is_grabing_edge:
                    self.group.remove(sprite)
            elif sprite.id == "dash_attack_effect":
                if self.player.dash_attack_image.finish:
                    self.group.remove(self.player.dash_attack_image)
                    self.player.dash_attack_image_added=False
                    self.player.dash_attack_image=None

        for sprite in self.group_wave.sprites():      
            # suppression des images dash apres le cooldown
            if sprite.id == "image_dash":
                if time.time() - sprite.t1 > sprite.cooldown:
                    self.group_wave.remove(sprite)
                if sprite.body.collidelist([tuple[0] for tuple in self.get_all_mob()]) > -1 and self.player.is_grabing_edge:
                    self.group_wave.remove(sprite)
            elif sprite.id == "dash_attack_effect":
                if self.player.dash_attack_image.finish:
                    self.group_wave.remove(self.player.dash_attack_image)
                    self.player.dash_attack_image_added=False
                    self.player.dash_attack_image=None
    
    def gestion_chute(self, mob):
        # si le j saut ou dash la chute prends fin
        if (mob.is_jumping or mob.is_dashing or mob.is_rolling) and mob.is_falling:
            mob.fin_chute(jump_or_dash = True) 
        
        # si le joueur n'est pas sur un sol et ne chute pas on commence la chute
        if not self.collision.joueur_sur_sol(mob):
            if mob.action != "Edge_climb" and not mob.is_falling and not mob.is_jumping and not mob.is_dashing and not mob.is_grabing_edge and not mob.is_jumping_edge:
                if mob.is_attacking or mob.is_dashing_attacking or mob.is_rolling or mob.is_sliding_ground:
                    mob.debut_chute(attack=True)
                else:
                    mob.debut_chute()
        else:
            # sinon on stop la chute si il y en a une
            if mob.is_falling:
                mob.fin_chute()

    def add_particule_to_group(self, p):
        self.group_particle.add(p)
    
    def update_particle(self):
        """update les infos concernant les particles, ajoute ou en supprime """
        # si l'action du joueur a changer on l'update dans la classe particule
        
        for parti in [i[0].particule for i in self.get_all_mob()]+[p for p in self.tab_particule_dead]:
            parti.update()

            i=0
            for key, values in parti.all_particle.items():
                while (i<len(values) and time.time() - values[i].t1 > values[i].cooldown):
                    self.group_particle.remove(values[i])
                    i+=1
                parti.all_particle[key]=values[i:len(values)]
                i=0

        tmp=[]
        for p in self.tab_particule_dead:
            i=0
            for tab in p.all_particle.values():
                i+=len(tab)
            if i==0 : tmp.append(p)

        for p in tmp:
            self.tab_particule_dead.remove(p)
    
    def handle_is_attacking(self, attacking_mob):
        if attacking_mob.is_dashing_attacking or attacking_mob.current_image in attacking_mob.attack_damage[attacking_mob.action_image][0]:
            for mob in [tuple[0] for tuple in self.get_all_mob()]:
                if mob.id != attacking_mob.id and mob.is_mob != attacking_mob.is_mob and (not "roll" in mob.actions or not mob.is_rolling):
                    if (attacking_mob.is_dashing_attacking and attacking_mob.dash_attack_image != None and mob.body.collidelist([attacking_mob.dash_attack_image.body]) > -1) or (mob.body.collidelist([attacking_mob.rect_attack]) > -1 or (attacking_mob.has_air_attack and mob.body.collidelist([attacking_mob.rect_air_attack]) > -1)) and mob.action_image!="dying":
                        if not mob.is_parying or attacking_mob.is_dashing_attacking:
                            if attacking_mob.is_dashing_attacking: mob.health -= attacking_mob.dash_attack_damage
                            else :mob.health -=  attacking_mob.attack_damage[attacking_mob.action_image][1]

                            if not "hurt" in mob.action_image:
                                mob.take_damage()
                            if mob.health <=0:
                                mob.start_dying()

                        else:
                            attacking_mob.take_damage()
                            mob.is_parying=False
                            if not mob.is_falling:
                                mob.change_direction("idle", mob.direction)
                            else:
                                mob.change_direction("up_to_fall", mob.direction)
    
    def _handle_collisions_wall_dash(self, mob, dist, fin_dash, direction, fall=True, distance_y=0):   
        step=round((self.render.tile_width)-2)
        if dist != 0 and step > 0:
            tmp=[mob.position[0], mob.position[1]]
            for i in [y for y in range(step, abs(round(dist)), step)]+[abs(round(dist))+1]:
                if direction == "right":mob.position[0]+=i
                else:mob.position[0]-=i
                if distance_y>0:mob.position[1]+=i
                elif distance_y<0:mob.position[1]-=i
                if self.collision.stop_if_collide(direction, mob, dash=True) or self.collision.joueur_se_cogne(mob):
                    fin_dash()
                    self.collision.check_grab(mob, direction)
                    if fall:
                        if not mob.is_grabing_edge:
                            mob.debut_chute()
                    if not mob.is_grabing_edge:
                        mob.position=[tmp[0], tmp[1]]
                    return
            mob.position=[tmp[0], tmp[1]]

    def handle_action(self, mob):
        if "player" not in mob.id and mob.action=="dying":
            if mob.compteur_image==mob.images[mob.weapon][mob.action_image]["compteur_image_max"] and mob.current_image == mob.images[mob.weapon][mob.action_image]["nbr_image"]:
                mob.particule.is_alive=False
                self.tab_particule_dead.append(mob.particule)
                if self.render.current_map_is_wave:
                    self.group_wave.remove(mob)
                    self.all_mobs_wave.remove([mob, "bot"])
                    if len(self.group_wave)==1:
                        self.end_wave_map()
                else:
                    self.group.remove(mob)
                    self.all_mobs.remove([mob, "bot"])

        # # because action is fall
        # if mob.is_dashing_attacking:
        #     mob.dash_attack()
        
        # le joueur ne peut pas de cogner pendant 2 ticks car sinon il ne peut pas sauter si il tiens un wall du bout des doigts
        if mob.is_jumping_edge and self.collision.joueur_se_cogne(mob) and (mob.jump_edge_pieds or (not mob.jump_edge_pieds and mob.compteur_jump_edge >= mob.compteur_jump_edge_min + mob.increment_jump_edge*4)):
            mob.fin_saut_edge(cogne=True)
        
        if mob.is_jumping and self.collision.joueur_se_cogne(mob):
            mob.fin_saut()
              
        if mob.is_dashing and self.collision.joueur_se_cogne(mob):
            mob.fin_dash()
    
        # gestion collision avec les sols
        
        if mob.is_dashing and self.collision.joueur_sur_sol(mob):
            mob.fin_dash()
            mob.debut_crouch()
            
        # slide on wall
        if mob.is_sliding and self.collision.joueur_sur_sol(mob):
            mob.fin_grab_edge()
            if mob.direction == "right":
                mob.change_direction("idle", "left")
            elif mob.direction == "left":
                mob.change_direction("idle", "right")
        
        # gestion collision avec les murs
        
        mob.save_location()    

        if mob.is_jumping_edge and self.collision.stop_if_collide(mob.direction_jump_edge, mob):
            mob.fin_saut_edge()
            self.collision.check_grab(mob, mob.direction_jump_edge)
        
        if mob.is_sliding_ground and self.collision.stop_if_collide(mob.slide_ground_direction_x, mob):
            mob.fin_slide_ground()
            self.collision.check_grab(mob, mob.slide_ground_direction_x)
        
        if mob.is_rolling and self.collision.stop_if_collide(mob.roll_direction_x, mob):
            mob.fin_roll()
            if mob.is_falling : 
                self.collision.check_grab(mob, mob.roll_direction_x)

        #  if mob.is_dashing_attacking and self.collision.stop_if_collide(mob.direction, mob):
        #     mob.fin_dash_attack()
        #     if mob.is_falling :
        #         self.collision.check_grab(mob)

        # called every tick because distance change every tick
        
        if mob.is_dashing_attacking and time.time()-mob.timer_debut_dash_attack_grabedge > mob.cooldown_not_collide_dash_attack:
            self._handle_collisions_wall_dash(mob, mob.distance_dash_attack(), mob.fin_dash_attack, mob.direction, False)     

        if mob.is_dashing  and time.time()-mob.timer_debut_dash_grabedge > mob.cooldown_not_collide_dash:   
            self._handle_collisions_wall_dash(mob, mob.distance_dash(), mob.fin_dash, mob.dash_direction_x, distance_y=mob.distance_dash_y())  
        
        # le joueur glisse contre les murs au debut du saut puis les grabs ensuite
        if mob.is_jumping and mob.compteur_jump > mob.compteur_jump_min * 0.4 and self.collision.stop_if_collide(mob.direction, mob):
            mob.fin_saut()
            self.collision.check_grab(mob, mob.direction)
        
        if mob.position[1] > self.map_height + 100:
            mob.position = [mob.checkpoint[0], mob.checkpoint[1]-mob.image.get_height()]
        
        self.gestion_chute(mob) 
        
        if (mob.is_attacking or mob.is_dashing_attacking) and mob.action_image!="up_to_attack":
            self.handle_is_attacking(mob)
        
        if mob.is_sliding:
            self.collision.check_tombe_ou_grab(mob)
            
        # if mob.id == "player1":
        #     if not self.render.current_map_is_wave and not self.render.is_current_map_beated(self.scroll_rect.x, self.scroll_rect.y) and self.collision.need_change_map(mob):
        #         self.load_wave()
        
        mob.update_action()
    
    def get_all_mob(self):
        if not self.render.current_map_is_wave:
            return self.all_mobs
        else:
            return self.all_mobs_wave
    
    def update(self):
        """ fonction qui update les informations du jeu"""   
        self.suppr_dash_image()
        
        if not self.render.current_map_is_wave:
            for mob in [tuple[0] for tuple in self.all_mobs]:
                tu=self.render.get_coord_tile_matrix(mob.position[0], mob.position[1])
                mob.coord_map=(tu[-2], tu[-1])
                
        for group in self.all_groups:
            group.update()
            
        for mob in [tuple[0] for tuple in self.get_all_mob()]:
            if mob.bot == None or mob.bot.get_distance_target()<750*self.render.zoom:
                mob.update_action()
                self.handle_action(mob)
                
                if mob.action in mob.dico_action_functions.keys():
                    mob.dico_action_functions[mob.action]()
                    
                if mob.is_jumping and mob.action=="run":
                    mob.is_jumping=False
            else:
                mob.reset_actions()
        
        if self.player.images_dash != []:
            # [x,y, image_modifié, cooldown]
            im = Dash_images(self.player.images_dash[0][0], self.player.images_dash[0][1], self.player.images_dash[0][2], self.player.images_dash[0][3])
            if self.render.current_map_is_wave:self.group_wave.add(im)
            else:self.group.add(im)
            del self.player.images_dash[:]
        
        if self.player.dash_attack_image != None:
            if not self.player.dash_attack_image_added:
                if self.render.current_map_is_wave:self.group_wave.add(self.player.dash_attack_image)
                else:self.group.add(self.player.dash_attack_image)
                self.player.dash_attack_image_added=True
        
        self.update_particle()      
        
        self.update_camera(self.player.position[0], self.player.position[1], self.player.speed_dt)

    def circle_surf(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def fullscreen_surf(self, color):
        surf = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        surf.fill(color)
        return surf

    def add_lightning(self, surface):
        #surface.blit(self.fullscreen_surf((10,10,10)), (0,0), special_flags=BLEND_RGB_SUB)
        for co in self.all_coords_mobs_screen:
            for i in range(co[2]):
                r=self.radiusL+self.radiusLInc*i
                surface.blit(self.circle_surf(r, (4,3,3)), (int(co[0] - r), int(co[1] - r)), special_flags=BLEND_RGB_ADD)
        for co in self.all_coords_particule:
            surface.blit(self.circle_surf(co[2], (15, 7, 7)), (int(co[0] - co[2]), int(co[1] - co[2])), special_flags=BLEND_RGB_ADD)


    def update_ecran(self):     
        self.bg.fill((155,100,100))
        self.minimap.fill((200, 155,155))
        self.render.render(self.bg,self.minimap, self.scroll_rect.x, self.scroll_rect.y)
        self.blit_group(self.bg, self.all_groups)
        self.blit_health_bar(self.bg, [tuple[0] for tuple in self.get_all_mob()])
        if not self.render.current_map_is_wave:
            self.bg.blit(self.minimap, (self.screen.get_width()-self.minimap.get_width(), 0))

        self.add_lightning(self.bg)
        self.screen.blit(self.bg, (0,0))

        self.last_player_position=self.player.position.copy()
    
    def run(self):
        """boucle du jeu"""

        clock = pygame.time.Clock()
        #t1=time.time()
        self.running = True
        while self.running:
            # print(time.time() -t1)
            # if time.time() -t1 > 3:
            #     t1 = time.time()
            #     self.player.take_damage()
            self.player.is_mouving_x = False
            self.handle_input()
            
            self.update()
            
            self.update_ecran()
            #self.collision.draw_walls(self.player, self.screen, self.scroll_rect)
            self.collision.draw(self.player, self.screen, self.scroll_rect, "wall")
            pygame.display.update()      
            
            self.dt = clock.tick(60)
            for mob in [tuple[0] for tuple in self.get_all_mob()]:
                mob.update_tick(self.dt)

        pygame.quit()