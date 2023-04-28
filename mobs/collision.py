import time
import pygame

class Collision:
    def __init__(self, zoom, matrix):
        self.zoom=zoom
        self.matrix_map=matrix
        self.dico_map_wave={}
        self.current_map_is_wave=False

    def _get_coords_maps(self, c, d):
        liste=[]    
        if self.matrix_map[d][c]!=None: liste.append((d,c))
        if c < len(self.matrix_map[0])-1 and self.matrix_map[d][c+1]!=None: 
            if d < len(self.matrix_map)-1 and self.matrix_map[d+1][c+1]!=None:
                liste.append((d+1,c+1))
            if d > 0 and self.matrix_map[d-1][c+1]!=None:
                liste.append((d-1,c+1))
            liste.append((d,c+1))
        if c > 0 and self.matrix_map[d][c-1]!=None:
            if d < len(self.matrix_map)-1 and self.matrix_map[d+1][c-1]!=None:
                liste.append((d+1,c-1))
            if d > 0 and self.matrix_map[d-1][c-1]!=None:
                liste.append((d-1,c-1))
            liste.append((d,c-1))
        if d < len(self.matrix_map)-1 and self.matrix_map[d+1][c]!=None:
            liste.append((d+1,c))
        if d > 0 and self.matrix_map[d-1][c]!=None:
            liste.append((d-1,c))
        return liste

    def _get_dico(self, coord_map):
        liste=[]
        if not self.current_map_is_wave:
            for tu in self._get_coords_maps(coord_map[0], coord_map[1]):
                liste.append(self.matrix_map[tu[0]][tu[1]])
        else:
            liste.append(self.dico_map_wave)
        return liste

    def collide_platform_bot(self,mob, direction, add=""):
        for dico in self._get_dico(mob.coord_map):
            if direction=="right" and dico["bot"][f"platform_{add}right"] != []:
                for rect in dico["bot"][f"platform_{add}right"]:
                    if mob.body.collidelist(rect) > -1:    
                        return True
            elif direction=="left" and dico["bot"][f"platform_{add}left"] != []:
                for rect in dico["bot"][f"platform_{add}left"]:
                    if mob.body.collidelist(rect) > -1:    
                        return True
        return False 

    def draw(self, mob, screen, scroll_rect, type):
        for dico in self._get_dico(mob.coord_map):
            for obj in dico[type]:
                new_x = screen.get_width()/2 + obj[0].left - scroll_rect.x
                new_y = screen.get_height()/2 + obj[0].top - scroll_rect.y
                pygame.draw.rect(screen, (255, 0, 0), (new_x, new_y, obj[0].w, obj[0].h))


    def joueur_sur_sol(self, mob, platform_only=False, dash=False):
        """renvoie True si les pieds du joueur est sur une plateforme ou sur le sol.
        De plus, place la coordonee en y du joueur juste au dessus de la plateforme / du sol"""
        passage_a_travers = time.time() - mob.t1_passage_a_travers_plateforme < mob.cooldown_passage_a_travers_plateforme
        bool=False
        gd=None
        if dash : rect=mob.body
        else: rect=mob.feet
        for dico in self._get_dico(mob.coord_map):
            if not platform_only:
                if not mob.is_falling:
                    for little_ground in dico["little_ground"]:
                        if rect.collidelist(little_ground) > -1:
                            if not mob.is_jumping_edge and not mob.is_jumping:
                                if not gd:
                                    gd=little_ground
                                elif gd[0].y>little_ground[0].y:
                                    gd=little_ground
                                # comme le joueur est sur le sol, il peut de nouveau dash / sauter
                                mob.a_sauter = False
                                mob.a_dash = False
                            bool= True
                
                for ground in dico["ground"]:
                    if rect.collidelist(ground) > -1:
                        if not mob.is_jumping_edge and not mob.is_jumping:
                            if not gd:
                                gd=ground
                            elif gd[0].y>ground[0].y:
                                gd=ground
                            # comme le joueur est sur le sol, il peut de nouveau dash / sauter
                            mob.a_sauter = False
                            mob.a_dash = False
                        bool= True
            for plateforme in dico["platform"]:
                # and not sprite.is_sliding
                if not passage_a_travers:
                    if rect.collidelist(plateforme) > -1:
                        if (mob.position[1] + mob.image.get_height() - plateforme[0].y < 20) or "crab" in mob.id:
                            if not mob.is_jumping_edge and not mob.is_jumping:
                                #if mob.action != "Edge_climb": mob.position[1] = plateforme[0].y - mob.image.get_height() + 1 + mob.increment_foot*2
                                if not gd:
                                    gd=ground
                                elif gd[0].y>ground[0].y:
                                    gd=ground
                                # comme le joueur est sur une plateforme, il peut de nouveau dash / sauter
                                mob.a_sauter = False
                                mob.a_dash = False
                            bool=True
        if bool : 
            if not mob.is_jumping_edge and not mob.is_jumping and mob.action != "Edge_climb": 
                mob.position[1] = gd[0].y - mob.image.get_height() + 1 + mob.increment_foot*2
            return True
        return False

    def joueur_se_cogne(self, mob):
        """renvoie True si la tete du joueur est en collision avec un plafond"""
        for dico in self._get_dico(mob.coord_map):
            for ceilling in dico["ceilling"]:
                if mob.head.collidelist(ceilling) > -1:
                    return True
        return False
        
    def stop_if_collide(self, direction,mob, head = False, move_back=True, dash=False, dontmove=False):
        """fait en sorte que le joueur avance plus lorsque qu'il avance dans un mur
        /!\           /!\          /!\        /!\ 
        
            its normal if we work with list (wall[0]) 
            because collide list need to use list
                 
                /!\           /!\         /!\         /!\ 
        """
        if head:rect = mob.head
        else:rect = mob.body
        if dash: temp=None
        for dico in self._get_dico(mob.coord_map):
            for wall in dico["wall"]:
                if rect.collidelist(wall) > -1:
                    
                    # si le joueur va a droite en etant a gauche du mur
                    # limage est plus grande que la partie visible du joueur, d'où mob.image.get_width()/2
                    if dash: 
                        if dontmove: return True
                        if temp==None: temp=wall[0]
                        else:
                            if direction== 'right' and wall[0].x < temp.x: temp=wall[0]
                            elif direction == 'left' and wall[0].x+wall[0].w > temp.x+temp.w : temp=wall[0]
                    else:
                        if direction == 'right' and wall[0].x < mob.body.x + mob.body.w and mob.body.x + mob.body.w-wall[0].x < mob.max_distance_collide:
                            if dontmove: return True
                            if not mob.is_dashing and not mob.is_dashing_attacking and move_back: 
                                mob.move_back()   
                            elif not move_back:
                                mob.position[0]=wall[0].x-mob.rect.w
                            return True
                        # si le joueur va a gauche en etant a droite du mur
                        if direction == 'left' and wall[0].x + wall[0].w > mob.body.x and wall[0].x + wall[0].w-mob.body.x < mob.max_distance_collide:  
                            if dontmove: return True
                            if not mob.is_dashing and not mob.is_dashing_attacking and move_back:  
                                mob.move_back()  
                            elif not move_back:
                                mob.position[0]=wall[0].x+wall[0].w
                            return True
        if dash and temp != None:
            if direction == 'right':mob.position[0]=temp.x+5-mob.image.get_width()
            else:mob.position[0]=temp.x+temp.w-5
            return True                
    
        return False

    def stick_to_wall(self, mob, direction):
        if mob.direction == "right":
                mob.position[0] += 2*self.zoom
        elif mob.direction == "left":
                mob.position[0] -= 2*self.zoom
        temp=None
        for dico in self._get_dico(mob.coord_map):
            for wall in dico["wall"]:
                if mob.body.collidelist(wall) > -1:
                    if temp==None: temp=wall[0]
                    else:
                        if direction== 'right' and wall[0].x < temp.x: temp=wall[0]
                        elif direction == 'left' and wall[0].x+wall[0].w > temp.x+temp.w : temp=wall[0]
        if direction=="left": mob.position[0] = temp.x + temp.w - 1.26 * mob.body.w
        else: mob.position[0] = temp.x - 2.11 * mob.body.w
        return True 
                        
    def check_grab(self, mob, direction):
        """Grab SSI head collide"""
        for dico in self._get_dico(mob.coord_map):
            for wall in dico["wall"]:
                # check method collide wall pour la collision
                #  and ((mob.direction == 'right' and wall[0].x < mob.body.x + mob.body.w  and mob.body.x + mob.body.w-wall[0].x < mob.max_distance_collide) or (mob.direction == 'left' and wall[0].x + wall[0].w > mob.body.x and wall[0].x + wall[0].w-mob.body.x < mob.max_distance_collide))
                if mob.body.collidelist(wall) > -1 and mob.head.collidelist(wall) > -1:
                    if "Edge_grab" in mob.actions:
                        if not mob.is_jumping_edge:
                            mob.fin_chute()
                            mob.debut_grab_edge()
                        self.stick_to_wall(mob, direction)
                          
    def check_pieds_collide_wall(self, mob):
        for dico in self._get_dico(mob.coord_map):
            for wall in dico["wall"]:
                if mob.feet.collidelist(wall) > -1:
                    return True
        return False

    def check_head_collide_ground(self, mob, changing_y=False):
        pos=-999999
        for dico in self._get_dico(mob.coord_map):
            for ground in dico["ground"]:
                if mob.big_head.collidelist(ground) > -1:
                    if changing_y==True:
                        if pos == -999999 or ground[0].y < pos : pos = ground[0].y
                    if not changing_y : return True
        if changing_y and pos != -999999 :mob.position[1]=pos
        if not changing_y : return False
    
    def check_tombe_ou_grab(self, mob):
        """stop le grab edge si on est plus en collision avce un mur"""
        for dico in self._get_dico(mob.coord_map):
            for wall in dico["wall"]:
                if (mob.body.collidelist(wall) > -1 or mob.head.collidelist(wall) > -1 or mob.body_wallslide.collidelist(wall) > -1) and mob.is_sliding:
                    return
        mob.fin_grab_edge()
    
    def handle_collisions_wall_dash(self, mob, dist, fin_dash, direction, tile_width, fall=True, distance_y=0, ground=False):   
        """only check when dist != 0 because if the player only go up or down the body is big enough that the player
        wont go through the grounds / ceillings.
        Moreover the distance parcoured in x is equal to the one in y so we can use i in the loop to 
        add the distance in the y axix little by little"""
        step=round(tile_width-2)
        if dist != 0 and step > 0:
            tmp=[mob.position[0], mob.position[1]]
            for i in [y for y in range(step, abs(round(dist)), step)]+[abs(round(dist))+1]:
                if direction == "right":mob.position[0]+=i
                else:mob.position[0]-=i
                if distance_y>0:mob.position[1]+=i
                elif distance_y<0:mob.position[1]-=i
                if self.stop_if_collide(direction, mob, dash=True) or self.joueur_se_cogne(mob) or (ground and self.joueur_sur_sol(mob, dash=True)):
                    fin_dash()
                    self.check_grab(mob, direction)
                    if fall:
                        if not mob.is_grabing_edge:
                            mob.debut_chute()
                    if not mob.is_grabing_edge and (not ground or not self.joueur_sur_sol(mob, dash=True)):
                        mob.position=[tmp[0], tmp[1]]
                    if ground and self.joueur_sur_sol(mob, dash=True) : mob.debut_crouch()
                    return
            mob.position=[tmp[0], tmp[1]]