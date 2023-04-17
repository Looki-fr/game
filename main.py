import os
from game import Game
import pygame

dierectory = os.path.dirname(os.path.realpath(__file__))

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# if 
#
#
# __|  | => |__|/ | + hill on left
#
# => node[2] and not

# TODO hill mais au plafond

# pas changer image chute qd air hurt
# hurt and death falling


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab