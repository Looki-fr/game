import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# DOING 

# BUG => tp a travers un mur quand attaque dans autre direction

# TODO : news mouvement

# BUG : particles qui spawn à l'infini quand on saute puis shoot inastant

# TODO : ajouter sons pour les armes

# TODO : add platformes qui ne collide rien (ni quand == 4)

# BUG quand on edge climb into sauter dans un pilier on se tp

# BUG quand slide down un closed room wall on tombe dans le vide