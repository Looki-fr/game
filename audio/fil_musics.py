import os
directory = os.getcwd()
os.chdir(directory+"\\audio\\temp")
files = [f for f in os.listdir() if os.path.isfile(f)]
lst=[]
for f in files:
    lst.append({
        "name": f.replace("-", " ").replace(".mp3", ""),
        "file": f
    })
import json
json.dump(lst, open(directory+"\\audio\\fil_musics.json", "w"), indent=4)