import json
from typing import Any

class Config:
    def __init__(self, directory):
        self.directory=directory+"\\config"
        self.data = json.load(open(self.directory+"\\config.json"))

    def get(self, key):
        return self.data[key]
    
    def set(self, key, value): 
        self.data[key]=value
    
    def save(self):
        with open(self.directory+"\\config.json", "w") as f:
            json.dump(self.data, f, indent=4)
