""" jeu en cours de developpement
debut de la creation : 04/09/2021
des commentaires sont presents partout (ou presque) dans le code donc il ne devrait pas être trop dur à comprendre 
les commentaires en bas de ce fichier sont des mémos de choses a faire

bibliotheque à installer :
    - pygame
    - pytmx
    - sqlite3
    - pyscroll
"""
import os
from game import Game
import pygame

directory = os.path.dirname(os.path.realpath(__file__))
os.chdir = directory

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()
    
