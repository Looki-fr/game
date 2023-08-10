import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()
# BUG qd dash en diagonal to a ground

# TODO possibilite de mixer ile et hill (falaise) pour faire un balcon simpa
# => interdire ile qd ya une hill mais la mettre en calculant les coordonnées comme on veut

# TODO si barre alors mettre ile collé ou gros champignon ou arbre dessus ? ?? ou grosse hill si compatible

# TODO si carre alors faire grande ile au milieu

# BUG generation weird : ile trop bas comme ya hill

# TODO faire salle enfermé par plateforme à sauter

# TODO cacher salles que l'on voit pas à travers les murs => polygone pour si on est sur une crete ?

# TODO qd 3 bas daffile sans gauche ou droite il faut au moins une ile

# TODO utiliser gen normal pour grand ile

# BUG ce serait mieux si dash attack continue qd on collide un little ground au lieu de sarreter
# , uniquement si pas chest collide

# TODO ile plus petite qd hill à cote 

# TODO add plateforme / arbre / rocher / bateau ....


# TODO spawn plateforme
# mat[i][y]=1 = normal
# mat[i][y]=2 = plateforme


# TODO : faire spawn crab à chaque milieu de map si ya pas bas


# BUG d'affichage qd dash dans mur ?


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab