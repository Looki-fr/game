import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# BUG en haut dash ground suivit de dash attack => passaga a travers sol

# BUG saut depuis la droite jusqu'a en haut + rester appuyer sur touche du haut : 
# l'animation du saut reste en boucle


# TODO map : 
# habiller coins de map => plus accentué sur les 
#  _
# | |

# pas changer image chute qd air hurt
# hurt and death falling


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab