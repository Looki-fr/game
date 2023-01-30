import os
from game import Game
import pygame

dierectory = os.path.dirname(os.path.realpath(__file__))

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# idee : memo tel

# en cours : rajouter range trigger pour bot => utiliser distance vecteur
#            ajouter spawn de mob dans toute la map
#            add more mob to gameaa

# zoom dans bot and range attack

# BUG target forward bot

# timer attack crab