import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# BUG check si cogne avant de sauter pour deny

# BUG passaga a travers mur et stick wall dans le vide quand jump edge sur falaise

# BUG passage a travers mur en haut qd dash attack vers le bas    

# TODO affichier mur / sol etc en couleur pour check si c bon

# BUG continuer relief alors que gen current == 0 qd coins gauche

# BUG sur un little ground vers la droite => on est bloqué à cause du mur q don va à gauche

# TODO clean collision, pk wall[0] ??

# TODO reunir move right du player dans mother

# BUG saut depuis la droite jusqu'a en haut + rester appuyer sur touche du haut : 
# l'animation du saut reste en boucle


# TODO map : 
# habiller coins de map => plus accentué sur les 
#  _
# | |

# pas changer image chute qd air hurt
# hurt and death falling


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab