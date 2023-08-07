import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()
    
# BUG les particules sont pas continues qd on slide sur un mur

# BUG transi animation qd slide ground dans un little ground => crouch ?

# variation de plafond sur tt les plafonds, faire un truc general inter map comme le sol avec un reset et tt, qui marche avec les iles

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