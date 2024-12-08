import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# DOING 


# TODO : news mouvement

# BUG : particles qui spawn à l'infini quand on saute puis shoot inastant

# TODO : ajouter sons pour les armes

# TODO : add platformes qui ne collide rien (ni quand == 4)

# BUG quand on edge climb into sauter dans un pilier on se tp

# BUG quand on reste appuyé sur bas l'animation bloque sur la 1ere frame

# BUG quand slide down un closed room wall on tombe dans le vide