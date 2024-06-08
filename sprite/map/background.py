import os
import pygame
from pygame.locals import *     

class Clouds():
    """class that contain all the necessaries informations about clouds"""
    def __init__(self,x,y,directory,zoom):
        self.zoom = zoom
        
        self.type="clouds"
        
        self.objList={}
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # IMPORTANT : mettre les obj par odre de blit                 #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        
        # they are 3 differents images for clouds
        # all the y of clouds are increased by c, so they have are 80 pixels away from each others
        c=100
        for i in range(1,4):
            #small cloud
            image=pygame.image.load(os.path.join(directory,"assets","TreasureHunters","PalmTreeIsland","Sprites","Background","Small_Cloud_{i}.png"))
            self.objList[f"SmallCloud{i}"]={
                "originalSpeed":1 if i == 1 else 1.2 if i == 2 else 1.4 ,
                "speed":2 if i == 1 else 1.4 if i == 2 else 1,
                "image":pygame.transform.scale(image, (image.get_width()*self.zoom*2, image.get_height()*self.zoom*2)),
            }
            # the width is increased so the clouds are not to close
            self.objList[f"SmallCloud{i}"]["width"]=self.objList[f"SmallCloud{i}"]["image"].get_width() + (300 if i == 1 else 250 if i == 2 else 400)*self.zoom
            self.objList[f"SmallCloud{i}"]["height"]=self.objList[f"SmallCloud{i}"]["image"].get_height()
            self.objList[f"SmallCloud{i}"]["coords"]=[
                [ x - c*self.zoom - self.objList[f"SmallCloud{i}"]["width"], y -80*self.zoom- c*self.zoom - self.objList[f"SmallCloud{i}"]["height"]],
                [ x - c*self.zoom ,  y -80*self.zoom- c*self.zoom - self.objList[f"SmallCloud{i}"]["height"]],
                [ x - c*self.zoom  + self.objList[f"SmallCloud{i}"]["width"], y -80*self.zoom- c*self.zoom- self.objList[f"SmallCloud{i}"]["height"]]
            ]
            c+=80
        
        #big clouds
        image=pygame.image.load(os.path.join(directory,"assets","TreasureHunters","PalmTreeIsland","Sprites","Background","BigClouds.png")).convert_alpha()
        self.objList["BigClouds"]={
            "originalSpeed":1.25,
            "speed":1.25,
            "image":pygame.transform.scale(image, (round(image.get_width()*self.zoom*1.5), round(image.get_height()*self.zoom*1.5))).convert_alpha(),
            "random":'no'
        }
        # 84*self.zoom is the height of the water part of the background image
        self.objList["BigClouds"]["width"]=self.objList["BigClouds"]["image"].get_width()
        self.objList["BigClouds"]["height"]=self.objList["BigClouds"]["image"].get_height()
        self.objList["BigClouds"]["coords"]=[
            [ x-self.objList["BigClouds"]["width"], y - 84*self.zoom - self.objList["BigClouds"]["height"] ],
            [ x,y - 84*self.zoom - self.objList["BigClouds"]["height"] ],
            [ x+self.objList["BigClouds"]["width"], y - 84*self.zoom - self.objList["BigClouds"]["height"]]
        ]  
        
    def update(self, speed_dt):
        for objList in self.objList.values():
            for tu in objList["coords"]:
                tu[0] -= objList["speed"]*speed_dt
    
    def verif_coords(self,position):
        """for every clouds, if the player is on the left or on the right cloud, we moves all the clouds so the player will be on the middle one
        it permit the background to have an infinite scrolling"""
        for cloud in self.objList.values():
            if position[0] < cloud["coords"][1][0]:
                cloud["coords"][1][0] -= cloud["width"]
            elif position[0] > cloud["coords"][1][0] + cloud["width"]:
                cloud["coords"][1][0] += cloud["width"]
            cloud["coords"][0][0] = cloud["coords"][1][0] - cloud["width"]
            cloud["coords"][2][0] = cloud["coords"][1][0] + cloud["width"]
                     
class Background():
    def __init__(self, x, y, directory, zoom, screen_width, screen_height):
        self.images={}
        self.zoom = zoom
        self.dt = 17
        self.speed_dt = round(self.dt/17)
        
        self.all_obj=[Clouds(x, y, directory, zoom)]
        
        # image of the sky / the water
        self.images["bg_image"]=pygame.image.load(os.path.join(directory,"assets","TreasureHunters","PalmTreeIsland","Sprites","Background","BG_Image.png")).convert()
        self.images["bg_image"]=pygame.transform.scale(self.images["bg_image"], (round(self.images["bg_image"].get_width()*self.zoom*2), round(self.images["bg_image"].get_height()*self.zoom*2))).convert()   
        
        self.y = y
        
        self.width=self.images["bg_image"].get_width()
        self.height=self.images["bg_image"].get_height()
        
        self.coordsX=[x-self.width, x, x+self.width]
        
        # image of the size of the screen that only the color of the sky
        self.images["additionalSky"]=pygame.image.load(os.path.join(directory,"assets","TreasureHunters","PalmTreeIsland","Sprites","Background","AdditionalSky.png")).convert()
        self.images["additionalSky"]=pygame.transform.scale(self.images["additionalSky"], (screen_width, screen_height)).convert()
        
        self.images["additionalWater"]=pygame.image.load(f'{directory}","assets","TreasureHunters","PalmTreeIsland","Sprites","Background","AdditionalWater.png').convert()
        self.images["additionalWater"]=pygame.transform.scale(self.images["additionalWater"], (screen_width, screen_height)).convert()
        
        # water reflexion animation
        self.images["WaterReflexion"]={
            "nbr_image":4,
            "compteur_image_max":4,
            "image":{}
        }
        for i in range(1,5):
            self.images["WaterReflexion"]["image"][str(i)] = pygame.image.load(os.path.join(directory,"assets","TreasureHunters","PalmTreeIsland","Sprites","Background",f"WaterReflectBig{i}.png")).convert_alpha()
            self.images["WaterReflexion"]["image"][str(i)] = pygame.transform.scale(self.images["WaterReflexion"]["image"][str(i)], (self.images["WaterReflexion"]["image"][str(i)].get_width()*self.zoom*3, self.images["WaterReflexion"]["image"][str(i)].get_height()*self.zoom*3)).convert_alpha()
        
        self.compteur_image = 0
        self.current_image = 1
        self.imageWaterReflexion=self.images["WaterReflexion"]["image"]["1"]
        # we add 200*self.zoom so all the waters animations are not too close
        self.width_imageWaterReflexion = self.imageWaterReflexion.get_width() + 200*self.zoom
        self.height_imageWaterReflexion = self.imageWaterReflexion.get_height()
        
        self.coordsXWater=self.coordsX.copy()
        
    def update(self):
        for obj in self.all_obj:
            obj.update(self.speed_dt)
        self.update_animation()
    
    def move(self, direction):
        """move the three background image to the right / left so the player can move to infinity because
        they'll always be the image on the screen"""
        if direction == "gauche":
            self.coordsX[1] -= self.width
        elif direction == "droite":
            self.coordsX[1] +=  self.width
        self.coordsX[0] = self.coordsX[1] - self.width
        self.coordsX[2] = self.coordsX[1] + self.width
    
    def moveWater(self, direction):
        """move the three waters reflexions image to the right / left so the player can move to infinity because
        they'll always be the image on the screen"""
        if direction == "gauche":
            self.coordsXWater[1] -= self.width_imageWaterReflexion
        elif direction == "droite":
            self.coordsXWater[1] += self.width_imageWaterReflexion
        self.coordsXWater[0] = self.coordsXWater[1] - self.width_imageWaterReflexion
        self.coordsXWater[2] = self.coordsXWater[1] + self.width_imageWaterReflexion
        
    def update_speed(self, last_player_position, player_position, direction):
        # the water relfections images are moving a bit to the player as he move, its proportionnal to the speed of the player
        if direction == "right":
            c=last_player_position[0]/player_position[0] if player_position[0] != 0 else 1
        elif direction == "left":
            c=-last_player_position[0]/player_position[0] if player_position[0] != 0 else 1
        if c not in (-1,1):
            for i in range(3):
                self.coordsXWater[i]+=c*2*self.speed_dt
        # the speed of the clouds are getting greater as the player go to the right since the clouds go to the left
        # and are getting lower as the player go to the left
        for typeObj in self.all_obj:
            for obj in typeObj.objList.values():
                if -1<= player_position[0] <=1:
                    obj["speed"]=obj["originalSpeed"]/(round(last_player_position[0])/player_position[0])
                else:
                    obj["speed"]=obj["originalSpeed"]
    
    def update_animation(self):
        """change les animations de l'eau, appelé toutes les frames"""
        # changement de l'image tout les X ticks
        if self.compteur_image < self.images["WaterReflexion"]["compteur_image_max"]:
            self.compteur_image += 1*self.speed_dt
        else:
            # changement de l'image
            self.compteur_image = 0
            # si l'image en cours est la derniere on re passe a la 1ere, sinon on passe a la suivante
            if self.current_image < self.images["WaterReflexion"]["nbr_image"]:
                self.current_image += 1
            else:
                self.current_image = 1
            
            self.imageWaterReflexion = self.images["WaterReflexion"]["image"][str(self.current_image)]
    
    def update_tick(self, dt):
        """i created a multiplicator for the mouvements that based on 60 fps (clock.tick() = 17) because the original
        frame rate is 60, and so the mouvements are speeder when the game is lagging so when
        the game has a lower frame rate, same for animations but it doesnt work perfectly for animations"""
        self.dt = dt
        self.speed_dt = round(self.dt/17)