import time

def pressed_left(liste_mob, collision):
    for mob in liste_mob:
        if "ground_slide" in mob.actions and mob.is_sliding_ground and mob.slide_ground_direction_x == 'right':
            mob.fin_slide_ground()
        if not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping_edge and not mob.is_grabing_edge and not mob.is_sliding_ground and not mob.is_dashing and not mob.is_dashing_attacking:
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
        if "ground_slide" in mob.actions:
            if mob.is_sliding_ground and mob.slide_ground_direction_x == 'left':
                mob.fin_slide_ground()
        if not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping_edge and not mob.is_grabing_edge and not mob.is_sliding_ground and not mob.is_dashing and not mob.is_dashing_attacking:
            mob.save_location()
            bool = collision.joueur_sur_sol(mob)
            if bool:
                mob.move_right(pieds_sur_sol=True)
            # si le joueur ne dash pas et est en lair
            else:
                mob.move_right()
            if collision.stop_if_collide("right", mob) and not bool and not mob.is_jumping:
                collision.check_grab(mob, "right")

            #     if collide and not bool and not mob.is_jumping:
            #     collision.check_grab(mob)
            # elif collide:
            #     if "ground_slide" in mob.actions and mob.is_sliding_ground: mob.fin_slide_ground()
            #     if "roll" in mob.actions and mob.is_rolling: mob.fin_roll()
                
def pressed_up(liste_mob, down, left, right, pressed_up_bool, collision, zoom):
    for mob in liste_mob:
        if not collision.joueur_se_cogne(mob) and not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping_edge and not mob.is_dashing and not mob.is_attacking and not mob.is_dashing_attacking and not "hurt" in mob.action_image and not mob.is_parying:
            pieds=collision.check_pieds_collide_wall(mob)
            # cogne = collision.joueur_se_cogne(mob)
            #  and not cogne
            if "Edge_climb" in mob.actions and ((mob.direction=="right" and right) or (mob.direction=="left" and left) or (mob.direction=="right" and not left) or (mob.direction=="left" and not right)) and not pressed_up_bool[0] and collision.check_head_collide_ground(mob) and mob.is_grabing_edge:
                mob.position[1]-=20
                collision.check_head_collide_ground(mob, True)
                mob.fin_grab_edge()
                mob.debut_edge_climb()
            else:
                if "jump_edge" in mob.actions:
                    if not pressed_up_bool[0]:
                        dir_x = ""
                        if left:
                            dir_x = "left"
                        elif right:
                            dir_x = "right"
                        #  and (( cogne and not pieds) or not cogne)
                        if time.time()-mob.timer_jump_edge_cogne > mob.cooldown_jump_edge_cogne and mob.is_grabing_edge and time.time() - mob.timer_cooldown_next_jump > mob.cooldown_next_jump:
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
                if not down and (collision.joueur_sur_sol(mob) or time.time() - mob.timer_cooldown_able_to_jump < mob.cooldown_able_to_jump) and not mob.a_sauter and time.time() - mob.timer_cooldown_next_jump > mob.cooldown_next_jump*2:
                    if mob.is_sliding_ground:
                        mob.fin_slide_ground()
                    mob.debut_saut()
                    if collision.stop_if_collide(mob.direction, mob):
                        if mob.direction=="right":mob.position[0]-=5*zoom
                        else:mob.position[0]+=5*zoom

def pressed_dash(liste_mob, left, right, down, up, joueur_sur_sol, zoom, collision):
    for mob in liste_mob:
        if 'dash' in mob.actions:
            if not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping and not mob.is_dashing and not mob.a_dash and not mob.is_sliding_ground and not mob.is_jumping_edge and not mob.is_attacking and not mob.is_dashing_attacking:           
                if not joueur_sur_sol(mob):
                    if time.time() - mob.timer_dash > mob.cooldown_dash  and ((not mob.is_grabing_edge and not collision.stop_if_collide(mob.direction, mob, dash=True, dontmove=True)) or ( mob.is_grabing_edge and mob.direction_wall == "left" and right ) or ( mob.direction_wall == "right" and left )):
                        print(mob.timer_dash, time.time()-mob.timer_dash, mob.cooldown_dash)
                        if ( mob.direction_wall == "left" and right ) or ( mob.direction_wall == "right" and left ):
                            mob.timer_debut_dash_grabedge=time.time()
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
                elif down and not ((left and collision.stop_if_collide("left",mob, dontmove=True)) or (right and collision.stop_if_collide("right",mob, dontmove=True)))and time.time() - mob.timer_cooldown_slide_ground > mob.cooldown_slide_ground : 
                    if mob.is_parying:
                        mob.is_parying=False
                    if mob.is_falling: mob.fin_chute()
                    if left:
                        mob.debut_slide_ground("left")
                    elif right:
                        mob.debut_slide_ground("right")

def pressed_attack(liste_mob):
    for mob in liste_mob:
        if "attack" in mob.actions:
            if not mob.is_rolling and mob.action != "Edge_climb" and (not mob.is_jumping or mob.can_attack_while_jump) and not mob.is_jumping_edge and not mob.is_dashing and not mob.is_attacking and not mob.is_grabing_edge and not mob.is_parying and not mob.is_dashing_attacking and not "hurt" in mob.action_image:
                if mob.is_sliding_ground:
                    mob.fin_slide_ground()
                if (not mob.is_falling and not mob.action == "jump") or not mob.has_air_attack:
                    if "player" in mob.id and time.time()-mob.timer_attack < mob.cooldown_attack and not mob.a_attaquer2:
                        mob.attack2()
                    else:
                        mob.debut_attack()
                elif time.time() - mob.timer_attack_aerienne > mob.cooldown_attack_aerienne:
                    mob.debut_attack(air=True)

def pressed_pary(liste_mob, left, right, collision):
    for mob in liste_mob:
        if "pary" in mob.actions:
            if not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping and not mob.is_jumping_edge and not mob.is_dashing and not mob.is_attacking and not mob.is_grabing_edge and not mob.is_dashing_attacking and time.time()-mob.timer_pary>mob.cooldown_pary and not "hurt" in mob.action_image:
                if mob.is_sliding_ground:
                    mob.fin_slide_ground()
                if not mob.is_parying:
                    mob.debut_pary()
        if "roll" in mob.actions:
            if left: dir="left"
            elif right: dir="right"
            else: dir=mob.direction
            if not collision.stop_if_collide(dir,mob, dontmove=True) and not mob.is_falling and not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_jumping and not mob.is_dashing and not mob.a_dash and not mob.is_sliding_ground and not mob.is_grabing_edge and not mob.is_jumping_edge and not mob.is_attacking and not mob.is_dashing_attacking and time.time() - mob.timer_roll > mob.cooldown_roll :
                mob.debut_roll(dir)


def pressed_heavy_attack(liste_mob, collision, left, right):
    for mob in liste_mob:
        if "dash_attack" in mob.actions:
            mob.save_location()
            # if collision.stop_if_collide(mob.direction, mob, move_back=True) and not bool:
            #     if not collision.joueur_sur_sol(mob) and not mob.is_grabing_edge: collision.check_grab(mob, mob.direction)
            #     mob.timer_dash_attack=time.time()
            bool_=mob.action=="Wall_slide" and ((mob.direction_wall == "left" and right) or (mob.direction_wall == "right" and left))
            if (bool_ or not collision.stop_if_collide(mob.direction, mob, dash=True, dontmove=True)) and not (mob.is_grabing_edge and not bool_) \
                and not mob.is_rolling and mob.action != "Edge_climb" and not mob.is_dashing_attacking and not mob.is_dashing and not mob.is_jumping and not mob.is_jumping_edge and bool and not "hurt" in mob.action_image and not mob.is_parying and time.time()-mob.timer_dash_attack > mob.cooldown_dash_attack:
                if bool_: mob.timer_debut_dash_attack_grabedge=time.time()
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
                
def pressed_down(liste_mob):
    for mob in liste_mob:
        if not mob.is_dashing_attacking:
            # le joueur passe a travers les plateformes pendant X secondes
            mob.t1_passage_a_travers_plateforme = time.time()
        if mob.action != "Edge_climb" and mob.action != "Wall_slide" and mob.is_grabing_edge and "Wall_slide" in mob.actions:
            mob.debut_wallslide()
        
def handle_input_ralentissement(mob,collision):
    # si le joueur avance pas, il deviens idle
    
    if not mob.is_dashing_attacking and mob.action != "fall" and mob.action != "up_to_fall" and not mob.is_sliding_ground and not mob.is_dashing_attacking and not mob.is_rolling and not mob.is_grabing_edge :
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
                
def handle_is_attacking(attacking_mob, get_all_mob):
    if attacking_mob.is_dashing_attacking or attacking_mob.current_image in attacking_mob.attack_damage[attacking_mob.action_image][0]:
        for mob in [tuple[0] for tuple in get_all_mob()]:
            if mob.id != attacking_mob.id and mob.is_mob != attacking_mob.is_mob and (not "roll" in mob.actions or not mob.is_rolling):
                if (attacking_mob.is_dashing_attacking and attacking_mob.dash_attack_image != None and mob.body.collidelist([attacking_mob.dash_attack_image.body]) > -1) or (mob.body.collidelist([attacking_mob.rect_attack]) > -1 or (attacking_mob.has_air_attack and mob.body.collidelist([attacking_mob.rect_air_attack]) > -1)) and mob.action_image!="dying":
                    if not mob.is_parying or attacking_mob.is_dashing_attacking:
                        if attacking_mob.is_dashing_attacking: mob.health -= attacking_mob.dash_attack_damage
                        else :mob.health -=  attacking_mob.attack_damage[attacking_mob.action_image][1]

                        if not "hurt" in mob.action_image:
                            mob.take_damage()
                        if mob.health <=0:
                            mob.start_dying()

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
    if not collision.joueur_sur_sol(mob):
        if mob.action != "Edge_climb" and not mob.is_falling and not mob.is_jumping and not mob.is_dashing and not mob.is_grabing_edge and not mob.is_jumping_edge:
            if mob.is_attacking or mob.is_dashing_attacking or mob.is_rolling or mob.is_sliding_ground:
                mob.debut_chute(attack=True)
            else:
                mob.debut_chute()
    else:
        # sinon on stop la chute si il y en a une
        if mob.is_falling:
            mob.fin_chute()