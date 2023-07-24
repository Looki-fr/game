

# hill bit ground
#seed=2343

# hill
# seed=123

# falaise droite
#seed=134

# falaise gauche
#seed = 1234

# solo tile en haut
#seed=1690106899.0068386

import time
seed=time.time()

with open("seed.txt", "w") as file:
    file.write(str(seed))