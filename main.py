import os   
from game import Game
import pygame

pygame.init()

if __name__ == "__main__":

    game = Game()
    game.run()

# BUG passage a travers sol qd change dir sur un sol reduit pour pas climb edge le wall

# TODO clean collision, pk wall[0] ??

# TODO reunir move right du player dans mother

# BUG saut depuis la droite jusqu'a en haut + rester appuyer sur touche du haut : 
# l'animation du saut reste en boucle




# pas changer image chute qd air hurt
# hurt and death falling


# BUG  crab coin qd on est en bas il arete davancer

# BUG target forward bot

# timer attack crab