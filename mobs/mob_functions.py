import time

def pressed_left(liste_mob, collision):
    for mob in liste_mob:
        if not "hurt" in mob.action_image and not ("star" in mob.id and mob.is_attacking):
            if "ground_slide" in mob.actions and mob.is_sliding_ground and mob.slide_ground_direction_x == 'right':
                mob.fin_slide_ground()
            if not mob.is_dashing_ground and not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping_edge and not mob.is_grabing_edge and not mob.is_sliding_ground and not mob.is_dashing and not mob.is_dashing_attacking:
                mob.save_location()
                bool = collision.joueur_sur_sol(mob)
                if bool:
                    mob.move_left(pieds_sur_sol=True)
                # si le joueur ne dash pas et est en lair
                else:
                    mob.move_left()
                if collision.stop_if_collide("left", mob) and not bool and not mob.is_jumping:
                    collision.check_grab(mob, "left")
                

def pressed_right(liste_mob, collision):
    for mob in liste_mob:
        if not "hurt" in mob.action_image and not ("star" in mob.id and mob.is_attacking):
            if "ground_slide" in mob.actions:
                if mob.is_sliding_ground and mob.slide_ground_direction_x == 'left':
                    mob.fin_slide_ground()
            if not mob.is_dashing_ground and not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping_edge and not mob.is_grabing_edge and not mob.is_sliding_ground and not mob.is_dashing and not mob.is_dashing_attacking:
                mob.save_location()
                bool = collision.joueur_sur_sol(mob)
                if bool:
                    mob.move_right(pieds_sur_sol=True)
                # si le joueur ne dash pas et est en lair
                else:
                    mob.move_right()

                if collision.stop_if_collide("right", mob, debug="player" in mob.id and mob.is_attacking) and not bool and not mob.is_jumping:
                    collision.check_grab(mob, "right")
                # if "player" in mob.id and mob.is_attacking and mob.direction_attack == "right" and mob.

                
def jump_edge(mob, pressed_up_bool, left, right,down, collision, pieds, zoom):
    if "jump_edge" in mob.actions:
        if not pressed_up_bool[0]:
            dir_x = ""
            if left:
                dir_x = "left"
            elif right:
                dir_x = "right"
            #  and (( cogne and not pieds) or not cogne)
            if time.time()-mob.timers["timer_jump_edge_cogne"] > mob.cooldown_jump_edge_cogne and mob.is_grabing_edge and time.time() - mob.timers["timer_cooldown_next_jump"] > mob.cooldown_next_jump:
                mob.fin_grab_edge()
                # si les pieds sont sur le mur des particles apparaissent
                if collision.check_pieds_collide_wall(mob):
                    if mob.is_parying:
                        mob.is_parying=False
                    mob.debut_saut_edge(direction_x=dir_x, pieds=pieds)
                    mob.particule.pieds_collide_jump_edge = True
                else:
                    mob.debut_saut_edge(direction_x=dir_x, pieds=pieds)
                    mob.particule.pieds_collide_jump_edge = False
            # pressed_up sert à savoir si le joueur viens d'appyuer sur la touche
            # il pourrait juste rester appuyer       
            pressed_up_bool[0] = True
        else:
            pressed_up_bool[0] = False
    if not down and (collision.joueur_sur_sol(mob) or time.time() - mob.timers["timer_cooldown_able_to_jump"] < mob.cooldown_able_to_jump) and not mob.a_sauter and time.time() - mob.timers["timer_cooldown_next_jump"] > mob.cooldown_next_jump*2:
        if mob.is_sliding_ground:
            mob.fin_slide_ground()
        if mob.is_dashing_ground:
            mob.fin_dash_ground()
        mob.debut_saut()
        if collision.stop_if_collide(mob.direction, mob):
            if mob.direction=="right":mob.position[0]-=5*zoom
            else:mob.position[0]+=5*zoom

