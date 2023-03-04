from math import ceil
from map.graph import Graphe
import random
import pygame
from map.graph_generator import get_matrix

class RenderMap:
    def __init__(self, screen_width, screen_height, directory):
        """cf la documentation de pytmx"""
        self.directory=directory
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.graphe=get_matrix()

        self.minimap_tile_width=32            
        self.zoom=2
        self.tile_width=30*self.zoom
        self.room_width=self.tile_width*15
        self.room_height=self.tile_width*10
        
        self.increment=7*self.zoom
        self.increment_ground=30*self.zoom
        self.all_pic=[]
        self._init_all_pics()
        
        # value : dictionnary : keys : id of the tile value : image of the tile
        self.matrix_picture=[ [[] for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]

        # matrix map is used to load all the map objects
        self.matrix_map=[[None for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]
        
        # we dont start at 0 since the map as empty maps around it
        i=0; z=0
        for i,line in enumerate(self.graphe):
            for z,node in enumerate(line):
                    # E and S correspond to if the map has a neightboor on the right or on the bot
                self.load_map(node, i, z)
                # else:
                #     self.load_map("", i, z, empty=True)
                #     self.load_map("", i+self.tm.height, z, empty=True)
                #     self.load_map("", i, z+self.tm.width, empty=True)
                # just remove it and see what happened if you dont understand why we load this map
            
        
        self.minimap_picture=pygame.image.load(f"{directory}\\assets\\tiled_maps\\minimap.png")
        self.minimap_picture=pygame.transform.scale(self.minimap_picture, (self.minimap_tile_width,self.minimap_tile_width))
        self.minimap_tile=[[None for _ in range(len(self.graphe))] for _ in range(len(self.graphe[0]))]
        # for i, line in enumerate(self.graphe):
        #     for y, node in enumerate(line):
        #         if node != []: 
        #             self.minimap_tile[i][y]=self.minimap_picture
                    
        # self.current_map_objects={"walls":[], "grounds":[], "ceillings":[], "plateformes":[], "spawn_player":()}    
        # self.current_map=[]
        self.current_map_is_wave=False
        # self.coord_current_map=(0,0)
        # for _ in range(self.tm.height):
        #     self.current_map.append([])
        #     for _ in range(self.tm.width):
        #         self.current_map[-1].append(None)
        
        self.get_first_map()["info"]["beated"]=True
        
        # self.type_objects_map=[[None for _ in range(len(self.graphe.matrix_of_node[0])*2+2)] for _ in range(len(self.graphe.matrix_of_node)*2+2)]
        # differents_types_random=["wave","wave","wave", "fontain", "devil", "old_men", "secret", "trap"]
        # # at least one of those
        # pile_types=['trader', 'boss',"wave", "fontain", "devil", "old_men", "secret", "trap"]
        # c=self.get_first_map(index=True)
        # self.type_objects_map[c[0]][c[1]]="spawn"
        # liste=[]
        # for i, line in enumerate(self.matrix_map):
        #     for y,map in enumerate(line):
        #         if map != None and list((i,y))!=list(self.get_first_map(index=True)):
        #             liste.append((i,y))
        # random.shuffle(liste)
        # while len(liste)>0:
        #     if len(pile_types)>0:
        #         type_=pile_types.pop()
        #     else:
        #         type_=random.choice(differents_types_random)
        #     temp=liste.pop()
        #     self.type_objects_map[temp[0]][temp[1]]=type_
            
        # string=""
        # for line in self.type_objects_map:
        #     for obj in line:
        #         if obj != None:
        #             string+=obj+"-"*(7-len(obj))+" "
        #         else:
        #             string+="-"*7+" "
        #     string+="\n"
        # with open(f"{self.directory}\\map\\output\\objects_maps.txt", "w") as f:
        #     f.write(string)
    
    def _init_all_pics(self):
        pic=pygame.Surface((self.tile_width, self.tile_width))
        pic.fill((200,200,200))
        pic2=pygame.Surface((self.room_width, self.room_height))
        pic2.fill((200,200,200))
        self.all_pic.append(pic)
        self.all_pic.append(pic2)

    def get_height(self):
        """return the height of the map in coordonates"""
        # we remove the 2 empty map that are on the top and on the bot of the map
        return len(self.graphe)*self.room_height

    def get_width(self):
        """return the width of the map in coordonates"""
        # we remove the 2 empty map that are on the left and on the right of the map
        return len(self.graphe[0])*self.room_width
                    
    def get_first_map(self, index=False):
        """return the if of the map of spawn in  self.matrix_map"""
        for i, line in enumerate(self.matrix_map):
            for y, map in enumerate(line):
                if map != None:
                    if not index:
                        return map
                    else:
                        return (i,y)

    def load_map(self, node, i, z, empty=False):
        """call load_objects_map if the map is not empty and load all tiles for the map widht the coordinates i and z""" 

        self.matrix_map[i][z]={"wall":[], "ground":[], "ceilling":[], "platform":[],"bot":{"platform_right":[], "platform_left":[], "platform_go_right":[], "platform_go_left":[]}, "spawn_player":(), "object_map":(), "object_map":(), "spawn_crab":[], "info":{"beated":True, "type":node}}
        dico=self.matrix_map[i][z]
        # [g, d, h, b]
        if node:
            if not node[0]:
                for i_ in range(0,self.room_height, self.tile_width):
                    self.matrix_picture[i][z].append({"x":z*self.room_width,"y":i*self.room_height+i_,"img":0})
                if z==0 or not self.graphe[i][z-1]:dico["wall"].append([pygame.Rect(z*self.room_width, i*self.room_height+self.increment, self.tile_width, self.room_height-2*+self.increment)])

            if not node[1]:
                for i_ in range(0,self.room_height, self.tile_width):
                    self.matrix_picture[i][z].append({"x":z*self.room_width+self.room_width-self.tile_width,"y":i*self.room_height+i_,"img":0})
                dico["wall"].append([pygame.Rect((z+1)*self.room_width-self.tile_width, i*self.room_height+self.increment, self.tile_width*2, self.room_height-2*+self.increment)])

            if not node[2]:
                for i_ in range(0,self.room_width, self.tile_width):
                    self.matrix_picture[i][z].append({"x":z*self.room_width+i_,"y":i*self.room_height,"img":0})
                dico["ceilling"].append([pygame.Rect(z*self.room_width+self.increment, i*self.room_height, self.room_width-2*self.increment, self.tile_width)])   

            if not node[3]:
                for i_ in range(0,self.room_width, self.tile_width):
                    self.matrix_picture[i][z].append({"x":z*self.room_width+i_,"y":i*self.room_height+self.room_height-self.tile_width,"img":0})
                if (z==0 or (self.graphe[i][z-1] and not self.graphe[i][z-1][3])) and (z==len(self.graphe[0])-1 or (self.graphe[i][z+1] and not self.graphe[i][z+1][3])):
                    dico["ground"].append([pygame.Rect(z*self.room_width+self.increment, (i+1)*self.room_height-self.tile_width, self.room_width-2*self.increment, self.tile_width)])
                elif z==0 or (self.graphe[i][z-1] and not self.graphe[i][z-1][3]):
                    dico["ground"].append([pygame.Rect(z*self.room_width+self.increment, (i+1)*self.room_height-self.tile_width, self.room_width-self.increment_ground - self.increment, self.tile_width)])
                elif (z==len(self.graphe[0])-1 or (self.graphe[i][z+1] and not self.graphe[i][z+1][3])):
                    dico["ground"].append([pygame.Rect(z*self.room_width+self.increment_ground, (i+1)*self.room_height-self.tile_width, self.room_width-self.increment_ground - self.increment, self.tile_width)])
                else:dico["ground"].append([pygame.Rect(z*self.room_width+self.increment_ground, (i+1)*self.room_height-self.tile_width, self.room_width-2*self.increment_ground, self.tile_width)])
            if node[0] and node[2] : 
                self.matrix_picture[i][z].append({"x":z*self.room_width,"y":i*self.room_height,"img":0})
                dico["wall"].append([pygame.Rect(z*self.room_width, i*self.room_height+self.increment, self.tile_width, self.tile_width-2*self.increment)])
                dico["ceilling"].append([pygame.Rect(z*self.room_width+self.increment, i*self.room_height, self.tile_width-2*self.increment, self.tile_width)]) 
            if node[0] and node[3] : 
                self.matrix_picture[i][z].append({"x":z*self.room_width,"y":(i+1)*self.room_height-self.tile_width,"img":0})    
                dico["wall"].append([pygame.Rect(z*self.room_width, (i+1)*self.room_height-self.tile_width+self.increment, self.tile_width, self.tile_width-2*self.increment)])
                dico["ground"].append([pygame.Rect(z*self.room_width+self.increment, (i+1)*self.room_height-self.tile_width, self.tile_width-2*self.increment, self.tile_width)])
            if node[1] and node[2] : 
                self.matrix_picture[i][z].append({"x":(z+1)*self.room_width-self.tile_width,"y":i*self.room_height,"img":0})
                dico["wall"].append([pygame.Rect((z+1)*self.room_width-self.tile_width, i*self.room_height+self.increment, self.tile_width, self.tile_width-2*self.increment)])
                dico["ceilling"].append([pygame.Rect((z+1)*self.room_width-self.tile_width+self.increment, i*self.room_height, self.tile_width-2*self.increment, self.tile_width)]) 
            if node[1] and node[3] : 
                dico["wall"].append([pygame.Rect((z+1)*self.room_width-self.tile_width, (i+1)*self.room_height-self.tile_width+self.increment, self.tile_width, self.tile_width-2*self.increment)])
                dico["ground"].append([pygame.Rect((z+1)*self.room_width-self.tile_width+self.increment, (i+1)*self.room_height-self.tile_width, self.tile_width-2*self.increment, self.tile_width)])
                self.matrix_picture[i][z].append({"x":(z+1)*self.room_width-self.tile_width,"y":(i+1)*self.room_height-self.tile_width,"img":0})
        else:
            # dico["wall"].append([pygame.Rect(z*self.room_width, i*self.room_height+self.increment, self.tile_width, self.room_height-2*self.increment)])
            # dico["wall"].append([pygame.Rect((z+1)*self.room_width-self.tile_width, i*self.room_height+self.increment, self.tile_width, self.room_height-2*self.increment)])
            # dico["ground"].append([pygame.Rect(z*self.room_width+self.increment, i*self.room_height, self.room_width-2*self.increment, self.tile_width)])
            # dico["ceilling"].append([pygame.Rect(z*self.room_width+self.increment, (i+1)*self.room_height-self.tile_width, self.room_width-2*self.increment, self.tile_width)])
            self.matrix_picture[i][z].append({"x":z*self.room_width,"y":i*self.room_height,"img":1})

    def is_current_map_beated(self, cam_x, cam_y):
        # y_min, y_max, x_min, x_max, a, b, c, d = self.get_coord_tile_matrix(cam_x, cam_y)
        # if self.matrix_map[d][c]!=None:
        #     return self.matrix_map[d][c]["info"]["beated"]
        return True

    def get_coord_tile_matrix(self, cam_x, cam_y):
        y_min = ceil((cam_y-self.screen_height/2)-2)
        y_max = ceil((cam_y+self.screen_height/2)+1)
        x_min = ceil((cam_x-self.screen_width/2)-2)
        x_max = ceil((cam_x+self.screen_width/2)+1)
        a=((x_max+x_min)/2)/(self.room_width)
        b=((y_max+y_min)/2)/(self.room_height) 
        c=((x_max+x_min)//2)//(self.room_width)
        d=((y_max+y_min)//2)//(self.room_height) 
        if c<0: c=0
        elif c>=len(self.graphe[0]): c=len(self.graphe[0])-1
        if d<0: d=0
        elif d>=len(self.graphe): d=len(self.graphe)-1
        return y_min, y_max, x_min, x_max, a, b, c ,d
        
    def render(self, surface, minimap, cam_x, cam_y):
        """called all tick => blit only the visible tiles (compare to the position of the camera) to 'surface'"""

        # computation of the minimal and maximals coordinates that the tiles need to have to be visible
        y_min, y_max, x_min, x_max, a, b, c, d = self.get_coord_tile_matrix(cam_x, cam_y)

        # try:
        if not self.current_map_is_wave:
            # c = x
            for ligne in self.matrix_picture[(d-1 if d>0 else d):(d+2 if d<len(self.matrix_picture)-1 else d+3)]:
                for tab in ligne[(c-1 if c>0 else c):(c+2 if c<len(self.matrix_picture[0])-1 else c+3)]:
                    for img in tab:
                        surface.blit(self.all_pic[img["img"]], (self.screen_width/2 + img["x"] - cam_x, self.screen_height/2 + img["y"] - cam_y))

            # loading of the minimap
            # for i, line in enumerate(self.minimap_tile):
            #     for y, tile in enumerate(line):
            #             if tile != None:
            #                 minimap.blit(tile, (-a*self.minimap_picture.get_width()+y*self.minimap_picture.get_width() + minimap.get_width()/2 + self.minimap_picture.get_width(), -b*self.minimap_picture.get_height()+i*self.minimap_picture.get_height() +minimap.get_height()/2 + self.minimap_picture.get_height()))
        else:
            y = 0
            x = 0
            for ligne in self.current_map:
                for tile in ligne:
                    if tile != None:
                        surface.blit(tile, (self.screen_width/2 + self.coord_current_map[0]*self.tm.width*self.tm.tilewidth*self.zoom +x*self.tm.tilewidth*self.zoom +  - cam_x, self.screen_height/2 + self.coord_current_map[1]*self.tm.height*self.tm.tileheight*self.zoom + y*self.tm.tileheight*self.zoom - cam_y))
                    x+=1
                x=0
                y += 1