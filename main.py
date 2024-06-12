import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# TODO : news mouvement

# BUG : particles qui spawn à l'infini quand on saute puis shoot inastant

# TODO : ajouter sons pour les armes