def pressed_up(liste_mob, down, left, right, pressed_up_bool, collision, zoom):
    for mob in liste_mob:
        if not collision.joueur_se_cogne(mob) and not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping_edge and not mob.is_dashing and (not mob.is_attacking or "star" in mob.id) and not mob.is_dashing_attacking and not "hurt" in mob.action_image and not mob.is_parying and not mob.is_jumping:
            pieds=collision.check_pieds_collide_wall(mob)
            # cogne = collision.joueur_se_cogne(mob)
            #  and not cogne
            if "Edge_climb" in mob.actions and ((mob.direction=="right" and right) or (mob.direction=="left" and left) or (mob.direction=="right" and not left) or (mob.direction=="left" and not right)) and not pressed_up_bool[0] and collision.check_head_collide_ground(mob) and mob.is_grabing_edge:
                wall, w = collision.stop_if_collide(mob.direction, mob, dontmove=True, get_pos=True, dash=True, big_head=True)  
                sol, s=collision.check_head_collide_ground(mob, changing_y=False, get_pos=mob.direction)
                wall_added=collision.stop_if_collide(mob.direction, mob, dontmove=True, get_pos=True, dash=True, big_head=True, closed_room=True)  
                if not wall_added and wall and sol and w in s:
                    mob.fin_grab_edge()
                    collision.check_head_collide_ground(mob, changing_y=True, x=w)
                    mob.debut_edge_climb()
                else:
                    jump_edge(mob, pressed_up_bool, left, right,down, collision, pieds, zoom)
            else:
                jump_edge(mob, pressed_up_bool, left, right,down, collision, pieds, zoom)

def pressed_dash(liste_mob, left, right, down, up, joueur_sur_sol, collision, pressed_dash_bool):
    for mob in liste_mob:
        if 'dash' in mob.actions:
            
            if not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping and not mob.is_dashing and not mob.a_dash and not mob.is_sliding_ground and not mob.is_dashing_ground and not mob.is_jumping_edge and not mob.is_attacking and not mob.is_dashing_attacking:           
                if not joueur_sur_sol(mob) and not collision.joueur_se_cogne(mob):
                    mob.update_rect()
                    wall=collision.stop_if_collide(mob.direction, mob, dash=True, dontmove=True)
                    if not collision.foot_on_little_ground(mob) and not pressed_dash_bool[0] and time.time() - mob.timers["timer_dash"] > mob.cooldown_dash  and ((not mob.is_grabing_edge and not wall) or ( mob.is_grabing_edge and mob.direction_wall == "left" and right ) or ( mob.direction_wall == "right" and left )):
                        if ( mob.direction_wall == "left" and right ) or ( mob.direction_wall == "right" and left ):
                            mob.timers["timer_debut_dash_grabedge"]=time.time()
                        if mob.is_parying:
                            mob.is_parying=False
                        dir_y = ""
                        dir_x = ""
                        bool_ = False
                        if mob.is_grabing_edge:
                            bool_ = True
                            if mob.direction_wall == "left": dir_x="right"
                            else:dir_x="left"
                            mob.fin_grab_edge()
                        else:

                            if right:dir_x = "right"
                            if left:dir_x = "left"
                        if down:dir_y = "down"
                        if up:dir_y = "up"
                        
                        if dir_y == "" and dir_x == "":dir_y = "up"
                        mob.debut_dash(dir_x, dir_y, bool_) 
                        if not wall:
                            mob.update_rect()
                            if collision.stop_if_collide(dir_x, mob, dash=True, dontmove=True):
                                mob.timers["timer_debut_dash_grabedge"]=time.time()

                        # collision.handle_collisions_wall_dash(mob, mob.fin_dash, mob.dash_direction_x, ground=True)         
                        pressed_dash_bool[0] = True
                elif not ((left and collision.stop_if_collide("left",mob, dontmove=True)) or (right and collision.stop_if_collide("right",mob, dontmove=True))):
                    if down and time.time() - mob.timers["timer_cooldown_slide_ground"] > mob.cooldown_slide_ground : 
                        if mob.is_parying:
                            mob.is_parying=False
                        if mob.is_falling: mob.fin_chute()
                        if left:
                            mob.debut_slide_ground("left")
                            mob.update_rect()
                            if collision.stop_if_collide("left",mob, dontmove=True):
                                mob.fin_slide_ground()
                        elif right:
                            mob.debut_slide_ground("right")
                            mob.update_rect()
                            if collision.stop_if_collide("right",mob, dontmove=True):
                                mob.fin_slide_ground()
                        pressed_dash_bool[0] = True
                    elif not down and time.time() - mob.timers["timer_cooldown_dash_ground"] > mob.cooldown_dash_ground:
                        if mob.is_parying:
                            mob.is_parying=False
                        if mob.is_falling: mob.fin_chute()
                        if left:
                            mob.debut_dash_ground("left")
                            mob.update_rect()
                            if collision.stop_if_collide("left",mob, dontmove=True):
                                mob.fin_dash_ground()
                        elif right:
                            mob.debut_dash_ground("right")
                            mob.update_rect()
                            if collision.stop_if_collide("right",mob, dontmove=True):
                                mob.fin_dash_ground()
                        pressed_dash_bool[0] = True 
                        
def pressed_attack(liste_mob):
    for mob in liste_mob:
        if not mob.is_aiming:
            if "attack" in mob.actions:
                if not mob.is_rolling and mob.action != "Edge_climb" and (not mob.is_jumping or mob.can_attack_while_jump) and not mob.is_jumping_edge and not mob.is_dashing and not mob.is_attacking and not mob.is_grabing_edge and not mob.is_parying and not mob.is_dashing_attacking and not "hurt" in mob.action_image:
                    if mob.is_sliding_ground:
                        mob.fin_slide_ground()
                    if mob.is_dashing_ground:
                        mob.fin_dash_ground()
                    if (not mob.is_falling and not mob.action == "jump") or not mob.has_air_attack:
                        if "player" in mob.id and time.time()-mob.timers["timer_attack"] < mob.cooldown_attack and not mob.a_attaquer2:
                            mob.attack2()
                        else:
                            mob.debut_attack()
                    elif time.time() - mob.timers["timer_attack_aerienne"] > mob.cooldown_attack_aerienne:
                        mob.debut_attack(air=True)
        else:
            if time.time()-mob.timers["timer_attack_aim"] > mob.cooldown_attack_aim[mob.weapon] and not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping_edge and not mob.is_dashing and not mob.is_attacking and not mob.is_grabing_edge and not mob.is_parying and not mob.is_dashing_attacking and not "hurt" in mob.action_image:
                mob.lauch_projectile()

def pressed_pary(liste_mob, left, right, collision):
    for mob in liste_mob:
        if "pary" in mob.actions:
            if not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping and not mob.is_jumping_edge and not mob.is_dashing and not mob.is_dashing_ground and not mob.is_attacking and not mob.is_grabing_edge and not mob.is_dashing_attacking and time.time()-mob.timers["timer_pary"]>mob.cooldown_pary and not "hurt" in mob.action_image:
                if mob.is_sliding_ground:
                    mob.fin_slide_ground()
                if mob.is_dashing_ground:
                    mob.fin_dash_ground()
                if not mob.is_parying:
                    mob.debut_pary()
        if "roll" in mob.actions:
            if left: dir="left"
            elif right: dir="right"
            else: dir=mob.direction
            if not collision.stop_if_collide(dir,mob, dontmove=True) and not mob.is_falling and not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping and not mob.is_dashing and not mob.is_dashing_ground and not mob.a_dash and not mob.is_sliding_ground and not mob.is_grabing_edge and not mob.is_jumping_edge and not mob.is_attacking and not mob.is_dashing_attacking and time.time() - mob.timers["timer_roll"] > mob.cooldown_roll :
                mob.debut_roll(dir)

def pressed_heavy_attack(liste_mob, collision, left, right):
    for mob in liste_mob:
        if not mob.is_aiming:
            if "dash_attack" in mob.actions:
                mob.save_location()
                # if collision.stop_if_collide(mob.direction, mob, move_back=True) and not bool:
                #     if not collision.joueur_sur_sol(mob) and not mob.is_grabing_edge: collision.check_grab(mob, mob.direction)
                #     mob.timers["timer_dash_attack"]=time.time()
                bool_=mob.action=="Wall_slide" and ((mob.direction_wall == "left" and right) or (mob.direction_wall == "right" and left))
                wall=collision.stop_if_collide(mob.direction, mob, dash=True, dontmove=True)
                if (bool_ or not wall) and not (mob.is_grabing_edge and not bool_) \
                    and not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_dashing_attacking and not mob.is_dashing and not mob.is_jumping and not mob.is_jumping_edge and bool and not "hurt" in mob.action_image and not mob.is_parying and time.time()-mob.timers["timer_dash_attack"] > mob.cooldown_dash_attack:
                    if bool_: mob.timers["timer_debut_dash_attack_grabedge"]=time.time()
                    if mob.is_grabing_edge:
                        if mob.direction_wall == "left": direc="right"
                        else:direc="left"
                        mob.fin_grab_edge()
                    elif left:
                        direc="left"
                    elif right:
                        direc="right"
                    else:
                        direc=""

                    if mob.is_sliding_ground:
                        mob.fin_slide_ground()
                    
                    mob.debut_dash_attack(direc)
                    if not wall:
                        mob.update_rect()
                        if collision.stop_if_collide(mob.direction, mob, dash=True, dontmove=True):
                            mob.timers["timer_debut_dash_attack_grabedge"]=time.time()
                
def pressed_down(liste_mob, collision):
    for mob in liste_mob:
        if not mob.is_dashing_attacking:
            # le joueur passe a travers les plateformes pendant X secondes
            mob.timers["t1_passage_a_travers_plateforme"] = time.time()
        if mob.action != "Edge_climb" and mob.action != "Wall_slide" and mob.is_grabing_edge and "Wall_slide" in mob.actions:
            mob.debut_wallslide()
        else:
            if time.time() - mob.timers["timer_fin_crouch"] >mob.cooldown_crouch_pressed and "crouch" in mob.actions and collision.joueur_sur_sol(mob) and not mob.is_rolling and not mob.is_dashing and not mob.is_dashing_ground and not mob.is_sliding_ground and not mob.is_jumping and not mob.is_jumping_edge and not mob.is_attacking and not mob.is_dashing_attacking and not "hurt" in mob.action_image:
                if not mob.action=="crouch":
                    mob.debut_crouch(pressed=True)
                else:
                    mob.fin_crouch()
        
def handle_input_ralentissement(mob,collision):
    # si le joueur avance pas, il deviens idle
    
    if not mob.is_dashing_attacking and mob.action != "fall" and mob.action != "up_to_fall" and not mob.is_sliding_ground and not mob.is_dashing and not mob.is_rolling and not mob.is_grabing_edge :
        bool=collision.stop_if_collide(mob.direction, mob)
        if not bool and mob.action == "run" and mob.ralentit_bool == False:
            mob.debut_ralentissement()
        # si mob.ralentissement na pas ete appele, mob.ralentissement aura aucun effet
        # => donc le ralentissement a lieu que quand le joueur arrete de courir
        if not bool :
            mob.ralentissement()
        if (mob.ralentit_bool or mob.action_image == "run") and bool:
            mob.ralentit_bool = False
            if mob.action_image == "run":
                mob.change_direction("idle", mob.direction)

def pressed_interact(liste_mob, group_object):
    for mob in liste_mob:
        if mob.id=='player1':
            for sprite in group_object:
                if sprite.rect.collidelist([mob.body]) > -1:
                    return sprite.id

def handle_take_damage(mob, collision, group_projectile):
    if not "hurt" in mob.action_image:
        mob.take_damage()
    if mob.health <=0:
        mob.start_dying(collision.joueur_sur_sol(mob, change_pos=False), group_projectile)     

def handle_is_attacking(attacking_mob, get_all_mob, collision, group_projectile):
    if attacking_mob.is_dashing_attacking or attacking_mob.current_image in attacking_mob.attack_damage[attacking_mob.action_image][0]:
        for mob in [tuple[0] for tuple in get_all_mob()]:
            if mob.id != attacking_mob.id and mob.is_mob != attacking_mob.is_mob and (not "roll" in mob.actions or not mob.is_rolling):
                dash_attack_image=None
                if attacking_mob.is_dashing_attacking and len(attacking_mob.group_dash_attack_image_player.sprites())>0:
                    dash_attack_image = attacking_mob.group_dash_attack_image_player.sprites()[0]
                if (attacking_mob.is_dashing_attacking and dash_attack_image != None and mob.body.collidelist([dash_attack_image.body]) > -1) or (mob.body.collidelist([attacking_mob.rect_attack]) > -1 or (attacking_mob.has_air_attack and mob.body.collidelist([attacking_mob.rect_air_attack]) > -1)) and not "dying" in mob.action_image:
                    if not mob.is_parying or attacking_mob.is_dashing_attacking:
                        if attacking_mob.is_dashing_attacking: mob.health -= attacking_mob.dash_attack_damage
                        else :mob.health -=  attacking_mob.attack_damage[attacking_mob.action_image][1]
                        handle_take_damage(mob, collision, group_projectile)
                    else:
                        attacking_mob.take_damage()
                        mob.is_parying=False
                        if not mob.is_falling:
                            mob.change_direction("idle", mob.direction)
                        else:
                            mob.change_direction("up_to_fall", mob.direction)

def gestion_chute(mob, collision):
    # si le j saut ou dash la chute prends fin
    if (mob.is_jumping or mob.is_dashing or mob.is_rolling) and mob.is_falling:
        mob.fin_chute(jump_or_dash = True) 
    
    # si le joueur n'est pas sur un sol et ne chute pas on commence la chute
    if (not "player" in mob.id and not collision.joueur_sur_sol(mob)) or ("player" in mob.id and not mob.update_pieds_sur_sol(collision.joueur_sur_sol(mob))):
        if mob.action_image != "air_hurt" and mob.action != "Edge_climb" and not mob.is_falling and not mob.is_jumping and not mob.is_dashing and not mob.is_grabing_edge and not mob.is_jumping_edge:
            if mob.is_attacking or mob.is_dashing_attacking or mob.is_rolling or mob.is_sliding_ground or mob.is_dashing_ground:
                mob.debut_chute(attack=True)
            else:
                mob.debut_chute()
        
    elif mob.action_image == "air_hurt":
        mob.fin_chute(jump_or_dash=True)
        mob.action_image = "hurt"
        mob.action="idle"
    elif mob.action_image == "air_dying":
        mob.fin_chute(jump_or_dash=True)
        mob.action_image = "dying"
        mob.action="idle"
    else:
        # sinon on stop la chute si il y en a une
        if mob.is_falling:
            mob.fin_chute()

def handle_aim(liste_mob):
    for mob in liste_mob:
        mob.is_aiming=not mob.is_aiming
        mob.change_direction(mob.action_image, mob.direction, compteur_image=mob.compteur_image, current_image=mob.current_image)

def handle_change_weapon(liste_mob):
    for mob in liste_mob:
        if mob.can_change_weapon and time.time()-mob.timers["timer_change_weapon"] > mob.cooldown_change_weapon:
            mob.change_weapon()
            mob.change_direction(mob.action_image, mob.direction, compteur_image=mob.compteur_image, current_image=mob.current_image)