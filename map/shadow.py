import random
import pygame
from seed import seed
random.seed(seed)

def lineLineIntersect(P0, P1, Q0, Q1):  
    d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
    if d == 0:
        return None
    t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
    u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return round(P1[0] * t + P0[0] * (1-t)), round(P1[1] * t + P0[1] * (1-t))
    return None

class Shadow:
    def __init__(self, tile_width, room_width, room_height, all_mat, graphe):
        # if intersection too far we don't use it
        self.tile_width = tile_width
        self.room_width = room_width
        self.room_height = room_height
        self.all_mat = all_mat
        self.graphe = graphe
        # id = index
        self.all_vertex=[]
        self.all_points=[]
        self.all_points_matrices=[[[] for _ in range(room_width//tile_width)] for _ in range(room_height//tile_width)]
        self.vertex_in_matrices = [[[] for _ in range(room_width//tile_width)] for _ in range(room_height//tile_width)]
        self._fill_all_figures()
        for i in range(len(self.vertex_in_matrices)):
            for y in range(len(self.vertex_in_matrices[i])):
                self.vertex_in_matrices[i][y]=list(set(self.vertex_in_matrices[i][y]))
                self.all_points_matrices[i][y]=list(set(self.all_points_matrices[i][y]))


    def has_neighboor(self,i,z,i_,z_,co):
        if i_+co[0]<0 and z_+co[1]<0:
            return i>0 and z>0 and self.all_mat[i-1][z-1][-1][-1]
        elif i_+co[0]<0 and z_+co[1]>len(self.all_mat[i][z][i_])-1:
            return i>0 and z<len(self.all_mat[i])-1 and self.all_mat[i-1][z+1][-1][0]
        elif i_+co[0]>len(self.all_mat[i][z])-1 and z_+co[1]<0:
            return i<len(self.all_mat)-1 and z>0 and self.all_mat[i+1][z-1][0][-1]
        elif i_+co[0]>len(self.all_mat[i][z])-1 and z_+co[1]>len(self.all_mat[i][z][i_])-1:
            return i<len(self.all_mat)-1 and z<len(self.all_mat[i])-1 and self.all_mat[i+1][z+1][0][0]
        elif i_+co[0]<0:
            return i>0 and self.all_mat[i-1][z][-1][z_]
        elif i_+co[0]>len(self.all_mat[i][z])-1:
            return i<len(self.all_mat)-1 and self.all_mat[i+1][z][0][z_]
        elif z_+co[1]<0:
            return z>0 and self.all_mat[i][z-1][i_][-1]
        elif z_+co[1]>len(self.all_mat[i][z][i_])-1:
            return z<len(self.all_mat[i])-1 and self.all_mat[i][z+1][i_][0]
        return self.all_mat[i][z][i_+co[0]][z_+co[1]]


    def _is_sommet(self,i, z, i_, z_, tile):
        coos=((-1,0), (0,1), (1,0), (0,-1))
        for c, co in enumerate(coos):
            c1=self.has_neighboor(i,z,i_,z_,co) ; c2=self.has_neighboor(i,z,i_,z_,coos[c-1]) ; c3 = self.has_neighboor(i,z,i_,z_,coos[c-2]) ; c4 = self.has_neighboor(i,z,i_,z_,coos[c-3])
            if c1 and c2 and not c3 and not c4:
                return (co, coos[c-1])
            elif not tile and c1 and c2 and c3 and not c4:
                return (co, coos[c-1], coos[c-2])

            # if c1 and c2 and c3 and c4:
            #     if not self.has_neighboor(i,z,i_,z_,(1,-1)): return ((-1,0), (0,1))
            #     if not self.has_neighboor(i,z,i_,z_,(-1,-1)): return ((0,1), (1,0))
            #     if not self.has_neighboor(i,z,i_,z_,(-1,1)): return ((1,0), (0,-1))
            #     if not self.has_neighboor(i,z,i_,z_,(1,1)): return ((-1,0), (0,-1))
        return ()
    
    def _create_sommet(self,s,i,z,i_,z_,tile, all_sommets):
        inc_x=inc_y=0
        if (-1,0) in s and (0, -1) in s: inc_x=1 ; inc_y=1
        if (-1,0) in s  and (0,1) in s: inc_y=1
        if (1,0) in s and (0,-1) in s: inc_x=1
        if not tile : 
            if inc_x==1: inc_x=0
            elif inc_x==0: inc_x=1
            if inc_y==1: inc_y=0
            elif inc_y==0: inc_y=1
            new_i_ = i_+s[0][0]+s[1][0]
            new_i=i
            new_z=z
            if new_i_ < 0:
                new_i_ = len(self.all_mat[i][z])-1
                new_i-=1
            elif new_i_ > len(self.all_mat[i][z])-1:
                new_i_ = 0
                new_i+=1
            new_z_ = z_+s[0][1]+s[1][1]
            if new_z_ < 0:
                new_z_ = len(self.all_mat[i][z][i_])-1
                new_z-=1
            elif new_z_ > len(self.all_mat[i][z][i_])-1:
                new_z_ = 0
                new_z+=1
            all_sommets.append(((i*self.room_height + (i_+inc_y)*self.tile_width, z*self.room_width + (z_+inc_x)*self.tile_width), (new_i,new_z,new_i_,new_z_)))
            return
        all_sommets.append(((i*self.room_height + (i_+inc_y)*self.tile_width, z*self.room_width + (z_+inc_x)*self.tile_width), (i,z,i_,z_)))


    def _fill_all_figures(self):
        all_sommets=[]
        for i, line in enumerate(self.all_mat):
            for z, mat in enumerate(line):
                for i_, line_mat in enumerate(mat):
                    for z_, tile in enumerate(line_mat):
                        s=self._is_sommet(i,z,i_,z_, tile)
                        if len(s)==2: self._create_sommet(s,i,z,i_,z_,tile,all_sommets)
                        elif len(s)==3: 
                            self._create_sommet(s[:2],i,z,i_,z_,tile,all_sommets)
                            self._create_sommet(s[1:],i,z,i_,z_,tile,all_sommets)

        same_x={}
        same_y={}
        for sommet in all_sommets:
            same_x[sommet[0][1]]=same_x.get(sommet[0][1],[])+[len(self.all_points)]
            same_y[sommet[0][0]]=same_y.get(sommet[0][0],[])+[len(self.all_points)]
            self.all_points.append(sommet)
            self.all_points_matrices[sommet[1][0]][sommet[1][1]].append(len(self.all_points)-1)
            if sommet[0][0]%self.room_height == 0 and sommet[1][0]>0: self.all_points_matrices[sommet[1][0]-1][sommet[1][1]].append(len(self.all_points)-1)
            if sommet[0][1]%self.room_width == 0 and sommet[1][1]>0: self.all_points_matrices[sommet[1][0]][sommet[1][1]-1].append(len(self.all_points)-1)
            if sommet[0][0]%self.room_height == self.room_height-self.tile_width and sommet[1][0]<len(self.all_mat)-1: self.all_points_matrices[sommet[1][0]][sommet[1][1]-1].append(len(self.all_points)-1)
            if sommet[0][1]%self.room_width == self.room_width-self.tile_width and sommet[1][1]<len(self.all_mat[sommet[1][0]])-1: self.all_points_matrices[sommet[1][0]][sommet[1][1]+1].append(len(self.all_points)-1)

        self._fill_vertex(same_x, same_y)
        
    def _reach(self, s1, direction, same):
        mat=[(s1[1][0], s1[1][1])]
        if direction == "top":
            i=s1[1][0] ; z=s1[1][1] ; i_=s1[1][2] ; z_=s1[1][3]
            i_-=1
            if i_ < 0:
                i_ = len(self.all_mat[i][z])-1
                i-=1
                mat.append((i,z))
            while i >=0:
                if (i, z, i_, z_) in same:
                    return same.index((i, z, i_, z_)), mat
                if self.has_neighboor(i,z,i_,z_,(0,1)) and self.has_neighboor(i,z,i_,z_,(0,-1)):
                    return None, []             
                if not self.all_mat[i][z][i_][z_]:
                    return None, []
                i_-=1
                if i_ < 0:
                    i_ = len(self.all_mat[i][z])-1
                    i-=1
                    mat.append((i,z))
                
            return None, []
        
        elif direction == "left":
            i=s1[1][0] ; z=s1[1][1] ; i_=s1[1][2] ; z_=s1[1][3]
            z_-=1
            if z_ < 0:
                z_ = len(self.all_mat[i][z][i_])-1
                z-=1
                mat.append((i,z))
            while z >=0:
                if (i, z, i_, z_) in same:
                    return same.index((i, z, i_, z_)), mat
                if self.has_neighboor(i,z,i_,z_,(1,0)) and self.has_neighboor(i,z,i_,z_,(-1,0)):
                    return None , []              
                if not self.all_mat[i][z][i_][z_]:
                    return None, []
                z_-=1
                if z_ < 0:
                    z_ = len(self.all_mat[i][z][i_])-1
                    z-=1
                    mat.append((i,z))
                
            return None, []

    def _fill_vertex(self,same_x, same_y):
        for liste in same_x.values():
            for s1 in liste:
                s1Index=s1
                s1=self.all_points[s1]
                s2, mat=self._reach(s1, "top",  [self.all_points[s][1] for s in liste])
                if s2 != None:
                    for i,z in mat:
                        self.vertex_in_matrices[i][z].append(len(self.all_vertex))

                    if s1[0][1]%self.room_width == 0 and s1[1][1]>0: self.vertex_in_matrices[s1[1][0]][s1[1][1]-1].append(len(self.all_vertex))
                    if s1[0][1]%self.room_width == self.room_width-self.tile_width and s1[1][1]<len(self.all_mat[s1[1][0]])-1: self.vertex_in_matrices[s1[1][0]][s1[1][1]+1].append(len(self.all_vertex))

                    s2index=liste[s2]
                    s2=self.all_points[liste[s2]]
                    for s in (s1,s2):
                        if s[0][0]%self.room_height == 0 and s[1][0]>0: self.vertex_in_matrices[s[1][0]-1][s[1][1]].append(len(self.all_vertex))
                        if s[0][0]%self.room_height == self.room_height-self.tile_width and s[1][0]<len(self.all_mat)-1: self.vertex_in_matrices[s[1][0]+1][s[1][1]].append(len(self.all_vertex))

                    self.all_vertex.append((s2index, s1Index))
        
        for liste in same_y.values():
            for s1 in liste:
                s1Index=s1
                s1=self.all_points[s1]
                s2, mat=self._reach(s1, "left",  [self.all_points[s][1] for s in liste])
                if s2 != None:
                    for i,z in mat:
                        self.vertex_in_matrices[i][z].append(len(self.all_vertex))

                    if s1[0][0]%self.room_height == 0 and s1[1][0]>0: self.vertex_in_matrices[s1[1][0]-1][s1[1][1]].append(len(self.all_vertex))
                    if s1[0][0]%self.room_height == self.room_height-self.tile_width and s1[1][0]<len(self.all_mat)-1: self.vertex_in_matrices[s1[1][0]+1][s1[1][1]].append(len(self.all_vertex))

                    s2index=liste[s2]
                    s2=self.all_points[liste[s2]]
                    for s in (s1,s2):
                        if s[0][1]%self.room_width == 0 and s[1][1]>0: self.vertex_in_matrices[s[1][0]][s[1][1]-1].append(len(self.all_vertex))
                        if s[0][1]%self.room_width == self.room_width-self.tile_width and s[1][1]<len(self.all_mat[s[1][0]])-1: self.vertex_in_matrices[s[1][0]][s[1][1]+1].append(len(self.all_vertex))
                    

                    self.all_vertex.append((s2index, s1Index))

    def _get_matrix(self, co_map):
        co_map=co_map[::-1]
        h=co_map[0]
        if h<0: h=0
        b=co_map[0]+1
        if b>len(self.vertex_in_matrices): b=len(self.vertex_in_matrices)
        g=co_map[1]
        if g<0: g=0
        d=co_map[1]+1
        if d>len(self.vertex_in_matrices[0]): d=len(self.vertex_in_matrices[0])
        return h,b,g,d
        # h=co_map[1]
        # b=co_map[1]+1
        # g=co_map[0]
        # d=co_map[0]+1
        # node=self.graphe[co_map[1]][co_map[0]]
        # if node:
        #     if node[0]:
        #         g-=1
        #         if self.graphe[co_map[1]][co_map[0]-1][3] or : g-=1
        #     if node[1]:d+=1
        #     if node[2]:h-=1
        #     if node[3]:b+=1
        # return h,b,g,d


    def draw_matrix(self, surface,scroll_rect, co_map):
        h,b,g,d = self._get_matrix(co_map)
        for mat in self.vertex_in_matrices[h:b]:
            for line in mat[g:d]:
                for vertex_id in line:
                    vertex=self.all_vertex[vertex_id]
                    for sommet in vertex:
                        sommet=self.all_points[sommet]
                        new_x=surface.get_width()/2 + sommet[0][1] - scroll_rect.x 
                        new_y=surface.get_height()/2 + sommet[0][0] - scroll_rect.y
                        pygame.draw.circle(surface, (255,0,0), (new_x, new_y), 5)
                    new_x=surface.get_width()/2 + self.all_points[vertex[0]][0][1] - scroll_rect.x 
                    new_y=surface.get_height()/2 + self.all_points[vertex[0]][0][0] - scroll_rect.y
                    width=self.all_points[vertex[1]][0][1]-self.all_points[vertex[0]][0][1]
                    height=self.all_points[vertex[1]][0][0]-self.all_points[vertex[0]][0][0]
                    pygame.draw.line(surface, (255,0,0), (new_x, new_y), (new_x+width, new_y+height), 5)

    def _fill_lst(self, h, b, g, d, lst, x1, y1, x2, y2):
        for mat in self.vertex_in_matrices[h:b]:
            for line in mat[g:d]:
                for vertex_id in line:
                    vertex=self.all_vertex[vertex_id]
                    y3, x3= self.all_points[vertex[0]][0]
                    y4, x4= self.all_points[vertex[1]][0]
                    P=lineLineIntersect((x1,y1), (x2,y2), (x3,y3), (x4,y4))
                    if P!=None and vertex_id not in lst:
                        lst.append(vertex_id)
                        if len(lst)>3:
                            return

    def draw_shadow(self, surface, scroll_rect, co_map, head):
        """
        
        
        
        
        
        /!\

                - se balader dans tt les points au debut et check cb de collision ils ont avec les segments de la mm map
                et ensuite check len(lst)<= ce chiffre

                                                    /!\
                                                    
                - generation lumiere : si pt est en extremite, chercher un autre point en extremite 
                generer un polygone de 1 vers loppose du joueur de tt les segments entre les 2
                et des 2 points hors map avec le +-0.0001 radian

                - sinon faire la mm avec le segment proche        
        
                - si bug creer point et segment ds la map qd certains depacent


        
        
        
        
        
        
        """





















        h,b,g,d = self._get_matrix(co_map)
        x2, y2= head.center

        for m in self.all_points_matrices[h:b]:
            for l in m[g:d]:
                for p in l:
                    p=self.all_points[p]
                    new_x=surface.get_width()/2 + p[0][1] - scroll_rect.x
                    new_y=surface.get_height()/2 + p[0][0] - scroll_rect.y
                    pygame.draw.circle(surface, (0,0,255), (new_x, new_y), 5)
                    lst=[]
                    y1, x1= p[0]
                    self._fill_lst(h, b, g, d, lst, x1, y1, x2, y2)
                    if len(lst)==2:
                        new_x=surface.get_width()/2 + x1 - scroll_rect.x 
                        new_y=surface.get_height()/2 + y1 - scroll_rect.y
                        pygame.draw.line(surface, (0,255,0), (new_x, new_y), (new_x+x2-x1, new_y+y2-y1), 5)
        


        
