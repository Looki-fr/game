""" jeu en cours de developpement
debut de la creation : 04/09/2021
des commentaires sont presents partout (ou presque) dans le code donc il ne devrait pas être trop dur à comprendre 
les commentaires en bas de ce fichier sont des mémos de choses a faire

bibliotheque à installer :
    - pygame
    - pytmx
    - sqlite3
    
les noms de variables / fonctions peuvent paraître inutilement long, mais ça à un GROS avantage:
si vous rajouter un mouvement par exemple et donc qu'il faut faire en sorte que les autres mouvements ne declenche pas pendant qu'il est actif
faites juste ctrl + f 'debut' et en 2s c'est plié
"""
import os
from game import Game
import pygame

directory = os.path.dirname(os.path.realpath(__file__))

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()
    
# TODO

# COMMENTAIRE

# reduire update => more method

# dictionnaire de methode avec self.player.action en key:
# { "chute":self.player.chute}

# REFAIRE MOUVEMENT => good sound effects

# modif taille textes en fonction zoom

# blit textes avant Goupe

# en cours : map tutoriel
# => 'fantome' + REFAIRE MAP







# commentaire en anglais

# implementer mannette

# idee bloc note tel
