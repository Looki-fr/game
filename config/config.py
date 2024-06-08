import json
import os

class Config:
    def __init__(self, directory):
        self.directory=os.path.join(directory,"config")
        self.data = json.load(open(os.path.join(self.directory,"config.json")))

    def get(self, key):
        return self.data[key]
    
    def set(self, key, value): 
        self.data[key]=value
    
    def save(self):
        with open(os.path.join(self.directory,"config.json"), "w") as f:
            json.dump(self.data, f, indent=4)
