
# interesting generation with isle
#seed=1690213340.3968208

# 2 bugs de generation : une barre tt seul et une tile tt seul à un  bord
#seed=1691662771.3016784

# bug 2 hills en mm temps + ile ? = passage bouche
# seed=1691663098.4508078

# faire hill qui fait 2 de haut 
# seed=1691663197.5484853

# baton tt seul trop chelou qui vbole
# 1691674131.9426541

# weird
# seed=1691671385.29449


import time
seed=time.time()

with open("seed.txt", "w") as file:
    file.write(str(seed))
