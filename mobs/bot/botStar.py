from math import sqrt
from mobs.mob_functions import *
import random

class Bot:
    def update_timers(dt):
        pass

    def __init__(self, mob, target):
        self.target=target
        self.mob=mob
        
        # each first element in any tuple eather correspond to a probability (random.randint(1, X), where X is the 1 element in the tuple))
        # or a choice, like in 'type_attack', 0 correspond to normal focus, 1 to a behind attack only and 2 to forward attack only
        # and the 2nd element is the weight in the random choice that will follow
        # the 2nd element of the list is the last choice
        
        self.behind_start=15
        self.behind_end=125
        self.current_behind=random.randint(self.behind_start, self.behind_end)

        if self._get_distance_target_x()<0: 
            self.direction = "right"
        else : 
            self.direction = "left"
        
        # variables used when the mob is forced to jump when it collide specials rect in the map
        self.timers={
            "change_dir_collision_wall": 0,
        }
        
        self.cooldowns={
            "change_dir_collision_wall": 0.5,
            }
        
        #jump
        self.random_coefficient={
            "jump":
                {
                    "normal": 100,
                    "top": 50,
                    "bottom": 150
                },
            "attack":
                {
                    "normal": 25,
                    "anticipation": 35,
                }
        }

    def update_timers(self, dt):
        for key in self.timers.keys():
            self.timers[key]+=dt

    def _get_distance_target_x(self):
        return self.mob.body.x + self.mob.body.w/2 - (self.target.body.x+self.target.body.w/2)

    def _get_distance_target_y(self):
        return self.mob.body.y + self.mob.body.h/2 - (self.target.body.y+self.target.body.h/2)
    
    def get_distance_target(self):
        """pythagore"""
        return sqrt(self._get_distance_target_x()**2 + self._get_distance_target_y()**2)
    
    def _invert_dir(self, dir):
        if dir == "right":
            return "left"
        else:
            return "right"
        
    def need_to_jump(self, tile_width, dist_y, dist_x):
        if (dist_x < 0 and self.direction == "right") or (dist_x > 0 and self.direction == "left"):
            if (dist_y > tile_width*3):
                return random.randint(1, self.random_coefficient["jump"]["top"]) == 1
            elif (dist_y < -tile_width*3):
                return random.randint(1, self.random_coefficient["jump"]["bottom"]) == 1
            else:
                return random.randint(1, self.random_coefficient["jump"]["normal"]) == 1
    
    def make_mouvement(self, collision, zoom, distance, tile_width):
        if self.get_distance_target() < distance*zoom and not self.mob.is_attacking:
            right = left = down = up = attack = False
            
            # initialisation of all variables that will be use multiple times to optimisation purpose (not calling the functions multiple times)
            sol=collision.joueur_sur_sol(self.mob)
            y=self._get_distance_target_y()
            x=self._get_distance_target_x()

            change_dir_falling=False
            if sol :
                temp=self.mob.position[0]
                if self.direction == "right":
                    self.mob.position[0] += self.mob.speed * 3 * zoom
                elif self.direction == "left":
                    self.mob.position[0] -= self.mob.speed * 3 * zoom
                self.mob.update_rect()
                if not collision.joueur_sur_sol(self.mob, change_pos=False):
                    change_dir_falling=True
                self.mob.position[0]=temp
                self.mob.update_rect()

            if change_dir_falling and y>-tile_width*2.5 and not ((x < 0 and self.direction == "right") or (x > 0 and self.direction == "left")):
                self.direction = self._invert_dir(self.direction)
                self.current_behind=random.randint(self.behind_start, self.behind_end)
                self.timers["change_dir_collision_wall"]=time.time()
            elif collision.stop_if_collide(self.direction, self.mob, dontmove=True) and time.time() - self.timers["change_dir_collision_wall"] > self.cooldowns["change_dir_collision_wall"]:
                self.direction = self._invert_dir(self.direction)
                self.current_behind=random.randint(self.behind_start, self.behind_end)
                self.timers["change_dir_collision_wall"]=time.time()
            elif time.time() - self.timers["change_dir_collision_wall"] > self.cooldowns["change_dir_collision_wall"] :
                if abs(x) > self.current_behind*zoom:
                    if x < 0:
                        self.direction = "right"
                    else:
                        self.direction = "left"
                    self.current_behind=random.randint(self.behind_start, self.behind_end)
                self.timers["change_dir_collision_wall"]=time.time()
            elif change_dir_falling and ((x < 0 and self.direction == "right") or (x > 0 and self.direction == "left")):
                up=True

            if self.direction == "right":
                right = True
            elif self.direction == "left":
                left = True

            if self.need_to_jump(tile_width, y, x):
                up = True

            if time.time() - self.mob.timers["timer_attack"] > self.mob.cooldown_attack and ((sol and abs(x) < self.mob.range_attack and random.randint(1, self.random_coefficient["attack"]["normal"]) == 1) \
                or (self.mob.range_attack < abs(x) < self.mob.range_attack*3 and ((x<0 and self.target.direction=="left") or (x>0 and self.target.direction=="right")) and random.randint(1, self.random_coefficient["attack"]["anticipation"]) == 1)):
                attack=True

            if right:
                pressed_right([self.mob], collision)
            elif left:
                pressed_left([self.mob], collision)
        
            if up:
                pressed_up([self.mob], down, left, right, [False], collision, zoom)

            if attack:
                pressed_attack([self.mob])