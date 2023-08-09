import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()
    

# BUG faire full tile autour de empty map et grosse image au milieu

# TODO faire bottom island mais pour tt plafond avec plus grandes valeurs, valeurs du sol ???


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