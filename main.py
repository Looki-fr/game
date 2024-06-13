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

# TODO : add platformes qui ne collide rien (ni quand == 4)

# BUG edge climb throw wall when attaking spam (cf map : island too close)

# BUG des fois le star ne meurt pas