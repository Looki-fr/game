import random

class Graph:
    def __init__(self, height, width,room_to_remove, remove_wall, seed):
        random.seed(seed)
        self.height=height
        self.width=width
        self.room_to_remove=room_to_remove
        self.remove_wall=remove_wall

    def printTab(self,mat, valMat=None):
        for i, line in enumerate(mat):
            for y, val in enumerate(line):
                if val : 
                    if valMat:
                        print(valMat[i][y], end="")
                    else:
                        print("O", end="")
                    if val[1]:print("-",end="")
                    else :print(" ",end="")
                else : print("X ", end="")
                
            print()
        
            for val in line:
                if val and val[3]:print("| ",end="")
                else :print("  ",end="")
            print()

    def get_shortest_path(self,start, end, mat):
            """simple graphe shortest path function"""
            pile=[[start]]
            vu=set(start)
            while len(pile)>0:

                current_path=pile.pop(0)
                tab=[]
                n=current_path[-1]
                
                if mat[n[0]][n[1]]:
                    if mat[n[0]][n[1]][0]: tab.append((n[0], n[1]-1))
                    if mat[n[0]][n[1]][1]: tab.append((n[0], n[1]+1))
                    if mat[n[0]][n[1]][2]: tab.append((n[0]-1, n[1]))
                    if mat[n[0]][n[1]][3]: tab.append((n[0]+1, n[1]))
                    for node in tab:
                        if node == end:
                            return current_path+[node]
                        if node not in vu:
                            vu.add(node)
                            pile.append(current_path+[node])
            return []

    def get_all_neighboors(self,i, y, mat, vu):
        tab=[]
        if i>0 and mat[i-1][y] and mat[i][y][2] and (i-1, y) not in vu:tab.append((i-1, y))
        if i<len(mat)-1 and mat[i+1][y] and mat[i][y][3]  and (i+1, y) not in vu:tab.append((i+1, y))
        if y>0 and mat[i][y-1] and mat[i][y][0]  and (i, y-1) not in vu:tab.append((i, y-1))
        if y<len(mat[0])-1 and mat[i][y+1] and mat[i][y][1]  and (i, y+1) not in vu:tab.append((i, y+1))
        return tab

    def remove_path(self,co, c, mat, add=False):
        if co[1]-c[1]==-1: 
            mat[co[0]][co[1]][1]=add
            mat[c[0]][c[1]][0]=add
        elif co[1]-c[1]==1: 
            mat[co[0]][co[1]][0]=add
            mat[c[0]][c[1]][1]=add
        elif co[0]-c[0]==-1: 
            mat[co[0]][co[1]][3]=add
            mat[c[0]][c[1]][2]=add
        elif co[0]-c[0]==1: 
            mat[co[0]][co[1]][2]=add
            mat[c[0]][c[1]][3]=add

    def get_matrix(self):
        mat=[[[True, True, True, True] for _ in range(self.width)] for _ in range(self.height)]
        # BUG faire en sorte que X pas tt une ligne / colonne

        for i in range(len(mat)):
            for y in range(len(mat[0])):
                if mat[i][y]:
                    if i==0:mat[i][y][2]=False
                    if i==len(mat)-1:mat[i][y][3]=False
                    if y==0:mat[i][y][0]=False
                    if y==len(mat[0])-1:mat[i][y][1]=False



        c=0
        # remove x nodes randomly
        while c<self.room_to_remove:
            i, y = random.randint(0,len(mat)-1), random.randint(0,len(mat[0])-1)
            
            if mat[i][y]:
                bool=True

                tmp=self.get_all_neighboors(i, y, mat, [])

                for node in tmp:
                    self.remove_path((i,y), node, mat)
                    for other_node in tmp:
                        if node != other_node:
                            if self.get_shortest_path(other_node, node, mat) == [] : bool=False

                if bool or len(tmp)==0:
                    c+=1
                    mat[i][y]=[]
                    for co in tmp:
                        if co[1]-y==-1: mat[co[0]][co[1]][1]=False
                        elif co[1]-y==1: mat[co[0]][co[1]][0]=False
                        elif co[0]-i==-1: mat[co[0]][co[1]][3]=False
                        elif co[0]-i==1: mat[co[0]][co[1]][2]=False
                else:
                    for node in tmp:
                        self.remove_path((i,y), node, mat, True)

        # [g, d, h, b]

        corner=random.randint(1,4)
        if corner == 1:
            for i in range(self.width):
                for y in range(self.height):
                    if len(mat[i][y])>0:
                        path=[(i,y)]
                        break
        elif corner==2:
            for i in range(self.width-1, -1, -1):
                for y in range(self.height):
                    if len(mat[i][y])>0:
                        path=[(i,y)]
                        break
        elif corner==3:
            for i in range(self.width-1, -1, -1):
                for y in range(self.height-1, -1, -1):
                    if len(mat[i][y])>0:
                        path=[(i,y)]
                        break
        elif corner==4:
            for i in range(self.width):
                for y in range(self.height-1, -1, -1):
                    if len(mat[i][y])>0:
                        path=[(i,y)]
                        break

        # 1 get a random node not in path
        # 2 remove all other path
        # 3 print pour voir

        vu=set(path[0])
        while (len(path))>0:
            node = path.pop()
            bool=True
            tab=self.get_all_neighboors(node[0], node[1], mat, vu)
            if len(tab) > 0 :
                n = random.choice(tab)
                vu.add(n)
                for other_node in tab:
                    if other_node != n:
                        self.remove_path(node, other_node, mat)
                        if self.get_shortest_path(other_node, node, mat) == [] : bool=False

                if not bool:
                    for other_node in tab:
                        if other_node != n:
                            self.remove_path(node, other_node, mat, True)
                        
                path.append(node)
                path.append(n)

        tmp=0
        while tmp<self.remove_wall:
            i=random.randint(0,self.height-1)
            z=random.randint(0,self.width-1)
            if not mat[i][z]: continue
            lst=[]
            for i_ in range(4):
                bool_=False
                if i_==0 and z>0 and mat[i][z-1]:bool_=True
                elif i_==1 and z< len(mat[i])-1 and mat[i][z+1]:bool_=True
                elif i_==2 and i>0 and mat[i-1][z]:bool_=True
                elif i_==3 and i<len(mat)-1 and mat[i+1][z]:bool_=True
                if bool_ and not mat[i][z][i_]: lst.append(i_)
            if len(lst)==0: continue
            choice=random.choice(lst)
            mat[i][z][choice]=True
            if choice==0:mat[i][z-1][1]=True
            if choice==1:mat[i][z+1][0]=True
            if choice==2:mat[i-1][z][3]=True
            if choice==3:mat[i+1][z][2]=True
            tmp+=1
    
        return mat

    def get_matrix_room_recur(self, mat, mat_room_bal, i, y, vu, cur, cur_length):
        if mat[i][y]:
            if cur_length[0] > 2 or (cur_length[0]==2 and random.randint(0,1)==0):
                cur_length[0]=0
                cur[0]+=1
            vu.add((i,y))
            mat_room_bal[i][y]=self.get_letter(cur)
            cur_length[0]+=1
            tab=self.get_all_neighboors(i, y, mat, vu)
            for node in tab:
                if node not in vu:
                    self.get_matrix_room_recur(mat, mat_room_bal, node[0], node[1], vu, cur, cur_length)
            if len(tab)==0:
                cur_length[0]=0
                cur[0]+=1
        else:
            vu.add((i,y))

    def get_all_neighboors_rooms_rec(self,i, y, mat, mat_room, tab):
        if mat[i][y]:
            if mat[i][y][2] and (i-1, y) not in tab and mat_room[i][y]==mat_room[i-1][y]:
                tab.append((i-1, y))
                self.get_all_neighboors_rooms_rec(i-1, y, mat, mat_room, tab)
            if mat[i][y][3]  and (i+1, y) not in tab and mat_room[i][y]==mat_room[i+1][y]:
                tab.append((i+1, y))
                self.get_all_neighboors_rooms_rec(i+1, y, mat, mat_room, tab)
            if mat[i][y][0]  and (i, y-1) not in tab and mat_room[i][y]==mat_room[i][y-1]:
                tab.append((i, y-1))
                self.get_all_neighboors_rooms_rec(i, y-1, mat, mat_room, tab)
            if mat[i][y][1]  and (i, y+1) not in tab and mat_room[i][y]==mat_room[i][y+1]:
                tab.append((i, y+1))
                self.get_all_neighboors_rooms_rec(i, y+1, mat, mat_room, tab)

    def get_all_neighboors_rooms(self,i, y, mat, mat_room):
        tab=[(i, y)]
        self.get_all_neighboors_rooms_rec(i, y, mat, mat_room, tab)
        return tab

    def get_letter(self, cur):
        return chr(ord('a')+cur[0]-1)

    def get_matrix_room(self, mat):
        mat_room_bal=[[0 for _ in range(len(mat[0]))] for _ in range(len(mat))]
        cur=[1]
        vu=set()
        cur_length=[0]
        for i in range(len(mat)):
            for y in range(len(mat[0])):
                if len(mat[i][y])>0 and mat[i][y][1] and mat[i][y][3] and mat[i][y+1][3] and mat[i+1][y][1]:
                    mat_room_bal[i][y]=self.get_letter(cur)
                    vu.add((i,y))
                    mat_room_bal[i][y+1]=self.get_letter(cur)
                    vu.add((i,y+1))
                    mat_room_bal[i+1][y]=self.get_letter(cur)
                    vu.add((i+1,y))
                    mat_room_bal[i+1][y+1]=self.get_letter(cur)
                    vu.add((i+1,y+1))
                    cur[0]+=1
        for i in range(len(mat)):
            for y in range(len(mat[0])):
                if len(mat[i][y])>0 and (i,y) not in vu:
                    self.get_matrix_room_recur(mat, mat_room_bal, i, y, vu,cur, cur_length)
        print(self.get_all_neighboors_rooms(0,0,mat,mat_room_bal))
        return mat_room_bal

                    



