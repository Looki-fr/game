import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# BUG haut dash ou dash attack ? stick to wall bc trop haut dans le vide

# TODO map : 
# habiller coins de map => plus accentué sur les 
#  _
# | |

# pas changer image chute qd air hurt
# hurt and death falling


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab