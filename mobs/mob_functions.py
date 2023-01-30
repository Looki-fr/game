import time

def pressed_left(liste_mob, collision):
    for mob in liste_mob:
        if "slide_ground" in mob.actions:
            if mob.is_sliding_ground and mob.slide_ground_direction_x == 'right':
                mob.fin_slide_ground()
        if not mob.is_jumping_edge and not mob.is_grabing_edge and not mob.is_sliding_ground and not mob.is_dashing and not mob.is_dashing_attacking:
            mob.save_location()
            bool = collision.joueur_sur_sol(mob)
            if bool:
                mob.move_left(pieds_sur_sol=True)
            # si le joueur ne dash pas et est en lair
            else:
                mob.move_left()
            if collision.stop_if_collide("left", mob) and not bool and not mob.is_jumping:
                collision.check_grab(mob)

def pressed_right(liste_mob, collision):
    for mob in liste_mob:
        if "slide_ground" in mob.actions:
            if mob.is_sliding_ground and mob.slide_ground_direction_x == 'left':
                mob.fin_slide_ground()
        if not mob.is_jumping_edge and not mob.is_grabing_edge and not mob.is_sliding_ground and not mob.is_dashing and not mob.is_dashing_attacking:
            mob.save_location()
            bool = collision.joueur_sur_sol(mob)
            if bool:
                mob.move_right(pieds_sur_sol=True)
            # si le joueur ne dash pas et est en lair
            else:
                mob.move_right()
            if collision.stop_if_collide("right", mob) and not bool and not mob.is_jumping:
                collision.check_grab(mob)
                
def pressed_up(liste_mob, down, left, right, pressed_up_bool, collision):
    for mob in liste_mob:
        if "jump_edge" in mob.actions:
            if not pressed_up_bool[0]:
                dir_x = ""
                if left:
                    dir_x = "left"
                elif right:
                    dir_x = "right"
                if pressed_up_bool[0] == False and mob.is_grabing_edge and not mob.is_dashing_attacking and (( collision.joueur_se_cogne(mob) and not collision.check_pieds_collide_wall(mob)) or not collision.joueur_se_cogne(mob)):
                    mob.fin_grab_edge()
                    # si les pieds sont sur le mur des particles apparaissent
                    if collision.check_pieds_collide_wall(mob):
                        if mob.is_parying:
                            mob.is_parying=False
                        mob.debut_saut_edge(direction_x=dir_x)
                        mob.particule.pieds_collide_jump_edge = True
                    else:
                        mob.debut_saut_edge(direction_x=dir_x)
                        mob.particule.pieds_collide_jump_edge = False
                # pressed_up sert à savoir si le joueur viens d'appyuer sur la touche
                # il pourrait juste rester appuyer       
                pressed_up_bool[0] = True
            else:
                pressed_up_bool[0] = False
        if not down and (collision.joueur_sur_sol(mob) or time.time() - mob.timer_cooldown_able_to_jump < mob.cooldown_able_to_jump) \
            and not mob.a_sauter and not mob.is_jumping_edge\
            and time.time() - mob.timer_cooldown_next_jump > mob.cooldown_next_jump \
            and not mob.is_jumping_edge and not mob.is_dashing and not mob.is_attacking and not mob.is_dashing_attacking \
                and not mob.action_image=="hurt" and not mob.is_parying:
            if mob.is_sliding_ground:
                mob.fin_slide_ground()
            mob.debut_saut()

def pressed_dash(liste_mob, left, right, down, up, joueur_sur_sol, zoom):
    for mob in liste_mob:
        if 'dash' in mob.actions:
            if not mob.is_jumping and not mob.is_dashing and not mob.a_dash and not mob.is_sliding_ground and not mob.is_grabing_edge and not mob.is_jumping_edge and not mob.is_attacking and not mob.is_dashing_attacking :           
                if not joueur_sur_sol(mob):
                    if mob.is_parying:
                        mob.is_parying=False
                    dir_y = ""
                    dir_x = ""
                    if down:dir_y = "down"
                    if up:dir_y = "up"
                    if right:dir_x = "right"
                    if left:dir_x = "left"
                    if dir_y == "" and dir_x == "":dir_y = "up"
                    mob.debut_dash(dir_x, dir_y)         
                elif down and time.time() - mob.timer_cooldown_slide_ground > mob.cooldown_slide_ground : 
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
            if (not mob.is_jumping or mob.can_attack_while_jump) and not mob.is_jumping_edge and not mob.is_dashing and not mob.is_attacking and not mob.is_grabing_edge and not mob.is_parying and not mob.is_dashing_attacking and not mob.action_image=="hurt":
                if mob.is_sliding_ground:
                    mob.fin_slide_ground()
                if (not mob.is_falling and not mob.action == "jump") or not mob.has_air_attack:
                    if "player" in mob.id and time.time()-mob.timer_attack < mob.cooldown_attack and not mob.a_attaquer2:
                        mob.attack2()
                    else:
                        mob.debut_attack()
                # elif time.time() - mob.timer_attack_aerienne > mob.cooldown_attack_aerienne:
                #     mob.debut_attack(fast=True)

def pressed_pary(liste_mob):
    for mob in liste_mob:
        if "pary" in mob.actions:
            if not mob.is_jumping and not mob.is_jumping_edge and not mob.is_dashing and not mob.is_attacking and not mob.is_grabing_edge and not mob.is_dashing_attacking and time.time()-mob.timer_pary>mob.cooldown_pary and not mob.action_image=="hurt":
                if mob.is_sliding_ground:
                    mob.fin_slide_ground()
                if not mob.is_parying:
                    mob.debut_pary()

def pressed_heavy_attack(liste_mob):
    for mob in liste_mob:
        if "dash_attack" in mob.actions:
            if not mob.is_dashing_attacking and not mob.is_dashing and not mob.is_jumping and not mob.is_jumping_edge and not mob.is_grabing_edge and not mob.action_image=="hurt" and not mob.is_parying:
                if mob.is_sliding_ground:
                    mob.fin_slide_ground()
                mob.debut_dash_attack()
                
def pressed_down(liste_mob):
    for mob in liste_mob:
        if not mob.is_dashing_attacking:
            # le joueur passe a travers les plateformes pendant X secondes
            mob.t1_passage_a_travers_plateforme = time.time()
        
def handle_input_ralentissement(mob):
    # si le joueur avance pas, il deviens idle
    if mob.action != "fall" and mob.action != "up_to_fall" and not mob.is_sliding_ground and not mob.is_dashing_attacking:
        if mob.action == "run" and mob.ralentit_bool == False:
            mob.debut_ralentissement()
        # si mob.ralentissement na pas ete appele, mob.ralentissement aura aucun effet
        # => donc le ralentissement a lieu que quand le joueur arrete de courir
        mob.ralentissement()
        
def pressed_interact(liste_mob, group_object):
    for mob in liste_mob:
        if mob.id=='player1':
            for sprite in group_object:
                if sprite.rect.collidelist([mob.body]) > -1:
                    return sprite.id