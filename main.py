import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# TODO pour carre : 
# 2 choix : 

#           - 4 petites iles en N S W E ; W  qui sont soient tt en bas de la map du haut, 
# soit tt en haut de la map du bas, E inversement
#
#           - 3

# TODO possibilite de mixer ile et hill (falaise) pour faire un balcon simpa
# => interdire ile qd ya une hill mais la mettre en calculant les coordonnées comme on veut

# TODO si barre alors mettre ile collé ou gros champignon ou arbre dessus ? ?? ou grosse hill si compatible

# TODO faire salle enfermé par plateforme à sauter

# TODO cacher salles que l'on voit pas à travers les murs => polygone pour si on est sur une crete ?

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