from menu.menuLibrairie import *
import sys

def help():
    print("help is not available for the moment")

def nothing():
    pass
    
def quit():
    sys.exit(0)

class Menu(MenuLibrairie):
    def __init__(self, directory, screen, update_ecran, update_timers, audio):
        MenuLibrairie.__init__(self)
        self.screen = screen
        self.audio=audio
        self.is_running=False

        # text qui defile
        self.pointeur=0
        self.max_text=20
        self.timer_defilement=0
        self.cooldown_defilement=0.3
        self.last_music=None
        self.text_to_display=""

        # functions from game
        self.update_ecran=update_ecran
        self.update_timers = update_timers

        self.restart_bool=False
        t1=0    
        self.last=""
        self.cpt=0

        # 0 = music | 1 = audio
        self.music_audio=[True, True]
        path=f"{directory}\\menu\\assets\\Menu Buttons\\Large Buttons\\Large Buttons"
        path2=f"{directory}\\menu\\assets\\Menu Buttons\\Square Buttons\\Square Buttons"
        c=0.4
        pic=get_picture_scale(f"{path}\\Quit Button.png", c, c)
        c2=0.4
        pic_square = get_picture_scale(f"{path2}\\Audio Square Button.png", c2, c2)
        self.add_button_menu("base", "Resume", get_picture_scale(f"{path}\\Resume Button.png", c, c), self.end,[], 30)

        self.add_menu("settings")
        self.add_button_menu("base", "goto_settings", get_picture_scale(f"{path}\\Settings Button.png", c, c), self.goto_settings, [], 30)
        # inside settings
        self.add_button_menu("settings", "goto_base", get_picture_scale(f"{path}\\Back Button.png", c, c), self.change_menu,["base"], 30)
        self.add_button_menu("settings", "Audio", pic_square, nothing, [], "goto_base", x=self.all_menu["settings"]["button"]["goto_base"]["x"]+self.all_menu["settings"]["button"]["goto_base"]["image"].get_width()+pic_square.get_width()+30)
        self.add_button_menu("settings", "Music", get_picture_scale(f"{path2}\\Music Square Button.png", c2, c2), self.audio.pause_unpause_music, [], "goto_base", x=self.all_menu["settings"]["button"]["goto_base"]["x"]+self.all_menu["settings"]["button"]["goto_base"]["image"].get_width()+pic_square.get_width()*2.5+30)
        self.add_button_menu("settings", "PrevMusic", get_picture_scale(f"{path2}\\Back Square Button.png", c2, c2), self.audio.start_music, [False], 30, x=screen.get_width()/2-1.25*pic_square.get_width())
        self.add_button_menu("settings", "NextMusic", get_picture_scale(f"{path2}\\Next Square Button.png", c2, c2), self.audio.start_music, [], "PrevMusic", x=screen.get_width()/2+0.25*pic_square.get_width())
        self.add_text_menu("settings", "MusicText", "♫ "+ "music"+ " ♫ ", screen.get_width()/2+1.5*pic_square.get_width(), "PrevMusic", 30, pic.get_height())
        self.add_button_menu("settings", "PrevPlaylist", get_picture_scale(f"{path2}\\Back Square Button.png", c2, c2), self.change_playlist, [True], 30, x=screen.get_width()/2-1.25*pic_square.get_width())
        self.add_button_menu("settings", "NextPlaylist", get_picture_scale(f"{path2}\\Next Square Button.png", c2, c2), self.change_playlist, [False], "PrevPlaylist", x=screen.get_width()/2+0.25*pic_square.get_width())
        self.add_text_menu("settings", "PlaylistText", "Current Radio : "+audio.get_current_playlist(), screen.get_width()/2+1.5*pic_square.get_width(), "PrevPlaylist", 30, pic.get_height())
        self.add_button_menu("settings", "Controls", get_picture_scale(f"{path}\\Controls Button.png", c, c), self.change_menu,["base"], 30)

        self.add_button_menu("base", "quit", pic, quit,[],30)
        self.add_button_menu("base", "Restart", get_picture_scale(f"{path}\\New game Button.png", c, c), self.restart,[], 30)

    def change_playlist(self, next):
        if self.last =="":
            self.last=next
            self.cpt=1
        else:
            if self.last == next:
                self.cpt=1
                self.last=next
            else:
                self.last=next
                self.cpt+=1
        if self.cpt == 5:
            self.audio.change_playlist(next, True)
            self.cpt=0
            self.last=""
        else:
            self.audio.change_playlist(next)
        self.update_text_menu("settings", "PlaylistText", "Current Radio : "+self.audio.get_current_playlist(), 30)

    def goto_settings(self):
        self.pointeur=0
        self.change_menu("settings")

    def _handle_input(self, pressed):
        if self.last_music != self.audio.get_current_track():
            self.last_music=self.audio.get_current_track()
            self.pointeur=0
        elif self.timer_defilement+self.cooldown_defilement < time.time():
            self.timer_defilement=time.time()
            self.pointeur+=1
        if len(self.last_music) > self.max_text:
            l=self.audio.get_current_track()+self.audio.get_current_track()
            self.text_to_display="♫ "+l[self.pointeur%len(self.last_music):self.pointeur%len(self.last_music)+self.max_text]+" ♫"
        else:
            self.text_to_display="♫ "+self.last_music+" ♫"
        self.update_text_menu("settings", "MusicText", self.text_to_display, 30)
        self.handle_input(pressed)
        self.update_ecran_menu()

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
