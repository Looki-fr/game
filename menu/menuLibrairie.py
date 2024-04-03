import pygame
from pygame.locals import *
from math import ceil
import time

def center_width(image, screen):
    """return l'abscisse necessaire pour centrer une image"""
    x = ceil(screen.get_width() / 2) - ceil(image.get_width() / 2)
    return x

def center_height(image, screen):
    """return l'abscisse necessaire pour centrer une image"""
    y = ceil(screen.get_height() / 2) - ceil(image.get_height() / 2)
    return y

def get_picture_scale(path, coefx,coefy):
    img = pygame.image.load(path)
    width=ceil(img.get_width() * coefx)
    height=ceil(img.get_height() * coefy)
    img = pygame.transform.scale(img, (width, height)).convert_alpha() 
    return img

class MenuLibrairie:
    def __init__(self):
        self.all_menu={}
        self.add_menu("base")
        self.current_menu='base'
        self.all_bind_keys={}
        
        self.background=None
        self.color_background=None
        self.running = False
        
        self.temps = time.time()
        
    def add_menu(self, name):
        self.all_menu[name]={}
        self.all_menu[name]["button"]={}
        self.all_menu[name]["text"]={}
        self.all_menu[name]["text_selectionne"]=""
        self.all_menu[name]["lines"]=0
    
    def add_button_menu(self,name_menu, name_button,image,function, arguments,y, x=None):
        """- name_menu :          (str)  name of the menu where you want to add a button
           - name_button :        (str)  name of the button you want to add
           - image :              (pygame.image)  picture off the button
           - function :           (function) function that will be executed when the user click on the button
           - arguments :          (list)  arguments of the function
           - y :                  (int)  position on x of the button
           - x : OPTIONNAL        (int)  position on x of the button => if x is not entered the button will be centered on the screen
            
            the function will be executed like that : 
                    function(*arguments)
           """
        if x == None:
            x=center_width(image, self.screen)
        if type(y)==str:
            if y in self.all_menu[name_menu]["button"].keys(): 
                y = self.all_menu[name_menu]["button"][y]["y"]
            else:
                y = self.all_menu[name_menu]["text"][y]["y"]
        elif type(y)==float:
            y=y
        else:
            y=self.all_menu[name_menu]["lines"]*(image.get_height()+y) + y
            self.all_menu[name_menu]["lines"]+=1
        self.all_menu[name_menu]["button"][name_button]={"image": image,"x":x,"y":y,"function":function, "arguments":arguments}
    
    def add_text_menu(self,menu,name, texte, x, y, taille_carac, height, entry=False):
        BaseText = texte
        font = pygame.font.SysFont('courier', taille_carac, bold=True)
        img = font.render(BaseText, True, (0, 0, 0))
        rect = img.get_rect()
        if x == None:
            x=center_width(img, self.screen)
        if type(y)==str:
            if y in self.all_menu[menu]["button"].keys(): 
                y = self.all_menu[menu]["button"][y]["y"]
            else:
                y = self.all_menu[menu]["text"][y]["y"]
        elif type(y)==float:
            y=y
        else:
            y=self.all_menu[menu]["lines"]*(height+y) + y
            self.all_menu[menu]["lines"]+=1
        y+=(height-img.get_height())/2
        rect.topleft = (x, y)
        if entry:
            cursor = Rect(rect.topright, (3, rect.height))
        else:
            cursor = None
        

        self.all_menu[menu]["text"][name] =  {"name":name,"text":BaseText,"font":font,"img":img,"rect":rect,"x":x,"y":y,"cursor":cursor}
        
    def update_text_menu(self, menu, name, texte, taille_carac, x=None):
        BaseText = texte
        font = pygame.font.SysFont('courier', taille_carac, bold=True)
        img = font.render(BaseText, True, (0, 0, 0))
        rect = img.get_rect()
        if x == None:
            x=self.all_menu[menu]["text"][name]["x"]
        rect.topleft = (x, self.all_menu[menu]["text"][name]["y"])
        self.all_menu[menu]["text"][name]["text"]=BaseText
        self.all_menu[menu]["text"][name]["rect"]=rect
        self.all_menu[menu]["x"]=x

    def change_menu(self, name):
        self.current_menu=name
        self.update_ecran_menu()
    
    def update_ecran_menu(self):
        if self.background != None:
            self.screen.blit(self.background, (0,0))
        elif self.color_background:
            self.screen.fill(self.color_background)
        else:
            self.update_ecran(True)
        
        for value in self.all_menu[self.current_menu]["text"].values():
            value["img"] = value["font"].render(value["text"], True, (0, 0, 0))
            value["rect"].size = value["img"].get_size()
            if value["cursor"] : value["cursor"].topleft = value["rect"].topright

        for value in self.all_menu[self.current_menu]["button"].values():
            self.screen.blit(value["image"], (value["x"], value["y"]))
        
        for value in self.all_menu[self.current_menu]["text"].values():
            self.screen.blit(value["img"], value["rect"])

        if time.time() % 1 > 0.5:
            if self.all_menu[self.current_menu]["text_selectionne"]!="":
                pygame.draw.rect(self.screen, (0, 0, 0), self.all_menu[self.current_menu]["text"][self.all_menu[self.current_menu]["text_selectionne"]]["cursor"])

    def bind_key(self, key, function, args):
        if self.all_bind_keys.get(str(key))==None:
            self.all_bind_keys[str(key)]=[]
        self.all_bind_keys[str(key)].append([function, args])
    
    def handle_input(self, pressed):
        """gere les differents cliques de la souris et appelle mouse_button si on fait un clique gauche"""
        mouse = pygame.mouse.get_pressed()
        if mouse[0] == True:
            if time.time() - self.temps > 0.2:
                self.temps = time.time()
                self.mouse_button(pygame.mouse.get_pos())
        for key, value in self.all_bind_keys.items():
            if pressed[int(key)]:
                for liste in value:
                    liste[0](*liste[1])
        
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key not in [pygame.K_RETURN, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_TAB]:
                if self.all_menu[self.current_menu]["text_selectionne"]!="":
                    if event.key == pygame.K_BACKSPACE:
                        self.all_menu[self.current_menu]["text"][self.all_menu[self.current_menu]["text_selectionne"]]["text"]=self.all_menu[self.current_menu]["text"][self.all_menu[self.current_menu]["text_selectionne"]]["text"][:-1]
                    else:
                        if self.all_menu[self.current_menu]["text"][self.all_menu[self.current_menu]["text_selectionne"]]["text"]=="file name":
                            self.all_menu[self.current_menu]["text"][self.all_menu[self.current_menu]["text_selectionne"]]["text"]=""
                        self.all_menu[self.current_menu]["text"][self.all_menu[self.current_menu]["text_selectionne"]]["text"]+=event.unicode
                    self.update_text_menu(self.current_menu, self.all_menu[self.current_menu]["text_selectionne"], self.all_menu[self.current_menu]["text"][self.all_menu[self.current_menu]["text_selectionne"]]["text"], 30)
            elif event.key == pygame.K_RETURN:
                if self.current_menu=="load":
                    self.validate_load()
        if self.all_menu[self.current_menu]["text_selectionne"]!="" and self.all_menu[self.current_menu]["text"][self.all_menu[self.current_menu]["text_selectionne"]]["text"]=="":
            self.all_menu[self.current_menu]["text"][self.all_menu[self.current_menu]["text_selectionne"]]["text"]="file name"


    def mouse_button(self, mouse_pos):
        """ regarde sur quel bouton on a cliquer et agit en consequance"""
        for key, value in self.all_menu[self.current_menu]["button"].items():
            if (value["x"] < mouse_pos[0] < value["x"] + value["image"].get_width()) and (value["y"] < mouse_pos[1] < value["y"] + value["image"].get_height()):
                self.audio.play_random_sound("menu", 3)
                value["function"](*value["arguments"])
        
        for key, value in self.all_menu[self.current_menu]["text"].items():
            if value["cursor"] != None and (value["x"] < mouse_pos[0] < value["x"] + value["img"].get_width()) and (value["y"] < mouse_pos[1] < value["y"] + value["img"].get_height()):
                self.all_menu[self.current_menu]["text_selectionne"]=key
                return
            
        self.all_menu[self.current_menu]["text_selectionne"]=""
