import pygame
import pyscroll
import pytmx
import os
import time
from player import Player
from pygame.locals import *
from dash_images import Dash_images
from particule import Particule

directory = os.path.dirname(os.path.realpath(__file__))
os.chdir = directory


class Game:
    def __init__(self):
        
        # créer la fenetre du jeu
        flags = FULLSCREEN | DOUBLEBUF | NOFRAME | SCALED
        self.screen = pygame.display.set_mode((900,700))
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        pygame.display.set_caption(f"Looki's aventure")
        
        # chargement map
        self.tmx_data = pytmx.util_pygame.load_pygame(f"{directory}\\assets\\maps\\Test_map2.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 1.5
        
        # initialization joueur
        player_position = self.tmx_data.get_object_by_name("spawn_player") 
        self.player = Player(player_position.x, player_position.y, directory)
        
        # creation groupe de sprite 
        self.group = pyscroll.PyscrollGroup(map_layer = self.map_layer, default_layer = 7)
        self.group.add(self.player)
        
        # particule lors de mouvement du joueur
        self.particule = Particule(directory)
        self.direction_joueur = ""
        self.action_joueur = ""
        
        # chaque element de walls / etc est sous la forme : [x, y, rect]
        self.walls = []
        self.grounds = []
        self.ceillings = []
        self.plateformes = []
        self.centre_camera = {}
        self.zone_camera = []
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                if obj.name == "wall":
                    self.walls.append((obj.x,obj.y,[pygame.Rect(obj.x, obj.y, obj.width, obj.height)]))
                elif obj.name == "ground":
                    self.grounds.append((obj.x,obj.y,[pygame.Rect(obj.x, obj.y, obj.width, obj.height)]))
                elif obj.name == "ceilling":
                    self.ceillings.append((obj.x,obj.y,[pygame.Rect(obj.x, obj.y, obj.width, obj.height)]))
                elif obj.name == 'plateforme':
                    self.plateformes.append((obj.x,obj.y,[pygame.Rect(obj.x, obj.y, obj.width, obj.height)]))
            elif obj.type == "centre_camera":
                self.centre_camera[obj.name] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)       
            elif obj.type == "zone_camera":
                self.zone_camera.append((obj.name, [pygame.Rect(obj.x, obj.y, obj.width, obj.height)]))
        
        # variable pour le changement de camera        
        self.current_centre = "top"
        self.cooldown_changement_centre = 0.5
        self.current_rect_center = self.centre_camera["top"]
        self.timer_cooldown_changement_centre = 0 
       
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
       
    def stop_if_collide(self, direction):
        """fait en sorte que le joueur avance plus lorsque qu'il vance dans un mur"""
        for sprite in self.group.sprites():
            if sprite.id == 'player':
                # si le joueur est en collision avec un mur
                for wall in self.walls:
                    if sprite.body.collidelist(wall[2]) > -1:
                        # si le joueur va a droite en etant a gauche du mur
                        # limage est plus grande que la partie visible du joueur, d'où self.player.image.get_width()/2
                        if direction == 'right' and wall[0] > self.player.position[0] + self.player.image.get_width()/2:
                            sprite.move_back()   
                            return True
                        # si le joueur va a gauche en etant a droite du mur
                        if direction == 'left' and wall[0] < self.player.position[0] + self.player.image.get_width()/2:
                            sprite.move_back()  
                            return True
       
    def handle_input(self):
        """agit en fonction des touches appuye par le joueur"""
        pressed = pygame.key.get_pressed()
        
        # dash
        if self.joueur_sur_sol() == False and self.player.is_jumping == False and self.player.is_dashing == False and self.player.a_dash == False and pressed[pygame.K_q]:
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
        
        # aller a gauche
        elif pressed[pygame.K_LEFT]:
            self.player.save_location()
            if self.joueur_sur_sol():
                self.player.move_left(pieds_sur_sol=True)
            # si le joueur ne dash pas et est en lair
            elif not self.player.is_dashing:
                self.player.move_left()
            self.stop_if_collide("left")
            
        # aller a droite    
        elif pressed[pygame.K_RIGHT]:
            self.player.save_location()
            if self.joueur_sur_sol():
                self.player.move_right(pieds_sur_sol=True)
            # si le joueur ne dash pas et est en lair
            elif not self.player.is_dashing:
                self.player.move_right()
            self.stop_if_collide("right")
        else:
            # si le joueur avance pas, il deviens idle
            if self.player.action != "fall" and self.player.action != "up_to_fall":
                if self.player.action == "run" and self.player.ralentit_bool == False:
                    self.player.debut_ralentissement()
                # si self.player.ralentissement na pas ete appele, self.player.ralentissement aura aucun effet
                # => donc le ralentissement a lieu que quand le joueur arrete de courir
                self.player.ralentissement()
            
        if pressed[pygame.K_DOWN]:
            # le joueur passe a travers les plateformes pendant X secondes
            self.player.t1_passage_a_travers_plateforme = time.time()
        elif pressed[pygame.K_UP]:
            # saut
            if (self.joueur_sur_sol() or time.time() - self.player.timer_cooldown_able_to_jump < self.player.cooldown_able_to_jump) and self.player.a_sauter == False and time.time() - self.player.timer_cooldown_next_jump > self.player.cooldown_next_jump:
                self.player.debut_saut()
    
    def changement_centre(self, zone_cam):
        
        if zone_cam != self.current_centre:
            self.current_centre = zone_cam
            self.current_rect_center = self.centre_camera[zone_cam]
            self.timer_cooldown_changement_centre = time.time()            
    
    def update(self):
        """ fonction qui update les informations du jeu"""
        
        for sprite in self.group.sprites():
            if sprite.id == 'player':
                # si le joueur est en collision avec un mur
                for zone_cam in self.zone_camera:
                    if sprite.body.collidelist(zone_cam[1]) > -1:
                        if time.time() - self.timer_cooldown_changement_centre > self.cooldown_changement_centre:
                            self.changement_centre(zone_cam[0])
            elif sprite.id == "image_dash":
                if time.time() - sprite.t1 > sprite.cooldown:
                    self.group.remove(sprite)
        
        if self.joueur_se_cogne() and self.player.is_jumping:
            self.player.fin_saut()
        
        if self.joueur_se_cogne() and self.player.is_dashing:
            self.player.fin_dash()
            
        if self.joueur_sur_sol() and self.player.is_dashing:
            self.player.fin_dash()
            
        self.player.save_location()    
            
        if self.stop_if_collide(self.player.dash_direction_x) and self.player.is_dashing:
            self.player.fin_dash()
        
        if (self.player.is_jumping or self.player.is_dashing) and self.player.is_falling:
            self.player.fin_chute(jump_or_dash = True) 
        
        # si le joueur n'est pas sur un sol on commence la chute
        if not self.joueur_sur_sol():
            if not self.player.is_falling and not self.player.is_jumping and not self.player.is_dashing:
                self.player.debut_chute()
        else:
            # sinon on stop la chute si il y en a une
            if self.player.is_falling:
                self.player.fin_chute() 
        
        if self.player.is_jumping == False and self.player.action == 'jump' and self.joueur_sur_sol():
            self.player.change_direction("idle", self.player.direction)        
        
        self.player.chute()
        self.player.saut()
        self.player.dash()
        
        if self.player.images_dash != []:
            im = Dash_images(self.player.images_dash[0][0], self.player.images_dash[0][1], self.player.images_dash[0][2], self.player.images_dash[0][3])
            self.group.add(im)
            del self.player.images_dash[:]
        
        # particle
        temp_action = self.player.action
        if temp_action == "jump" and self.player.is_dashing:
            temp_action = 'dash'
        if self.action_joueur != temp_action:
            self.action_joueur = temp_action
            self.particule.action_joueur = temp_action
            
        if self.direction_joueur != self.player.direction:
            self.direction_joueur = self.player.direction
            self.particule.direction_joueur = self.player.direction
        
        self.group.update() 
        
        y = self.player.body.y + self.player.body.h
        y_debut_jump = self.player.coord_debut_jump[1]+ self.player.body.h
        debut_dash_y = self.player.coord_debut_dash[1]+ self.player.body.h
        dir_dash_x = self.player.dash_direction_x
        dir_dash_y = self.player.dash_direction_y
        if self.player.direction == "right":
            x = self.player.body.x - 20
            x_debut_jump = self.player.coord_debut_jump[0] + self.player.body.w - 15
            debut_dash_x = self.player.coord_debut_dash[0] + self.player.body.w + 10
            self.particule.update(x, y,x_debut_jump, y_debut_jump, dir_dash_x, dir_dash_y, debut_dash_x, debut_dash_y)
        elif self.player.direction == "left":
            x = self.player.body.x + self.player.body.w + 20
            x_debut_jump = self.player.coord_debut_jump[0] + self.player.body.w + 56
            debut_dash_x = self.player.coord_debut_dash[0] + self.player.body.w + 26
            self.particule.update(x, y,x_debut_jump, y_debut_jump, dir_dash_x, dir_dash_y, debut_dash_x, debut_dash_y)
            
        if self.particule.new_particle != []:
            for i in self.particule.new_particle:
                self.group.add(i)
            self.particule.new_particle.clear()
        
        if self.particule.remove_particle != []:
            for id in self.particule.remove_particle:
                for sprite in self.group.sprites():
                    if sprite.id == f"particule{id}":
                        self.group.remove(sprite)
            self.particule.remove_particle.clear()
                 
        
    def run(self):
        """boucle du jeu"""

        clock = pygame.time.Clock()

        self.running = True
        
        while self.running:

            # appelle de la methode gerant les inputs
            self.handle_input()
            
            self.update()
            # dessin des sprites
            #self.group.center(self.current_rect_center)
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            
            #pygame.display.update(self.player.rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            clock.tick(60)

        pygame.quit()