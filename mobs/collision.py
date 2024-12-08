import time
import pygame

class Collision:
    def __init__(self, zoom, matrix):
        self.zoom=zoom
        self.matrix_map=matrix
        self.dico_map_wave={}
        self.current_map_is_wave=False

    def _get_coords_maps(self, c, d,only):
        liste=[]    
        if self.matrix_map[d][c]!=None: liste.append((d,c))
        if only: return liste
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

    def get_dico(self, coord_map, only=False):
        liste=[]
        if not self.current_map_is_wave:
            for tu in self._get_coords_maps(coord_map[0], coord_map[1], only=only):
                liste.append(self.matrix_map[tu[0]][tu[1]])
        else:
            liste.append(self.dico_map_wave)
        return liste

    def collide_platform_bot(self,mob, direction, add=""):
        for dico in self.get_dico(mob.coord_map):
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
        for dico in self.get_dico(mob.coord_map):
            for obj in dico[type]:
                new_x = screen.get_width()/2 + obj[0].left - scroll_rect.x
                new_y = screen.get_height()/2 + obj[0].top - scroll_rect.y
                pygame.draw.rect(screen, (255, 0, 0), (new_x, new_y, obj[0].w, obj[0].h))

    def foot_on_little_ground(self, mob):
        for dico in self.get_dico(mob.coord_map):
            for little_ground in dico["little_ground"]:
                if mob.feet.collidelist(little_ground) > -1:
                    return True

    def joueur_sur_sol(self, mob, platform_only=False, dash=False, change_pos=True, chest=False, get_pos=None, wallslide=False):
        """renvoie True si les pieds du joueur est sur une plateforme ou sur le sol.
        De plus, place la coordonee en y du joueur juste au dessus de la plateforme / du sol"""
        passage_a_travers = time.time() - mob.timers["t1_passage_a_travers_plateforme"] < mob.cooldown_passage_a_travers_plateforme
        bool=False
        gd=None
        if get_pos!=None: pos=None
        if dash : rect=mob.body
        elif chest : rect=mob.chest
        else: rect=mob.feet
        for dico in self.get_dico(mob.coord_map):
            if not platform_only:
                if not mob.is_falling:
                    for little_ground in dico["little_ground"]:
                        if rect.collidelist(little_ground) > -1:
                            if not change_pos and not platform_only and get_pos==None: return True
                            if not mob.is_jumping_edge and not mob.is_jumping:
                                if get_pos!=None: 
                                    pass
                                elif not gd:
                                    gd=little_ground
                                elif gd[0].y>little_ground[0].y:
                                    gd=little_ground
                                # comme le joueur est sur le sol, il peut de nouveau dash / sauter
                                mob.a_sauter = False
                                mob.a_dash = False
                            bool= True
                
                for ground in dico["ground"] + [a[0:1] for a in dico["ground-closed_room"]]:
                    if rect.collidelist(ground) > -1:
                        continuer=True
                        if not wallslide and "player" in mob.id:
                            for wall__ in [a[0:1] for a in dico["wall-closed_room"]]:
                                if mob.body.collidelist(wall__) > -1 and ((wall__[0].x==ground[0].x and mob.body.x) or (ground[0].x+ground[0].w==wall__[0].x+wall__[0].w and mob.body.x+mob.body.w<ground[0].x+ground[0].w)):
                                    continuer=False
                                    break

                        if continuer:
                            if not change_pos and not platform_only  and get_pos==None: return True
                            if not mob.is_jumping_edge and not mob.is_jumping:
                                if get_pos!=None:
                                    if get_pos=="left":
                                        if pos==None:pos=ground[0].x+ground[0].w
                                        elif ground[0].x+ground[0].w>pos:pos=ground[0].x+ground[0].w
                                    elif get_pos=="right":
                                        if pos==None:pos=ground[0].x
                                        elif ground[0].x<pos:pos=ground[0].x
                                elif not gd:
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
                        if not change_pos  and get_pos==None: return True
                        if (mob.position[1] + mob.image.get_height() - plateforme[0].y < 20) or "crab" in mob.id:
                            if not mob.is_jumping_edge and not mob.is_jumping:
                                #if mob.action != "Edge_climb": mob.position[1] = plateforme[0].y - mob.image.get_height() + 1 + mob.increment_foot*2
                                if get_pos!=None:pass
                                elif not gd:
                                    gd=ground
                                elif gd[0].y>ground[0].y:
                                    gd=ground
                                # comme le joueur est sur une plateforme, il peut de nouveau dash / sauter
                                mob.a_sauter = False
                                mob.a_dash = False
                            bool=True
        if get_pos!=None:return pos!=None, pos
        if bool and get_pos==None: 
            if not mob.is_jumping_edge and not mob.is_jumping and mob.action != "Edge_climb" and change_pos: 
                mob.position[1] = gd[0].y - mob.image.get_height() + 1 + mob.increment_foot*2
            return True
        return False

    def joueur_se_cogne(self, mob, dash=False,chest=False, get_pos=None):
        """renvoie True si la tete du joueur est en collision avec un plafond"""
        if dash : rect=mob.body
        elif chest: rect=mob.chest
        else: rect=mob.head
        if get_pos!=None: pos=None
        for dico in self.get_dico(mob.coord_map):
            for ceilling in dico["ceilling"] + [a[0:1] for a in dico["ceilling-closed_room"]]:
                if rect.collidelist(ceilling) > -1:
                    if get_pos==None:return True
                    elif get_pos=="left":
                        if pos==None:pos=ceilling[0].x+ceilling[0].w
                        elif ceilling[0].x+ceilling[0].w>pos:pos=ceilling[0].x+ceilling[0].w
                    elif get_pos=="right":
                        if pos==None:pos=ceilling[0].x
                        elif ceilling[0].x<pos:pos=ceilling[0].x
        if get_pos==None:return False
        return pos!=None, pos

    def star_is_attacking(self, mob):
        temp=mob.position.copy()
        temp_speed=mob.speed
        mob.speed*=0.33
        for i in range(6):
            if mob.direction_attack == "right":
                mob.move_right(change_image=False,just_run=True)
            elif mob.direction_attack == "left":
                mob.move_left(change_image=False,just_run=True)
            mob.update_rect()
            if self.foot_on_little_ground(mob):
                mob.speed=temp_speed
                return False
            if self.stop_if_collide(mob.direction_attack, mob, dash=True): 
                mob.speed=temp_speed
                return True
        mob.position=temp.copy()
        mob.update_rect()
        mob.speed=temp_speed
    
    def stop_if_collide(self, direction,mob, head = False, move_back=True, dash=False, dontmove=False, chest=False, stick=False,get_pos=False,big_head=False, debug=False, closed_room=False):
        """fait en sorte que le joueur avance plus lorsque qu'il avance dans un mur
        /!\           /!\          /!\        /!\ 
        
            its normal if we work with list (wall[0]) 
            because collide list need to use list
                 
                /!\           /!\         /!\         /!\ 
        """
        if head:rect = mob.head
        elif chest: rect=mob.chest
        elif big_head: rect=mob.big_head
        else:rect = mob.body
        if dash or stick: temp=None
        for dico in self.get_dico(mob.coord_map):
            for wall in dico["wall"] + [a[0:1] for a in dico["wall-closed_room"]] if not closed_room else [a[0:1] for a in dico["wall-closed_room"]] :
                if rect.collidelist(wall) > -1:
                    # si le joueur va a droite en etant a gauche du mur
                    # limage est plus grande que la partie visible du joueur, d'où mob.image.get_width()/2
                    if dash or stick: 
                        if dontmove and get_pos==False:  return True
                        if temp==None and ((not big_head) or (big_head and mob.body.x < wall[0].x and direction=="right") or (direction=="left" and big_head and mob.body.x + mob.body.w> wall[0].x+wall[0].w )): temp=wall[0]
                        elif temp!=None:
                            if direction== 'right' and wall[0].x < temp.x and ((not big_head) or (big_head and mob.body.x < wall[0].x )): 
                                temp=wall[0]
                            elif direction == 'left' and wall[0].x+wall[0].w> temp.x+temp.w and ((not big_head) or (big_head and mob.body.x + mob.body.w> wall[0].x+wall[0].w )):temp=wall[0]
                    else:
                        if direction == 'right' and wall[0].x < mob.body.x + mob.body.w and(mob.is_sliding_ground or ("player" in mob.id and mob.is_attacking) or (mob.body.x + mob.body.w-wall[0].x < mob.max_distance_collide)):
                            if dontmove: 
                                return True
                            if not mob.is_dashing and not mob.is_dashing_attacking and move_back: 
                                mob.move_back()   
                            elif not move_back:
                                mob.position[0]=wall[0].x-mob.rect.w
                            
                            return True
                        # si le joueur va a gauche en etant a droite du mur
                        if direction == 'left' and wall[0].x + wall[0].w > mob.body.x and (mob.is_sliding_ground  or ("player" in mob.id and mob.is_attacking) or (wall[0].x + wall[0].w-mob.body.x < mob.max_distance_collide)):  
                            if dontmove: 
                                return True
                            
                            if not mob.is_dashing and not mob.is_dashing_attacking and move_back:  
                                mob.move_back()  
                            elif not move_back:
                                mob.position[0]=wall[0].x+wall[0].w

                            return True
        if dash and temp != None:
            if not dontmove and direction == 'right':mob.position[0]=temp.x+5-mob.image.get_width()
            elif not dontmove and direction=="left":mob.position[0]=temp.x+temp.w-5
            if get_pos: 
                if direction=="right": return (True, temp.x)
                elif direction=="left": return (True, temp.x + temp.w)
            return True                
    
        if stick and temp!=None:
            if direction=="right":mob.body.x=temp.x-mob.body.w+mob.max_distance_collide
            elif direction=="left":mob.body.x=temp.x+temp.w-mob.max_distance_collide
            mob.rect.midbottom = mob.body.midbottom
            mob.position=[mob.rect.topleft[0], mob.rect.topleft[1]]
            mob.speed=mob.max_speed_run
            if direction=="right":mob.move_right()
            elif direction=="left":mob.move_left()
        if get_pos: return False, None
        return False

    def stick_to_wall(self, mob, direction):
        if mob.direction == "right":
                mob.position[0] += 2*self.zoom
        elif mob.direction == "left":
                mob.position[0] -= 2*self.zoom
        temp=None
        for dico in self.get_dico(mob.coord_map):
            for wall in dico["wall"] + [a[0:1] for a in dico["wall-closed_room"]]:
                if mob.body.collidelist(wall) > -1:
                    if temp==None: temp=wall[0]
                    else:
                        if direction== 'right' and wall[0].x < temp.x: temp=wall[0]
                        elif direction == 'left' and wall[0].x+wall[0].w > temp.x+temp.w : temp=wall[0]
        if direction=="left": mob.position[0] = temp.x + temp.w - 1.26 * mob.body.w
        else: mob.position[0] = temp.x - 2.11 * mob.body.w
        return True 
                        
    def check_grab(self, mob, direction, chest=False, dash=False):
        """Grab SSI head collide"""
        for dico in self.get_dico(mob.coord_map):
            for wall in dico["wall"] + [a[0:1] for a in dico["wall-closed_room"]]:
                # check method collide wall pour la collision
                #  and ((mob.direction == 'right' and wall[0].x < mob.body.x + mob.body.w  and mob.body.x + mob.body.w-wall[0].x < mob.max_distance_collide) or (mob.direction == 'left' and wall[0].x + wall[0].w > mob.body.x and wall[0].x + wall[0].w-mob.body.x < mob.max_distance_collide))
                if mob.body.collidelist(wall) > -1 and ((dash and  mob.body.collidelist(wall) > -1)or(chest and mob.chest.collidelist(wall) > -1) or mob.head.collidelist(wall) > -1):
                    if "Edge_grab" in mob.actions:
                        if not mob.is_jumping_edge:
                            mob.fin_chute()
                            mob.debut_grab_edge()
                        self.stick_to_wall(mob, direction)
                        # REMOVE RETURN TRUE SI BUG
                        return True
                          
    def check_pieds_collide_wall(self, mob):
        for dico in self.get_dico(mob.coord_map):
            for wall in dico["wall"] + [a[0:1] for a in dico["wall-closed_room"]]:
                if mob.feet.collidelist(wall) > -1:
                    return True
        return False

    def check_head_collide_ground(self, mob, changing_y=False, body=False, x=None, get_pos=None):
        lst=[]
        pos=None
        for dico in self.get_dico(mob.coord_map):
            for ground in dico["ground"] + [a[0:1] for a in dico["ground-closed_room"]]:
                if mob.big_head.collidelist(ground) > -1 or (body and mob.body.collidelist(ground) > -1):
                    if changing_y==True:
                        if (pos == None or ground[0].y < pos) and (x==None or ground[0].x+ground[0].w==x or ground[0].x==x) : pos = ground[0].y
                    if get_pos=="left":
                        lst.append(ground[0].x+ground[0].w)
                    elif get_pos=="right":
                        lst.append(ground[0].x)
                    if not changing_y and get_pos==None: return True
        if get_pos!=None: return len(lst)>0, lst
        if changing_y and pos != None :
            mob.position[1]=pos
            return True
        if not changing_y : return False
    
    def check_tombe_ou_grab(self, mob):
        """stop le grab edge si on est plus en collision avce un mur"""
        for dico in self.get_dico(mob.coord_map):
            for wall in dico["wall"] +[a[0:1] for a in dico["wall-closed_room"]]:
                if (mob.body.collidelist(wall) > -1 or mob.head.collidelist(wall) > -1 or mob.body_wallslide.collidelist(wall) > -1) and mob.is_sliding:
                    return
        mob.fin_grab_edge()

    def ground_above_wall(self,mob,direction):
        gd=None
        for dico in self.get_dico(mob.coord_map):
            for ground in dico["ground"] +[a[0:1] for a in dico["ground-closed_room"]]:
                    if mob.body.collidelist(ground) > -1:
                        if not mob.is_jumping_edge and not mob.is_jumping:
                            if not gd:
                                gd=ground
                            elif gd[0].y>ground[0].y:
                                gd=ground
                            # comme le joueur est sur le sol, il peut de nouveau dash / sauter
                            mob.a_sauter = False
                            mob.a_dash = False
        temp=None
        for dico in self.get_dico(mob.coord_map):
            for wall in dico["wall"] + [a[0:1] for a in dico["wall-closed_room"]]:
                if mob.body.collidelist(wall) > -1:
                    
                    # si le joueur va a droite en etant a gauche du mur
                    # limage est plus grande que la partie visible du joueur, d'où mob.image.get_width()/2
                    if temp==None: temp=wall
                    else:
                        if direction== 'right' and wall[0].x < temp[0].x: temp=wall
                        elif direction == 'left' and wall[0].x+wall[0].w > temp[0].x+temp[0].w :temp=wall
        if gd == None or temp == None : return False
        else: return gd[0].y < temp[0].y

    def handle_collisions_wall_dash(self, mob, fin_dash, direction, fall=True, ground=False):   
        """only check when dist != 0 because if the player only go up or down the body is big enough that the player
        wont go through the grounds / ceillings.
        Moreover the distance parcoured in x is equal to the one in y so we can use i in the loop to 
        add the distance in the y axix little by little"""

        falling = mob.is_falling ; 
        if direction != "" :
            wall, w = self.stop_if_collide(direction, mob, dash=True, dontmove=True, get_pos=True)  
            cogne, c=self.joueur_se_cogne(mob, chest=True, get_pos=direction) 
            sol, s=self.joueur_sur_sol(mob, dash=True, change_pos=False, get_pos=direction) 

        else:
            wall= self.stop_if_collide(direction, mob, dash=True, dontmove=True)  
            cogne=self.joueur_se_cogne(mob, chest=True) 
            sol=self.joueur_sur_sol(mob, dash=True, change_pos=False) 


        if ( wall and not ((mob.action=="dash_attack" or mob.action=="dash_ground") and self.foot_on_little_ground(mob) and not self.stop_if_collide(direction, mob, dash=True, chest=True, dontmove=True)))  or cogne or (ground and sol):
            if wall : self.stop_if_collide(direction, mob, dash=True)
            dashing_attacking=mob.is_dashing_attacking ; pieds=self.joueur_sur_sol(mob, change_pos=False)
            fin_dash()
            if not direction=="": self.check_grab(mob, direction, dash=True)
            if pieds and dashing_attacking and mob.is_grabing_edge: 
                mob.fin_grab_edge()
                mob.change_direction("idle", mob.direction)
                self.stop_if_collide(direction, mob, stick=True)
            # why not cogne ???????????????
            if fall and not mob.is_grabing_edge and (not ground or not sol or not cogne):
                mob.debut_chute()
            if not cogne and (ground or (not ground and falling)) and sol:
                if mob.is_grabing_edge and self.ground_above_wall(mob, direction) and direction!="" and s==w and self.check_head_collide_ground(mob, False,True, x=s):
                    self.check_head_collide_ground(mob, True, True)
                    mob.fin_grab_edge()
                    mob.debut_edge_climb()
                else:
                    if mob.is_grabing_edge: mob.fin_grab_edge()
                    self.joueur_sur_sol(mob, dash=True)
                    mob.debut_crouch()
            if not direction=="" and mob.is_grabing_edge and cogne and ((direction=="right" and c<w) or (direction=="left" and c>w)):
                mob.fin_grab_edge()
                mob.debut_chute()

    def mob_collide_object(self, mobs, obj, Projectile):
        for mob in mobs:
            if mob.body.collidelist([obj.rect]) > -1 and (type(obj)!=Projectile or obj.sender!=mob):
                return mob
        return None

    def projectile_collide_map(self, projectile):
        for dico in self.get_dico(projectile.coord_map):
            for wall in dico["wall"]:
                if projectile.rect.collidelist(wall) > -1:
                    return True
            for ground in dico["ground"] + [a[0:1] for a in dico["ground-closed_room"]] :
                if projectile.rect.collidelist(ground) > -1:
                    return True
            for platform in dico["platform"]:
                if projectile.rect.collidelist(platform) > -1:
                    return True
            for ceilling in dico["ceilling"]:
                if projectile.rect.collidelist(ceilling) > -1:
                    return True
        return False
    
    def get_closest_wall(self, mob):
        """
        /!\ doesnt take into account the walls that are under the player or above
        """
        for dico in self.get_dico(mob.coord_map):
            for wall in dico["wall"] + [a[0:1] for a in dico["wall-closed_room"]]:
                if mob.large_rect_spawn_item.collidelist(wall) > -1:
                    return wall
        return None
    
    def get_closed_room_object(self, mob):
        returned=[]
        for dico in self.get_dico(mob.coord_map):
            for ground in dico["ground-closed_room"]:
                if mob.rect_attack.collidelist([ground[0]]) > -1:
                    dico["ground-closed_room"].remove(ground)
                    returned.append((ground, "ground"))
                    for dico_ in self.get_dico(mob.coord_map):
                        for ceiling_ in dico_["ceilling-closed_room"]:
                            if (ceiling_[1] == ground[2] and ceiling_[2] == ground[1]) or (ceiling_[1] == ground[1] and ceiling_[2] == ground[2]):
                                dico_["ceilling-closed_room"].remove(ceiling_)
                                returned.append((ceiling_, "ceilling"))
                    return returned
            for wall in dico["wall-closed_room"]:
                if mob.rect_attack.collidelist([wall[0]]) > -1:
                    dico["wall-closed_room"].remove(wall)
                    returned.append((wall, "wall"))
                    for dico_ in self.get_dico(mob.coord_map):
                        for wall_ in dico_["wall-closed_room"]:
                            if (wall_[1] == wall[2] and wall_[2] == wall[1]) or (wall_[1] == wall[1] and wall_[2] == wall[2]):
                                dico_["wall-closed_room"].remove(wall_)
                                returned.append((wall_, "wall"))
                    return returned
            for ceilling in dico["ceilling-closed_room"]:
                if mob.rect_attack.collidelist([ceilling[0]]) > -1 or mob.body.collidelist([ceilling[0]]) > -1:
                    dico["ceilling-closed_room"].remove(ceilling)
                    returned.append((ceilling, "ceilling"))
                    for dico_ in self.get_dico(mob.coord_map):
                        for ground_ in dico_["ground-closed_room"]:
                            if (ground_[1] == ceilling[2] and ground_[2] == ceilling[1]) or (ground_[1] == ceilling[1] and ground_[2] == ceilling[2]):
                                dico_["ground-closed_room"].remove(ground_)
                                returned.append((ground_, "ground"))
                    return returned
        return returned