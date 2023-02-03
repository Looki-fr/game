import os
from game import Game
import pygame

dierectory = os.path.dirname(os.path.realpath(__file__))

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

#https://youtu.be/NGFk44fY0O4

# if head collide sol and not collide plafond then edge climb

# fleche du bas qd edge grab => edge slide

# BUG se faire attaquer en etant en edge grab

# add effet dash attack

# en cours : rajouter nv perso
#            reparer mvm
#            reparer roulade + grab edge + remonter edge

# BUG on peut sortir de la map à cause du saut edge => timer qd on se cogne

# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab