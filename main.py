import os
from game import Game
import pygame

dierectory = os.path.dirname(os.path.realpath(__file__))

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# if this or this then wider wall
#               __ __
#         or      |
# __|__    
#
# => node[2] and not node[1] and mat[i-1][y][1] and mat[i-1][y+1][3]
#    node[3] and not node[1] and not mat[i+1][y][1] and mat[i+1][y+1][3]
#
# --> then modify the ground generation to add grounds relief to it
#     --> create a function to call at whenever y we want and add a limit on the right


# if 
#
#
# __|  | => |__|/ | + hill on left
#
# => node[2] and not

# TODO hill mais au plafond

# pas changer image chute qd air hurt
# hurt and death falling

# BUG creation sol quand ground haut et mur a cote

# BUG collision dash dans mur quand jump edge

# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab