from math import ceil, sqrt
import time
import random
import pygame
from map.shadow import Shadow
from map.map_generation import MapGeneration

class RenderMap:
    def __init__(self, directory, seed):
        self.zoom=2
        self.tile_width=20*self.zoom
        self.room_width=self.tile_width*30
        self.room_height=self.tile_width*20

        self.minimap_tile_width=50  
        self.all_pic=[]
        self.all_pics=[self.all_pic,[]]
        self._init_all_pics(directory) 
        self.increment=7*self.zoom
        self.increment_ground=30*self.zoom         
                
        self.minimap_picture=pygame.image.load(f"{directory}\\assets\\minimap.png")
        self.minimap_picture=pygame.transform.scale(self.minimap_picture, (self.minimap_tile_width,self.minimap_tile_width))
        self.seed=seed
        
    def init_new_map(self, screen_width, screen_height, directory, seed):
        if seed==None:
            self.seed.new_seed()
        else:
            self.seed.seed=float(seed)
        random.seed(self.seed.seed)

        self.map_generation=MapGeneration(screen_width, screen_height, directory, self.zoom, self.tile_width, self.room_width, self.room_height, self.seed.seed)

        self.matrix_picture=[ [[] for _ in range(len(self.map_generation.graphe[0]))] for _ in range(len(self.map_generation.graphe))]


        for i,line in enumerate(self.map_generation.graphe):
            #parameters for the generation of reliefs
            for z,node in enumerate(line):
                    # E and S correspond to if the map has a neightboor on the right or on the bot
                self.load_map(node, i, z)
                
        self._load_pictures_tiles()

        self.get_first_map()["info"]["beated"]=True
        self.current_map_is_wave=False

        # self.shadow = Shadow(self.map_generation.tile_width, self.map_generation.room_width, self.map_generation.room_height, self.map_generation.all_mat, self.map_generation.graphe)

        self.map_generation.clear_memory()


    def _load_pictures_tiles(self):
        liste_top=[]
        liste_current=[]
        liste_bot=[]
        # correcting id of pictures
        self.cpt=0
        for i in range(len(self.matrix_picture)):
            matleft=[]

            if i>0:
                liste_top=liste_current[::]
                liste_current=liste_bot[::]
            liste_bot=[]
            for y in range(len(self.matrix_picture[i])):
                if i==0:liste_current.append(self._get_map(i,y))
                if i<len(self.matrix_picture)-1: liste_bot.append(self._get_map(i+1,y))

            for y in range(len(self.matrix_picture[i])):
                maptopleft=[]
                maptopright=[]
                if i>0: 
                    maptop=liste_top[y]
                    if y>0: maptopleft=liste_top[y-1]
                    else:maptopleft=[]
                    if y<len(self.matrix_picture[i])-1: maptopright=liste_top[y+1]
                    else:maptopright=[]
                else:
                    maptop=[]
                    maptopleft=[]
                    maptopright=[]
                if i<len(self.matrix_picture)-1: 
                    matbot=liste_bot[y]
                    if y>0:matbotleft=liste_bot[y-1]
                    else:matbotleft=[]
                    if y<len(self.matrix_picture[i])-1: matbotright=liste_bot[y+1]
                    else:matbotright=[]
                else:
                    matbot=[]
                    matbotleft=[]
                    matbotright=[]
                base_mat=liste_current[y]
                if y<len(self.matrix_picture[i])-1: matright=liste_current[y+1]
                else:matright=[]

                for i_ in range(len(self.matrix_picture[i][y])):
                    if self.matrix_picture[i][y][i_]["img"] not in (len(self.all_pic)-2, len(self.all_pic)-1):
                        bot=self._has_bot(i,y, i_, base_mat+matbot, self.matrix_picture[i][y][i_]["type_image"])
                        top=self._has_top(i,y, i_,base_mat+maptop, self.matrix_picture[i][y][i_]["type_image"])
                        left=self._has_left(i,y, i_,base_mat+matleft, self.matrix_picture[i][y][i_]["type_image"])
                        right=self._has_right(i,y, i_,base_mat+matright, self.matrix_picture[i][y][i_]["type_image"])
                        top_right=self.has_top_right(i,y,i_,base_mat,maptop,matright,maptopright, self.matrix_picture[i][y][i_]["type_image"])
                        top_left=self.has_top_left(i,y,i_,base_mat,maptop,matleft,maptopleft, self.matrix_picture[i][y][i_]["type_image"])
                        bot_right=self.has_bot_right(i,y,i_,base_mat,matbot,matright,matbotright, self.matrix_picture[i][y][i_]["type_image"])
                        bot_left=self.has_bot_left(i,y,i_,base_mat,matbot,matleft,matbotleft, self.matrix_picture[i][y][i_]["type_image"])
                        if not bot and not top and not left and not right: self.matrix_picture[i][y][i_]["img"]=0
                        elif bot and not top and not left and not right: self.matrix_picture[i][y][i_]["img"]=1
                        elif bot and top and not left and not right: self.matrix_picture[i][y][i_]["img"]=2
                        elif not bot and top and not left and not right: self.matrix_picture[i][y][i_]["img"]=3
                        elif bot and not top and left and not right: self.matrix_picture[i][y][i_]["img"]=4
                        elif bot and not top and not left and right: self.matrix_picture[i][y][i_]["img"]=5
                        elif bot and not top and left and right: self.matrix_picture[i][y][i_]["img"]=6
                        elif bot and top and left and not right: self.matrix_picture[i][y][i_]["img"]=7
                        elif bot and top and not left and right: self.matrix_picture[i][y][i_]["img"]=8
                        elif not bot and top and left and not right: self.matrix_picture[i][y][i_]["img"]=9
                        elif not bot and top and not left and right: self.matrix_picture[i][y][i_]["img"]=10
                        elif bot and top and left and right: self.matrix_picture[i][y][i_]["img"]=11
                        elif not bot and top and left and right : self.matrix_picture[i][y][i_]["img"]=12
                        elif not bot and not top and left and right: self.matrix_picture[i][y][i_]["img"]=13
                        elif left and not top and not bot and not right: self.matrix_picture[i][y][i_]["img"]=21
                        elif right and not top and not bot and not left: self.matrix_picture[i][y][i_]["img"]=22
                        if bot and top and right and left and not (top_right and top_left and bot_right and bot_left):
                            if not top_left and not top_right: self.matrix_picture[i][y][i_]["img"]=15
                            elif not top_left and top_right: self.matrix_picture[i][y][i_]["img"]=16
                            elif top_left and not top_right: self.matrix_picture[i][y][i_]["img"]=17
                            if not bot_left and not bot_right: self.matrix_picture[i][y][i_]["img"]=20
                            elif not bot_left and bot_right: self.matrix_picture[i][y][i_]["img"]=19
                            elif bot_left and not bot_right: self.matrix_picture[i][y][i_]["img"]=18
                matleft=base_mat[::]

    def _get_map(self,i,y):
        self.cpt+=1
        return [(self.matrix_picture[i][y][z]["x"], self.matrix_picture[i][y][z]["y"], self.matrix_picture[i][y][z]["type_image"]) for z in range(len(self.matrix_picture[i][y]))]

    def _has_left(self,i,y, i_, mat, texture):
        return (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width > 0 and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == 0 and y>0 and self.matrix_picture[i][y-1] and self.matrix_picture[i][y-1][0]["img"]==len(self.all_pic)-2) or  ((self.matrix_picture[i][y][i_]["x"]-self.map_generation.tile_width, self.matrix_picture[i][y][i_]["y"],texture) in mat)

    def _has_top(self,i,y, i_, mat, texture):
        return (texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height>0 and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2)or(texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == 0 and i>0 and self.matrix_picture[i-1][y] and self.matrix_picture[i-1][y][0]["img"]==len(self.all_pic)-2) or  ((self.matrix_picture[i][y][i_]["x"], self.matrix_picture[i][y][i_]["y"]-self.map_generation.tile_width,texture) in mat)

    def _has_right(self,i,y, i_, mat, texture):
        return (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width < self.map_generation.room_width-self.map_generation.tile_width and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == self.map_generation.room_width-self.map_generation.tile_width and y<len(self.matrix_picture[i])-1 and self.matrix_picture[i][y+1] and self.matrix_picture[i][y+1][0]["img"]==len(self.all_pic)-2) or  ((self.matrix_picture[i][y][i_]["x"]+self.map_generation.tile_width, self.matrix_picture[i][y][i_]["y"],texture) in mat)

    def _has_bot(self,i,y, i_, mat, texture):
        return (texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height < self.map_generation.room_height-self.map_generation.tile_width and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == self.map_generation.room_height-self.map_generation.tile_width and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y] and self.matrix_picture[i+1][y][0]["img"]==len(self.all_pic)-2) or ((self.matrix_picture[i][y][i_]["x"], self.matrix_picture[i][y][i_]["y"]+self.map_generation.tile_width,texture) in mat)

    def has_top_left(self,i,y,i_, mat, maptop, matleft, maptopleft, texture):
        return (texture == 1 and  self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height > 0 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width > 0 and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == 0 and not self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == 0 and i>0 and self.matrix_picture[i-1][y] and self.matrix_picture[i-1][y][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == 0 and not self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == 0 and y>0 and self.matrix_picture[i][y-1] and self.matrix_picture[i][y-1][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == 0 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == 0 and y>0 and i>0 and self.matrix_picture[i-1][y-1] and self.matrix_picture[i-1][y-1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]-self.map_generation.tile_width, self.matrix_picture[i][y][i_]["y"]-self.map_generation.tile_width,texture) in mat+maptopleft+maptop+matleft

    def has_top_right(self,i,y,i_, mat, maptop, matright, maptopright, texture):
        return (texture == 1 and  self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height > 0 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width < self.map_generation.room_width-self.map_generation.tile_width and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or  (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == self.map_generation.room_width-self.map_generation.tile_width and not self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == 0 and y<len(self.matrix_picture[i])-1 and self.matrix_picture[i][y+1] and self.matrix_picture[i][y+1][0]["img"]==len(self.all_pic)-2)or (texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == 0 and not self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == self.map_generation.room_width-self.map_generation.tile_width and i>0 and self.matrix_picture[i-1][y] and self.matrix_picture[i-1][y][0]["img"]==len(self.all_pic)-2)or(texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == 0 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == self.map_generation.room_width-self.map_generation.tile_width and y<len(self.matrix_picture[i])-1 and i>0 and self.matrix_picture[i-1][y+1] and self.matrix_picture[i-1][y+1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]+self.map_generation.tile_width, self.matrix_picture[i][y][i_]["y"]-self.map_generation.tile_width,texture) in maptopright+mat+maptop+matright
    
    def has_bot_left(self,i,y,i_,mat, mapbot, matleft, matbotleft, texture):
        return (texture == 1 and  self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height < self.map_generation.room_height-self.map_generation.tile_width and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width > 0 and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or  (texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == self.map_generation.room_height-self.map_generation.tile_width and not self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == 0 and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y] and self.matrix_picture[i+1][y][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == 0 and not self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == self.map_generation.room_height-self.map_generation.tile_width and y>0 and self.matrix_picture[i][y-1] and self.matrix_picture[i][y-1][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == 0 and y>0 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == self.map_generation.room_height-self.map_generation.tile_width and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y-1] and self.matrix_picture[i+1][y-1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]-self.map_generation.tile_width, self.matrix_picture[i][y][i_]["y"]+self.map_generation.tile_width,texture) in mat+matbotleft+mapbot+matleft
    
    def has_bot_right(self,i,y,i_,mat, mapbot, matright, matbotright, texture):
        return (texture == 1 and  self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height < self.map_generation.room_height-self.map_generation.tile_width and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width < self.map_generation.room_width-self.map_generation.tile_width and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or  (texture == 1 and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == self.map_generation.room_width-self.map_generation.tile_width and not self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == self.map_generation.room_height-self.map_generation.tile_width and y<len(self.matrix_picture[i])-1 and self.matrix_picture[i][y+1] and self.matrix_picture[i][y+1][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == self.map_generation.room_height-self.map_generation.tile_width and not self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == self.map_generation.room_width-self.map_generation.tile_width and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y] and self.matrix_picture[i+1][y][0]["img"]==len(self.all_pic)-2) or (texture == 1 and self.matrix_picture[i][y][i_]["y"]%self.map_generation.room_height == self.map_generation.room_height-self.map_generation.tile_width and self.matrix_picture[i][y][i_]["x"]%self.map_generation.room_width == self.map_generation.room_width-self.map_generation.tile_width and y<len(self.matrix_picture[i])-1 and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y+1] and self.matrix_picture[i+1][y+1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]+self.map_generation.tile_width, self.matrix_picture[i][y][i_]["y"]+self.map_generation.tile_width,texture) in mat+matbotright+mapbot+matright

    

    def _init_all_pics(self, directory):

        for i in range(23):
            try:
                pic=pygame.image.load(f"{directory}\\assets\\TreasureHunters\\PalmTreeIsland\\Sprites\\Terrain\\{str(i)}.png")
                pic=pygame.transform.scale(pic, (self.tile_width,self.tile_width))
                self.all_pic.append(pic)
            except:
                self.all_pic.append(None)
            for n in range(2,3+1):
                if n-1==len(self.all_pics):
                    self.all_pics.append([])
                try:
                    pic=pygame.image.load(f"{directory}\\assets\\TreasureHunters\\PalmTreeIsland\\Sprites\\Terrain\\{str(n)}_{str(i)}.png")
                    pic=pygame.transform.scale(pic, (self.tile_width,self.tile_width))
                    self.all_pics[n-1].append(pic)
                except:
                    self.all_pics[n-1].append(None)

        # pic=pygame.Surface((self.map_generation.tile_width, self.map_generation.tile_width))
        # pic.fill((200,200,200))
        pic2=pygame.transform.scale(self.all_pic[11], (self.room_width-2*self.tile_width,self.room_height-2*self.tile_width))
        pic3=pygame.Surface((self.tile_width//2, self.tile_width//2))
        pic3.fill((200,200,200))
        # self.all_pic.append(pic)
        self.all_pic.append(pic2)
        self.all_pic.append(pic3)

    def get_height(self):
        """return the height of the map in coordonates"""
        # we remove the 2 empty map that are on the top and on the bot of the map
        return self.map_generation.graphe_height*self.map_generation.room_height

    def get_width(self):
        """return the width of the map in coordonates"""
        # we remove the 2 empty map that are on the left and on the right of the map
        return self.map_generation.graphe_width*self.map_generation.room_width
                    
    def get_first_map(self, index=False):
        """return the if of the map of spawn in  self.map_generation.matrix_map"""
        for i, line in enumerate(self.map_generation.matrix_map):
            for y, map in enumerate(line):
                if map != None:
                    if not index:
                        return map
                    else:
                        return (i,y)

    def _spawn_big_ground(self, i, z, i_, y_, tmp):
        self.map_generation.matrix_map[i][z]["ground"].append([pygame.Rect(z*self.map_generation.room_width+(tmp)*self.map_generation.tile_width, i*self.map_generation.room_height+i_*self.map_generation.tile_width, self.map_generation.tile_width*(y_-tmp), self.map_generation.tile_width)])

    def _spawn_big_ceilling(self, i, z, i_, y_, tmp):
        self.map_generation.matrix_map[i][z]["ceilling"].append([pygame.Rect(z*self.map_generation.room_width+(tmp)*self.map_generation.tile_width+self.increment, i*self.map_generation.room_height+i_*self.map_generation.tile_width, self.map_generation.tile_width*(y_-tmp)-2*self.increment, self.map_generation.tile_width)])

    def _spawn_big_walls(self, i, z, i_, y_, tmp):
        self.map_generation.matrix_map[i][z]["wall"].append([pygame.Rect(z*self.map_generation.room_width+y_*(self.map_generation.tile_width), i*self.map_generation.room_height+(tmp)*self.map_generation.tile_width+self.increment, self.map_generation.tile_width, self.map_generation.tile_width*(i_-tmp) - 2*+self.increment)])
                
    def complete_picture_matrix(self, i, z, node, mat=None):
        if not mat : mat=self.map_generation.all_mat[i][z]
        g=0
        d=len(mat[0])
        if node == [False, False, False, False]:
            h=len(mat)-2
        else:h=0
        b=len(mat)

        for i_ in range(h, b):
            tmp=-1
            tmp2=-1
            for y_ in range(g, d):
                if mat[i_][y_]:
                    self.matrix_picture[i][z].append({"x":z*self.map_generation.room_width+y_*self.map_generation.tile_width,"y":i*self.map_generation.room_height+i_*self.map_generation.tile_width,"img":0,"type_image":mat[i_][y_]})

                    if node != [False, False, False, False]:
                    
                        
                        #adding little ground if there is a change of 
                        # left
                        if (y_>g and not mat[i_][y_-1] and i_<len(mat)-1 and mat[i_+1][y_-1] and i_>0 and not mat[i_-1][y_]) or (y_==g and z>0 and self.map_generation.all_mat[i][z-1] and not self.map_generation.all_mat[i][z-1][i_][-1] and i_<len(mat)-1 and self.map_generation.all_mat[i][z-1][i_+1][-1] and i_>0 and not mat[i_-1][y_]):
                            self.matrix_picture[i][z].append({"x":z*self.map_generation.room_width+(y_-0.5)*self.map_generation.tile_width,"y":i*self.map_generation.room_height+(i_+0.5)*self.map_generation.tile_width,"img":len(self.all_pic)-1,"type_image":1})
                            self.map_generation.matrix_map[i][z]["little_ground"].append([pygame.Rect(z*self.map_generation.room_width+(y_-0.6)*self.map_generation.tile_width, i*self.map_generation.room_height+(i_+0.5)*self.map_generation.tile_width, self.map_generation.tile_width/4, self.map_generation.tile_width/2)])
                        #  or (y==d-1 and self.last_mat and not self.last_mat[i_][0])
                        # right
                        if ((y_<d-1 and not mat[i_][y_+1] and i_<len(mat)-1 and mat[i_+1][y_+1] and i_>0 and not mat[i_-1][y_]) or (y_==d-1 and node[1] and (self.map_generation.gen_current_width==0 or (z<len(self.map_generation.all_mat[i])-1 and self.map_generation.all_mat[i][z+1] and not self.map_generation.all_mat[i][z+1][i_][0] and self.map_generation.all_mat[i][z+1][i_+1][0])))):
                            self.matrix_picture[i][z].append({"x":z*self.map_generation.room_width+(y_+1)*self.map_generation.tile_width,"y":i*self.map_generation.room_height+(i_+0.5)*self.map_generation.tile_width,"img":len(self.all_pic)-1,"type_image":1})
                            self.map_generation.matrix_map[i][z]["little_ground"].append([pygame.Rect(z*self.map_generation.room_width+(y_+1.1)*self.map_generation.tile_width, i*self.map_generation.room_height+(i_+0.5)*self.map_generation.tile_width, self.map_generation.tile_width/4, self.map_generation.tile_width/2)])

                        # ground
                        if tmp == -1 and ((i_>0 and not mat[i_-1][y_]) or (i_==0 and i>0 and self.map_generation.all_mat[i-1][z] and not self.map_generation.all_mat[i-1][z][-1][y_])) :
                            tmp=y_
                        # not elif because if lenght is 1
                        if tmp != -1 and (y_ == d-1 or not mat[i_][y_+1] or ((i_>0 and mat[i_-1][y_+1]) or (i_==0 and i>0 and self.map_generation.all_mat[i-1][z] and self.map_generation.all_mat[i-1][z][-1][y_+1]))):
                            # or self.map_generation.graphe[i][z][0] or


                # jai virer les inc

                            if tmp==y_ or tmp>1 or z==0 or len(self.map_generation.graphe[i][z-1])==0 or not self.map_generation.graphe[i][z-1][3] or node[0] or len(mat)-1-i_ > self.map_generation.gen_max_height or (tmp*self.map_generation.tile_width)%self.map_generation.room_width>2*self.map_generation.tile_width:inc=0
                            else: inc=0.5
                            #or self.map_generation.graphe[i][z][1] or
                            if tmp==y_ or y_<len(mat)-2 or z==len(self.map_generation.graphe[0])-1 or len(self.map_generation.graphe[i][z+1])==0 or not self.map_generation.graphe[i][z+1][3] or node[1] or len(mat)-1-i_ > self.map_generation.gen_max_height or (y_*self.map_generation.tile_width)%self.map_generation.room_width<self.map_generation.room_width-2*self.map_generation.tile_width:inc2=0
                            else: inc2=0.5
                            self._spawn_big_ground(i, z, i_, y_+1-0, tmp+0)
                            tmp=-1

                    # ceillings
                    if i_<len(mat)-1 or (i_==len(mat)-1 and not node[3]):
                        if tmp2 == -1 and ( i_==len(mat)-1 or not mat[i_+1][y_]) :tmp2=y_
                        # not elif because if lenght is 1
                        if tmp2 != -1 and (y_ == d-1 or not mat[i_][y_+1] or (i_<len(mat)-1 and ( mat[i_+1][y_+1] or mat[i_+1][y_]))):
                            plus1=plus2=0
                            if (tmp2==0 and z>0 and self.map_generation.all_mat[i][z-1] and self.map_generation.all_mat[i][z-1][i_][-1]) or ( tmp2>0 and mat[i_][tmp2-1]): plus1=1
                            if (y_==d-1 and z<len(self.map_generation.all_mat)-1 and self.map_generation.all_mat[i][z+1] and self.map_generation.all_mat[i][z+1][i_][0]) or (y_<len(mat[i_])-1 and mat[i_][y_+1]): plus2=1
                            self._spawn_big_ceilling(i, z, i_, y_+1+plus2, tmp2-plus1)
                            tmp2=-1
        if i>0:
            tmp=-1
            for y_ in range(g, d):
                if tmp==-1 and not mat[0][y_] and self.map_generation.all_mat[i-1][z] and self.map_generation.all_mat[i-1][z][-1][y_] and not mat[1][y_]: tmp=y_
                if tmp != -1 and (y_==d-1 or mat[1][y_+1] or mat[0][y_+1] or not self.map_generation.all_mat[i-1][z][-1][y_+1]):
                    self._spawn_big_ceilling(i-1, z, len(mat)-1, y_+1, tmp)
                    tmp=-1
        if node != [False, False, False, False]:

            for y_ in range(g, d):
                tmp=-1
                type_=0
                for i_ in range(h, b):
                    if mat[i_][y_]:
                        #if tmp == -1 and  (((y_==0 and (not mat[i_][1] or (z>0 and self.map_generation.all_mat[i][z-1] and not self.map_generation.all_mat[i][z-1][i_][-1]))) or (y_==len(mat[0])-1 and (not mat[i_][-2] or (z<len(self.map_generation.all_mat[i])-1 and not self.map_generation.all_mat[i][z+1] and self.map_generation.all_mat[i][z+1][i_][0])))) or ((y_>0 and y_<len(mat[0])-1) and (not mat[i_][y_-1] or not mat[i_][y_+1]))):
                        if tmp == -1 and not(y_==0 and mat[i_][1] and z>0 and self.map_generation.all_mat[i][z-1] and self.map_generation.all_mat[i][z-1][i_][-1]) and not(y_==len(mat[0])-1 and mat[i_][-2] and z<len(self.map_generation.all_mat[i])-1 and self.map_generation.all_mat[i][z+1] and self.map_generation.all_mat[i][z+1][i_][0]) and ((y_==0 or y_==len(mat[0])-1) or ((y_>0 and y_<len(mat[0])-1) and (not mat[i_][y_-1] or not mat[i_][y_+1]))):
                            if ((y_!=len(mat[0])-1 or not mat[i_][y_-1]) or (y_==len(mat[0])-1 and z<len(self.map_generation.all_mat[0])-1 and (not self.map_generation.all_mat[i][z+1] or not self.map_generation.all_mat[i][z+1][i_][0]))) and ((y_>0 or not mat[i_][y_+1]) or (y_==0 and z>0 and (not self.map_generation.all_mat[i][z-1] or not self.map_generation.all_mat[i][z-1][i_][-1]))):
                                if (y_==0 and mat[i_][y_+1]) or (y_>0 and not mat[i_][y_-1]): type_=1
                                tmp=i_
                            
                            # not elif because if lenght is 1
                        if tmp != -1 and type_ == 1 and (i_ == b-1 or not mat[i_+1][y_] or ((y_>0 and mat[i_][y_-1]) or (y_==0 and z>0 and (self.map_generation.all_mat[i][z-1] and self.map_generation.all_mat[i][z-1][i_][-1])))):
                            if i_-tmp>=0 : self._spawn_big_walls(i, z, i_+1, y_, tmp)
                            elif (i_>0 and mat[i_-1][y_]) or (i_==0 and i>0 and self.map_generation.all_mat[i-1][z] and self.map_generation.all_mat[i-1][z][-1][y_]) :  self._spawn_big_walls(i, z, i_+1, y_, tmp-1)
                            tmp=-1
                            
                        elif tmp != -1 and type_ == 0 and (i_ == b-1 or not mat[i_+1][y_] or ((not y_==len(mat[0])-1 and mat[i_][y_+1]) or (y_==len(mat[0])-1 and z<len(self.map_generation.all_mat[0])-1 and (self.map_generation.all_mat[i][z+1] and self.map_generation.all_mat[i][z+1][i_][0])))):
                            if i_-tmp>=0 : self._spawn_big_walls(i, z, i_+1, y_, tmp)
                            elif (i_>0 and mat[i_-1][y_]) or (i_==0 and i>0 and self.map_generation.all_mat[i-1][z] and self.map_generation.all_mat[i-1][z][-1][y_]) :  self._spawn_big_walls(i, z, i_+1, y_, tmp-1)
                            tmp=-1

    def load_map(self, node, i, z, empty=False):
        """call load_objects_map if the map is not empty and load all tiles for the map widht the coordinates i and z""" 

        self.map_generation.matrix_map[i][z]={"wall":[], "ground":[], "little_ground":[], "ceilling":[], "platform":[],"bot":{"platform_right":[], "platform_left":[], "platform_go_right":[], "platform_go_left":[]}, "spawn_player":(), "object_map":(), "object_map":(), "spawn_crab":[], "info":{"beated":True, "type":node}}
        # [g, d, h, b]
        if node:
            self.complete_picture_matrix(i, z, node)
            if node[3] and not node[0] and not node[1]:self.map_generation.re_initialize_gen_var()
        else:
            #self._spawn_big_walls(i,z,dico,0,0,len(self.map_generation.all_mat[i][z]))
            mat = [[0 for _ in range(self.map_generation.room_width//self.map_generation.tile_width)] for _ in range(self.map_generation.room_height//self.map_generation.tile_width)]
            #self._spawn_big_ceilling(i,z,self.map_generation.room_height//self.map_generation.tile_width-1,0,self.map_generation.room_width//self.map_generation.tile_width)
            self.matrix_picture[i][z].append({"x":z*self.map_generation.room_width+self.map_generation.tile_width,"y":i*self.map_generation.room_height+self.map_generation.tile_width,"img":len(self.all_pic)-2,"type_image":1})

            for i_ in range(self.map_generation.room_height//self.map_generation.tile_width):
                self.matrix_picture[i][z].append({"x":z*self.map_generation.room_width,"y":i*self.map_generation.room_height+i_*self.map_generation.tile_width,"img":0,"type_image":1})
                mat[i_][0]=1
                if i_ == 0 or i_ == self.map_generation.room_height//self.map_generation.tile_width-1:
                    for y in range(1,self.map_generation.room_width//self.map_generation.tile_width-1):
                        mat[i_][y]=1
                        self.matrix_picture[i][z].append({"x":z*self.map_generation.room_width+y*self.map_generation.tile_width,"y":i*self.map_generation.room_height+i_*self.map_generation.tile_width,"img":0,"type_image":1})

                mat[i_][-1]=1
                self.matrix_picture[i][z].append({"x":z*self.map_generation.room_width+(self.map_generation.room_width//self.map_generation.tile_width-1)*self.map_generation.tile_width,"y":i*self.map_generation.room_height+i_*self.map_generation.tile_width,"img":0,"type_image":1})
                self.complete_picture_matrix(i, z, [False,False,False,False], mat=mat)
            self.map_generation.all_mat[i][z]=mat[::]
            self.map_generation.re_initialize_gen_var()


    def is_current_map_beated(self, cam_x, cam_y):
        # y_min, y_max, x_min, x_max, a, b, c, d = self.get_coord_tile_matrix(cam_x, cam_y)
        # if self.map_generation.matrix_map[d][c]!=None:
        #     return self.map_generation.matrix_map[d][c]["info"]["beated"]
        return True

    def get_coord_tile_matrix(self, cam_x, cam_y):
        y_min = ceil((cam_y-self.map_generation.screen_height/2)-2)
        y_max = ceil((cam_y+self.map_generation.screen_height/2)+1)
        x_min = ceil((cam_x-self.map_generation.screen_width/2)-2)
        x_max = ceil((cam_x+self.map_generation.screen_width/2)+1)
        a=((x_max+x_min)/2)/(self.map_generation.room_width)
        b=((y_max+y_min)/2)/(self.map_generation.room_height) 
        c=((x_max+x_min)//2)//(self.map_generation.room_width)
        d=((y_max+y_min)//2)//(self.map_generation.room_height) 
        if c<0: c=0
        elif c>=self.map_generation.graphe_width: c=self.map_generation.graphe_width-1
        if d<0: d=0
        elif d>=self.map_generation.graphe_height: d=self.map_generation.graphe_height-1
        return y_min, y_max, x_min, x_max, a, b, c ,d
    
    def _not_visible(self,i, z):
        dico={}
        dico[f"({i},{z})"]=True
        for i_ in range(-1,2):
            for z_ in range(-1,2):
                if not (i_ == 0 and z_ == 0) and i+i_>=0 and z+z_ >= 0 and i+i_ < len(self.map_generation.graphe) and z+z_ < len(self.map_generation.graphe[i]):
                    if len(self.g.get_shortest_path((i,z), (i+i_,z+z_), self.map_generation.graphe))<=3 and (not self.map_generation.graphe[i][z] or ((i_==0 and z_==-1 and self.map_generation.graphe[i][z][0] ) or (i_==0 and z_==1 and self.map_generation.graphe[i][z][1] ) or (i_==1 and z_==0 and self.map_generation.graphe[i][z][3] ) or (i_==-1 and z_==0 and self.map_generation.graphe[i][z][2]))): dico[f"({i+i_},{z+z_})"]=True
                    else:dico[f"({i+i_},{z+z_})"]=False
        
        # for i_ in range(-1,2):
        #     for z_ in range(-1,2):
        #         if not (i_ == 0 and z_ == 0) and i+i_>=0 and z+z_ >= 0 and i+i_ < len(self.map_generation.graphe) and z+z_ < len(self.map_generation.graphe[i]) and dico[f"({i+i_},{z+z_})"]==False and not self.map_generation.graphe[i+i_][z+z_]:
        #             if dico.get(f"({i+i_+1},{z+z_})", False) or dico.get(f"({i+i_},{z+z_+1})", False) or (i>0 and self.map_generation.graphe[i-1][z] and dico.get(f"({i+i_-1},{z+z_})", False)) or (z>0 and self.map_generation.graphe[i][z-1] and dico.get(f"({i+i_},{z+z_-1})", False)):
        #                 dico[f"({i+i_},{z+z_})"]=True
        
        return dico
        
    def render(self, surface, minimap, cam_x, cam_y):
        """called all tick => blit only the visible tiles (compare to the position of the camera) to 'surface'"""
        # computation of the minimal and maximals coordinates that the tiles need to have to be visible
        y_min, y_max, x_min, x_max, a, b, c, d = self.get_coord_tile_matrix(cam_x, cam_y)

        # try:
        if not self.current_map_is_wave:
            # c = x
            #visible=self._not_visible(d,c)
            for ligne in [d_ for d_ in range((d-1 if d>0 else d),(d+2 if d<len(self.matrix_picture)-1 else d+3))]:
                for tab in [c_ for c_ in range((c-1 if c>0 else c),(c+2 if c<len(self.matrix_picture[0])-1 else c+3))]:
                    for img in self.matrix_picture[ligne][tab]:
                        # if img["img"] == len(self.all_pic)-2 or visible[f"({ligne},{tab})"]:
                        if img["type_image"]==1:img_=self.all_pic[img["img"]]
                        elif img["type_image"]==2:img_=self.all_pics[1][img["img"]]
                        elif img["type_image"]==3:img_=self.all_pics[2][img["img"]]
                        if not img_:img_=self.all_pics[img["type_image"]-1][0]
                        surface.blit(img_, (self.map_generation.screen_width/2 + img["x"] - cam_x, self.map_generation.screen_height/2 + img["y"] - cam_y))

            # loading of the minimap
            for i, line in enumerate(self.map_generation.graphe):
                for y, node in enumerate(line):
                    if len(node)>0:
                        # also blit transition
                        w=self.minimap_picture.get_width()
                        h=self.minimap_picture.get_height()
                        minimap.blit(self.minimap_picture, ( w*(2*y-2*a+1) + minimap.get_width()/2, h*(2*i-2*b+1) + minimap.get_height()/2))
                        if node[1]:minimap.blit(self.minimap_picture, ( w*(2*y-2*a+2) + minimap.get_width()/2, h*(2*i-2*b+1) + minimap.get_height()/2))
                        if node[3]:minimap.blit(self.minimap_picture, ( w*(2*y-2*a+1) + minimap.get_width()/2, h*(2*i-2*b+2) + minimap.get_height()/2))
                        
        
        else:
            y = 0
            x = 0
            for ligne in self.current_map:
                for tile in ligne:
                    if tile != None:
                        surface.blit(tile, (self.map_generation.screen_width/2 + self.coord_current_map[0]*self.tm.width*self.tm.tilewidth*self.zoom +x*self.tm.tilewidth*self.zoom +  - cam_x, self.map_generation.screen_height/2 + self.coord_current_map[1]*self.tm.height*self.tm.tileheight*self.zoom + y*self.tm.tileheight*self.zoom - cam_y))
                    x+=1
                x=0
                y += 1