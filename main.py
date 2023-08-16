import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()


# https://ncase.me/sight-and-light/
# https://stackoverflow.com/questions/38239309/optimize-field-of-vision-algorithm-in-a-grid-tiled-map

# faire une ligne qui pars des yeux du joueur et qui va en bas
# check les intersection avec tt les segments de tt les figures de la map
# faire partir des rayons vers chaque sommet de segment et check leurs intersections avec les segments
# si trop lent => diviser la map en pls parti ( en fonction tete joueur) et check les segments que avec 
# les figures de la partir où il va, si figure ds pls parti alors le mettre dans les pls parti
# => si un point ds parti alors mettre la figure dedans
# check si point qui est intercepter existe dans la map d'a cote => si oui alors c pas une intersection (ex sol)
# afficher tt les lignes de la tete du joueur jusqu'aux segments
# https://ncase.me/sight-and-light/


# TODO re organiser render map => too big and messy

# TODO opti les + mat dans collision en faisanrt avec des brackets

# TODO vision : savoir si un wall collide un ground ou un ceilling et si on est en bas
# on pernds en compte que ceux qui collide un ceilling

# TODO vision : faire avec ceillings et ground et murs

# clean code, trp de boolean dans collision, var rect par exemple dans collide wall

# BUG saut sur place bizarre qd saut edge into rester appuyer saut sur un trou de pilier

# TODO petite construction en bois aux extremités des piliers

# TODO couper vision => dessiner polygone où on voit pas : rajouter des autres points de vision dans les salles

# TODO faire salle enfermé par plateforme à sauter

# TODO cacher salles que l'on voit pas à travers les musrs + polygone pour les salles en cours

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