import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# clean code, trp de boolean dans collision, var rect par exemple dans collide wall

# BUG saut sur place bizarre qd saut edge into rester appuyer saut sur un trou de pilier

# TODO petite construction en bois aux extremités des piliers

# BUG better bottom marche pas qd hill == 5 (a gauche) et que ile : 1691949104.8551548

# EN BOIS
# faire plateforme en bois lorsqu'il y a des longs pics verticaux de tailles random (et de nbr)
#

# TODO couper vision => dessiner polygone où on voit pas : rajouter des autres points de vision dans les salles


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