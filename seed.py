
#-----------------------------------------------------------------
#                                                                |
#          Before l'addition du mur suppr au pif                 |
#                                                                |
#-----------------------------------------------------------------


# interesting generation with isle
# seed=1690213340.3968208

# faire hill qui fait 2 de haut 
# seed=1691663197.5484853

# weird
# seed=1691671385.29449

# map très aerienne
# seed=1691937020.8591151


#-----------------------------------------------------------------
#                                                                |
#          After                                                 |
#                                                                |
#-----------------------------------------------------------------

# BUG generation carre, pilier inconnu
#1691948406.90053

#map stylé
#seed=1691948484.45544

# map avec gros pilier qui vole
#seed=1691955286.989919

# BUG generation salle pilier
#seed=1692010423.8739157

# salle piler + carre + ile
#seed=1692015864.3185315

# BUG BUG gen salle pilier peut pas passer ++ ile qui est trop basse
# seed=1692090527.498834

# BUG gen island dans map 7 
#seed=1692094695.4801812

# bug island too close on the right
#seed=1692100607.7870162

# map used for shadow
# seed=1692181610.1185951

# BUG generation ile trop proche + une tile tt seul à son plafond
#seed=1694958033.799719

# BUG carre tt seul
seed=1694958765.0083292

import time
seed=time.time()

with open("seed.txt", "w") as file:
    file.write(str(seed))
    