import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# BUG ce serait mieux si dash attack continue qd on collide un little ground au lieu de sarreter
# , uniquement si pas chest collide

# TODO ile plus petite qd hill à cote 

# TODO add plateforme / arbre / rocher / bateau ....


# TODO spawn plateforme
# mat[i][y]=1 = normal
# mat[i][y]=2 = plateforme


# TODO : faire spawn crab à chaque milieu de map si ya pas bas


# BUG d'affichage qd dash dans mur ?


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab