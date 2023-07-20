

# hill bit ground
#seed=2343

# hill
# seed=123

# falaise droite
#seed=134

# falaise gauche
#seed = 1234

# weird solo tile
# seed = 1689526799.140814

import time
seed=time.time()

with open("seed.txt", "w") as file:
    file.write(str(seed))