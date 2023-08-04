import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()
    


# generer ile, trouver longueur et largeur, coordonne en x du pic vers le bas, modif ou sinspirer du pic vers bas

# TODO spawn plateforme
# mat[i][y]=1 = normal
# mat[i][y]=2 = plateforme


# TODO map : 
#  _
#  _|__  faire comme grotte
# 

# TODO île qd g d h b

# TODO add plateforme / arbre / rocher / bateau ....

# TODO : faire spawn crab à chaque milieu de map si ya pas bas


# BUG d'affichage qd dash dans mur ?


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab