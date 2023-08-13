import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()


# TODO couper vision => parametre visible => si invisible alors image noire

# Puis generer truc dans salle vide ??
# rajouter des trucs en bois dans les maps


# BUG carre tt seul map carre bug

# TODO faire salle enfermé par plateforme à sauter

# TODO cacher salles que l'on voit pas à travers les musrs => polygone pour si on est sur une crete ?

# TODO add plateforme / arbre / rocher / bateau ....


# TODO spawn plateforme

# les pose direct en rajoutant image + co ou blit objet map ? comment ct avant
# conditions :
#   - aider joueur à sauter
#   - random dans une salle vide ? 
#   - qd peut despace horizontal entre 2 trucs

# idee : diviser la map en x troncons et voir si conditions alors mettre la plateforme, entre 2 troncons aussi 



# TODO : faire spawn crab à chaque milieu de map si ya pas bas

# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab