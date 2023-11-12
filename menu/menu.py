from menu.menuLibrairie import *
import sys

def help():
    print("help is not available for the moment")

def disable_able(list_bool, indice):
    if list_bool[indice]:
        list_bool[indice]=False
    else:
        list_bool[indice]=True

def nothing():
    pass
    
def quit():
    sys.exit(0)

class Menu(MenuLibrairie):
    def __init__(self, directory, screen, update_ecran, update_timers):
        MenuLibrairie.__init__(self)
        self.screen = screen
        self.is_running=False

        # functions from game
        self.update_ecran=update_ecran
        self.update_timers = update_timers

        self.restart_bool=False
        
        t1=0    

        # 0 = music | 1 = audio
        self.music_audio=[True, True]
        path=f"{directory}\\menu\\assets\\Menu Buttons\\Large Buttons\\Large Buttons"
        c=0.4
        pic=get_picture_scale(f"{path}\\Quit Button.png", c, c)
        self.add_button_menu("base", "quit", pic, quit,[],30)
        self.add_menu("settings")
        self.add_button_menu("base", "goto_settings", get_picture_scale(f"{path}\\Options Button.png", c, c), self.change_menu, ["settings"], 30)
        self.add_button_menu("settings", "goto_base", get_picture_scale(f"{path}\\Back Button.png", c, c), self.change_menu,["base"], 30)
        self.add_button_menu("base", "resume", get_picture_scale(f"{path}\\Resume Button.png", c, c), self.end,[], 30)
        self.add_button_menu("base", "restart", get_picture_scale(f"{path}\\New game Button.png", c, c), self.restart,[], 30)

    def _handle_input(self, pressed):
        self.handle_input(pressed)

    def restart(self):
        self.restart_bool=True
        self.end()

    def start(self):
        self.change_menu("base")
        self.is_running=True
        self.restart=False
        self.t1=time.time()
        
    def end(self):
        self.is_running=False
        dt=time.time()-self.t1
        self.update_timers(dt)
