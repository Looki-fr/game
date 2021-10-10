import pygame
import os
import time
from math import ceil
from player import Player
from pygame.locals import *
from dash_images import Dash_images
from particule import Particule
from textSprite import TextSprite
from toucheSprite import ToucheSprite
from tileMap import TileMap

directory = os.path.dirname(os.path.realpath(__file__))

class Game:
    def __init__(self):
        info_screen = pygame.display.Info()
        # créer la fenetre du jeu
        #flags = FULLSCREEN | DOUBLEBUF | NOFRAME | SCALED
        #flags = HWSURFACE|DOUBLEBUF
        flags = FULLSCREEN | DOUBLEBUF # + 16 in args
        self.screen = pygame.display.set_mode((round(info_screen.current_w*0.7),round(info_screen.current_h*0.7)))
        self.bg = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        pygame.display.set_caption(f"Looki's aventure")
        self.zoom = 2
        self.dt = 1/30
        
        # chargement map
        self.map = TileMap(f"{directory}\\assets\\maps\\Test_map2.tmx", self.screen.get_width(), self.screen.get_height(), self.zoom)
        
        # initialization joueur
        player_position = self.map.tm.get_object_by_name("spawn_player") 
        self.player = Player(player_position.x*self.zoom, player_position.y*self.zoom, directory, self.zoom)
        self.all_players = [self.player.body]
        
        # creation groupe de sprite 
        self.group = pygame.sprite.Group()
        self.group.add(self.player)
        self.group_particle = pygame.sprite.Group()
        self.all_groups = [self.group, self.group_particle]
        
        # particule lors de mouvement du joueur
        self.particule = Particule(directory, self.player.body.h, self.player.body.w, self.zoom)
        self.direction_joueur = ""
        self.action_joueur = ""
        
        # chaque element de walls / etc est sous la forme : [x, y, [rect]]
        self.walls = []
        self.grounds = []
        self.ceillings = []
        self.plateformes = []
        self.all_text = []
        for obj in self.map.tm.objects:
            if obj.type == "collision":
                if obj.name == "wall":
                    self.walls.append((obj.x * self.zoom ,obj.y * self.zoom ,[pygame.Rect(obj.x * self.zoom , obj.y * self.zoom , obj.width * self.zoom , obj.height * self.zoom )]))
                elif obj.name == "ground":
                    self.grounds.append((obj.x * self.zoom ,obj.y * self.zoom ,[pygame.Rect(obj.x * self.zoom , obj.y * self.zoom , obj.width * self.zoom , obj.height * self.zoom )]))
                elif obj.name == "ceilling":
                    self.ceillings.append((obj.x * self.zoom ,obj.y * self.zoom ,[pygame.Rect(obj.x * self.zoom , obj.y * self.zoom , obj.width * self.zoom , obj.height * self.zoom )]))
                elif obj.name == 'plateforme':
                    self.plateformes.append((obj.x * self.zoom ,obj.y * self.zoom ,[pygame.Rect(obj.x * self.zoom , obj.y * self.zoom , obj.width * self.zoom , obj.height * self.zoom )]))
            elif obj.type == 'spawn_phrase':
                self.spawn_phrase(obj.name, obj.x * self.zoom , obj.y * self.zoom )
        
        self.pressed_up = False
        
        self.scroll=[0,0]
        self.scroll_rect = Rect(self.player.position[0],self.player.position[1],1,1)
        
    def spawn_phrase(self, name, x, y):
        text_id = name.split(";")
        for id in text_id:
            # c'est un text
            if id[0] == "0":
                self.all_text.append(TextSprite(x, y, id[1::], directory))
                x += self.all_text[-1].image.get_width() + 15
            elif id[0] == "1":
                self.all_text.append(ToucheSprite(x, y, id[1::], directory))
                x += self.all_text[-1].image.get_width() + 15
    
    def joueur_sur_sol(self):
        """renvoie True si les pieds du joueur est sur une plateforme ou sur le sol.
        De plus, place la coordonee en y du joueur juste au dessus de la plateforme / du sol"""
        for sprite in self.group.sprites():
            if sprite.id == 'player':
                passage_a_travers = time.time() - sprite.t1_passage_a_travers_plateforme < sprite.cooldown_passage_a_travers_plateforme
                # si le joueur est en collision avec un mur
                for ground in self.grounds:
                    if sprite.feet.collidelist(ground[2]) > -1:
                        sprite.position[1] = ground[1] - sprite.image.get_height() + 1
                        # comme le joueur est sur le sol, il peut de nouveau dash / sauter
                        sprite.a_sauter = False
                        sprite.a_dash = False
                        return True
                for plateforme in self.plateformes:
                    # and not sprite.is_sliding
                    if not passage_a_travers:
                        if sprite.feet.collidelist(plateforme[2]) > -1:
                            if sprite.position[1] + self.player.image.get_height() - plateforme[1] < 20:
                                sprite.position[1] = plateforme[1] - sprite.image.get_height() + 1
                                # comme le joueur est sur une plateforme, il peut de nouveau dash / sauter
                                sprite.a_sauter = False
                                sprite.a_dash = False
                                return True
        return False
    
    def joueur_se_cogne(self):
        """renvoie True si la tete du joueur est en collision avec un plafond"""
        for sprite in self.group.sprites():
            if sprite.id == 'player':
                for ceilling in self.ceillings:
                    if sprite.head.collidelist(ceilling[2]) > -1:
                        return True
       
    def stop_if_collide(self, direction, head = False):
        """fait en sorte que le joueur avance plus lorsque qu'il vance dans un mur"""
        for sprite in self.group.sprites():
            if sprite.id == 'player':
                if head:
                    rect = sprite.head
                else:
                    rect = sprite.body
                # si le joueur est en collision avec un mur
                for wall in self.walls:
                    if rect.collidelist(wall[2]) > -1:
                        # si le joueur va a droite en etant a gauche du mur
                        # limage est plus grande que la partie visible du joueur, d'où self.player.image.get_width()/2
                        if direction == 'right' and wall[0] > self.player.position[0] + self.player.image.get_width()/3:
                            sprite.move_back()   
                            return True
                        # si le joueur va a gauche en etant a droite du mur
                        if direction == 'left' and wall[0] < self.player.position[0] + self.player.image.get_width()/2:
                            sprite.move_back()  
                            return True

    def stick_to_wall(self):
        if self.player.direction == "right":
            self.player.position[0] += 30
            for sprite in self.group.sprites():
                if sprite.id == 'player':
                    # si le joueur est en collision avec un mur
                    for wall in self.walls:
                        if sprite.body.collidelist(wall[2]) > -1:
                            self.player.position[0] = wall[0] - self.player.body.w * 1.8
        elif self.player.direction == "left":
            self.player.position[0] -= 30
            for sprite in self.group.sprites():
                if sprite.id == 'player':
                    # si le joueur est en collision avec un mur
                    for wall in self.walls:
                        if sprite.body.collidelist(wall[2]) > -1:
                            self.player.position[0] = wall[0] - self.player.body.w * 1.8 + wall[2][0].w
        
    def handle_input(self):
        """agit en fonction des touches appuye par le joueur"""
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_LEFT] and self.player.is_sliding_ground and self.player.slide_ground_direction_x == 'right':
            self.player.fin_slide_ground()
        elif pressed[pygame.K_RIGHT] and self.player.is_sliding_ground and self.player.slide_ground_direction_x == 'left':
            self.player.fin_slide_ground()
        if pressed[pygame.K_UP]:
            if self.pressed_up == False and self.player.is_grabing_edge:
                self.player.fin_grab_edge()
                dir_x = ""
                if pressed[pygame.K_LEFT]:
                    dir_x = "left"
                elif pressed[pygame.K_RIGHT]:
                    dir_x = "right"
                if self.check_pieds_collide_wall():
                    self.player.debut_saut_edge(direction_x=dir_x)
                    self.particule.pieds_collide_jump_edge = True
                    self.particule.y_debut_jump_edge = self.player.coord_debut_jump_edge[1] + self.player.body.h
                    if self.player.direction == "right":
                        self.particule.x_debut_jump_edge = self.player.coord_debut_jump_edge[0] + self.player.body.w * 2 - 10
                    elif self.player.direction == "left":
                        self.particule.x_debut_jump_edge = self.player.coord_debut_jump_edge[0] + self.player.body.w *2 -10
                else:
                    self.player.debut_saut_edge(direction_x=dir_x)
                    self.particule.pieds_collide_jump_edge = False
                    
            self.pressed_up = True
        else:
            self.pressed_up = False
        
        # dash
        if not self.player.is_jumping and not self.player.is_dashing and not self.player.a_dash and not self.player.is_sliding_ground and not self.player.is_grabing_edge and not self.player.is_jumping_edge:
            if not self.joueur_sur_sol() and pressed[pygame.K_q]:    
                dir_y = ""
                dir_x = ""
                if pressed[pygame.K_DOWN]:
                    dir_y = "down"
                if pressed[pygame.K_UP]:
                    dir_y = "up"
                if pressed[pygame.K_RIGHT]:
                    dir_x = "right"
                if pressed[pygame.K_LEFT]:
                    dir_x = "left"
                if dir_y == "" and dir_x == "":
                    dir_y = "up"
                    
                self.player.debut_dash(dir_x, dir_y)
                
                self.particule.debut_dash_y = self.player.coord_debut_dash[1]+ self.player.body.h
                self.particule.dir_dash_x = self.player.dash_direction_x
                self.particule.dir_dash_y = self.player.dash_direction_y    
                if self.player.direction == "right":    
                    self.particule.debut_dash_x = self.player.coord_debut_dash[0] + self.player.body.w + 10
                elif self.player.direction == "left":
                    self.particule.debut_dash_x = self.player.coord_debut_dash[0] + self.player.body.w + 26
            elif self.joueur_sur_sol() and pressed[pygame.K_LEFT] and not pressed[pygame.K_RIGHT] and pressed[pygame.K_DOWN] and time.time() - self.player.timer_cooldown_slide_ground > self.player.cooldown_slide_ground :
                if self.player.is_falling: self.player.fin_chute()
                self.player.debut_slide_ground("left")
            elif self.joueur_sur_sol() and pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT] and pressed[pygame.K_DOWN] and time.time() - self.player.timer_cooldown_slide_ground > self.player.cooldown_slide_ground :
                if self.player.is_falling: self.player.fin_chute()
                self.player.debut_slide_ground("right")
        
        # aller a gauche
        if pressed[pygame.K_LEFT] and not self.player.is_jumping_edge and not self.player.is_grabing_edge and not self.player.is_sliding_ground and not self.player.is_dashing:
            self.player.save_location()
            bool = self.joueur_sur_sol()
            if bool:
                self.player.move_left(pieds_sur_sol=True)
            # si le joueur ne dash pas et est en lair
            else:
                self.player.move_left()
            if self.stop_if_collide("left") and not bool and not self.player.is_jumping:
                self.check_grab()
            
        # aller a droite    
        elif pressed[pygame.K_RIGHT] and not self.player.is_jumping_edge and not self.player.is_grabing_edge and not self.player.is_sliding_ground and not self.player.is_dashing:
            self.player.save_location()
            bool = self.joueur_sur_sol()
            if bool:
                self.player.move_right(pieds_sur_sol=True)
            # si le joueur ne dash pas et est en lair
            else:
                self.player.move_right()
            if self.stop_if_collide("right") and not bool and not self.player.is_jumping:
                self.check_grab()
        else:
            # si le joueur avance pas, il deviens idle
            if self.player.action != "fall" and self.player.action != "up_to_fall" and not self.player.is_sliding_ground:
                if self.player.action == "run" and self.player.ralentit_bool == False:
                    self.player.debut_ralentissement()
                # si self.player.ralentissement na pas ete appele, self.player.ralentissement aura aucun effet
                # => donc le ralentissement a lieu que quand le joueur arrete de courir
                self.player.ralentissement()
            
        if pressed[pygame.K_DOWN]:
            # le joueur passe a travers les plateformes pendant X secondes
            self.player.t1_passage_a_travers_plateforme = time.time()
            # if self.player.is_grabing_edge:
            #     self.player.fin_grab_edge(mouvement = False)
        elif pressed[pygame.K_UP]:
            # saut
            if (self.joueur_sur_sol() or time.time() - self.player.timer_cooldown_able_to_jump < self.player.cooldown_able_to_jump) \
                and not self.player.a_sauter and not self.player.is_jumping_edge\
                and time.time() - self.player.timer_cooldown_next_jump > self.player.cooldown_next_jump \
                and not self.player.is_jumping_edge and not self.player.is_dashing:
                if self.player.is_sliding_ground:
                    self.player.fin_slide_ground()
                self.player.debut_saut()
                self.particule.y_debut_jump = self.player.coord_debut_jump[1]+ self.player.body.h
                if self.player.direction == "right":
                    self.particule.x_debut_jump = self.player.coord_debut_jump[0] + self.player.body.w - 15
                elif self.player.direction == "left":
                    self.particule.x_debut_jump = self.player.coord_debut_jump[0] + self.player.body.w + 56
    
    def check_grab(self):
        """Grab SSI head collide"""
        
        for sprite in self.group.sprites():
            if sprite.id == 'player':
                # si le joueur est en collision avec un mur
                for wall in self.walls:
                    if sprite.body.collidelist(wall[2]) > -1 and sprite.head.collidelist(wall[2]) > -1:
                        if not self.player.is_jumping_edge:
                            sprite.fin_chute()
                            sprite.debut_grab_edge()
                        self.stick_to_wall()
                          
    def check_pieds_collide_wall(self):
        for sprite in self.group.sprites():
            if sprite.id == 'player':
                # si le joueur est en collision avec un mur
                collide_wall = False
                for wall in self.walls:
                    if sprite.feet.collidelist(wall[2]) > -1:
                        collide_wall = True
                return collide_wall
    
    def check_tombe_ou_grab(self):
        for sprite in self.group.sprites():
            if sprite.id == 'player':
                # si le joueur est en collision avec un mur
                collide_wall = False
                for wall in self.walls:
                    if (sprite.body.collidelist(wall[2]) > -1 or sprite.head.collidelist(wall[2]) > -1) and sprite.is_sliding:
                        collide_wall = True
                if not collide_wall:
                    sprite.fin_grab_edge()
    
    def blit_texte(self):
        """blit les textes presents sur l'écran et ensuite blit le joueur par dessus si les rect se collide"""
        for texte in self.all_text:
            texte.update()
            if self.screen.get_width()/2 > self.player.position[0] - texte.x + texte.image.get_width() < self.screen.get_width()/2 and - self.screen.get_height()/2 < self.player.position[0] - texte.x < self.screen.get_height()/2:
                # les images doivent etre agrandis en fonction du zoom
                image = pygame.transform.scale(texte.image, (round(texte.rect.w*self.zoom),round(texte.rect.h*self.zoom)))
                image.set_colorkey(texte.image.get_at((0,0)))
                self.screen.blit(image, (self.screen.get_width()/2 + (texte.x - self.player.position[0]) * self.zoom, self.screen.get_height()/2 + (texte.y - self.player.position[1])* self.zoom))     
                image_p = pygame.transform.scale(self.player.image, (round(self.player.rect.w*self.zoom),round(self.player.rect.h*self.zoom)))
                image_p.set_colorkey(image_p .get_at((0,0)))
                if self.player.body.collidelist([texte.rect]) > -1:
                    self.screen.blit(image_p, (self.screen.get_width()/2,self.screen.get_height()/2))

    def blit_group(self):
        for group in self.all_groups:
            for sprite in group.sprites():
                if self.scroll_rect.x - (self.screen.get_width()/2) - sprite.image.get_width() <= sprite.position[0] <= self.scroll_rect.x + (self.screen.get_width()/2)  + sprite.image.get_width() and \
                    self.scroll_rect.y - (self.screen.get_height()/2) - sprite.image.get_height() <= sprite.position[1] <= self.scroll_rect.y + (self.screen.get_height()/2)  + sprite.image.get_height():
                        new_x = self.screen.get_width()/2 + sprite.position[0] - self.scroll_rect.x
                        new_y = self.screen.get_height()/2 + sprite.position[1] - self.scroll_rect.y
                        self.bg.blit(sprite.image, (new_x,new_y))
                    
    def update(self):
        """ fonction qui update les informations du jeu"""   
        
        for sprite in self.group.sprites():      
            # suppression des images dash apres le cooldown
            if sprite.id == "image_dash":
                if time.time() - sprite.t1 > sprite.cooldown:
                    self.group.remove(sprite)
                if sprite.body.collidelist(self.all_players) > -1 and self.player.is_grabing_edge:
                    self.group.remove(sprite)
        
        # le joueur ne peut pas de cogner pendant 2 ticks car sinon il ne peut pas sauter si il tiens un wall du bout des doigts
        if self.joueur_se_cogne() and self.player.is_jumping_edge and self.player.compteur_jump_edge >= self.player.compteur_jump_edge_min + self.player.increment_jump_edge*1:
            print(self.player.compteur_jump_edge, self.player.compteur_dash_min)
            self.player.fin_saut_edge()
        
        if self.joueur_se_cogne() and self.player.is_jumping:
            self.player.fin_saut()
            
        if self.joueur_se_cogne() and self.player.is_dashing:
            self.player.fin_dash()
        
        if self.joueur_sur_sol() and self.player.is_dashing:
            self.player.fin_dash()
            self.player.debut_crouch()
        
        if self.joueur_sur_sol() and self.player.is_sliding:
            self.player.fin_grab_edge()
            if self.player.direction == "right":
                self.player.change_direction("idle", "left")
            elif self.player.direction == "left":
                self.player.change_direction("idle", "right")
        
        self.player.save_location()    
            
        if self.player.is_jumping_edge and self.stop_if_collide(self.player.direction_jump_edge):
            self.player.fin_saut_edge()
            self.check_grab()
        
        if self.player.is_sliding_ground and self.stop_if_collide(self.player.slide_ground_direction_x):
            self.player.fin_slide_ground()
            self.check_grab()
            
        if self.player.is_dashing and self.stop_if_collide(self.player.dash_direction_x):
            self.player.fin_dash()
            self.check_grab()
        
        if self.player.is_jumping and self.player.compteur_jump > self.player.compteur_jump_min * 0.4 and self.stop_if_collide(self.player.direction):
            self.player.fin_saut()
            self.check_grab()
        
        if (self.player.is_jumping or self.player.is_dashing) and self.player.is_falling:
            self.player.fin_chute(jump_or_dash = True) 
        
        # si le joueur n'est pas sur un sol et ne chute pas on commence la chute
        if not self.joueur_sur_sol():
            if not self.player.is_falling and not self.player.is_jumping and not self.player.is_dashing and not self.player.is_grabing_edge and not self.player.is_jumping_edge:
                if self.player.is_sliding_ground:
                    self.player.fin_slide_ground()
                self.player.debut_chute()
        else:
            # sinon on stop la chute si il y en a une
            if self.player.is_falling:
                self.player.fin_chute() 
        
        if not self.player.is_jumping and not self.player.is_jumping_edge and self.player.action == 'jump' and self.joueur_sur_sol():
            self.player.change_direction("idle", self.player.direction)       
        
        if self.player.is_sliding:
            self.check_tombe_ou_grab()
        
        self.player.chute()
        self.player.saut()
        self.player.dash()
        self.player.saut_edge()
        self.player.sliding()
        self.player.slide_ground()
        
        if self.player.images_dash != []:
            # [x,y, image_modifié, cooldown]
            im = Dash_images(self.player.images_dash[0][0], self.player.images_dash[0][1], self.player.images_dash[0][2], self.player.images_dash[0][3])
            self.group.add(im)
            del self.player.images_dash[:]
        
        # particle
        
        temp_action = self.player.action
        if temp_action == "jump" and self.player.is_dashing:
            temp_action = 'dash'
        elif temp_action == "jump" and self.player.is_jumping_edge:
            temp_action = "jump_edge"
        
        # si l'action du joueur a changer on l'update dans la classe particule
        if self.action_joueur != temp_action:
            self.action_joueur = temp_action
            self.particule.action_joueur = temp_action
            
        # si la direction du joueur a changer on l'update dans la classe particule    
        if self.direction_joueur != self.player.direction:
            self.direction_joueur = self.player.direction
            self.particule.direction_joueur = self.player.direction
        
        self.group.update() 
        self.group_particle.update()
        
        y = self.player.body.y + self.player.body.h
        
        # ajustement de la position en x du joueur pour que les particle spawn au bon endroit puis update de la position du joueur dans lobjet de la classe particle
        if self.player.direction == "right":
            x = self.player.body.x - 20
            self.particule.update(x, y)
        elif self.player.direction == "left":
            x = self.player.body.x + self.player.body.w + 20
            self.particule.update(x, y)
            
        # transmition de donnee a travers des tableau de lobjet de la classe particle vers la clsse game    
        if self.particule.new_particle != []:
            for i in self.particule.new_particle:
                self.group_particle.add(i)
            self.particule.new_particle.clear()
        
        if self.particule.remove_particle != []:
            for id in self.particule.remove_particle:
                for sprite in self.group_particle.sprites():
                    if sprite.id == f"particule{id}":
                        self.group_particle.remove(sprite)
            self.particule.remove_particle.clear()      
        
        self.scroll[0] = ((self.player.position[0] - self.scroll_rect.x) // 15)*self.zoom*self.player.speed_dt
        self.scroll_rect.x += self.scroll[0] 
        self.scroll[1] = ((self.player.position[1] - self.scroll_rect.y) // 15)*self.zoom*self.player.speed_dt
        self.scroll_rect.y += self.scroll[1] 
        if self.scroll_rect.x < self.screen.get_width()/2 : self.scroll_rect.x = self.screen.get_width()/2
        if self.scroll_rect.y < self.screen.get_height()/2 : self.scroll_rect.y = self.screen.get_height()/2
        if self.scroll_rect.x > self.map.width - self.screen.get_width()/2 : self.scroll_rect.x = self.map.width - self.screen.get_width()/2
        if self.scroll_rect.y > self.map.height - self.screen.get_height()/2 : self.scroll_rect.y = self.map.height - self.screen.get_height()/2
        
    def run(self):
        """boucle du jeu"""

        clock = pygame.time.Clock()

        self.running = True
        while self.running:
            
            # appelle de la methode gerant les inputs
            self.player.is_mouving_x = False
            self.handle_input()
            
            self.update()
            self.bg.fill((255,155,155))
            self.map.render(self.bg, self.scroll_rect.x, self.scroll_rect.y)
            #self.bg.blit(self.image_bg,(0,0))
            #self.bg.blit(self.map_img,(-(self.scroll_rect.x - self.screen.get_width()/2) ,-(self.scroll_rect.y - self.screen.get_height()/2)))
            self.blit_group()
            self.screen.blit(self.bg, (0,0))
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.dt = clock.tick(60)
            self.player.update_tick(self.dt)
            self.particule.update_tick(self.dt)

        pygame.quit()