import pytmx
import pygame
from math import ceil

class TileMap:
    def __init__(self, filename, screen_width, screen_height, zoom):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.zoom = zoom
        self.tm = pytmx.util_pygame.load_pygame(filename, pixelalpha=True)
        self.width = self.tm.width * self.tm.tilewidth * self.zoom
        self.height = self.tm.height * self.tm.tileheight * self.zoom
        self.tmxdata = self.tm
        self.liste_tile=[]
        self.liste_tile.append([[] for _ in range(self.tm.height)])
        c=0
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    if ti(gid):
                        tile = pygame.transform.scale(ti(gid), (ti(gid).get_width()*self.zoom, ti(gid).get_height()*self.zoom))
                    else:
                        tile = None
                    self.liste_tile[c][y].insert(x, tile)
                self.liste_tile.append([[] for _ in range(self.tm.height)])
                c+=1
        self.liste_tile = self.liste_tile[:-1]

    def render(self, surface, cam_x, cam_y):
        y_min = ceil((cam_y-self.screen_height/2)/(self.tm.tileheight* self.zoom))-2
        y_max = ceil((cam_y+self.screen_height/2)/(self.tm.tileheight* self.zoom))+1
        x_min = ceil((cam_x-self.screen_width/2)/(self.tm.tilewidth* self.zoom))-2
        x_max = ceil((cam_x+self.screen_width/2)/(self.tm.tilewidth* self.zoom))+1
        if y_min < 0:
            y_min = 0
        if x_min < 0:
            x_min = 0
        if y_max > len(self.liste_tile[0])-1:
            y_max = len(self.liste_tile[0])-1
        if x_max > len(self.liste_tile[0][0])-1:
            x_max = len(self.liste_tile[0][0])-1
        y = y_min
        x = x_min
        for layer in self.liste_tile:
            for ligne in layer[y_min:y_max]:
                for tile in ligne[x_min:x_max]:
                    if tile != None:
                        surface.blit(tile.convert(), (self.screen_width/2 + x*self.zoom*self.tm.tilewidth - cam_x, self.screen_height/2 + y*self.zoom*self.tm.tileheight - cam_y))
                    x+=1
                x=x_min
                y += 1