import random
room_to_remove=3
width=5
height=5
from seed import seed
random.seed(seed)
def printTab(mat):
    for line in mat:
        for val in line:
            if val : 
                print("O", end="")
                if val[1]:print("-",end="")
                else :print(" ",end="")
            else : print("X ", end="")
            
        print()
     
        for val in line:
            if val and val[3]:print("| ",end="")
            else :print("  ",end="")
        print()

def get_shortest_path(start, end, mat):
        """simple graphe shortest path function"""
        pile=[[start]]
        vu=[start]
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
                        vu.append(node)
                        pile.append(current_path+[node])
        return None

def get_all_neighboors(i, y, mat, vu):
    tab=[]
    if i>0 and mat[i-1][y] and mat[i][y][2] and (i-1, y) not in vu:tab.append((i-1, y))
    if i<len(mat)-1 and mat[i+1][y] and mat[i][y][3]  and (i+1, y) not in vu:tab.append((i+1, y))
    if y>0 and mat[i][y-1] and mat[i][y][0]  and (i, y-1) not in vu:tab.append((i, y-1))
    if y<len(mat[0])-1 and mat[i][y+1] and mat[i][y][1]  and (i, y+1) not in vu:tab.append((i, y+1))
    return tab

def remove_path(co, c, mat, add=False):
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

def get_matrix():
    mat=[[[True, True, True, True] for _ in range(width)] for _ in range(height)]
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
    while c<room_to_remove:
        i, y = random.randint(0,len(mat)-1), random.randint(0,len(mat[0])-1)
        
        if mat[i][y]:
            bool=True

            tmp=get_all_neighboors(i, y, mat, [])

            for node in tmp:
                remove_path((i,y), node, mat)
                for other_node in tmp:
                    if node != other_node:
                        if get_shortest_path(other_node, node, mat) == None : bool=False

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
                    remove_path((i,y), node, mat, True)

    # [g, d, h, b]



    for i in range(11):
        if mat[i//(len(mat)-1)][i%(len(mat)-1)]:
            path=[(i//(len(mat)-1), i%(len(mat)-1))]
            break


    # 1 get a random node not in path
    # 2 remove all other path
    # 3 print pour voir

    vu=[path[0]]
    while (len(path))>0:
        node = path.pop()
        bool=True
        tab=get_all_neighboors(node[0], node[1], mat, vu)
        if len(tab) > 0 :
            n = random.choice(tab)
            vu.append(n)
            for other_node in tab:
                if other_node != n:
                    remove_path(node, other_node, mat)
                    if get_shortest_path(other_node, node, mat) == None : bool=False

            if not bool:
                for other_node in tab:
                    if other_node != n:
                        remove_path(node, other_node, mat, True)
                    
            path.append(node)
            path.append(n)
    return mat





