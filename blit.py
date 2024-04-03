import pygame
from pygame.locals import *
from sprite.map.textSprite import TextSprite
from sprite.map.toucheSprite import ToucheSprite
from sprite.entities.pp import Profile_picture

class Blit:
    def __init__(self, zoom, screen, bg, minimap, player):
        self.scroll=[0,0]
        self.scroll_rect = Rect(player.position[0],player.position[1],1,1)
        self.radiusL=80
        self.radiusLInc=40
        self.zoom=zoom
        self.screen=screen
        self.bg=bg
        self.minimap=minimap
        self.pp=Profile_picture(50, screen.get_height() - 100, pygame.image.load("assets\\pp\\Hearts\\Hearts\\Red Heart\\Idle\\Red\\heart_1.png").convert_alpha(), pygame.image.load("assets\\pp\\Hearts\\Hearts\\Red Heart\\Idle\\Red\\heart_2.png").convert_alpha(), player.play_random_sound, player)

    def update_camera(self, playerx, playery, player_speed_dt, player_rect_width):
        self.scroll[0] = ((playerx + player_rect_width/2 - self.scroll_rect.x) // 15)*self.zoom*player_speed_dt
        self.scroll_rect.x += self.scroll[0] 
        self.scroll[1] = ((playery - self.scroll_rect.y) // 15)*self.zoom*player_speed_dt
        self.scroll_rect.y += self.scroll[1] 
        # if self.scroll_rect.x < self.screen.get_width()/2 : self.scroll_rect.x = self.screen.get_width()/2
        # if self.scroll_rect.y < self.screen.get_height()/2 : self.scroll_rect.y = self.screen.get_height()/2
        # if self.scroll_rect.x > self.map_width - self.screen.get_width()/2 : self.scroll_rect.x = self.map_width - self.screen.get_width()/2
        # if self.scroll_rect.y > self.map_height - self.screen.get_height()/2 : self.scroll_rect.y = self.map_height - self.screen.get_height()/2   
    
    def spawn_phrase(self, name, x, y):
        """creer des objets des classes TextSprite et ToucheSprite pour afficher des phrases à l'écran
        en fonction d'objet spawn dans la map tiled sous la forme :
        0nom;1;nom => 0 : on creer TextSprite; 1 => on creer ToucheSprite """
        text_id = name.split(";")
        # the first element can be an special id that will allow us to do a special sentence
        for id in text_id[1:]:
            # c'est un text
            if id[0] == "0":
                self.all_text.append(TextSprite(x, y, id[1::], self.directory, self.zoom))
                x += self.all_text[-1].image.get_width() + 15*self.zoom
            elif id[0] == "1":
                self.all_text.append(ToucheSprite(x, y, id[1::], self.directory, self.zoom))
                x += self.all_text[-1].image.get_width() + 15*self.zoom
    
    def update_coordonee_bg(self, player_position_copy):
        if player_position_copy[0] < self.background.coordsX[1]:
            self.background.move("gauche")
        elif player_position_copy[0] > self.background.coordsX[1] + self.background.width:
            self.background.move("droite")
            
        if player_position_copy[0] < self.background.coordsXWater[1]:
            self.background.moveWater("gauche")
        elif player_position_copy[0] > self.background.coordsXWater[1] + self.background.width:
            self.background.moveWater("droite")
    
    def blit_background(self, bg,last_player_position, player_position_copy, player_direction):
        """update tous les elements du bg et le blit ensuite sur bg"""
        bg.fill(pygame.Color(0,0,0,0))
        self.background.update_speed(last_player_position, player_position_copy, player_direction)
        self.background.update()
        
        # couleur de fond blit partout sur lecran
        bg.blit(self.background.images["additionalSky"], (0,0))
        bg.blit(self.background.images["additionalWater"], (0,self.screen.get_height()/2 + self.background.y - self.scroll_rect.y))
        
        self.update_coordonee_bg(player_position_copy)
        new_y = self.screen.get_height()/2 + self.background.y  - self.background.height - self.scroll_rect.y
        for i in range(3):
            new_x = self.screen.get_width()/2 + self.background.coordsX[i] - self.scroll_rect.x
            bg.blit(self.background.images["bg_image"], (new_x, new_y))
        
        new_y = self.screen.get_height()/2 + self.background.y  - self.background.height_imageWaterReflexion - self.scroll_rect.y - 50*self.zoom
        for i in range(3):
            new_x = self.screen.get_width()/2 + self.background.coordsXWater[i] - self.scroll_rect.x
            bg.blit(self.background.imageWaterReflexion, (new_x, new_y))
        
        for obj in self.background.all_obj:
            if obj.type=='clouds':
                obj.verif_coords([self.scroll_rect.x, self.scroll_rect.y])
                for cloud in obj.objList.values():
                    for tu in cloud["coords"]: 
                        new_x = self.screen.get_width()/2 + tu[0] - self.scroll_rect.x
                        new_y = self.screen.get_height()/2 + tu[1] - self.scroll_rect.y
                        bg.blit(cloud["image"], (new_x, new_y))      
    
    def blit_health_bar(self, bg):
        self.pp.update()
        bg.blit(self.pp.image, self.pp.position)
    
    def blit_texte(self, bg):
        """blit les images des textes sur la surface bg"""
        for texte in self.all_text:
            texte.update()
            if self.scroll_rect.x - (self.screen.get_width()/2) - texte.image.get_width() <= texte.position[0] <= self.scroll_rect.x + (self.screen.get_width()/2)  + texte.image.get_width() and \
                self.scroll_rect.y - (self.screen.get_height()/2) - texte.image.get_height() <= texte.position[1] <= self.scroll_rect.y + (self.screen.get_height()/2)  + texte.image.get_height():
                    new_x = self.screen.get_width()/2 + texte.position[0] - self.scroll_rect.x
                    new_y = self.screen.get_height()/2 + texte.position[1] - self.scroll_rect.y
                    bg.blit(texte.image, (new_x,new_y))

    def blit_group(self, bg, all_groups):
        """blit les images des sprites des groupes sur la surface bg"""
        all_coords_mobs_screen = []
        all_coords_particule = []
        for group in all_groups:
            for sprite in group.sprites():
                if self.scroll_rect.x - (self.screen.get_width()/2) - sprite.image.get_width() <= sprite.position[0] <= self.scroll_rect.x + (self.screen.get_width()/2)  + sprite.image.get_width() and \
                    self.scroll_rect.y - (self.screen.get_height()/2) - sprite.image.get_height() <= sprite.position[1] <= self.scroll_rect.y + (self.screen.get_height()/2)  + sprite.image.get_height():
                        new_x=self.screen.get_width()/2 + sprite.position[0] - self.scroll_rect.x
                        new_y = self.screen.get_height()/2 + sprite.position[1] - self.scroll_rect.y
                        if "particule" not in sprite.id: 
                            if "arbre" in sprite.id :new_x = self.screen.get_width()/2 + sprite.position[0] - self.scroll_rect.x - sprite.image.get_width()/2

                            if "player" in sprite.id: 
                                new_x_=self.screen.get_width()/2 + sprite.body.centerx - self.scroll_rect.x  
                                new_y_ = self.screen.get_height()/2 + sprite.body.centery - self.scroll_rect.y 
                                all_coords_mobs_screen.append((new_x_, new_y_, 3))
                            elif "crab" in sprite.id:
                                new_x_ = self.screen.get_width()/2 + sprite.body.centerx - self.scroll_rect.x  
                                new_y_ = self.screen.get_height()/2 + sprite.body.centery - self.scroll_rect.y 
                                nbr = 3
                                for co in all_coords_mobs_screen:
                                    if new_x_-(self.radiusL) <= co[0] <= new_x_+(self.radiusL) and new_y_-(self.radiusL) <= co[1] <= new_y_+(self.radiusL) : 
                                        nbr=0
                                        break
                                    elif new_x_-(self.radiusL+self.radiusLInc) <= co[0] <= new_x_+(self.radiusL+self.radiusLInc) and new_y_-(self.radiusL+self.radiusLInc) <= co[1] <= new_y_+(self.radiusL+self.radiusLInc) : nbr=min(nbr, 1)
                                    elif new_x_-(self.radiusL+self.radiusLInc*2) <= co[0] <= new_x_+(self.radiusL+self.radiusLInc*2) and new_y_-(self.radiusL+self.radiusLInc*2) <= co[1] <= new_y_+(self.radiusL+self.radiusLInc*2) : nbr=min(nbr, 2)
                                if nbr>0:
                                    all_coords_mobs_screen.append((new_x_, new_y_, nbr))
                        else: 
                            new_x_=self.screen.get_width()/2 + sprite.rect.centerx - self.scroll_rect.x  
                            new_y_ = self.screen.get_height()/2 + sprite.rect.centery - self.scroll_rect.y 
                            bool=False
                            for co in all_coords_mobs_screen:
                                if new_x_-5 <= co[0] <= new_x_+5 and new_y_-5 <= co[1] <= new_y_+5 : bool=True
                            if not bool:all_coords_particule.append((new_x_, new_y_, sprite.rect.w*2))
                        bg.blit(sprite.image, (new_x,new_y))
        return all_coords_mobs_screen, all_coords_particule

    def circle_surf(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def add_lightning(self, surface, all_coords_mobs_screen, all_coords_particule):
        for co in all_coords_mobs_screen:
            for i in range(co[2]):
                r=self.radiusL+self.radiusLInc*i
                surface.blit(self.circle_surf(r, (4,3,3)), (int(co[0] - r), int(co[1] - r)), special_flags=BLEND_RGB_ADD)
        for co in all_coords_particule:
            surface.blit(self.circle_surf(co[2], (15, 7, 7)), (int(co[0] - co[2]), int(co[1] - co[2])), special_flags=BLEND_RGB_ADD)