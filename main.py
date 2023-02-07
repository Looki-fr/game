import os
from game import Game
import pygame

dierectory = os.path.dirname(os.path.realpath(__file__))

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()


# add effet dash attack

# en cours : rajouter nv perso
#            reparer mvm
#            reparer roulade







# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab