import pygame
import time
import random
from pygame.locals import *
import math

class ParticuleDash(pygame.sprite.Sprite):
    """ class d'une particle qui apparait lors du dash du joueur"""
    def __init__(self, x, y, nbr, directory, dir_dash_x, dir_dash_y, zoom, speed_dt):
        super().__init__()
        self.id = f"particule{nbr}"
        
        taille = random.randint(1,5)
        
        self.zoom = zoom
        self.speed_dt = speed_dt

        self.image = pygame.image.load(f'{directory}\\assets\\particle.png')
        self.image = pygame.transform.scale(self.image, (taille*self.zoom, taille*self.zoom))

        self.position = [x,y-self.image.get_height()]
        self.rect = self.image.get_rect()
        
        # la particle disparait apres le cooldown
        self.t1 = time.time()
        self.cooldown = random.uniform(0.2, 0.8)
        
        # calcul de l'angle en radian en fonction de la direction du joueur, cf cercle trigo
        if dir_dash_y == "up" and dir_dash_x == "right":
            self.alpha = random.uniform(3*math.pi/4, 7*math.pi/4)
        elif dir_dash_y == "down" and dir_dash_x == "right":
            self.alpha = random.uniform(math.pi/4, 5*math.pi/4)
        elif dir_dash_y == "up" and dir_dash_x == "left":
            self.alpha = random.uniform((-3)*math.pi/4, math.pi/4)
        elif dir_dash_y == "down"and dir_dash_x == "left":
            self.alpha = random.uniform((-1)*math.pi/4, 3*math.pi/4)
        elif dir_dash_x == "left" and dir_dash_y == "":
            self.alpha = random.uniform(-math.pi/2, math.pi/2)
        elif dir_dash_x == "right" and dir_dash_y == "":
            self.alpha = random.uniform(math.pi/2, 3*math.pi/2)
        elif dir_dash_x == "" and dir_dash_y == "up":
            self.alpha = random.uniform((-1)*math.pi, 0)
        elif dir_dash_x == "" and dir_dash_y == "down":
            self.alpha = random.uniform(0, math.pi)

        self.speedx = math.cos(self.alpha)*self.zoom*self.speed_dt
        self.speedy = math.sin(self.alpha)*self.zoom*self.speed_dt
            
    def update(self):
        self.position[0] += self.speedx
        self.position[1] -= self.speedy
        self.rect.topleft = self.position

class ParticuleBaseMouvement(pygame.sprite.Sprite):
    """ class d'une particle qui apparait lors d'un saut ou d'une course du joueur'"""
    def __init__(self, x, y, direction_x, direction_y, nbr, directory, zoom, speed_dt, id = ""):
        super().__init__()
        self.id = f"particule{nbr}"
        self.zoom = zoom
        self.speed_dt = speed_dt
        
        taille = random.randint(1,5)

        self.image = pygame.image.load(f'{directory}\\assets\\particle.png')
        self.image = pygame.transform.scale(self.image, (taille*self.zoom, taille*self.zoom))

        self.direction_x = direction_x
        self.direction_y = direction_y
        self.position = [x,y-self.image.get_height()]
        self.rect = self.image.get_rect()
        self.t1 = time.time()
        # temps d'apparition
        self.cooldown = random.uniform(0.2, 0.8)
        
        if id == "":
            self.alpha = random.uniform(0, math.pi/4)
        elif id == "wall_slide":
            self.alpha = random.uniform(math.pi/4, math.pi/2)
        elif id == "jump_edge":
            self.alpha = random.uniform(math.pi/2, math.pi)
            
        self.speedx = math.cos(self.alpha)*self.zoom*self.speed_dt
        self.speedy = math.sin(self.alpha)*self.zoom*self.speed_dt
        
        if self.direction_x == "right":
            self.speedx = - self.speedx    
        if self.direction_y == "down":
            self.speedy = - self.speedy 
          
    def update(self):
        self.position[0] += self.speedx
        self.position[1] -= self.speedy
        self.rect.topleft = self.position
        
