from math import ceil
from map.graph import Graphe
import random
import pygame
from map.graph_generator import get_matrix, printTab
#random.seed(123)
class RenderMap:
    def __init__(self, screen_width, screen_height, directory):
        """cf la documentation de pytmx"""
        self.directory=directory
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.graphe=get_matrix()
        printTab(self.graphe)

        self.minimap_tile_width=50            
        self.zoom=2
        self.tile_width=20*self.zoom
        self.room_width=self.tile_width*30
        self.room_height=self.tile_width*20
        
        self.increment=7*self.zoom
        self.increment_ground=30*self.zoom
        self.all_pic=[]
        self._init_all_pics()

        self.gen_max_height=4
        self.gen_min_width=7
        self.gen_max_width=15
        self.gen_min_reduced_width=12
        self.gen_width_hill=3
        self.gen_width_width_hill=1
        self.gen_max_hill_height=(self.room_height//self.tile_width)//self.gen_width_hill + 5
        self.gen_min_hill_height=2
        self.all_mat=[[None for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]

        # value : dictionnary : keys : id of the tile value : image of the tile
        self.matrix_picture=[ [[] for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]

        # matrix map is used to load all the map objects
        self.matrix_map=[[None for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]
        
        # we dont start at 0 since the map as empty maps around it
        i=0; z=0
        for i,line in enumerate(self.graphe):
            self.re_initialize_gen_var()
            #parameters for the generation of reliefs
            for z,node in enumerate(line):
                    # E and S correspond to if the map has a neightboor on the right or on the bot
                self.load_map(node, i, z)
        
        self.minimap_picture=pygame.image.load(f"{directory}\\assets\\tiled_maps\\minimap.png")
        self.minimap_picture=pygame.transform.scale(self.minimap_picture, (self.minimap_tile_width,self.minimap_tile_width))

        self.current_map_is_wave=False
        
        self.get_first_map()["info"]["beated"]=True

    def re_initialize_gen_var(self, mat=True):
        self.gen_current_height=random.randint(1, self.gen_max_height)
        # 1 and not min because on the right it can be less than the min
        self.gen_current_width=random.randint(self.gen_min_width, self.gen_max_width)
        # self.gen_current_width=1

    def _init_all_pics(self):
        pic=pygame.Surface((self.tile_width, self.tile_width))
        pic.fill((200,200,200))
        pic2=pygame.Surface((self.room_width, self.room_height))
        pic2.fill((200,200,200))
        pic3=pygame.Surface((self.tile_width//2, self.tile_width//2))
        pic3.fill((200,200,200))
        self.all_pic.append(pic)
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

    def _spawn_big_ground(self, i, z, dico, i_, y_, tmp):
        dico["ground"].append([pygame.Rect(z*self.room_width+(tmp)*self.tile_width, i*self.room_height+i_*self.tile_width, self.tile_width*(y_-tmp), self.tile_width)])

    def _spawn_big_ceilling(self, i, z, dico, i_, y_, tmp):
        dico["ceilling"].append([pygame.Rect(z*self.room_width+(tmp)*self.tile_width, i*self.room_height+i_*self.tile_width, self.tile_width*(y_-tmp), self.tile_width)])

    def _spawn_big_walls(self, i, z, dico, i_, y_, tmp):
        dico["wall"].append([pygame.Rect(z*self.room_width+y_*(self.tile_width), i*self.room_height+(tmp)*self.tile_width+self.increment, self.tile_width, self.tile_width*(i_-tmp) - 2*+self.increment)])

    def _get_hill_heights(self, starting_height):
        tab=[]
        for _ in range(self.gen_width_hill):
            tab.append(random.randint(self.gen_min_hill_height, self.gen_max_hill_height))
        
        while sum(tab)>(self.room_height//self.tile_width)-starting_height:
            i = random.randint(0, len(tab)-1)
            if tab[i]>self.gen_min_hill_height: tab[i]-=1
        
        while sum(tab)<(self.room_height//self.tile_width)-starting_height:
            i = random.randint(0, len(tab)-1)
            if tab[i]<self.gen_max_hill_height: tab[i]+=1
        tab.append(0)
        return tab

    def _generate_relief_ground(self,start, end, node, mat, additionnal_height=0, hill=False):
        i_=start

        if hill : 
            print("hill")
            if hill==1:tab=self._get_hill_heights(self.gen_current_height)
            if hill==2:
                starting_height=0
                for i,line in enumerate(mat):
                    if line[1]==1:
                        starting_height=len(mat)-1-i
                        break
                tab=self._get_hill_heights(starting_height)
            i____=0

        while i_ <= end:
            # if the map on the left didnt had enough place to finish generating its reliefs then we finish it here so that it doesnt abrutly stop
            # if and only if there is a map on the left
            if self.gen_current_width==0:
                # choosing the height to add, remove or keep
                # 3 => up
                # 2 => up
                # 1 => down

                
                if not hill:
                    if self.gen_current_height<self.gen_max_height and self.gen_current_height>1:
                        c = random.randint(1,3)
                    elif self.gen_current_height<self.gen_max_height: c=random.randint(2,3)
                    else: c=random.choice([1,3])

                    self.gen_current_width=random.randint(self.gen_min_width, self.gen_max_width)
                    # saving the width that we cant generate here because of a lack of place so that we can generating it if there is a room on the right
                    if i_+self.gen_current_width>=self.room_width//self.tile_width:
                        width_=self.room_width//self.tile_width-i_
                        self.gen_current_width=self.gen_current_width-width_
                    else: 
                        if not node[1] and self.room_width//self.tile_width - (i_+self.gen_current_width) < self.gen_min_width:
                            if self.gen_current_width >= self.gen_min_reduced_width: self.gen_current_width-=self.room_width//self.tile_width - (i_+self.gen_current_width)
                            else: self.gen_current_width+=self.room_width//self.tile_width - (i_+self.gen_current_width)
                            
                        width_=self.gen_current_width
                        self.gen_current_width=0
                    if c==1: self.gen_current_height-=1
                    else:self.gen_current_height+=1

                else:
                    if -start+i_-i____>=len(tab):break
                    if hill==1:self.gen_current_height+=tab[-start+i_-i____]
                    elif hill==2:self.gen_current_height-=tab[-start+i_-i____]
                    self.gen_current_width=0
                    width_=self.gen_width_width_hill
                    i____+=self.gen_width_width_hill-1

                if width_>self.gen_min_width or node[1] or hill!=0:
                    # also generating the tiles below the current height
                    for i__ in range(i_, i_+width_):
                        for y in range(self.room_height//self.tile_width-(self.gen_current_height+additionnal_height), self.room_height//self.tile_width-1):
                            mat[y][i__]=1
                else:
                    if c==1: self.gen_current_height+=1
                    else:self.gen_current_height-=1
                    for i__ in range(i_, i_+width_):
                        for y in range(self.room_height//self.tile_width-(self.gen_current_height+additionnal_height), self.room_height//self.tile_width-1):
                            mat[y][i__]=1

                i_+=width_
                
            else:
                # finishing the last relief of the map on the left 
                for i__ in range(i_, i_+self.gen_current_width):
                    for y in range(self.room_height//self.tile_width-self.gen_current_height, self.room_height//self.tile_width-1):
                        mat[y][i__]=1

                i_+=self.gen_current_width
                self.gen_current_width=0

    def generate_relief(self, i, z, dico, node):
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
            if z>0 and self.graphe[i][z-1][3] and not self.graphe[i+1][z][0]:
                mat[-1][1]=1 
            mat[-1][0]=1
        if node[1] and node[2] : 
            mat[0][-1]=1
        if node[1] and node[3] : 
            mat[-1][-1]=1
            if z<len(self.graphe)-1 and self.graphe[i][z+1][3] and not self.graphe[i+1][z][1]:
                mat[-1][-2]=1
        # ground, generation is from left to right
        if not node[3]:
            self._generate_relief_ground(0, (self.room_width//self.tile_width)-1, node, mat)

        # hills generation from left to right
        if i>0 and z<len(self.graphe[i])-1 and not node[3] and node[2] and not node[1] and self.graphe[i-1][z][1] and self.graphe[i-1][z+1][3] and not self.graphe[i][z+1][3]:
            old_height, old_width=self.gen_current_height, self.gen_current_width
            self.gen_current_height, self.gen_current_width = 0, 0
            self._generate_relief_ground((self.room_width//self.tile_width)-2-self.gen_width_hill*self.gen_width_width_hill, (self.room_width//self.tile_width)-2, node, mat, hill=1)
            self.gen_current_height, self.gen_current_width = old_height, old_width
            

        if i>0 and z>0 and not node[3] and node[2] and not node[0] and self.graphe[i-1][z][0] and self.graphe[i-1][z-1][3] and not self.graphe[i][z-1][3]:
            old_height, old_width=self.gen_current_height, self.gen_current_width
            self.gen_current_height, self.gen_current_width = len(mat)-1, 0
            self._generate_relief_ground(2, self.gen_width_hill*self.gen_width_width_hill+2, node, mat, hill=2)
            for tmp in range(len(mat)-1):
                mat[tmp][1]=1
            self.gen_current_height, self.gen_current_width = old_height, old_width    

        # continuing relief when down and (right or left)
        if node[3] and node[0]:
            for y in range(self.room_height//self.tile_width-self.gen_current_height, self.room_height//self.tile_width-1):
                mat[y][0]=1
                if z>0 and self.graphe[i][z-1][3] and not self.graphe[i+1][z][0]:
                    mat[y][1]=1

        if node[3] and node[1]:
            self.re_initialize_gen_var(False)
            self.gen_current_width-=1
            for y in range(self.room_height//self.tile_width-self.gen_current_height, self.room_height//self.tile_width-1):
                mat[y][-1]=1
                if z<len(self.graphe)-1 and self.graphe[i][z+1][3] and not self.graphe[i+1][z][1]:
                    mat[y][-2]=1

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
                    
                    #adding little ground if there is a change of height
                    if not node[3] and ((y_>g and not mat[i_][y_-1] and i_<len(mat)-1 and mat[i_+1][y_-1] and i_>0 and not mat[i_-1][y_]) or (y_==g and z>0 and self.all_mat[i][z-1] and not self.all_mat[i][z-1][i_][-1] and i_<len(mat)-1 and self.all_mat[i][z-1][i_+1][-1] and i_>0 and not mat[i_-1][y_])):
                        self.matrix_picture[i][z].append({"x":z*self.room_width+(y_-0.5)*self.tile_width,"y":i*self.room_height+(i_+0.5)*self.tile_width,"img":2})
                        dico["little_ground"].append([pygame.Rect(z*self.room_width+(y_-0.6)*self.tile_width, i*self.room_height+(i_+0.5)*self.tile_width, self.tile_width/4, self.tile_width/2)])
                    #  or (y==d-1 and self.last_mat and not self.last_mat[i_][0])
                    if not node[3] and ((y_<d-1 and not mat[i_][y_+1] and i_<len(mat)-1 and mat[i_+1][y_+1] and i_>0 and not mat[i_-1][y_]) or (y_==d-1 and node[1] and self.gen_current_width<=1) and z<len(self.graphe[i])-1 and not self.graphe[i][z+1][3]):
                        self.matrix_picture[i][z].append({"x":z*self.room_width+(y_+1)*self.tile_width,"y":i*self.room_height+(i_+0.5)*self.tile_width,"img":2})
                        dico["little_ground"].append([pygame.Rect(z*self.room_width+(y_+1.1)*self.tile_width, i*self.room_height+(i_+0.5)*self.tile_width, self.tile_width/4, self.tile_width/2)])

                    # ground
                    if tmp == -1 and ((i_>0 and not mat[i_-1][y_]) or (i_==0 and i>0 and self.all_mat[i-1][z] and not self.all_mat[i-1][z][-1][y_])) :
            
                        tmp=y_
                        
                    # not elif because if lenght is 1
                    if tmp != -1 and (y_ == d-1 or not mat[i_][y_+1] or ((i_>0 and mat[i_-1][y_+1]) or (i_==0 and i>0 and self.all_mat[i-1][z] and self.all_mat[i-1][z][-1][y_+1]))):
                        
                        

                        if tmp==y_ or tmp>1 or z==0 or len(self.graphe[i][z-1])==0 or not self.graphe[i][z-1][3] or self.graphe[i][z][0] or len(mat)-1-i_ > self.gen_max_height:inc=0
                        else: inc=1

                        if tmp==y_ or y_<len(mat)-2 or z==len(self.graphe[0])-1 or len(self.graphe[i][z+1])==0 or not self.graphe[i][z+1][3] or self.graphe[i][z][1] or len(mat)-1-i_ > self.gen_max_height:inc2=0
                        else: inc2=1

                        self._spawn_big_ground(i, z, dico, i_, y_+1-inc2, tmp+inc)
                        tmp=-1

                    # ceillings
                    if i_<len(mat)-1:
                        if tmp2 == -1 and not mat[i_+1][y_] :tmp2=y_
                        # not elif because if lenght is 1
                        if tmp2 != -1 and (y_ == d-1 or not mat[i_][y_+1] or mat[i_+1][y_+1] or mat[i_+1][y_]):
                            self._spawn_big_ceilling(i, z, dico, i_, y_+1, tmp2)
                            tmp2=-1

        for y_ in range(g, d):
            tmp=-1
            type_=0
            for i_ in range(h, b):
                if mat[i_][y_]:
                    if tmp == -1 and  ((y_==0 or y_==len(mat[0])-1) or ((y_>0 and y_<len(mat[0])-1) and (not mat[i_][y_-1] or not mat[i_][y_+1]))):
                        if y_==0 or not mat[i_][y_-1]: type_=1
                        tmp=i_
                        
                        # not elif because if lenght is 1
                    if tmp != -1 and type_ == 1 and (i_ == b-1 or not mat[i_+1][y_] or (not y_==0 and mat[i_][y_-1])):
                        if i_-tmp>=1 : self._spawn_big_walls(i, z, dico, i_+1, y_, tmp)
                        tmp=-1
                        
                    elif tmp != -1 and type_ == 0 and (i_ == b-1 or not mat[i_+1][y_] or (not y_==len(mat[0])-1 and mat[i_][y_+1])):
                        if i_-tmp>=1 : self._spawn_big_walls(i, z, dico, i_+1, y_, tmp)
                        tmp=-1

        self.all_mat[i][z]=mat[::]

    

    def load_map(self, node, i, z, empty=False):
        """call load_objects_map if the map is not empty and load all tiles for the map widht the coordinates i and z""" 

        self.matrix_map[i][z]={"wall":[], "ground":[], "little_ground":[], "ceilling":[], "platform":[],"bot":{"platform_right":[], "platform_left":[], "platform_go_right":[], "platform_go_left":[]}, "spawn_player":(), "object_map":(), "object_map":(), "spawn_crab":[], "info":{"beated":True, "type":node}}
        dico=self.matrix_map[i][z]
        # [g, d, h, b]
        if node:
            self.generate_relief(i, z, dico, node)
            if node[3] and not node[0] and not node[1]:self.re_initialize_gen_var()
        else:
            self.matrix_picture[i][z].append({"x":z*self.room_width,"y":i*self.room_height,"img":1})
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