import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# EN COURS : 
# menu : cf discord pour orga
# BUG problématique du temps : faire une foncdaqtion qui donne le temps et garder en mémoire tt les temps perdus dans le menu
# ATTENTION : bug cooldown qd yaura des botzs











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


# TODO semi island 1 ou 2 mais pas les 2 qd bas à cote

# TODO : faire spawn crab à chaque milieu de map si ya pas bas

# TODO rebuild AI mob + faire en sorte qu'il focus que qd ils sont dans notre salle ou les salles lies à cotes

# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab