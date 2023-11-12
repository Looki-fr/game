from map.graph_generator import Graph
from math import ceil, sqrt
import time
import random
import pygame
from seed import seed
random.seed(seed)
class MapGeneration:
    def __init__(self, screen_width, screen_height, directory, zoom):
        self.directory=directory
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.g = Graph(5,5,3,1)

        self.graphe=self.g.get_matrix()
        new_graph=[]
        new_graph.insert(0, [[] for _ in range(len(self.graphe[0])+2)])
        
        for i in range(len(self.graphe)):
            new_graph.append([[]]+[self.graphe[i][z] for z in range(len(self.graphe[i]))]+[[]])
        
        new_graph.append([[] for _ in range(len(self.graphe[0])+2)])
        self.graphe=new_graph
        self.g.printTab(self.graphe)

        self.zoom=zoom
        self.tile_width=20*self.zoom
        self.room_width=self.tile_width*30
        self.room_height=self.tile_width*20
        
        self.gen_current_height=0
        self.gen_current_width=0
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
        self.gen_reboucher_mur_max_height=4
        # carre map 
        self.gen_carre_width=2*(self.room_width//self.tile_width)//5

        self.all_mat=[[None for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]
        self.all_island=[[False for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]
        self.all_hills=[[0 for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]
        # value : dictionnary : keys : id of the tile value : image of the tile

        # matrix map is used to load all the map objects
        self.matrix_map=[[None for _ in range(len(self.graphe[0]))] for _ in range(len(self.graphe))]
        
        for i,line in enumerate(self.graphe):
            for z,node in enumerate(line):
                if node : self._get_hills(i,z,node)

        for i,line in enumerate(self.graphe):
            self.re_initialize_gen_var()
            #parameters for the generation of reliefs
            for z,node in enumerate(line):
                    # E and S correspond to if the map has a neightboor on the right or on the bot
                if node:
                    self.generate_relief(i, z, node)
                    if node[3] and not node[0] and not node[1]:self.re_initialize_gen_var()
                    if not self.all_island[i][z]==None and (node[2] and (i==0 or not self.all_island[i-1][z]) and random.randint(1,5)==1) or (node[0] and node[1] and node[2] and node[3]) or (not node[0] and not node[1] and not node[2] and node[3] and random.randint(1,2)==1) or (node[2] and node[3] and random.randint(1,4)==1) or ((node[1] or node[0]) and node[2] and node[3] and random.randint(1,2)==1):
                        self.all_island[i][z]=True

        seen_better_bottom=set()
        # spawn of object 
        for i,line in enumerate(self.graphe):
            for z,node in enumerate(line):
                
                if node : self._get_hills(i,z,node, after_island=True)
                
                # removing corners when square
                if node and node[2] and node[3] and node[1] and self.graphe[i+1][z] and self.graphe[i+1][z][1] and self.graphe[i][z+1] and self.graphe[i][z+1][3]:
                    self.all_mat[i][z][-1][-1]=0
                    self.all_mat[i][z+1][-1][0]=0
                    self.all_mat[i+1][z][0][-1]=0
                    self.all_mat[i+1][z+1][0][0]=0
                

                # better bottom of ceillings
                self.manage_better_ceillings(i,z,node, seen_better_bottom)
                
                # spawn islands when big vertical space
                if node and not self.all_island[i][z] and node[3] and not self.all_island[i+1][z] and self.graphe[i+1][z][3] and not self.all_island[i+2][z]:  
                    self.all_island[i+random.randint(0,2)][z]=True

                # removing hills and islands when square
                if node and node[1] and node[3] and self.graphe[i+1][z][1] and self.graphe[i][z+1][3]:
                    self.spawn_square_map(i,z)

        self._spawn_island()

    def _get_hills(self,i,z,node, after_island=False):
        """
        hill : 
        1 : classique left / 2 : right
        3 : vers le bas left / 4 : right
        5 : falaise left / 6 : right
        7 : barre en bois qui bouche le passage de gauche à droite / 8 de haut en bas
        """
        if self.all_hills[i][z]==0 and self.all_hills[i][z]!=None: 
            if  (not (i<len(self.graphe)-1 and z<len(self.all_mat[i])-1 and node[1] and node[3] and self.graphe[i][z+1][3] and self.graphe[i+1][z][3] and not self.graphe[i+1][z+1][3] and not self.graphe[i+1][z+1][0]) or random.randint(1,2)==1) and i<len(self.graphe)-1 and z>0 and node[0] and node[3] and self.graphe[i][z-1][3] and self.graphe[i+1][z][3] and not self.graphe[i+1][z-1][3]  and not self.graphe[i+1][z-1][1]:
                self.all_hills[i][z]=5
                self.all_hills[i+1][z]=50
            elif i<len(self.graphe)-1 and z<len(self.all_mat[i])-1 and node[1] and node[3] and self.graphe[i][z+1][3] and self.graphe[i+1][z][3] and not self.graphe[i+1][z+1][3] and not self.graphe[i+1][z+1][0]:
                self.all_hills[i][z]=6
                self.all_hills[i+1][z]=60
            elif i>0 and z<len(self.graphe[i])-1 and not node[3] and node[2] and not node[1] and self.graphe[i-1][z][1] and self.graphe[i-1][z+1][3] and not self.graphe[i][z+1][3]:
                self.all_hills[i][z]=1
            elif i>0 and z>0 and not node[3] and node[2] and not node[0] and self.graphe[i-1][z][0] and self.graphe[i-1][z-1][3] and not self.graphe[i][z-1][3]:
                self.all_hills[i][z]=2
            elif i<len(self.graphe) and z<len(self.graphe[i])-1 and not node[2] and node[3] and not node[1] and self.graphe[i+1][z][1] and self.graphe[i+1][z+1][2] and not self.graphe[i][z+1][2]:
                self.all_hills[i][z]=3
            elif i<len(self.graphe) and z>0 and self.all_hills[i][z-1]==3 and not node[2] and node[3] and not node[0] and self.graphe[i+1][z][0] and self.graphe[i+1][z-1][2] and not self.graphe[i][z-1][2]:
                self.all_hills[i][z]=4
            if after_island:
                if self.all_island[i][z]!=None and not self.all_island[i][z] and node[3] and node[2] and not node[1] and not node[0] and not self.all_hills[i-1][z] == 7 and not self.all_hills[i+1][z] == 7 and random.randint(1,2)==1:
                    self.all_hills[i][z]=7
                    self.all_island[i][z]=None
                elif self.all_island[i][z]!=None and not self.all_island[i][z] and node[0] and node[1] and not node[3] and not node[2] and not self.all_hills[i][z-1] == 8 and not self.all_hills[i][z+1] == 8:
                    self.all_hills[i][z]=8
                    self.all_island[i][z]=None

    def _spawn_hills_7_8(self,mat, horizontal, debug=False):
        texture=3
        if horizontal:
            choice=random.randint(1,2)
            if choice==1:choice2=random.randint(1,2)
            for i in range(self.room_height//self.tile_width//2, 0, -1):
                if i*2+(i-1)*self.gen_reboucher_mur_max_height<=self.room_height//self.tile_width:
                    break
            
            for y in range(i):
                hole=random.randint(1,len(mat[0])-2-self.gen_reboucher_mur_max_height)
                if choice==1 and choice2==1: lst=[ h for h in range(0,hole)]
                elif choice==1 and choice2==2: lst=[ h for h in range(hole+self.gen_reboucher_mur_max_height,len(mat[0]))]
                else: lst=[ h for h in range(0,hole)] + [ h for h in range(hole+self.gen_reboucher_mur_max_height,len(mat[0]))]
                
                for z in lst: 
                    if mat[y*(self.gen_reboucher_mur_max_height+2)][z]==0: mat[y*(self.gen_reboucher_mur_max_height+2)][z]=texture
                    if mat[y*(self.gen_reboucher_mur_max_height+2)+1][z]==0: mat[y*(self.gen_reboucher_mur_max_height+2)+1][z]=texture
        else:
            for i in range(self.room_width//self.tile_width//2, 0, -1):
                if i*2+(i-1)*self.gen_reboucher_mur_max_height<=self.room_width//self.tile_width:
                    break

            for y in range(i):
                last=len(mat)-2-self.gen_reboucher_mur_max_height
                cpt=0
                for u in range(len(mat)-1, -1,-1):
                    if mat[u][y*(self.gen_reboucher_mur_max_height+2)-2]==0 and mat[u][y*(self.gen_reboucher_mur_max_height+2)-1]==0 and mat[u][y*(self.gen_reboucher_mur_max_height+2)]==0 and mat[u][y*(self.gen_reboucher_mur_max_height+2)+1]==0 and mat[u][y*(self.gen_reboucher_mur_max_height+2)+2]==0 and mat[u][y*(self.gen_reboucher_mur_max_height+2)+3]==0: cpt+=1
                    if cpt==self.gen_reboucher_mur_max_height: 
                        last=u
                        break

                hole=random.randint(1,last)
                for z in [ h for h in range(0,hole)]+[ h for h in range(hole+self.gen_reboucher_mur_max_height,len(mat))]: 
                    if mat[z][y*(self.gen_reboucher_mur_max_height+2)]==0: mat[z][y*(self.gen_reboucher_mur_max_height+2)]=texture
                    if mat[z][y*(self.gen_reboucher_mur_max_height+2)+1]==0: mat[z][y*(self.gen_reboucher_mur_max_height+2)+1]=texture

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

        # continuing relief when down and (right or left)

        # CARFUL : jai enlever :  and not (i<len(self.graphe)-1 and z>0 and node[0] and node[3] and self.graphe[i][z-1][3] and self.graphe[i+1][z][3] and not self.graphe[i+1][z-1][3]  and not self.graphe[i+1][z-1][1])

        if node[3] and node[0] and not (node[2] and self.graphe[i+1][z] and self.graphe[i+1][z][0] and self.graphe[i][z-1] and self.graphe[i][z-1][3]) :
            # if self.gen_current_width==0:
            #     self._change_height_ground()
            #     # was not here before but seems logical
            #     self.gen_current_width=random.randint(self.gen_min_width, self.gen_max_width)-1
            for y in range(self.room_height//self.tile_width-self.gen_current_height-1, self.room_height//self.tile_width):
                mat[y][0]=1
                if i<len(mat)-1 and z>0 and self.graphe[i][z-1][3] and not self.graphe[i+1][z][0] and not self.graphe[i+1][z][3] and not self.graphe[i+1][z-1][3]:
                    mat[y][1]=1

        # generation of the ground
        if self.all_hills[i][z]==5:
            #self.re_initialize_gen_var()
            self._generate_relief_ground(0, random.randint(self.gen_falaise_min_width, self.gen_falaise_max_width), node, mat, not_right=True)

        # generation of the bottom of the falaise
        if self.all_hills[i][z]==50:
            tmp=0
            for y___ in range(len(mat[i])):
                if self.all_mat[i-1][z][-1][y___]==0:
                    break
                tmp+=1
            self.gen_current_height, self.gen_current_width = len(mat)-1, 0
            self._generate_relief_ground(0, tmp, node, mat, hill=5)
            self.gen_current_height, self.gen_current_width = 0, 0

        # # generation of the bottom of the falaise
        if self.all_hills[i][z]==60:
            tmp=len(mat[i])
            for y___ in range(len(mat[i])-1, -1, -1):
                if self.all_mat[i-1][z][-1][y___]==0:
                    break
                tmp-=1
            self.gen_current_height, self.gen_current_width = 0, 0
            self._generate_relief_ground(tmp, len(mat[0])-1, node, mat, hill=6)
            self.re_initialize_gen_var()

        # hills generation from left to right
        if self.all_hills[i][z]==1:
            self.gen_current_width=0
            self._generate_relief_ground((self.room_width//self.tile_width)-2-self.gen_width_hill*self.gen_width_width_hill, (self.room_width//self.tile_width)-2, node, mat, hill=1)
            self.re_initialize_gen_var()

        if self.all_hills[i][z]==2:
            old_height, old_width=self.gen_current_height, self.gen_current_width
            self.gen_current_height, self.gen_current_width = len(mat)-1, 0
            self._generate_relief_ground(2, self.gen_width_hill*self.gen_width_width_hill+2, node, mat, hill=2)
            for tmp in range(len(mat)-1):
                mat[tmp][1]=1
            self.gen_current_height, self.gen_current_width = old_height, old_width    

        if not self.all_hills[i][z] == 6 and node[3] and node[1] and not (node[2] and self.graphe[i+1][z] and self.graphe[i+1][z][1] and self.graphe[i][z+1] and self.graphe[i][z+1][3]):
            # not reset when falaise gauche
            self.re_initialize_gen_var(False)

            self.gen_current_width-=1
            for y in range(self.room_height//self.tile_width-self.gen_current_height-1, self.room_height//self.tile_width):
                mat[y][-1]=1
                # hill stuff
                if i<len(mat)-1 and z<len(self.graphe)-1 and self.graphe[i][z+1][3] and not self.graphe[i+1][z][1] and not self.graphe[i+1][z][3] and not self.graphe[i+1][z+1][3]:
                    mat[y][-2]=1

        # hills on ceilling generation from left to right
        if self.all_hills[i][z]==3:
            old_height, old_width=self.gen_current_height, self.gen_current_width
            self.gen_current_height, self.gen_current_width = 0, 0
            self._generate_relief_ground((self.room_width//self.tile_width)-2-self.gen_width_hill*self.gen_width_width_hill, (self.room_width//self.tile_width)-2, node, mat, hill=3)
            self.gen_current_height, self.gen_current_width = old_height, old_width

        if self.all_hills[i][z]==4:
            old_height, old_width=self.gen_current_height, self.gen_current_width
            self.gen_current_height, self.gen_current_width = len(mat)-1, 0
            self._generate_relief_ground(2, self.gen_width_hill*self.gen_width_width_hill+2, node, mat, hill=4)
            for tmp in range(len(mat)-1):
                mat[tmp][1]=1
            self.gen_current_height, self.gen_current_width = old_height, old_width 

        # generation of the ground
        if self.all_hills[i][z]==6:
            self.re_initialize_gen_var()
            self._generate_relief_ground(random.randint(self.gen_falaise_min_width, self.gen_falaise_max_width), len(mat[0])-1, node, mat)

        self.all_mat[i][z]=mat[::]

    def spawn_square_map(self, i, z):
        self.all_mat[i+1][z][0][-1]=0
        self.all_mat[i+1][z+1][0][0]=0
        for i_ in range(self.gen_max_height+3):
            self.all_mat[i][z][-i_][-1]=0
            self.all_mat[i][z+1][-i_][0]=0

        if random.randint(1,2)==1:
            self.all_island[i][z]=None
            self.all_island[i][z+1]=None
            self.all_island[i+1][z]=None
            self.all_island[i+1][z+1]=None

        self.all_hills[i][z]=None
        self.all_hills[i][z+1]=None
        self.all_hills[i+1][z]=None
        self.all_hills[i+1][z+1]=None

        list_wall, list_ceilling=self._get_lists_carre()

        for i_____,level in enumerate(list_wall):
            for y_____, wall in enumerate(level):
                if wall:
                    posx=-self.gen_carre_width+y_____*self.gen_carre_width-1
                    posy=-self.gen_carre_width+i_____*self.gen_carre_width-1
                    for x in range(2):
                        posx+=x
                        for w in range(self.gen_carre_width):
                            self.all_mat[i+(1 if w+posy>=0 else 0)][z+(1 if posx>=0 else 0)][w+posy][posx]=3
        
        for i_____,level in enumerate(list_ceilling):
            for y_____, wall in enumerate(level):
                if wall:
                    posx=-self.gen_carre_width+y_____*self.gen_carre_width-1
                    posy=-self.gen_carre_width+i_____*self.gen_carre_width-1
                    for x in range(2):
                        posy+=x
                        for w in range(self.gen_carre_width):
                            self.all_mat[i+(1 if posy>=0 else 0)][z+(1 if w+posx>=0 else 0)][posy][w+posx]=3

    def manage_better_ceillings(self, i, z, node, seen_better_bottom):
        if node and (i,z) not in seen_better_bottom and not node[2]:
            seen_better_bottom.add((i,z))
            temp=[(i,z)]
            z_=z
            while self.graphe[i][z_+1] and self.graphe[i][z_+1][0]:
                seen_better_bottom.add((i,z_+1))
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

    def _get_lists_carre(self,print=False):
        """return a list of walls and ceillings for a square map"""
        g=Graph(4,4,0,0)
        mat=g.get_matrix()
        if print:g.printTab(mat)
        tab_wall = [[True for _ in range(3)] for _ in range(2)]
        tab_ceilling = [[True for _ in range(3)] for _ in range(2)]

        for i,line in enumerate(mat[1:-1]):
            for y,node in enumerate(line[1:-1]):
                if node[0]:tab_wall[i][y]=False
                if node[1]:tab_wall[i][y+1]=False

                if node[2]:tab_ceilling[i][y]=False
                if node[3]:tab_ceilling[i][y+1]=False
        
        return tab_wall,tab_ceilling

    def _spawn_island(self):
        a=self.gen_max_height ; b=self.gen_min_width ; c=self.gen_max_width
        self.gen_max_height=self.gen_island_max_height ; self.gen_min_width=self.gen_island_min_width ; self.gen_max_width=self.gen_island_max_width

        for i,line in enumerate(self.all_island):
            for z,island in enumerate(line):
                if not self.all_hills[i][z] in (7,8) and not self.all_island[i][z]==None and island and z<len(self.all_island[i])-1 and self.all_island[i][z+1] and self.graphe[i][z][1] and self.graphe[i][z][3] and self.graphe[i][z+1][3]:
                    self.gen_max_height=a ; self.gen_min_width=b ; self.gen_max_width=c
                    self.re_initialize_gen_var()
                    start=int(self.room_width//self.tile_width//2 - self.gen_island_max_width//2 + random.randint(0,self.gen_island_random_horizontal))
                    end=int(self.room_width//self.tile_width//2 + self.gen_island_max_width//2 - random.randint(0,self.gen_island_random_horizontal))
                    if self.graphe[i][z] and self.graphe[i][z][1] and self.graphe[i][z][3] and self.graphe[i+1][z][1] and self.graphe[i][z+1][3]:  start_height= round(self.gen_island_start_height*(1.3))+random.randint(-self.gen_island_additionnal_height, self.gen_island_additionnal_height)
                    elif not self.graphe[i][z][3] or not self.graphe[i][z+1][3]:start_height=len(self.all_mat[i][z])-1-self.gen_max_height-3-random.randint(0, self.gen_island_additionnal_height)
                    else:start_height= self.gen_island_start_height//2+random.randint(-self.gen_island_additionnal_height, self.gen_island_additionnal_height)
                    if self.all_hills[i][z]==4:start+=self.room_width//self.tile_width//10
                    elif self.all_hills[i][z+1]==3:end-=self.room_width//self.tile_width//10
                    if not self.all_hills[i][z] in (50,60) and i>0 and self.all_hills[i-1][z]==7: start_height=max(self.gen_island_start_height, start_height-self.room_height//self.tile_width//5)
                    if not self.all_hills[i][z] in (50,60) and i<len(self.all_hills)-1 and self.all_hills[i+1][z]==7: start_height=min(len(self.all_mat[i][z])-1-self.gen_max_height-6, start_height+self.room_height//self.tile_width//5)
                    if not self.all_hills[i][z] in (50,60) and z>0 and self.all_hills[i][z-1]==8: start, end=start+self.room_width//self.tile_width//6, end+self.room_width//self.tile_width//6
                    if not self.all_hills[i][z] in (50,60) and z<len(self.all_hills[i])-1 and self.all_hills[i][z+1]==8: start, end=start-self.room_width//self.tile_width//6, end-self.room_width//self.tile_width//6
                    self._generate_relief_ground(start if start >=0 else 0, len(self.all_mat[i][z][0])-1, self.graphe[i][z], self.all_mat[i][z], self.gen_island_additionnal_height, start_height=start_height, island=True)
                    self._generate_relief_ground(0, end if end <= len(self.all_mat[i][z][0])-1 else len(self.all_mat[i][z][0])-1, self.graphe[i][z+1], self.all_mat[i][z+1], self.gen_island_additionnal_height, start_height=start_height, island=True)
                    self._better_bottom_ceilling(-start_height-1, start, [(i,z), (i,z+1)])
                    self.gen_max_height=self.gen_island_max_height ; self.gen_min_width=self.gen_island_min_width ; self.gen_max_width=self.gen_island_max_width


                elif not self.all_hills[i][z] in (7,8) and not self.all_island[i][z]==None and island and (z==0 or not (self.all_island[i][z-1] and self.graphe[i][z][0] and self.graphe[i][z][3] and self.graphe[i][z-1][3])):
                    complete=False
                    self.re_initialize_gen_var()
                    start=int(self.room_width//self.tile_width//2 - self.gen_island_max_width//2 - random.randint(0,self.gen_island_random_horizontal))
                    end=int(self.room_width//self.tile_width//2 + self.gen_island_max_width//2 + random.randint(0,self.gen_island_random_horizontal))
                    island=True
                    # if self.all_island[i][z]==0
                    if self.all_island[i][z] and (not self.graphe[i][z][0] or not self.graphe[i][z][1]) and not self.all_hills[i-1][z] in (7,8) and not self.all_hills[i+1][z] in (7,8) and random.randint(1,3)==1:
                        island=False
                        if not self.graphe[i][z][0] and not not self.graphe[i][z][1]:
                            if random.randint(1,2)==1: start=0
                            else:  end=len(self.all_mat[i][z][0])-1
                        elif not self.graphe[i][z][0]: start=0
                        else : end=len(self.all_mat[i][z][0])-1
                    if self.all_hills[i][z]==50:
                        complete=True
                        start=0
                        start_height=random.randint(0, self.gen_island_additionnal_height)
                    elif self.all_hills[i][z]==60:
                        complete=True
                        end=len(self.all_mat[i][z][0])-1
                        start_height=random.randint(0, self.gen_island_additionnal_height)
                    elif self.all_hills[i][z] in (5,6):start_height=len(self.all_mat[i][z])-1-self.gen_max_height*2-self.gen_reboucher_mur_max_height-1
                    elif not self.graphe[i][z][3]:start_height=len(self.all_mat[i][z])-1-self.gen_max_height-3-random.randint(0, self.gen_island_additionnal_height)
                    else:start_height=self.gen_island_start_height+random.randint(-self.gen_island_additionnal_height, self.gen_island_additionnal_height)
                    if self.all_hills[i][z]==4:
                        start+=self.room_width//self.tile_width//10
                        if end-start<self.gen_island_min_width: end +=self.room_width//self.tile_width//10
                    elif self.all_hills[i][z]==3:
                        end-=self.room_width//self.tile_width//10
                        if end-start<self.gen_island_min_width: start -=self.room_width//self.tile_width//10
                    if not self.all_hills[i][z] in (50,60) and i>0 and self.all_hills[i-1][z]==7: start_height=max(self.gen_island_start_height, start_height-self.room_height//self.tile_width//5)
                    if not self.all_hills[i][z] in (50,60) and i<len(self.all_hills)-1 and self.all_hills[i+1][z]==7: start_height=min(len(self.all_mat[i][z])-1-self.gen_max_height-6, start_height+self.room_height//self.tile_width//5)
                    if not self.all_hills[i][z] in (50,60) and z>0 and self.all_hills[i][z-1]==8: start, end=start+self.room_width//self.tile_width//6, end+self.room_width//self.tile_width//6
                    if not self.all_hills[i][z] in (50,60) and z<len(self.all_hills[i])-1 and self.all_hills[i][z+1]==8: start, end=start-self.room_width//self.tile_width//6, end-self.room_width//self.tile_width//6
                    if self.graphe[i][z][2] and start_height>=(2/3)*(self.room_height//self.tile_width):
                        if self.graphe[i][z][1] and end>=len(self.all_mat[i][z][0])-4:
                            end-=3
                            start-=3
                        if self.graphe[i][z][0] and start <= 3:
                            start+=3
                            end+=3
                    self._generate_relief_ground(start if start >=0 else 0, end if end <= len(self.all_mat[i][z][0])-1 else len(self.all_mat[i][z][0])-1, self.graphe[i][z], self.all_mat[i][z], self.gen_island_additionnal_height, start_height=start_height, island=True, complete=complete)
                    self._better_bottom_ceilling(-start_height-1, start, [(i,z)], island=island)
            
                if self.all_hills[i][z]==7:
                    self._spawn_hills_7_8(self.all_mat[i][z], horizontal=True)
                
                if self.all_hills[i][z]==8:
                    self._spawn_hills_7_8(self.all_mat[i][z], horizontal=False)


        self.gen_max_height=a ; self.gen_min_width=b ; self.gen_max_width=c

    def re_initialize_gen_var(self, mat=True):
        self.gen_current_height=random.randint(1, self.gen_max_height)
        # 1 and not min because on the right it can be less than the min
        self.gen_current_width=random.randint(self.gen_min_width, self.gen_max_width)
        # self.gen_current_width=1

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
    
    def _condition_top_is_close(self,mat, max_height,i):
        if max_height-self.gen_reboucher_mur_max_height < 0 : return True
        for y in range(max_height-self.gen_reboucher_mur_max_height,max_height):
            if mat[y][i]: return True
        return False

    def _top_is_close(self, mat, max_height,i, texture=1):
        if self._condition_top_is_close(mat, max_height, i):
            start=max_height-self.gen_reboucher_mur_max_height
            if start < 0: start=0
            for y in range(start,max_height):
                mat[y][i]=texture


    def _generate_relief_ground(self,start, end, node, mat, additionnal_height=0, hill=0,start_height=0, debug=False, noderight=None, island=False, not_right=True, complete=False):
        if debug:
            print(start, end, node, additionnal_height, hill)
        i_=start
        if hill : 
            
            if hill==1:tab=self._get_hill_heights(self.gen_current_height)
            elif hill==2:
                starting_height=0
                for i,line in enumerate(mat):
                    if line[1]:
                        starting_height=len(mat)-1-i
                        break
                tab=self._get_hill_heights(starting_height)
            elif hill==3 or hill == 4:
                starting_height=0
                for i,line in enumerate(mat):
                    if line[1]:
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
                        if debug: print("not hill >>>>> end",width_, self.gen_current_height, self.gen_current_width,start,end)
                    
                    else: 
                        if not node[1] and end - (i_+self.gen_current_width) < self.gen_min_width:
                            if self.gen_current_width >= self.gen_min_reduced_width: self.gen_current_width-=end - (i_+self.gen_current_width)
                            else: self.gen_current_width+=end - (i_+self.gen_current_width)
                        
                        width_=self.gen_current_width
                        self.gen_current_width=0
                        if debug: print("not hill < end",width_, self.gen_current_height, self.gen_current_width,start,end)

                else:
                    if -start+i_-i____>=len(tab):break
                    if hill==1 or hill==3 or hill == 6:self.gen_current_height+=tab[-start+i_-i____]
                    elif hill==2 or hill == 4 or hill==5:self.gen_current_height-=tab[-start+i_-i____]
                    self.gen_current_width=0
                    width_=self.gen_width_width_hill
                    i____+=self.gen_width_width_hill-1
                if width_>self.gen_min_width or (not island and ((node[1] and not not_right) or hill!=0)):
                    # also generating the tiles below the current height
                    for i__ in range(i_, i_+width_):
                        if hill != 3 and hill != 4 and hill!=5 and hill != 6:
                            if complete :self._top_is_close(mat,self.room_height//self.tile_width-(self.gen_current_height+additionnal_height)-1 -start_height,i__)
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
                        if complete :self._top_is_close(mat,self.room_height//self.tile_width-(self.gen_current_height+additionnal_height)-1 -start_height,i__)
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
                    if complete :self._top_is_close(mat,self.room_height//self.tile_width-(self.gen_current_height+additionnal_height)-1 -start_height,i__)
                    for y in range(self.room_height//self.tile_width-self.gen_current_height-1-additionnal_height-start_height, self.room_height//self.tile_width - start_height):
                        mat[y][i__]=1

                i_+=width_
        
        if debug:
            for line in mat:
                print(line)

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