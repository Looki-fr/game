import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()
    


# BUG passage a travers mur qd dash au sol

# TODO => bug island haut droite, traverse mur qd saut edge

# BUG generation sol ou ile, un seul bloc vers haut avant fin de ile 
# => trouver generation et corriger

# generer ile, trouver longueur et largeur, coordonne en x du pic vers le bas, modif ou sinspirer du pic vers bas

# petite ile condition : [1,1,1,1]

# plus grande ile condition : [1,0,1,1] or [0,1,1,1]
#                         
#       and gauche ou droite [0,1,0/1,1] or [1,0,0/1,1]
# 
#   /!\ mini ile existe deja faut juste agrandir

# TODO add plateforme / arbre / rocher / bateau ....


# TODO spawn plateforme
# mat[i][y]=1 = normal
# mat[i][y]=2 = plateforme


# TODO map : 
#  _
#  _|__  faire comme grotte
# 


# TODO : faire spawn crab à chaque milieu de map si ya pas bas


# BUG d'affichage qd dash dans mur ?


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab