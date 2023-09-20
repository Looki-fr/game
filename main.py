import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# TODO : duplicated code in spawn island

# BUG saut sur place bizarre qd saut edge into rester appuyer saut sur un trou de pilier

# TODO add constructions en bois

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