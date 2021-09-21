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
    
# TODO

# commentaire (pas trop en mettre)
#  + re organise code

# rajouter une variable action pour les images seulements : self.action = 'jump' quand dash
# opti new_partile() : for i in X : machin.append(i) etc

# optimiser update particle, parametre que quand changement








# changer image transparente dash par silhouette ? => changer assets

# rebond quand le joueur se cogne ? ou au moins ralentissement

# focus sur mouvement avant de rajouter quoi que ce soit
# => quand finis mouvements mettre sur github sur discord graven etc et demander des retours sur plein de discord differents

# rebond quand accrocher au mur
# apres un petit delai le perso glisse contre le mur(vers le bas)

# implementer new mouvements à partir du fichier d'image

# implementer mannette

# inspiration mouvement de celeste : https://www.youtube.com/watch?v=tbRCCfo9Wgg

# idee bloc note tel

# se renseigner sur .json pour les niveaux
# => charger automatiquements tout, même nom pour tout les niveaux, try except si besoin. => json pour obstacles ?

