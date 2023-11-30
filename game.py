import pygame
from pygame.locals import *
import os
import time
from mobs.mobs.player import Player
from mobs.mobs.crab import Crab
from mobs.mob_functions import *
from mobs.collision import Collision
from sprite.entities.dash_images import Dash_images
from sprite.entities.particule import Particule
from sprite.entities.dash_attack_effect import Dash_attack_image
from map.render_map import RenderMap
from blit import Blit
from menu.menu import Menu
from audio.audio import Audio
from config.config import Config
from seed import Seed
from sprite.cooldown.sprite_cooldown import Sprite_cooldown

class Game:
    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(__file__))
        
        info_screen = pygame.display.Info()
        self.screen = pygame.display.set_mode((round(info_screen.current_w*1),round(info_screen.current_h*0.8)))
        self.screen.fill((0,0,0))       
        self.bg = pygame.Surface((self.screen.get_width(), self.screen.get_height()), flags=SRCALPHA)
        self.minimap = pygame.Surface((200,200), flags=SRCALPHA)
        self.dt = 1/30
        self.seed=Seed()
        self.distance_target_bot=350

        self.config = Config(self.directory)
        self.audio = Audio(self.directory, self.config.get("playlist"), self.config)

        self.menu = Menu(self.directory, self.screen, self.update_ecran, self.update_timers,self.audio, self.set_running_false, self.config, self.new_game, self.seed)
        self.pressed_escape=False

        self.render=RenderMap(self.directory, self.seed)

        self.new_game()

        self.map_height=self.render.get_height()
        self.map_width=self.render.get_width()

        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        # i=1  
        # for line in self.render.map_generation.matrix_map:
        #     for map in line:
        #         if map != None:      
        #             self.add_mob_to_game(Crab(map["spawn_player"][0], map["spawn_player"][1]+1, self.directory, self.render.zoom, i, self.checkpoint.copy(), Particule,self.add_particule_to_group, self.player, handle_input_ralentissement), "bot")
        #             i+=1
        
        self.all_controls={}
        self.all_controls["solo_clavier"]={"perso":[],"touches":[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,pygame.K_DOWN, pygame.K_q, pygame.K_a, pygame.K_d, pygame.K_z, pygame.K_e]}  

    def new_game(self, seed=None):
        self.menu.is_running=False

        self.all_mobs=[]
        self.all_mobs_wave=[]
        self.group = pygame.sprite.Group()
        self.group_particle = pygame.sprite.Group()
        self.group_object=pygame.sprite.Group()
        self.group_wave=pygame.sprite.Group()
        self.group_dash_image_player1=pygame.sprite.Group()
        self.group_dash_attack_image_player1=pygame.sprite.Group()
        self.group_cooldown=pygame.sprite.Group()
        self.all_groups = [self.group_object,self.group,self.group_dash_image_player1, self.group_dash_attack_image_player1, self.group_particle]
        self.tab_particule_dead=[]

        self.render.init_new_map(self.screen.get_width(), self.screen.get_height(), self.directory, seed)
        self.first_map=self.render.get_first_map()

        for i,line in enumerate(self.render.map_generation.matrix_map):
            for y, map in enumerate(line):
                self.load_object_map(y, i)

        positions=[]
        cpt=0
        for i in range(len(self.render.map_generation.matrix_map)):
            for y in range(len(self.render.map_generation.matrix_map[i])):
                if self.render.map_generation.matrix_map[i][y]!=None:
                    if cpt==0:
                        player_position=self.render.get_random_spawn(i, y)
                        if player_position!=None:
                            cpt+=1
                            positions.append(player_position)
                    else:
                        pos=self.render.get_random_spawn(i, y)
                        if pos!=None:
                            positions.append(pos)
                

        self.checkpoint=[player_position[0], player_position[1]+1] # the plus one is because the checkpoints are 1 pixel above the ground
        self.player=Player(player_position[0], player_position[1]+1, self.directory, self.render.zoom, "1", self.checkpoint.copy(), Particule, self.add_particule_to_group, Dash_attack_image,self.group_dash_attack_image_player1, self.group_dash_image_player1, Dash_images, self.audio)
        self.group_cooldown.add(Sprite_cooldown(pygame.image.load(self.directory+"\\assets\\cooldown\\dash_attack.png").convert_alpha(), 50+95+50, self.screen.get_height() - 100, self.player.timers, "timer_dash_attack", self.player.cooldown_dash_attack))
        self.group_cooldown.add(Sprite_cooldown(pygame.image.load(self.directory+"\\assets\\cooldown\\dash.png").convert_alpha(), 50+95+50+95+50, self.screen.get_height() - 100, self.player.timers, "timer_dash", self.player.cooldown_dash))
        self.group_cooldown.add(Sprite_cooldown(pygame.image.load(self.directory+"\\assets\\cooldown\\ground_slide.png").convert_alpha(), 50+95+50+95+50+95+50, self.screen.get_height() - 100, self.player.timers, "timer_cooldown_slide_ground", self.player.cooldown_slide_ground))
        self.group_cooldown.add(Sprite_cooldown(pygame.image.load(self.directory+"\\assets\\cooldown\\dash_ground.png").convert_alpha(), 50+95+50+95+50+95+50+95+50, self.screen.get_height() - 100, self.player.timers, "timer_cooldown_dash_ground", self.player.cooldown_dash_ground))

        self.motion = [0, 0]        

        self.collision=Collision(self.render.zoom, self.render.map_generation.matrix_map) 
        self.blit = Blit(self.render.zoom, self.screen, self.bg, self.minimap, self.player)

        self.pressed_up_bool = [False]
        self.pressed_dash_bool = [False]
        self.last_player_position=self.player.position.copy()

        self.total_friendly_mob=0
        self.add_mob_to_game(self.player, "solo_clavier")
        self.add_mob_to_game(self.player, "solo_clavier", group="wave")

        for pos in positions:
            self.add_mob_to_game(Crab(pos[0], pos[1]+1, self.directory, self.render.zoom, "1", self.checkpoint.copy(), Particule,self.add_particule_to_group, self.player), "bot")


    def load_object_map(self, c, d):
        pass
        #if self.render.type_objects_map[d][c]=="wave":
            # coord=self.render.map_generation.matrix_map[d][c]["object_map"]
            # self.group_object.add(Object_map(self.render.zoom, "wave", coord[0], coord[1], self.directory, 5, 8, "assets\\flag", "flag_", 2, 30, 5, c, d))
    
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
        self.blit.scroll_rect.x=self.player.position[0]
        self.blit.scroll_rect.y=self.player.position[1]
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
                self.add_mob_to_game(Crab(coord[0], coord[1]+1, self.directory, self.render.zoom, str(i+1), self.checkpoint.copy(), Particule,self.add_particule_to_group, self.player), "bot", group="wave")  
            self.all_groups.remove(self.group)
            self.all_groups.insert(1, self.group_wave)

    def handle_input(self):
        """agit en fonction des touches appuyes par le joueur"""
             
        pressed = pygame.key.get_pressed()
        self.all_controls["solo_clavier"]["perso"]=[]
        perso_manette=[]
        
        if pressed:
            if pressed[pygame.K_ESCAPE]:
                if not self.pressed_escape:
                    if self.menu.is_running:
                        self.menu.end()
                    else:
                        self.menu.start()

                    self.pressed_escape=True
            else:
                self.pressed_escape=False

            if self.menu.is_running:
                self.menu._handle_input(pressed)

            if not self.menu.is_running:
                for mob in self.get_all_mob():
                    if not "dying" in mob[0].action_image:
                        #le joueur joue au clavier
                        # elif player[1]=="manette":
                        #     perso_manette.append(player[0])
                        if mob[1] in self.all_controls.keys():
                            self.all_controls[mob[1]]["perso"].append(mob[0])
                        elif mob[1]=="manette":
                            perso_manette.append(mob[0])
                        elif mob[1]=="bot":
                            mob[0].bot.make_mouvement(self.collision, self.render.zoom, self.distance_target_bot, self.render.tile_width)
                
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
                    if pressed[control["touches"][4]]:pressed_dash(control["perso"], left, right, pressed[control["touches"][3]], pressed[control["touches"][2]], self.collision.joueur_sur_sol, self.collision, self.pressed_dash_bool)
                    else: self.pressed_dash_bool[0]=False
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
            if event.type == pygame.USEREVENT+1:
                self.audio.start_music()
            if not self.menu.is_running:
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
                        pressed_dash(perso_manette, left, right, down, up, self.collision.joueur_sur_sol, self.particule, self.collision)
                    if event.button == 2:    
                        pressed_attack(perso_manette)   
                    if event.button == 3:
                        pressed_heavy_attack(perso_manette, self.collision, left, right)
            else:
                self.menu.handle_events(event)
                                
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
        for group in [self.group_dash_image_player1, self.group_dash_attack_image_player1]:
            for sprite in group.sprites():      
                # suppression des images dash apres le cooldown
                if not "dash_attack_effect" in sprite.id and time.time() - sprite.t1 > sprite.cooldown or (sprite.body.collidelist([tuple[0] for tuple in self.get_all_mob()]) > -1 and self.player.is_grabing_edge):
                    group.remove(sprite)
                elif "dash_attack_effect" in sprite.id and sprite.finish:
                    group.remove(sprite)

    def add_particule_to_group(self, p):
        self.group_particle.add(p)
    
    def update_particle(self):
        """update les infos concernant les particles, ajoute ou en supprime """
        # si l'action du joueur a changer on l'update dans la classe particule
        
        self.player.particule.sur_sol = self.collision.joueur_sur_sol(self.player, change_pos=False)
        
        for parti in [i[0].particule for i in self.get_all_mob()]+[p for p in self.tab_particule_dead]:
            if "player" in parti.player.id and "jump_edge" in parti.player.action:
                parti.pieds_collide_jump_edge = self.collision.check_pieds_collide_wall(parti.player)
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

    def update_timers(self, dt):
        for group in self.all_groups:
            for sprite in group.sprites():
                sprite.update_timers(dt)

    def handle_action(self, mob):
        if "player" not in mob.id and "dying" in mob.action:
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
        
        # gestion collision avec les murs
        
        mob.save_location()    

        if mob.is_jumping_edge and self.collision.stop_if_collide(mob.direction_jump_edge, mob):
            tmp=mob.direction_jump_edge
            mob.fin_saut_edge()
            self.collision.check_grab(mob, tmp)
            
        temp_ground=False

        if mob.is_sliding_ground and self.collision.stop_if_collide(mob.slide_ground_direction_x, mob, dash=True, dontmove=True):
            temp_ground=not mob.is_falling
            tmp=mob.slide_ground_direction_x
            mob.fin_slide_ground()
            self.collision.check_grab(mob, tmp)

        # if mob.is_dashing_ground and self.collision.stop_if_collide(mob.dash_ground_direction_x, mob, dash=True, dontmove=True):
        #     temp_ground=not mob.is_falling
        #     tmp=mob.dash_ground_direction_x
        #     mob.fin_dash_ground()
        #     self.collision.check_grab(mob, tmp)
        
        if mob.is_rolling and self.collision.stop_if_collide(mob.roll_direction_x, mob):
            tmp=mob.roll_direction_x
            mob.fin_roll()
            if mob.is_falling : 
                self.collision.check_grab(mob, tmp)
        
        # after because if slide ground we need to cancel the grab wall before we see it on screen
        # slide on wall
        if temp_ground or (mob.is_sliding and self.collision.joueur_sur_sol(mob)):
            mob.fin_grab_edge(change_dir=temp_ground)
            if mob.direction == "right":
                mob.change_direction("run", "left")
            elif mob.direction == "left":
                mob.change_direction("run", "right")


        # le joueur ne peut pas de cogner pendant 2 ticks car sinon il ne peut pas sauter si il tiens un wall du bout des doigts
        if mob.is_jumping_edge and self.collision.joueur_se_cogne(mob) and (mob.jump_edge_pieds or (not mob.jump_edge_pieds and mob.compteur_jump_edge >= mob.compteur_jump_edge_min + mob.increment_jump_edge*4)):
            mob.fin_saut_edge(cogne=True)
        
        if mob.is_jumping and self.collision.joueur_se_cogne(mob):
            mob.fin_saut(ground=self.collision.joueur_sur_sol(mob), cogne=True)

        if mob.action=="Edge_climb" and self.collision.joueur_se_cogne(mob):
            mob.fin_grab_edge_cogne()

        # called every tick because distance change every tick
        
        if mob.is_dashing_attacking and time.time()-mob.timers["timer_debut_dash_attack_grabedge"] > mob.cooldown_not_collide_dash_attack:
            self.collision.handle_collisions_wall_dash(mob, mob.fin_dash_attack, mob.direction, fall=False)     

        if mob.is_dashing and time.time()-mob.timers["timer_debut_dash_grabedge"] > mob.cooldown_not_collide_dash:   
            self.collision.handle_collisions_wall_dash(mob, mob.fin_dash, mob.dash_direction_x, ground=True)  
        
        if mob.is_dashing_ground:
            self.collision.handle_collisions_wall_dash(mob, mob.fin_dash_ground, mob.dash_ground_direction_x, fall=True)

        # le joueur glisse contre les murs au debut du saut puis les grabs ensuite
        if mob.is_jumping and mob.compteur_jump > mob.compteur_jump_min * 0.4 and self.collision.stop_if_collide(mob.direction, mob):
            mob.fin_saut(ground=self.collision.joueur_sur_sol(mob))
            self.collision.check_grab(mob, mob.direction)
        
        if mob.position[1] > self.map_height + 100:
            mob.position = [mob.checkpoint[0], mob.checkpoint[1]-mob.image.get_height()]
        
        gestion_chute(mob, self.collision) 
        
        if (mob.is_attacking or mob.is_dashing_attacking) and mob.action_image!="up_to_attack":
            handle_is_attacking(mob, self.get_all_mob, self.collision)
        
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
        if not self.menu.is_running:
            self.suppr_dash_image()
            
            if not self.render.current_map_is_wave:
                for mob in [tuple[0] for tuple in self.all_mobs]:
                    tu=self.render.get_coord_tile_matrix(mob.position[0], mob.position[1])
                    mob.coord_map=(tu[-2], tu[-1])
                    
            for group in self.all_groups:
                group.update()

            self.group_cooldown.update()
                
            for mob in [tuple[0] for tuple in self.get_all_mob()]:
                if mob.bot == None or mob.bot.get_distance_target()<self.distance_target_bot*2*self.render.zoom:
                    mob.update_action()
                    self.handle_action(mob)
                    
                    if mob.action in mob.dico_action_functions.keys():
                        mob.dico_action_functions[mob.action]()
                        
                    if mob.is_jumping and mob.action=="run":
                        mob.is_jumping=False
            
            self.update_particle()      
            
            self.blit.update_camera(self.player.position[0], self.player.position[1], self.player.speed_dt, self.player.rect.width)

            self.last_player_position=self.player.position.copy()

            self.update_ecran()

    def update_ecran(self, menu=False):    
        #self.bg.fill((155,100,100)) 
        self.bg.fill((100,100,155))
        self.minimap.fill((200, 155,155))
        self.render.render(self.bg,self.minimap, self.blit.scroll_rect.x, self.blit.scroll_rect.y)
        all_coords_mobs_screen, all_coords_particule = self.blit.blit_group(self.bg, self.all_groups)
        for group in self.group_cooldown.sprites():
            self.bg.blit(group.image, group.position)
        #self.render.shadow.draw_matrix(self.bg, self.blit.scroll_rect, self.player.coord_map)
        #self.render.shadow.draw_shadow(self.bg, self.blit.scroll_rect, self.player.coord_map, self.player.head)
        self.blit.blit_health_bar(self.bg)
        if not self.render.current_map_is_wave:
            self.bg.blit(self.minimap, (self.screen.get_width()-self.minimap.get_width(), 0))
        self.blit.add_lightning(self.bg, all_coords_mobs_screen, all_coords_particule)
        if menu:
            s = pygame.Surface((self.screen.get_width(),self.screen.get_height()), pygame.SRCALPHA)
            s.fill((255,255,255,64))                       
            self.bg.blit(s, (0,0))
        self.screen.blit(self.bg, (0,0))
        
    def set_running_false(self):
        self.running=False

    def run(self):
        """boucle du jeu"""

        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.player.is_mouving_x = False
            self.handle_input()
            self.update()
        
            
            #self.collision.draw(self.player, self.screen, self.blit.scroll_rect, "ceilling")
            pygame.display.update()      
            self.dt = clock.tick(60)
            for mob in [tuple[0] for tuple in self.get_all_mob()]:
                mob.update_tick(self.dt)
        self.config.save()
        pygame.quit()