class Particule:
    """ class gerant les differentes particules"""
    def __init__(self, directory, height, width, zoom):
        self.zoom = zoom
        self.dt = 17
        self.speed_dt = round(self.dt/17)
        self.height_joueur = height
        self.width_joueur = width
        self.directory = directory
        self.direction_joueur = ""
        self.action_joueur = ""
        self.number_particule = 0
        self.x_debut_jump = 0
        self.y_debut_jump = 0
        self.x_debut_jump_edge = 0
        self.y_debut_jump_edge = 0
        self.debut_dash_x = 0
        self.debut_dash_y = 0
        self.dir_dash_x = ""
        self.dir_dash_y = ""
        self.pieds_collide_jump_edge = False
        # key : id | value : object of class ParticuleBaseMouvement or ParticuleDash
        self.current_particle_run = {}
        self.current_particle_jump = {}
        self.current_particle_dash = {}
        self.current_particle_wall_slide = {}
        self.current_particle_jump_edge = {}
        self.current_particle_ground_slide = {}
        self.all_dict = [self.current_particle_run, self.current_particle_jump, self.current_particle_dash, self.current_particle_wall_slide, self.current_particle_jump_edge, self.current_particle_ground_slide]
        # value : object of class ParticuleBaseMouvement or ParticuleDash
        self.new_particle = []
        # value : id of the particle
        self.remove_particle = []
    
    def update_tick(self, dt):
        self.dt = dt
        self.speed_dt = round(self.dt/17)
    
    def spawn_particle(self, action):
        """rajoute une particle dans new_particle et dans le dictionnaire correspondant au mouvement, en fonction du mouvement du joueur"""
        # pour eviter des chiffres trop grands qui prendrait trop de memoire
        if self.number_particule > 300:
            self.number_particule = 0
            
        if action == "run":
            self.number_particule += 1
            p = ParticuleBaseMouvement(self.x, self.y, self.direction_joueur,"", self.number_particule, self.directory, self.zoom, self.speed_dt)
            self.current_particle_run[str(self.number_particule)] = p
            self.new_particle.append(p)
            
        elif action == "jump":
            # reajustement de la position des particles
            if self.direction_joueur == "right":
                c = 27*self.zoom
            elif self.direction_joueur == "left":
                c = -27*self.zoom
            # apparition de deux particles, une a gauche et une a droite
            self.number_particule += 1
            p = ParticuleBaseMouvement(self.x_debut_jump+c, self.y_debut_jump+18*self.zoom, "right", "",self.number_particule, self.directory, self.zoom, self.speed_dt)
            self.current_particle_jump[str(self.number_particule)] = p
            self.new_particle.append(p)
            self.number_particule += 1
            p = ParticuleBaseMouvement(self.x_debut_jump+c, self.y_debut_jump+18*self.zoom, "left", "",self.number_particule, self.directory, self.zoom, self.speed_dt)
            self.current_particle_jump[str(self.number_particule)] = p
            self.new_particle.append(p)
            
        elif action == "dash":
            for _ in range(4):
                self.number_particule += 1
                p = ParticuleDash(self.debut_dash_x, self.debut_dash_y, self.number_particule, self.directory, self.dir_dash_x, self.dir_dash_y, self.zoom, self.speed_dt)
                self.current_particle_dash[str(self.number_particule)] = p
                self.new_particle.append(p)
        
        elif action == "Wall_slide":
            self.number_particule += 1
            if self.direction_joueur == "right":
                p = ParticuleBaseMouvement(self.x + self.width_joueur - 7*self.zoom, self.y - self.height_joueur,self.direction_joueur, "",self.number_particule, self.directory, self.zoom, self.speed_dt, id = "wall_slide")
            elif self.direction_joueur == "left":
                p = ParticuleBaseMouvement(self.x - self.width_joueur + 12*self.zoom, self.y - self.height_joueur, self.direction_joueur, "",self.number_particule, self.directory, self.zoom, self.speed_dt, id = "wall_slide")
            self.current_particle_run[str(self.number_particule)] = p
            self.new_particle.append(p)
        
        elif action == 'jump_edge':
            # reajustement de la position des particles
            # apparition de deux particles, une a gauche et une a droite
            self.number_particule += 1
            p = ParticuleBaseMouvement(self.x_debut_jump_edge, self.y_debut_jump_edge, self.direction_joueur, "up", self.number_particule, self.directory, self.zoom, self.speed_dt, id ="jump_edge")
            self.current_particle_jump_edge[str(self.number_particule)] = p
            self.new_particle.append(p)
            self.number_particule += 1
            p = ParticuleBaseMouvement(self.x_debut_jump_edge, self.y_debut_jump_edge, self.direction_joueur, "down", self.number_particule, self.directory, self.zoom, self.speed_dt, id ="jump_edge")
            self.current_particle_jump_edge[str(self.number_particule)] = p
            self.new_particle.append(p)
        
        elif action == 'ground_slide':
            self.number_particule += 1
            p = ParticuleBaseMouvement(self.x, self.y, self.direction_joueur,"", self.number_particule, self.directory, self.zoom, self.speed_dt)
            self.current_particle_ground_slide[str(self.number_particule)] = p
            self.new_particle.append(p)
            
        
    def update(self, x, y):
        """methode appeler a chaque tick"""
        # when the seconds between now and the apparition of the particle > its cooldown of lifetime : 
        # the particle is add in self.remove_particle and remove from the dictionnarry of the mouvement
        id_a_sup = []
        for dico in self.all_dict:
            for id,p in dico.items():
                if time.time() - p.t1 > p.cooldown:
                    self.remove_particle.append(id)
                    id_a_sup.append(int(id))
            for i in id_a_sup:
                del dico[str(i)]
            id_a_sup.clear()

        self.x = x
        self.y = y
        if self.action_joueur == "run" and len(self.current_particle_run) < 20:
            self.spawn_particle("run")
        elif self.action_joueur == "jump" and len(self.current_particle_jump) < 30:
            self.spawn_particle("jump")
        elif self.action_joueur == "dash" and len(self.current_particle_dash) < 15:
            self.spawn_particle("dash")
        elif self.action_joueur == "Wall_slide" and len(self.current_particle_wall_slide) < 20:
            self.spawn_particle("Wall_slide")
        elif self.action_joueur == "jump_edge" and len(self.current_particle_jump_edge) < 20 and self.pieds_collide_jump_edge:
            self.spawn_particle("jump_edge")
        elif self.action_joueur == "ground_slide" and len(self.current_particle_ground_slide) < 20:
            self.spawn_particle("ground_slide")