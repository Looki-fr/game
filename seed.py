# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# -                                                                                                             -
# -                                              Cool maps                                                      -
# -                                                                                                             -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# map stylé
#seed=1691948484.45544

# map avec gros pilier qui vole
#seed=1691955286.989919

# 2 carre collés
#seed=1692015864.3185315

# map used for shadow
# seed=1692181610.1185951

# map complete
# seed =1699827347.2238336



import time

class Seed:
    def __init__(self):
        self.seed=0

    def new_seed(self):
        self.seed=time.time()

        with open("seed.txt", "w") as file:
            file.write(str(self.seed))

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # -                                                                                                             -
        # -                                              Bugs                                                      -
        # -                                                                                                             -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        # BUG crash
        # seed = 1712149021.3348393

        # BUG en bas à droite saut diagonal dans l'ile on passe a travers qd don re saute => car tete est trop enfonce elle collide pas plafond ???
        # seed=1692090527.498834

        # BUG tile qui a depop à cause d'une ile
        # seed = 1700336112.335133

        # BUG trou
        # self.seed = 1700345499.171078

        # BUG climb edge traverse plafond
        # seed = 1700346541.011556

            
        # BUG map on est stuck
        # self.seed=1700094674.006223