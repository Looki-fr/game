import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# TODO : faire spawn crab à chaque milieu de map si ya pas bas
# TODO : optimisztion


# BUG d'affichage qd dash dans mur ?

# TODO map : 
# habiller coins de map => plus accentué sur les 
#  _
# | |


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab