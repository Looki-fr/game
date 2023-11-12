from math import sqrt
from mobs.mob_functions import *
import random

class Bot:
    def update_timers(dt):
        pass

    def __init__(self, mob, target, handle_input_ralentissement):
        self.handle_input_ralentissement = handle_input_ralentissement
        self.target=target
        self.mob=mob
        
        # each first element in any tuple eather correspond to a probability (random.randint(1, X), where X is the 1 element in the tuple))
        # or a choice, like in 'type_attack', 0 correspond to normal focus, 1 to a behind attack only and 2 to forward attack only
        # and the 2nd element is the weight in the random choice that will follow
        # the 2nd element of the list is the last choice
        self.random_coefficient={
            "jump_run":[[(85, 1), (90, 2), (105, 5),(120, 5),(135, 2),(150, 1)], 0],
            "attack_air": [[(3, 1), (4, 2), (5, 5),(6, 5),(7, 2),(8, 1)], 0],
            "type_attack": [[(0, 1), (1, 1), (2, 1)], 0],
            "anticipation": [[(15, 1), (20, 2), (25, 5),(30, 5),(35, 2),(40, 1)], 0],
            "jump_platform":[[(15,1), (40,3), (55,1)], 0]
        }
        for value in self.random_coefficient.values():
            value[1] = self.mob._random_choice(value[0])
            
        if self._get_distance_target_x()<0: 
            self.direction_behind = "right"
            self.direction_forward = "left"
        else : 
            self.direction_behind = "left"
            self.direction_forward = "right"
        
        # variables used when the mob is forced to jump when it collide specials rect in the map
        self.is_jumping_platform=False
        self.timer_jump_platform=0
        self.cooldown_jump_platform=0.2
        
        self.timer_changed_direction_behind=0
        self.cooldown_changed_direction_behind=0.5
        
        self.timer_changed_direction_forward=0
        self.cooldown_changed_direction_forward=0.5
    
    def _reset_coeff(self, key):
        """choose an element from self.random_coefficient using the weights"""
        self.random_coefficient[key][1]=self.mob._random_choice(self.random_coefficient[key][0])
        if key == "type_attack":
            if self._get_distance_target_x()<0: 
                self.direction_behind = "right"
            elif self._get_distance_target_x()>0: 
                self.direction_behind = "left"
    
    def _get_distance_target_x(self, abs_bool=False):
        """when x>0 : the mob is on the right of the target and
           when x<0 : the mob is on the left of the target"""
        if abs_bool: return abs(self.target.position[0] + self.target.image.get_width()/2 - self.mob.position[0] - self.mob.image.get_width()/2)/self.mob.zoom
        else: return (self.mob.position[0] - self.target.position[0])/self.mob.zoom
    
    def _get_distance_target_y(self, abs_bool=False):
        if abs_bool: return abs(self.mob.position[1] + self.mob.image.get_height() - self.mob.increment_foot*2 - (self.target.position[1]+self.target.image.get_height()-self.target.increment_foot*2))/self.mob.zoom
        else: return  (self.mob.position[1] + self.mob.image.get_height() - self.mob.increment_foot*2 - (self.target.position[1]+self.target.image.get_height()-self.target.increment_foot*2))/self.mob.zoom
    
    def get_distance_target(self):
        """pythagore"""
        return sqrt(self._get_distance_target_x()**2 + self._get_distance_target_y()**2)/self.mob.zoom
    
    def _is_behind(self):
        """a mob is concidered behind if he is far enough from the target and if he is in his back"""
        if self.target.direction=="right":
            return self._get_distance_target_x() < -self.mob.range_attack +60 
        elif self.target.direction=="left":
            return self._get_distance_target_x() > +self.mob.range_attack -60
    
    def _is_forward(self):
        """a mob is concidered behind if he is far enough from the target and if he is in his front"""
        if self.target.direction=="left":
            return self._get_distance_target_x() < -self.mob.range_attack +60 
        elif self.target.direction=="right":
            return self._get_distance_target_x() > +self.mob.range_attack -60
    
    def _invert_dir(self, dir):
        if dir == "right":
            return "left"
        else:
            return "right"
    
    def make_mouvement(self, collision):
        if self.get_distance_target() < 500:
            right = left = down = up = False
            
            # initialisation of all variables that will be use multiple times to optimisation purpose (not calling the functions multiple times)
            cplj=collision.collide_platform_bot(self.mob, "left")
            cprj=collision.collide_platform_bot(self.mob, "right")
            cpl=collision.collide_platform_bot(self.mob, "left", add="go_")
            cpr=collision.collide_platform_bot(self.mob, "right", add="go_")
            sol=collision.joueur_sur_sol(self.mob)
            behind=self._is_behind()
            forward=self._is_forward()
            y=self._get_distance_target_y()
            x=self._get_distance_target_x()
            
            # reset self.is_jumping_platform if the jump is ended
            if sol and not self.mob.is_jumping and self.is_jumping_platform!=False:
                self.is_jumping_platform=False
                self.timer_jump_platform=time.time()
            
            # we dont want every mob to jump at the same time so we add randomness
            rand=(y>0 and random.randint(1,5)==1) or (y == 0 and random.randint(1, self.random_coefficient["jump_platform"][1])==1)
            
            if sol and not self.mob.is_jumping and cprj and rand and self.is_jumping_platform == False and time.time()-self.timer_jump_platform>self.cooldown_jump_platform:
                self.is_jumping_platform="right"
                pressed_up([self.mob], down, left, True, [False], collision)
                self._reset_coeff("jump_platform")
            
            if sol and not self.mob.is_jumping and cplj and rand and self.is_jumping_platform == False and time.time()-self.timer_jump_platform>self.cooldown_jump_platform:
                self.is_jumping_platform="left"
                pressed_up([self.mob], down, True, right, [False], collision)
                self._reset_coeff("jump_platform")
            
            # we force the mob to move right or left if he collide a special rect in the map
            if cpl and y > 200 and not cprj and not cplj:
                pressed_left([self.mob], collision)
                left=True
            
            elif cpr and y > 200 and not cprj and not cplj:
                pressed_right([self.mob], collision)
                left=True
            
            # inversed the direction of the behind attack when we need (take a paper and do a sketch)
            if time.time() - self.timer_changed_direction_behind > self.cooldown_changed_direction_behind and \
                self.random_coefficient["type_attack"][1]==1 and (((self.direction_behind=="right" and self.target.direction=="right" and x >0) or \
                (self.direction_behind=="left" and self.target.direction=="left" and x<-0)) or (behind and self.direction_behind!=self.target.direction)):
                self.timer_changed_direction_behind=time.time()
                self.direction_behind=self._invert_dir(self.direction_behind)
            
            # inversed the direction of the forward attack when we need (take a paper and do a sketch)    
            if time.time() - self.timer_changed_direction_forward > self.cooldown_changed_direction_forward and \
                self.random_coefficient["type_attack"][1]==2 and (((self.direction_forward=="right" and self.target.direction=="left" and x >0) or \
                    (self.direction_forward=="left" and self.target.direction=="right" and x<0)) or (forward and self.direction_forward==self.target.direction)):
                self.timer_changed_direction_forward=time.time()
                self.direction_forward=self._invert_dir(self.direction_forward)
            
            # sometimes the mob will attack you even if you are not in range because we want it to anticipate
            if random.randint(1,self.random_coefficient["anticipation"][1])==1 and ((self.target.direction=="right" and 0 < x < (self.mob.range_attack)*2) or (self.target.direction=="left" and 0 > x > (-self.mob.range_attack)*2)) and self._get_distance_target_y(abs_bool=True)<100:
                self._reset_coeff("anticipation")
                pressed_attack([self.mob])
            
            # if the mob didnt has been forced to move    
            if not right and not left:   
                if self.is_jumping_platform == False:
                    # sometime the mob need to walk at the inverse sens of his direction when attacking forward or behind
                    # because he would continue walking infinitly
                    if self.random_coefficient["type_attack"][1]==0 or (self.random_coefficient["type_attack"][1]==1 and behind and self.direction_behind==self.target.direction) or \
                        (self.random_coefficient["type_attack"][1]==2 and forward and self.direction_forward!=self.target.direction):
                        if x < -self.mob.range_attack +60 and not(self.mob.is_attacking and sol): 
                            pressed_right([self.mob], collision)
                            right=True
                    elif self.random_coefficient["type_attack"][1]==1 and (self.direction_behind == "right" and not behind) and not self.mob.is_attacking:
                        pressed_right([self.mob], collision)
                        right=True
                    elif self.random_coefficient["type_attack"][1]==2 and (self.direction_forward=="right" and not forward) and not self.mob.is_attacking:
                        pressed_right([self.mob], collision)
                        right=True
                        
                    if self.random_coefficient["type_attack"][1]==0 or (self.random_coefficient["type_attack"][1]==1 and behind and self.direction_behind==self.target.direction) or \
                        (self.random_coefficient["type_attack"][1]==2 and forward and self.direction_forward!=self.target.direction):
                        if x > self.mob.range_attack -60 and not(self.mob.is_attacking and sol): 
                            pressed_left([self.mob], collision)
                            left=True
                    elif self.random_coefficient["type_attack"][1]==1 and (self.direction_behind == "left" and not behind) and not self.mob.is_attacking:
                        pressed_left([self.mob], collision)
                        left=True
                    elif self.random_coefficient["type_attack"][1]==2 and (self.direction_forward == "left" and not forward) and not self.mob.is_attacking:
                        pressed_left([self.mob], collision)
                        left=True
                        
                # sometimes the mob is forced to jump on the right or on the left        
                elif self.is_jumping_platform=="right":
                    pressed_right([self.mob], collision)
                elif self.is_jumping_platform=="left":
                    pressed_left([self.mob], collision)          
                    
            if not self.mob.is_attacking:
                if self.random_coefficient["type_attack"][1]==0: 
                    if not(x < -self.mob.range_attack or x > self.mob.range_attack):
                        handle_input_ralentissement(self.mob)
                        if time.time() - self.mob.timer_attack > self.mob.cooldown_attack: 
                            pressed_attack([self.mob])
                        self._reset_coeff("type_attack")
                elif self.random_coefficient["type_attack"][1]==1 and behind and self._get_distance_target_x(abs_bool=True) < self.mob.range_attack:
                    handle_input_ralentissement(self.mob)
                    if time.time() - self.mob.timer_attack > self.mob.cooldown_attack:
                        self._reset_coeff("type_attack")
                        pressed_attack([self.mob])
                elif self.random_coefficient["type_attack"][1]==2 and forward and self._get_distance_target_x(abs_bool=True) < self.mob.range_attack:
                    handle_input_ralentissement(self.mob)
                    if time.time() - self.mob.timer_attack > self.mob.cooldown_attack:
                        self._reset_coeff("type_attack")
                        pressed_attack([self.mob])
            
            # if the mob is running we make him do random jump if the target is not bellow it and if he is not on a platform        
            if (sol and self.mob.is_mouving_x) and not collision.joueur_sur_sol(self.mob, platform_only=True) and not cprj and not cplj and not cpl and not cpr:
                if random.randint(1,self.random_coefficient["jump_run"][1])==2: 
                    pressed_up([self.mob], down, left, right, [False], collision)
                    self._reset_coeff("jump_run")

            # we dont want every mob to jump at the same time so we add randomness
            if y > 200 and not cprj and not cplj and not cpl and not cpr: 
                if random.randint(1,10)==5: pressed_up([self.mob], down, left, right, [False], collision)
            elif y < - 200: 
                if random.randint(1,10)==5: pressed_down([self.mob])
                
            if not sol and random.randint(1,self.random_coefficient["attack_air"][1])==2 and self.get_distance_target() <= self.mob.range_attack: 
                pressed_attack([self.mob])
                self._reset_coeff("attack_air")
        else :
            self.mob.reset_actions()
            self.handle_input_ralentissement(self.mob)