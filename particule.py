import pygame
import time
import random
from pygame.locals import *
import math

class ParticuleDash(pygame.sprite.Sprite):
    """ class affichant une image du joueur quand il dash pour une courte duree"""
    def __init__(self, x, y,nbr, directory, dir_x, dir_y):
        super().__init__()
        self.id = f"particule{nbr}"
        
        taille = random.randint(1,5)

        self.image = pygame.image.load(f'{directory}\\assets\\particle.png')
        self.image = pygame.transform.scale(self.image, (taille, taille))

        self.dir_x = dir_x
        self.dir_y = dir_y
        self.position = [x,y-self.image.get_height()]
        self.rect = self.image.get_rect()
        self.t1 = time.time()
        # temps d'apparition
        self.cooldown = random.uniform(0.2, 0.8)
        
        if self.dir_y == "up" and self.dir_x == "right":
            self.alpha = random.uniform(3*math.pi/4, 7*math.pi/4)
        elif self.dir_y == "down" and self.dir_x == "right":
            self.alpha = random.uniform(math.pi/4, 5*math.pi/4)
        elif self.dir_y == "up" and self.dir_x == "left":
            self.alpha = random.uniform((-3)*math.pi/4, math.pi/4)
        elif self.dir_y == "down"and self.dir_x == "left":
            self.alpha = random.uniform((-1)*math.pi/4, 3*math.pi/4)
        elif self.dir_x == "left" and self.dir_y == "":
            self.alpha = random.uniform(math.pi/2, 3*math.pi/2)
        elif self.dir_x == "right" and self.dir_y == "":
            self.alpha = random.uniform((-1)*math.pi/2, math.pi/2)
        elif self.dir_x == "" and self.dir_y == "up":
            self.alpha = random.uniform((-1)*math.pi, 0)
        elif self.dir_x == "" and self.dir_y == "down":
            self.alpha = random.uniform(0, math.pi)
            
        if (self.dir_x == "right" and self.dir_y == "") or (self.dir_x == "left" and self.dir_y == ""):
            self.speedx = (-1) * math.cos(self.alpha)
            self.speedy = (-1) * math.sin(self.alpha)
        else:
            self.speedx = math.cos(self.alpha)
            self.speedy = math.sin(self.alpha)
        
        # if self.direction == "right":
        #     self.speedx = -1 * abs(self.speedx)   
        # elif self.direction == "left":
        #     self.speedx = abs(self.speedx)    
          
    def update(self):
        self.position[0] += self.speedx
        self.position[1] -= self.speedy
        self.rect.topleft = self.position

class ParticuleBaseMouvement(pygame.sprite.Sprite):
    """ class affichant une image du joueur quand il dash pour une courte duree"""
    def __init__(self, x, y, direction, nbr, directory):
        super().__init__()
        self.id = f"particule{nbr}"
        
        taille = random.randint(1,5)

        self.image = pygame.image.load(f'{directory}\\assets\\particle.png')
        self.image = pygame.transform.scale(self.image, (taille, taille))

        self.direction = direction
        self.position = [x,y-self.image.get_height()]
        self.rect = self.image.get_rect()
        self.t1 = time.time()
        # temps d'apparition
        self.cooldown = random.uniform(0.2, 0.8)
        
        self.alpha = random.uniform(0, math.pi/4)
        
        self.speedx = math.cos(self.alpha)
        self.speedy = math.sin(self.alpha)
        
        if self.direction == "right":
            self.speedx = -self.speedx    
          
    def update(self):
        self.position[0] += self.speedx
        self.position[1] -= self.speedy
        self.rect.topleft = self.position
        
class Particule:
    """ class affichant une image du joueur quand il dash pour une courte duree"""
    def __init__(self, directory):
        self.directory = directory
        self.direction_joueur = ""
        self.action_joueur = ""
        self.number_particule = 0
        self.x_debut_jump = 0
        self.y_debut_jump = 0
        self.dir_dash_x = ""
        self.dir_dash_y = ""
        
        self.current_particle_run = {}
        self.current_particle_jump = {}
        self.current_particle_dash = {}
        self.new_particle = []
        self.remove_particle = []
    
    def spawn_particle(self, action):
        if self.number_particule > 300:
            self.number_particule = 0
        if action == "run":
            self.number_particule += 1
            p = ParticuleBaseMouvement(self.x, self.y, self.direction_joueur, self.number_particule, self.directory)
            self.current_particle_run[str(self.number_particule)] = p
            self.new_particle.append(p)
        elif action == "jump":
            self.number_particule += 1
            if self.direction_joueur == "right":
                c = 27
            elif self.direction_joueur == "left":
                c = -27
            p = ParticuleBaseMouvement(self.x_debut_jump+c, self.y_debut_jump, "right", self.number_particule, self.directory)
            p2 = ParticuleBaseMouvement(self.x_debut_jump+c, self.y_debut_jump, "left", self.number_particule, self.directory)
            self.current_particle_jump[str(self.number_particule)] = p
            self.new_particle.append(p)
            self.number_particule += 1
            self.current_particle_jump[str(self.number_particule)] = p2
            self.new_particle.append(p2)
        elif action == "dash":
            self.number_particule += 1
            p = ParticuleDash(self.debut_dash_x, self.debut_dash_y, self.number_particule, self.directory, self.dir_dash_x, self.dir_dash_y)
            p2 = ParticuleDash(self.debut_dash_x, self.debut_dash_y, self.number_particule, self.directory, self.dir_dash_x, self.dir_dash_y)
            self.current_particle_dash[str(self.number_particule)] = p
            self.new_particle.append(p)
            self.number_particule += 1
            self.current_particle_dash[str(self.number_particule)] = p2
            self.new_particle.append(p2)
        
    def update(self, x, y, x_debut_jump, y_debut_jump, dir_dash_x, dir_dash_y, debut_dash_x, debut_dash_y):
        id_a_sup = []
        for id,p in self.current_particle_run.items():
            if time.time() - p.t1 > p.cooldown:
                self.remove_particle.append(id)
                id_a_sup.append(int(id))
        for i in id_a_sup:
            del self.current_particle_run[str(i)]
        id_a_sup.clear()
        for id,p in self.current_particle_jump.items():
            if time.time() - p.t1 > p.cooldown:
                self.remove_particle.append(id)
                id_a_sup.append(int(id))
        for i in id_a_sup:
            del self.current_particle_jump[str(i)]
        id_a_sup.clear()
        for id,p in self.current_particle_dash.items():
            if time.time() - p.t1 > p.cooldown:
                self.remove_particle.append(id)
                id_a_sup.append(int(id))
        for i in id_a_sup:
            del self.current_particle_dash[str(i)]
        id_a_sup.clear()

        self.debut_dash_x = debut_dash_x
        self.debut_dash_y = debut_dash_y
        self.x_debut_jump = x_debut_jump
        self.y_debut_jump = y_debut_jump
        self.x = x
        self.y = y
        self.dir_dash_x = dir_dash_x
        self.dir_dash_y = dir_dash_y
        if self.action_joueur == "run" and len(self.current_particle_run) < 20:
            self.spawn_particle("run")
        elif self.action_joueur == "jump" and len(self.current_particle_jump) < 30:
            self.spawn_particle("jump")
        elif self.action_joueur == "dash" and len(self.current_particle_dash) < 15:
            self.spawn_particle("dash")
        