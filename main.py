import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# BUG : piece spawn dans le vide et passe a travers mur
# BUG : particles qui spawn à l'infini quand on saute puis shoot instant