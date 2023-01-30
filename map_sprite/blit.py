import pygame
from pygame.locals import *
from .arbre import Arbre
from .background import Background
from .textSprite import TextSprite
from .toucheSprite import ToucheSprite

class Blit:
    def __init__(self, map, directory, zoom, group_arbre, screen, playerx, playery, map_height, map_width):
        # chaque element de walls / etc est sous la forme : [x, y, [rect]]
        self.image_pp=pygame.image.load(f'{directory}\\assets\\pp.png').convert_alpha()
        self.map_height=map_height
        self.map_width=map_width
        self.screen=screen
        self.directory=directory
        self.zoom=zoom
        self.all_text = []
        self.all_arbre=[]
        self.group_arbre=group_arbre
        for obj in map.tm.objects:
            if obj.type == 'spawn_phrase':
                self.spawn_phrase(obj.name, obj.x * self.zoom , obj.y * self.zoom )
            elif obj.type =="spawn":
                if obj.name=="spawn_background":
                    self.background = Background(obj.x * self.zoom , obj.y * self.zoom, directory, self.zoom, self.screen.get_width(), self.screen.get_height())
                elif 'spawn_arbre' in obj.name:
                    a=Arbre(obj.x* self.zoom, obj.y* self.zoom,obj.name[-1], directory, self.zoom)
                    self.group_arbre.add(a)
                    self.all_arbre.append([a.rect.x, a.rect.y, [a.rect]])
        # gestion camera
        self.scroll=[0,0]
        self.scroll_rect = Rect(playerx,playery,1,1)

    def update_camera(self, playerx, playery, player_speed_dt):
        self.scroll[0] = ((playerx - self.scroll_rect.x) // 15)*self.zoom*player_speed_dt
        self.scroll_rect.x += self.scroll[0] 
        self.scroll[1] = ((playery - self.scroll_rect.y) // 15)*self.zoom*player_speed_dt
        self.scroll_rect.y += self.scroll[1] 
        if self.scroll_rect.x < self.screen.get_width()/2 : self.scroll_rect.x = self.screen.get_width()/2
        if self.scroll_rect.y < self.screen.get_height()/2 : self.scroll_rect.y = self.screen.get_height()/2
        if self.scroll_rect.x > self.map_width - self.screen.get_width()/2 : self.scroll_rect.x = self.map_width - self.screen.get_width()/2
        if self.scroll_rect.y > self.map_height - self.screen.get_height()/2 : self.scroll_rect.y = self.map_height - self.screen.get_height()/2  
    
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
    
    def blit_health_bar(self, bg, all_mobs):
        i=1
        for mob in all_mobs:
            bg.blit(self.image_pp, (10*self.zoom, self.screen.get_height() - self.image_pp.get_height()*i - 15*self.zoom*i))
            new_x = 10*self.zoom+100/(mob.max_health/(mob.health+1))
            new_y = self.screen.get_height() - 12.5*self.zoom*(i+1) -self.image_pp.get_height()*i
            pygame.draw.line(bg, (255,0,0), (10*self.zoom, new_y), (new_x, new_y), 2*self.zoom)
            i+=1
    
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
        for group in all_groups:
            for sprite in group.sprites():
                if self.scroll_rect.x - (self.screen.get_width()/2) - sprite.image.get_width() <= sprite.position[0] <= self.scroll_rect.x + (self.screen.get_width()/2)  + sprite.image.get_width() and \
                    self.scroll_rect.y - (self.screen.get_height()/2) - sprite.image.get_height() <= sprite.position[1] <= self.scroll_rect.y + (self.screen.get_height()/2)  + sprite.image.get_height():
                        if "arbre" in sprite.id :new_x = self.screen.get_width()/2 + sprite.position[0] - self.scroll_rect.x - sprite.image.get_width()/2
                        else:new_x=self.screen.get_width()/2 + sprite.position[0] - self.scroll_rect.x
                        
                        new_y = self.screen.get_height()/2 + sprite.position[1] - self.scroll_rect.y
                        bg.blit(sprite.image, (new_x,new_y))
                        
                        if sprite.id == "arbre1":
                            new_x += sprite.image.get_width()/2 - sprite.images["Bot"].get_width()/2 +2*self.zoom
                            new_y = self.screen.get_height()/2 + sprite.position[1] - self.scroll_rect.y - sprite.image.get_height() + sprite.images["Bot"].get_height() + 8*self.zoom
                            bg.blit(sprite.images["Bot"], (new_x,new_y))
                        
                        elif sprite.id == "arbre2":
                            new_x += sprite.image.get_width()/2 -7*self.zoom
                            new_y = self.screen.get_height()/2 + sprite.position[1] - self.scroll_rect.y + sprite.image.get_height()/2 + sprite.images["Bot"].get_height() - 10*self.zoom
                            bg.blit(sprite.images["Bot"], (new_x,new_y))
                        
                        elif sprite.id == "arbre3":
                            new_x += -sprite.images["Bot"].get_width()/2 - 0*self.zoom
                            new_y = self.screen.get_height()/2 + sprite.position[1] - self.scroll_rect.y + sprite.image.get_height()/2 + sprite.images["Bot"].get_height() - 12*self.zoom
                            bg.blit(sprite.images["Bot"], (new_x,new_y))