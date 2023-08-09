from math import ceil
import random
import pygame
from map.graph_generator import get_matrix, printTab
from seed import seed
random.seed(seed)
class RenderMap:
    def __init__(self, screen_width, screen_height, directory):
        """cf la documentation de pytmx"""
        self.directory=directory
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.graphe=get_matrix()
        new_graph=[]
        new_graph.insert(0, [[] for _ in range(len(self.graphe[0])+2)])
        
        for i in range(len(self.graphe)):
            new_graph.append([[]]+[self.graphe[i][z] for z in range(len(self.graphe[i]))]+[[]])
        
        new_graph.append([[] for _ in range(len(self.graphe[0])+2)])
        self.graphe=new_graph
        printTab(self.graphe)

        self.minimap_tile_width=50            
        self.zoom=2
        self.tile_width=20*self.zoom
        self.room_width=self.tile_width*30
        self.room_height=self.tile_width*20
        
        self.increment=7*self.zoom
        self.increment_ground=30*self.zoom
        self.all_pic=[]
        self._init_all_pics(directory)

        self.gen_max_height=4
        self.gen_min_width=6
        self.gen_max_width=10
        self.gen_min_reduced_width=12
        self.gen_width_hill=3
        self.gen_width_width_hill=1
        self.gen_max_hill_height=(self.room_height//self.tile_width)//self.gen_width_hill + 4
        self.gen_min_hill_height=2
        self.gen_falaise_max_width=self.room_width/self.tile_width // 2
        self.gen_falaise_min_width=self.room_width/self.tile_width // 3
        self.gen_island_max_width=int(self.room_width/self.tile_width // 3)
        self.gen_island_additionnal_height=int(self.room_height/self.tile_width // 10)
        self.gen_island_random_horizontal=int(self.room_height/self.tile_width // 5)
        self.gen_island_start_height=int(self.room_height/self.tile_width // 2 - self.room_height/self.tile_width // 5)
        self.gen_island_max_height=2
        self.gen_island_min_width=3
        self.gen_island_max_width=7
        self.gen_min_width_bottom=10
        self.gen_max_width_bottom=20

        self.all_mat=[[None for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]
        self.all_island=[[False for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]

        # value : dictionnary : keys : id of the tile value : image of the tile
        self.matrix_picture=[ [[] for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]

        # matrix map is used to load all the map objects
        self.matrix_map=[[None for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]
        
        for i,line in enumerate(self.graphe):
            self.re_initialize_gen_var()
            #parameters for the generation of reliefs
            for z,node in enumerate(line):
                    # E and S correspond to if the map has a neightboor on the right or on the bot
                if node:
                    self.generate_relief(i, z, node)
                    if node[3] and not node[0] and not node[1]:self.re_initialize_gen_var()

        seen_better_bottom=[]
        # spawn of object 
        for i,line in enumerate(self.graphe):
            for z,node in enumerate(line):
                # marche pas car il faut aussi droite du node en bas et c trop rare flemme
                # if node and not node[0] and node[1] and node[2] and node[3] and line[z+1][2] and line[z+1][3]:
                #     print(i,z)
                if node and node[2] and node[3] and node[1] and self.graphe[i+1][z] and self.graphe[i+1][z][1] and self.graphe[i][z+1] and self.graphe[i][z+1][3]:
                    self.all_mat[i][z][-1][-1]=0
                    self.all_mat[i][z+1][-1][0]=0
                    self.all_mat[i+1][z][0][-1]=0
                    self.all_mat[i+1][z+1][0][0]=0
                if (node and node[2] and (i==0 or not self.all_island[i-1][z]) and random.randint(1,7)==1) or (node and node[0] and node[1] and node[2] and node[3]) or (node and not node[0] and not node[1] and not node[2] and node[3] and random.randint(1,2)==1) or (node and node[2] and node[3] and random.randint(1,10)==1) or (node and (node[1] or node[0]) and node[2] and node[3] and random.randint(1,2)==1):
                    self.all_island[i][z]=True

                # better bottom of ceillings
                if node and (i,z) not in seen_better_bottom and not node[2]:
                    seen_better_bottom.append((i,z))
                    temp=[(i,z)]
                    z_=z
                    while self.graphe[i][z_+1] and self.graphe[i][z_+1][0]:
                        seen_better_bottom.append((i,z_+1))
                        temp.append((i,z_+1))
                        if self.graphe[i][z_+1][2]: break
                        z_+=1

                    if self.graphe[i][z-1] and self.graphe[i][z-1][2]: 
                        temp = [(i,z-1)] + temp
                        self._better_bottom_ceilling(0, len(self.all_mat[i][z][0])-1, temp, island=False)
                    else:     
                        for temp_i in range(0,len(self.all_mat[i][z])):
                            if self.all_mat[i][z][0][temp_i] and not self.all_mat[i][z][1][temp_i] : break
                        self._better_bottom_ceilling(0, temp_i, temp, island=False)

        a=self.gen_max_height ; b=self.gen_min_width ; c=self.gen_max_width
        self.gen_max_height=self.gen_island_max_height ; self.gen_min_width=self.gen_island_min_width ; self.gen_max_width=self.gen_island_max_width

        for i,line in enumerate(self.all_island):
            for z,island in enumerate(line):
                if island and z<len(self.all_island[i])-1 and self.all_island[i][z+1]:
                    self.re_initialize_gen_var()
                    start=int(self.room_width//self.tile_width//2 - self.gen_island_max_width//2 + random.randint(0,self.gen_island_random_horizontal))
                    end=int(self.room_width//self.tile_width//2 + self.gen_island_max_width//2 - random.randint(0,self.gen_island_random_horizontal))
                    if not self.graphe[i][z][3] or not self.graphe[i][z+1][3]:start_height=len(self.all_mat[i][z])-1-self.gen_max_height-3-random.randint(0, self.gen_island_additionnal_height)
                    else:start_height= self.gen_island_start_height//2+random.randint(-self.gen_island_additionnal_height, self.gen_island_additionnal_height)
                    self._generate_relief_ground(start if start >=0 else 0, len(self.all_mat[i][z][0])-1, self.graphe[i][z], self.all_mat[i][z], self.gen_island_additionnal_height, start_height=start_height, island=True)
                    self._generate_relief_ground(0, end if end <= len(self.all_mat[i][z][0])-1 else len(self.all_mat[i][z][0])-1, self.graphe[i][z+1], self.all_mat[i][z+1], self.gen_island_additionnal_height, start_height=start_height, island=True)
                    self._better_bottom_ceilling(-start_height-1, start, [(i,z), (i,z+1)], island=True)

                elif island and (z==0 or not self.all_island[i][z-1]):
                    self.re_initialize_gen_var()
                    start=int(self.room_width//self.tile_width//2 - self.gen_island_max_width//2 - random.randint(0,self.gen_island_random_horizontal))
                    end=int(self.room_width//self.tile_width//2 + self.gen_island_max_width//2 + random.randint(0,self.gen_island_random_horizontal))
                    if not self.graphe[i][z][3]:start_height=len(self.all_mat[i][z])-1-self.gen_max_height-3-random.randint(0, self.gen_island_additionnal_height)
                    else:start_height=self.gen_island_start_height+random.randint(-self.gen_island_additionnal_height, self.gen_island_additionnal_height)
                    self._generate_relief_ground(start if start >=0 else 0, end if end <= len(self.all_mat[i][z][0])-1 else len(self.all_mat[i][z][0])-1, self.graphe[i][z], self.all_mat[i][z], self.gen_island_additionnal_height, start_height=start_height, island=True)
                    self._better_bottom_ceilling(-start_height-1, start, [(i,z)], island=True)

        self.gen_max_height=a ; self.gen_min_width=b ; self.gen_max_width=c
        
        for i,line in enumerate(self.graphe):
            #parameters for the generation of reliefs
            for z,node in enumerate(line):
                    # E and S correspond to if the map has a neightboor on the right or on the bot
                self.load_map(node, i, z)

        self._load_pictures_tiles()
                
        self.minimap_picture=pygame.image.load(f"{directory}\\assets\\tiled_maps\\minimap.png")
        self.minimap_picture=pygame.transform.scale(self.minimap_picture, (self.minimap_tile_width,self.minimap_tile_width))

        self.current_map_is_wave=False
        
        self.get_first_map()["info"]["beated"]=True

    def _better_bottom_ceilling(self, start_height, start, mats, island=False, switch=None, width=0, old_mat=[]):
        if switch==None:switch=random.randint(2,2)==1
        if len(mats)==0:return
        mat=mats[0]
        while self.all_mat[mat[0]][mat[1]][start_height][start] and not self.all_mat[mat[0]][mat[1]][start_height+1][start]:
            if width<=0:
                if island: width=random.randint(self.gen_island_min_width, self.gen_island_max_width)
                else:width=random.randint(self.gen_min_width_bottom, self.gen_max_width_bottom)
                switch=not switch
            if switch:
                self.all_mat[mat[0]][mat[1]][start_height][start]=0
            if start < len(self.all_mat[mat[0]][mat[1]][start_height])-1:
                start+=1
                width-=1
            else: return self._better_bottom_ceilling(start_height=start_height, start=0, mats=mats[1::], island=island, switch=switch, width=width-1, old_mat=mat)

        for i in range(2,0,-1):
            if start-i-1>=0:old=self.all_mat[mat[0]][mat[1]][start_height][start-i-1]
            elif len(old_mat)>0:old=self.all_mat[old_mat[0]][old_mat[1]][start_height][start-i-1]
            else: return
            if start-i>=0 and self.all_mat[mat[0]][mat[1]][start_height][start-i] != old : self.all_mat[mat[0]][mat[1]][start_height][start-i]=old
            elif start-i<0 and len(old_mat)>0 and self.all_mat[old_mat[0]][old_mat[1]][start_height][start-i] != old:self.all_mat[old_mat[0]][old_mat[1]][start_height][start-i]=old


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
                        bot=self._has_bot(i,y, i_, base_mat+matbot)
                        top=self._has_top(i,y, i_,base_mat+maptop)
                        left=self._has_left(i,y, i_,base_mat+matleft)
                        right=self._has_right(i,y, i_,base_mat+matright)
                        top_right=self.has_top_right(i,y,i_,base_mat,maptop,matright,maptopright)
                        top_left=self.has_top_left(i,y,i_,base_mat,maptop,matleft,maptopleft)
                        bot_right=self.has_bot_right(i,y,i_,base_mat,matbot,matright,matbotright)
                        bot_left=self.has_bot_left(i,y,i_,base_mat,matbot,matleft,matbotleft)
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
        return [(self.matrix_picture[i][y][z]["x"], self.matrix_picture[i][y][z]["y"]) for z in range(len(self.matrix_picture[i][y]))]

    def _has_left(self,i,y, i_, mat):
        return (self.matrix_picture[i][y][i_]["x"]%self.room_width > 0 and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]%self.room_width == 0 and y>0 and self.matrix_picture[i][y-1] and self.matrix_picture[i][y-1][0]["img"]==len(self.all_pic)-2) or  ((self.matrix_picture[i][y][i_]["x"]-self.tile_width, self.matrix_picture[i][y][i_]["y"]) in mat)

    def _has_top(self,i,y, i_, mat):
        return (self.matrix_picture[i][y][i_]["y"]%self.room_height>0 and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2)or(self.matrix_picture[i][y][i_]["y"]%self.room_height == 0 and i>0 and self.matrix_picture[i-1][y] and self.matrix_picture[i-1][y][0]["img"]==len(self.all_pic)-2) or  ((self.matrix_picture[i][y][i_]["x"], self.matrix_picture[i][y][i_]["y"]-self.tile_width) in mat)

    def _has_right(self,i,y, i_, mat):
        return (self.matrix_picture[i][y][i_]["x"]%self.room_width < self.room_width-self.tile_width and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]%self.room_width == self.room_width-self.tile_width and y<len(self.matrix_picture[i])-1 and self.matrix_picture[i][y+1] and self.matrix_picture[i][y+1][0]["img"]==len(self.all_pic)-2) or  ((self.matrix_picture[i][y][i_]["x"]+self.tile_width, self.matrix_picture[i][y][i_]["y"]) in mat)

    def _has_bot(self,i,y, i_, mat):
        return (self.matrix_picture[i][y][i_]["y"]%self.room_height < self.room_height-self.tile_width and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["y"]%self.room_height == self.room_height-self.tile_width and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y] and self.matrix_picture[i+1][y][0]["img"]==len(self.all_pic)-2) or ((self.matrix_picture[i][y][i_]["x"], self.matrix_picture[i][y][i_]["y"]+self.tile_width) in mat)

    def has_top_left(self,i,y,i_, mat, maptop, matleft, maptopleft):
        return ( self.matrix_picture[i][y][i_]["y"]%self.room_height > 0 and self.matrix_picture[i][y][i_]["x"]%self.room_width > 0 and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["y"]%self.room_height == 0 and not self.matrix_picture[i][y][i_]["x"]%self.room_width == 0 and i>0 and self.matrix_picture[i-1][y] and self.matrix_picture[i-1][y][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]%self.room_width == 0 and not self.matrix_picture[i][y][i_]["y"]%self.room_height == 0 and y>0 and self.matrix_picture[i][y-1] and self.matrix_picture[i][y-1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]%self.room_width == 0 and self.matrix_picture[i][y][i_]["y"]%self.room_height == 0 and y>0 and i>0 and self.matrix_picture[i-1][y-1] and self.matrix_picture[i-1][y-1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]-self.tile_width, self.matrix_picture[i][y][i_]["y"]-self.tile_width) in mat+maptopleft+maptop+matleft

    def has_top_right(self,i,y,i_, mat, maptop, matright, maptopright):
        return ( self.matrix_picture[i][y][i_]["y"]%self.room_height > 0 and self.matrix_picture[i][y][i_]["x"]%self.room_width < self.room_width-self.tile_width and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or  (self.matrix_picture[i][y][i_]["x"]%self.room_width == self.room_width-self.tile_width and not self.matrix_picture[i][y][i_]["y"]%self.room_height == 0 and y<len(self.matrix_picture[i])-1 and self.matrix_picture[i][y+1] and self.matrix_picture[i][y+1][0]["img"]==len(self.all_pic)-2)or (self.matrix_picture[i][y][i_]["y"]%self.room_height == 0 and not self.matrix_picture[i][y][i_]["x"]%self.room_width == self.room_width-self.tile_width and i>0 and self.matrix_picture[i-1][y] and self.matrix_picture[i-1][y][0]["img"]==len(self.all_pic)-2)or(self.matrix_picture[i][y][i_]["y"]%self.room_height == 0 and self.matrix_picture[i][y][i_]["x"]%self.room_width == self.room_width-self.tile_width and y<len(self.matrix_picture[i])-1 and i>0 and self.matrix_picture[i-1][y+1] and self.matrix_picture[i-1][y+1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]+self.tile_width, self.matrix_picture[i][y][i_]["y"]-self.tile_width) in maptopright+mat+maptop+matright
    
    def has_bot_left(self,i,y,i_,mat, mapbot, matleft, matbotleft):
        return ( self.matrix_picture[i][y][i_]["y"]%self.room_height < self.room_height-self.tile_width and self.matrix_picture[i][y][i_]["x"]%self.room_width > 0 and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or  (self.matrix_picture[i][y][i_]["y"]%self.room_height == self.room_height-self.tile_width and not self.matrix_picture[i][y][i_]["x"]%self.room_width == 0 and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y] and self.matrix_picture[i+1][y][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]%self.room_width == 0 and not self.matrix_picture[i][y][i_]["y"]%self.room_height == self.room_height-self.tile_width and y>0 and self.matrix_picture[i][y-1] and self.matrix_picture[i][y-1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]%self.room_width == 0 and y>0 and self.matrix_picture[i][y][i_]["y"]%self.room_height == self.room_height-self.tile_width and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y-1] and self.matrix_picture[i+1][y-1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]-self.tile_width, self.matrix_picture[i][y][i_]["y"]+self.tile_width) in mat+matbotleft+mapbot+matleft
    
    def has_bot_right(self,i,y,i_,mat, mapbot, matright, matbotright):
        return ( self.matrix_picture[i][y][i_]["y"]%self.room_height < self.room_height-self.tile_width and self.matrix_picture[i][y][i_]["x"]%self.room_width < self.room_width-self.tile_width and self.matrix_picture[i][y][0]["img"]==len(self.all_pic)-2) or  (self.matrix_picture[i][y][i_]["x"]%self.room_width == self.room_width-self.tile_width and not self.matrix_picture[i][y][i_]["y"]%self.room_height == self.room_height-self.tile_width and y<len(self.matrix_picture[i])-1 and self.matrix_picture[i][y+1] and self.matrix_picture[i][y+1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["y"]%self.room_height == self.room_height-self.tile_width and not self.matrix_picture[i][y][i_]["x"]%self.room_width == self.room_width-self.tile_width and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y] and self.matrix_picture[i+1][y][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["y"]%self.room_height == self.room_height-self.tile_width and self.matrix_picture[i][y][i_]["x"]%self.room_width == self.room_width-self.tile_width and y<len(self.matrix_picture[i])-1 and i<len(self.matrix_picture)-1 and self.matrix_picture[i+1][y+1] and self.matrix_picture[i+1][y+1][0]["img"]==len(self.all_pic)-2) or (self.matrix_picture[i][y][i_]["x"]+self.tile_width, self.matrix_picture[i][y][i_]["y"]+self.tile_width) in mat+matbotright+mapbot+matright

    def re_initialize_gen_var(self, mat=True):
        self.gen_current_height=random.randint(1, self.gen_max_height)
        # 1 and not min because on the right it can be less than the min
        self.gen_current_width=random.randint(self.gen_min_width, self.gen_max_width)
        # self.gen_current_width=1

    def _init_all_pics(self, directory):

        for i in range(21):
            pic=pygame.image.load(f"{directory}\\assets\\TreasureHunters\\PalmTreeIsland\\Sprites\\Terrain\\{str(i)}.png")
            pic=pygame.transform.scale(pic, (self.tile_width,self.tile_width))
            self.all_pic.append(pic)

        # pic=pygame.Surface((self.tile_width, self.tile_width))
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

    def _spawn_big_ground(self, i, z, i_, y_, tmp):
        self.matrix_map[i][z]["ground"].append([pygame.Rect(z*self.room_width+(tmp)*self.tile_width, i*self.room_height+i_*self.tile_width, self.tile_width*(y_-tmp), self.tile_width)])

    def _spawn_big_ceilling(self, i, z, i_, y_, tmp):
        self.matrix_map[i][z]["ceilling"].append([pygame.Rect(z*self.room_width+(tmp)*self.tile_width, i*self.room_height+i_*self.tile_width, self.tile_width*(y_-tmp), self.tile_width)])

    def _spawn_big_walls(self, i, z, i_, y_, tmp):
        self.matrix_map[i][z]["wall"].append([pygame.Rect(z*self.room_width+y_*(self.tile_width), i*self.room_height+(tmp)*self.tile_width+self.increment, self.tile_width, self.tile_width*(i_-tmp) - 2*+self.increment)])

    def _get_hill_heights(self, starting_height, width=0):
        bool_=False
        if width==0:
            width=self.gen_width_hill
            bool_=True
        tab=[]
        for _ in range(width):
            tab.append(random.randint(self.gen_min_hill_height, self.gen_max_hill_height))
        
        while sum(tab)>(self.room_height//self.tile_width)-starting_height:
            i = random.randint(0, len(tab)-1)
            if bool_ and tab[i]>self.gen_min_hill_height: tab[i]-=1
            elif not bool_ and tab[i]>0: tab[i]-=1
        
        while sum(tab)<(self.room_height//self.tile_width)-starting_height:
            i = random.randint(0, len(tab)-1)
            if tab[i]<self.gen_max_hill_height: tab[i]+=1
        tab.append(0)
        return tab

    def _change_height_ground(self):
        # choosing the height to add, remove or keep
        # 3 => up
        # 2 => up
        # 1 => down
        if self.gen_current_height<self.gen_max_height and self.gen_current_height>1:c = random.randint(1,2)
        elif self.gen_current_height<self.gen_max_height: c=2
        else: c=1
        if c==1: self.gen_current_height-=1
        else:self.gen_current_height+=1
        return c

    def _generate_relief_ground(self,start, end, node, mat, additionnal_height=0, hill=0,start_height=0, debug=False, noderight=None, island=False):
        """
        hill : 
        1 : classique left / 2 : right
        3 : vers le bas left / 4 : right
        5 : falaise left / 6 : right
        """
        if debug:
            print(start, end, node, additionnal_height, hill)
        i_=start
        if hill : 
            if hill==1:tab=self._get_hill_heights(self.gen_current_height)
            elif hill==2:
                starting_height=0
                for i,line in enumerate(mat):
                    if line[1]==1:
                        starting_height=len(mat)-1-i
                        break
                tab=self._get_hill_heights(starting_height)
            elif hill==3 or hill == 4:
                starting_height=0
                for i,line in enumerate(mat):
                    if line[1]==1:
                        starting_height=i
                        break
                tab=self._get_hill_heights(starting_height)
            elif hill==5 or hill==6:
                tab=self._get_hill_heights(0, width=end-start)
            i____=0
        while i_ <= end:
            # if the map on the left didnt had enough place to finish generating its reliefs then we finish it here so that it doesnt abrutly stop
            # if and only if there is a map on the left
            if self.gen_current_width==0:
                if not hill:
                    c=self._change_height_ground()

                    self.gen_current_width=random.randint(self.gen_min_width, self.gen_max_width)
                    # saving the width that we cant generate here because of a lack of place so that we can generating it if there is a room on the right
                    if i_+self.gen_current_width>end:
                        width_=end-i_+1
                        self.gen_current_width=self.gen_current_width-width_
                    else: 
                        if not node[1] and end - (i_+self.gen_current_width) < self.gen_min_width:
                            if self.gen_current_width >= self.gen_min_reduced_width: self.gen_current_width-=end - (i_+self.gen_current_width)
                            else: self.gen_current_width+=end - (i_+self.gen_current_width)
                            
                        width_=self.gen_current_width
                        self.gen_current_width=0

                else:
                    if -start+i_-i____>=len(tab):break
                    if hill==1 or hill==3 or hill == 6:self.gen_current_height+=tab[-start+i_-i____]
                    elif hill==2 or hill == 4 or hill==5:self.gen_current_height-=tab[-start+i_-i____]
                    self.gen_current_width=0
                    width_=self.gen_width_width_hill
                    i____+=self.gen_width_width_hill-1
                if width_>self.gen_min_width or (not island and (node[1] or hill!=0)):
                    # also generating the tiles below the current height
                    for i__ in range(i_, i_+width_):
                        if hill != 3 and hill != 4 and hill!=5 and hill != 6:
                            for y in range(self.room_height//self.tile_width-(self.gen_current_height+additionnal_height)-1 -start_height, self.room_height//self.tile_width - start_height):
                                mat[y][i__]=1
                        else:
                            for y in range(0, self.gen_current_height+additionnal_height):
                                mat[y][i__]=1
                    # to avoid a tile alone when down


                #    if i_+width_==len(mat[y]) and self.gen_current_width==0 and noderight and noderight[3]:
                # y pas 0
                # gros bugs chelou ???? remettre y

                    if i_+width_==len(mat[0]) and self.gen_current_width==0 and noderight and noderight[3]:
                        self.gen_current_width=10

                else:
                    if c==1: self.gen_current_height+=1
                    else:self.gen_current_height-=1
                    for i__ in range(i_, i_+width_):
                        for y in range(self.room_height//self.tile_width-(self.gen_current_height+additionnal_height)-1 -start_height, self.room_height//self.tile_width - start_height):
                            mat[y][i__]=1
                i_+=width_
                
            else:
                if i_+self.gen_current_width>end:
                    width_=end-i_+1
                    self.gen_current_width=self.gen_current_width-width_
                else:
                    width_=self.gen_current_width
                    self.gen_current_width=0
                # finishing the last relief of the map on the left 
                for i__ in range(i_, i_+width_):
                    for y in range(self.room_height//self.tile_width-self.gen_current_height-1-additionnal_height-start_height, self.room_height//self.tile_width - start_height):
                        mat[y][i__]=1

                i_+=width_
                
    def complete_picture_matrix(self, i, z, node):
        mat=self.all_mat[i][z]
        g=0
        d=len(mat[0])
        h=0
        b=len(mat)

        for i_ in range(h, b):
            tmp=-1
            tmp2=-1
            for y_ in range(g, d):
                if mat[i_][y_]:
                    self.matrix_picture[i][z].append({"x":z*self.room_width+y_*self.tile_width,"y":i*self.room_height+i_*self.tile_width,"img":0})
                    
                    #adding little ground if there is a change of 
                    # left
                    if ((y_>g and not mat[i_][y_-1] and i_<len(mat)-1 and mat[i_+1][y_-1] and i_>0 and not mat[i_-1][y_]) or (y_==g and z>0 and self.all_mat[i][z-1] and not self.all_mat[i][z-1][i_][-1] and i_<len(mat)-1 and self.all_mat[i][z-1][i_+1][-1] and i_>0 and not mat[i_-1][y_])):
                        self.matrix_picture[i][z].append({"x":z*self.room_width+(y_-0.5)*self.tile_width,"y":i*self.room_height+(i_+0.5)*self.tile_width,"img":len(self.all_pic)-1})
                        self.matrix_map[i][z]["little_ground"].append([pygame.Rect(z*self.room_width+(y_-0.6)*self.tile_width, i*self.room_height+(i_+0.5)*self.tile_width, self.tile_width/4, self.tile_width/2)])
                    #  or (y==d-1 and self.last_mat and not self.last_mat[i_][0])
                    # right
                    if ((y_<d-1 and not mat[i_][y_+1] and i_<len(mat)-1 and mat[i_+1][y_+1] and i_>0 and not mat[i_-1][y_]) or (y_==d-1 and node[1] and self.gen_current_width==0)):
                        self.matrix_picture[i][z].append({"x":z*self.room_width+(y_+1)*self.tile_width,"y":i*self.room_height+(i_+0.5)*self.tile_width,"img":len(self.all_pic)-1})
                        self.matrix_map[i][z]["little_ground"].append([pygame.Rect(z*self.room_width+(y_+1.1)*self.tile_width, i*self.room_height+(i_+0.5)*self.tile_width, self.tile_width/4, self.tile_width/2)])

                    # ground
                    if tmp == -1 and ((i_>0 and not mat[i_-1][y_]) or (i_==0 and i>0 and self.all_mat[i-1][z] and not self.all_mat[i-1][z][-1][y_])) :
                        tmp=y_
                    # not elif because if lenght is 1
                    if tmp != -1 and (y_ == d-1 or not mat[i_][y_+1] or ((i_>0 and mat[i_-1][y_+1]) or (i_==0 and i>0 and self.all_mat[i-1][z] and self.all_mat[i-1][z][-1][y_+1]))):

                        if tmp==y_ or tmp>1 or z==0 or len(self.graphe[i][z-1])==0 or not self.graphe[i][z-1][3] or self.graphe[i][z][0] or len(mat)-1-i_ > self.gen_max_height or (tmp*self.tile_width)%self.room_width>2*self.tile_width:inc=0
                        else: inc=0.5

                        if tmp==y_ or y_<len(mat)-2 or z==len(self.graphe[0])-1 or len(self.graphe[i][z+1])==0 or not self.graphe[i][z+1][3] or self.graphe[i][z][1] or len(mat)-1-i_ > self.gen_max_height or (y_*self.tile_width)%self.room_width<self.room_width-2*self.tile_width:inc2=0
                        else: inc2=0.5
                        self._spawn_big_ground(i, z, i_, y_+1-inc2, tmp+inc)
                        tmp=-1

                    # ceillings
                    if i_<len(mat)-1:
                        if tmp2 == -1 and (not mat[i_+1][y_]) :tmp2=y_
                        # not elif because if lenght is 1
                        if tmp2 != -1 and (y_ == d-1 or not mat[i_][y_+1] or (i_<len(mat)-1 and ( mat[i_+1][y_+1] or mat[i_+1][y_]))):
                            self._spawn_big_ceilling(i, z, i_, y_+1, tmp2)
                            tmp2=-1
        if i>0:
            tmp=-1
            for y_ in range(g, d):
                if tmp==-1 and not mat[0][y_] and self.all_mat[i-1][z] and self.all_mat[i-1][z][-1][y_] and not mat[1][y_]: tmp=y_
                if tmp != -1 and (y_==d-1 or mat[1][y_+1] or mat[0][y_+1] or not self.all_mat[i-1][z][-1][y_+1]):
                    self._spawn_big_ceilling(i-1, z, len(mat)-1, y_+1, tmp)
                    tmp=-1

        for y_ in range(g, d):
            tmp=-1
            type_=0
            for i_ in range(h, b):
                if mat[i_][y_]:
                    if tmp == -1 and  ((y_==0 or y_==len(mat[0])-1) or ((y_>0 and y_<len(mat[0])-1) and (not mat[i_][y_-1] or not mat[i_][y_+1]))):
                        if ((y_!=len(mat[0])-1 or not mat[i_][y_-1])or (y_==len(mat[0])-1 and z<len(self.all_mat[0])-1 and (not self.all_mat[i][z+1] or not self.all_mat[i][z+1][i_][0]))) and ((y_>0 or not mat[i_][y_+1]) or (y_==0 and z>0 and (not self.all_mat[i][z-1] or not self.all_mat[i][z-1][i_][-1]))):
                            if (y_==0 and mat[i_][y_+1]) or not mat[i_][y_-1]: type_=1
                            tmp=i_
                        
                        # not elif because if lenght is 1
                    if tmp != -1 and type_ == 1 and (i_ == b-1 or not mat[i_+1][y_] or ((y_>0 and mat[i_][y_-1]) or (y_==0 and z>0 and (not self.all_mat[i][z-1] or self.all_mat[i][z-1][i_][-1])))):
                        if i_-tmp>=1 : self._spawn_big_walls(i, z, i_+1, y_, tmp)
                        elif (i_>0 and mat[i_-1][y_]) or (i_==0 and i>0 and self.all_mat[i-1][z] and self.all_mat[i-1][z][-1][y_]) :  self._spawn_big_walls(i, z, i_+1, y_, tmp-1)
                        tmp=-1
                        
                    elif tmp != -1 and type_ == 0 and (i_ == b-1 or not mat[i_+1][y_] or ((not y_==len(mat[0])-1 and mat[i_][y_+1]) or (y_==len(mat[0])-1 and z<len(self.all_mat[0])-1 and (not self.all_mat[i][z+1] or self.all_mat[i][z+1][i_][0])))):
                        if i_-tmp>=1 : self._spawn_big_walls(i, z, i_+1, y_, tmp)
                        elif (i_>0 and mat[i_-1][y_]) or (i_==0 and i>0 and self.all_mat[i-1][z] and self.all_mat[i-1][z][-1][y_]) :  self._spawn_big_walls(i, z, i_+1, y_, tmp-1)
                        tmp=-1

    def generate_relief(self, i, z, node):
        # matrix used after for objects and images
        mat = [[0 for _ in range(self.room_width//self.tile_width)] for _ in range(self.room_height//self.tile_width)]

        # adding big walls or ground when there is no path
        if not node[0] or not node[1]: 
            for i_ in range (self.room_height//self.tile_width):
                if not node[0]: mat[i_][0]=1
                if not node[1]: mat[i_][-1]=1
        if not node[2] or not node[3]: 
            for i_ in range (self.room_width//self.tile_width):
                if not node[2]: mat[0][i_]=1
                if not node[3]: mat[-1][i_]=1

        
        if node[0] and node[2] : 
            mat[0][0]=1
        if node[0] and node[3] :
            if i<len(mat)-1 and z>0 and self.graphe[i][z-1][3] and not self.graphe[i+1][z][0] and not self.graphe[i+1][z][3] and not self.graphe[i+1][z-1][3]:
                mat[-1][1]=1 
            mat[-1][0]=1
        if node[1] and node[2] : 
            mat[0][-1]=1
        if node[1] and node[3] : 
            mat[-1][-1]=1
            if i<len(mat)-1 and z<len(self.graphe)-1 and self.graphe[i][z+1][3] and not self.graphe[i+1][z][1] and not self.graphe[i+1][z][3] and not self.graphe[i+1][z+1][3]:
                mat[-1][-2]=1

        # ground, generation is from left to right
        if not node[3]:
            if z<len(self.graphe[i])-1:right_node=self.graphe[i][z+1]
            else:right_node=None
            self._generate_relief_ground(0, (self.room_width//self.tile_width)-1, node, mat, noderight=right_node)

        # falaise droite
        # generation of the top left corner
        if i<len(self.graphe)-1 and z<len(self.graphe[0])-1 and node[1] and node[3] and self.graphe[i][z+1][3] and self.graphe[i+1][z+1][3] and not self.graphe[i+1][z][3] and not self.graphe[i+1][z][1]:
            self.re_initialize_gen_var()
            self._generate_relief_ground((self.room_width//self.tile_width)-1, (self.room_width//self.tile_width)-1, node, mat)

        # generation of the ground
        if i<len(self.graphe)-1 and z>0 and node[0] and node[3] and self.graphe[i][z-1][3] and self.graphe[i+1][z][3] and not self.graphe[i+1][z-1][3]  and not self.graphe[i+1][z-1][1]:
            #self.re_initialize_gen_var()
            self._generate_relief_ground(0, random.randint(self.gen_falaise_min_width, self.gen_falaise_max_width), node, mat)

        # generation of the bottom of the falaise
        if i>0 and z>0 and not node[0] and node[3] and node[2] and self.graphe[i-1][z][0] and self.graphe[i-1][z-1][3] and not self.graphe[i][z-1][3]:
            tmp=0
            for y___ in range(len(mat[i])):
                if self.all_mat[i-1][z][-1][y___]==0:
                    break
                tmp+=1
            self.gen_current_height, self.gen_current_width = len(mat)-1, 0
            self._generate_relief_ground(0, tmp, node, mat, hill=5)
            self.gen_current_height, self.gen_current_width = 0, 0

        # falaise gauche
        # generation of the top right corner
        if i<len(self.graphe)-1 and z>0 and node[0] and node[3] and self.graphe[i][z-1][3] and self.graphe[i+1][z-1][3] and not self.graphe[i+1][z][3] and not self.graphe[i+1][z][0]:
            self._generate_relief_ground(0, 0, node, mat)

        # generation of the ground
        if i<len(self.graphe)-1 and z<len(mat)-1 and node[1] and node[3] and self.graphe[i][z+1][3] and self.graphe[i+1][z][3] and not self.graphe[i+1][z+1][3] and not self.graphe[i+1][z+1][0]:
            self.re_initialize_gen_var()
            self._generate_relief_ground(random.randint(self.gen_falaise_min_width, self.gen_falaise_max_width), len(mat[0])-1, node, mat)

        # # generation of the bottom of the falaise
        if i>0 and z<len(mat)-1 and not node[1] and node[3] and node[2] and self.graphe[i-1][z][1] and self.graphe[i-1][z+1][3] and not self.graphe[i][z+1][3]:
            tmp=len(mat[i])
            for y___ in range(len(mat[i])-1, -1, -1):
                if self.all_mat[i-1][z][-1][y___]==0:
                    break
                tmp-=1
            self.gen_current_height, self.gen_current_width = 0, 0
            self._generate_relief_ground(tmp, len(mat[0])-1, node, mat, hill=6)
            self.re_initialize_gen_var()
                        
        # hills generation from left to right
        if i>0 and z<len(self.graphe[i])-1 and not node[3] and node[2] and not node[1] and self.graphe[i-1][z][1] and self.graphe[i-1][z+1][3] and not self.graphe[i][z+1][3]:
            self.gen_current_width=0
            self._generate_relief_ground((self.room_width//self.tile_width)-2-self.gen_width_hill*self.gen_width_width_hill, (self.room_width//self.tile_width)-2, node, mat, hill=1)
            self.re_initialize_gen_var()

        if i>0 and z>0 and not node[3] and node[2] and not node[0] and self.graphe[i-1][z][0] and self.graphe[i-1][z-1][3] and not self.graphe[i][z-1][3]:
            old_height, old_width=self.gen_current_height, self.gen_current_width
            self.gen_current_height, self.gen_current_width = len(mat)-1, 0
            self._generate_relief_ground(2, self.gen_width_hill*self.gen_width_width_hill+2, node, mat, hill=2)
            for tmp in range(len(mat)-1):
                mat[tmp][1]=1
            self.gen_current_height, self.gen_current_width = old_height, old_width    

        # continuing relief when down and (right or left)
        if node[3] and node[0] and not (node[2] and self.graphe[i+1][z] and self.graphe[i+1][z][0] and self.graphe[i][z-1] and self.graphe[i][z-1][3]):
            if self.gen_current_width==0:
                self._change_height_ground()
            for y in range(self.room_height//self.tile_width-self.gen_current_height-1, self.room_height//self.tile_width):
                mat[y][0]=1
                if i<len(mat)-1 and z>0 and self.graphe[i][z-1][3] and not self.graphe[i+1][z][0] and not self.graphe[i+1][z][3] and not self.graphe[i+1][z-1][3]:
                    mat[y][1]=1

        if node[3] and node[1] and not (node[2] and self.graphe[i+1][z] and self.graphe[i+1][z][1] and self.graphe[i][z+1] and self.graphe[i][z+1][3]):
            # not reset when falaise gauche
            if not (i<len(self.graphe)-1 and z<len(mat)-1 and node[1] and node[3] and self.graphe[i][z+1][3] and self.graphe[i+1][z][3] and not self.graphe[i+1][z+1][3] and not self.graphe[i+1][z+1][0]):
                self.re_initialize_gen_var(False)

            self.gen_current_width-=1
            for y in range(self.room_height//self.tile_width-self.gen_current_height-1, self.room_height//self.tile_width):
                mat[y][-1]=1
                # hill stuff
                if i<len(mat)-1 and z<len(self.graphe)-1 and self.graphe[i][z+1][3] and not self.graphe[i+1][z][1] and not self.graphe[i+1][z][3] and not self.graphe[i+1][z+1][3]:
                    mat[y][-2]=1

        # hills on ceilling generation from left to right
        if i<len(self.graphe) and z<len(self.graphe[i])-1 and not node[2] and node[3] and not node[1] and self.graphe[i+1][z][1] and self.graphe[i+1][z+1][2] and not self.graphe[i][z+1][2]:
            old_height, old_width=self.gen_current_height, self.gen_current_width
            self.gen_current_height, self.gen_current_width = 0, 0
            self._generate_relief_ground((self.room_width//self.tile_width)-2-self.gen_width_hill*self.gen_width_width_hill, (self.room_width//self.tile_width)-2, node, mat, hill=3)
            self.gen_current_height, self.gen_current_width = old_height, old_width

        if i<len(self.graphe) and z>0 and not node[2] and node[3] and not node[0] and self.graphe[i+1][z][0] and self.graphe[i+1][z-1][2] and not self.graphe[i][z-1][2]:
            old_height, old_width=self.gen_current_height, self.gen_current_width
            self.gen_current_height, self.gen_current_width = len(mat)-1, 0
            self._generate_relief_ground(2, self.gen_width_hill*self.gen_width_width_hill+2, node, mat, hill=4)
            for tmp in range(len(mat)-1):
                mat[tmp][1]=1
            self.gen_current_height, self.gen_current_width = old_height, old_width 

        self.all_mat[i][z]=mat[::]

    def load_map(self, node, i, z, empty=False):
        """call load_objects_map if the map is not empty and load all tiles for the map widht the coordinates i and z""" 

        self.matrix_map[i][z]={"wall":[], "ground":[], "little_ground":[], "ceilling":[], "platform":[],"bot":{"platform_right":[], "platform_left":[], "platform_go_right":[], "platform_go_left":[]}, "spawn_player":(), "object_map":(), "object_map":(), "spawn_crab":[], "info":{"beated":True, "type":node}}
        # [g, d, h, b]
        if node:
            self.complete_picture_matrix(i, z, node)
            if node[3] and not node[0] and not node[1]:self.re_initialize_gen_var()
        else:
            #self._spawn_big_walls(i,z,dico,0,0,len(self.all_mat[i][z]))
            self._spawn_big_ceilling(i,z,self.room_height//self.tile_width-1,0,self.room_width//self.tile_width)
            self.matrix_picture[i][z].append({"x":z*self.room_width+self.tile_width,"y":i*self.room_height+self.tile_width,"img":len(self.all_pic)-2})

            for i_ in range(self.room_height//self.tile_width):
                self.matrix_picture[i][z].append({"x":z*self.room_width,"y":i*self.room_height+i_*self.tile_width,"img":0})
                if i_ == 0 or i_ == self.room_height//self.tile_width-1:
                    for y in range(1,self.room_width//self.tile_width-1):
                        self.matrix_picture[i][z].append({"x":z*self.room_width+y*self.tile_width,"y":i*self.room_height+i_*self.tile_width,"img":0})

                self.matrix_picture[i][z].append({"x":z*self.room_width+(self.room_width//self.tile_width-1)*self.tile_width,"y":i*self.room_height+i_*self.tile_width,"img":0})


            self.re_initialize_gen_var()


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
            for i, line in enumerate(self.graphe):
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
                        surface.blit(tile, (self.screen_width/2 + self.coord_current_map[0]*self.tm.width*self.tm.tilewidth*self.zoom +x*self.tm.tilewidth*self.zoom +  - cam_x, self.screen_height/2 + self.coord_current_map[1]*self.tm.height*self.tm.tileheight*self.zoom + y*self.tm.tileheight*self.zoom - cam_y))
                    x+=1
                x=0
                y += 1