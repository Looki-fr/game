import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()


# TODO possibilite de mixer ile et hill (falaise) pour faire un balcon simpa
# => interdire ile qd ya une hill mais la mettre en calculant les coordonnées comme on veut

# TODO si barre alors mettre ile collé ou gros champignon ou arbre dessus ? ?? ou grosse hill si compatible

# TODO si carre alors faire grande ile au milieu

# BUG generation weird : ile trop bas comme ya hill

# TODO faire salle enfermé par plateforme à sauter

# TODO cacher salles que l'on voit pas à travers les murs => polygone pour si on est sur une crete ?

# TODO ile plus petite qd hill à cote 
# => changer tableau hills pour pas confondre les top des falaises

# TODO add plateforme / arbre / rocher / bateau ....


# TODO spawn plateforme
# mat[i][y]=1 = normal
# mat[i][y]=2 = plateforme


# TODO : faire spawn crab à chaque milieu de map si ya pas bas

# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab