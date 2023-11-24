import pygame
import json
import random

class Audio:
    def __init__(self, directory, playlist, config):
        self.path_music=directory+"\\audio\\musics\\"
        self.path_sound=directory+"\\audio\\sounds\\"
        self.config=config
        self.musics = json.load(open(directory+"\\audio\\musics.json"))
        self.playlists=list(self.musics.keys())
        self.is_paused_music=False
        self.is_paused_sound=False
        self.current=[]
        self.nbr_track=0
        self.current_playlist=self.playlists.index(playlist)
        pygame.mixer.init()
        self.volume_music=0.01
        self.volume_sound=1.0
        pygame.mixer.music.set_volume(self.volume_music)

        self.slide_sound=pygame.mixer.Sound(self.path_sound+"slide_1.mp3")
        self.slide_speed_sound=pygame.mixer.Sound(self.path_sound+"slide_speed_1.mp3")
        self.running_sound=pygame.mixer.Sound(self.path_sound+"running_1.mp3")
        
        self.dict_sounds={
            "slide":self.slide_sound,
            "slide_speed":self.slide_speed_sound,
            "run":self.running_sound
        }
        self.queue_musics_playlist()
        self.start_music()

        if self.config.get("sound") == "False":
            self.volume_sound=0.0
            self.is_paused_sound=True

        if self.config.get("music") == "False":
            self.pause_music()
            self.is_paused_music=True


    def play_long_sounds(self, sound_name):
        pygame.mixer.Sound.set_volume(self.dict_sounds[sound_name], self.volume_sound)
        pygame.mixer.Sound.play(self.dict_sounds[sound_name], -1)

    def stop_long_sounds(self, sound_name):
        pygame.mixer.Sound.stop(self.dict_sounds[sound_name])

    def play_random_sound(self, sound_name, nbr):
        self.play_sound(sound_name+"_"+str(random.randint(1, nbr))+".mp3")

    def play_sound(self, sound):
        sound=pygame.mixer.Sound(self.path_sound+sound)
        pygame.mixer.Sound.set_volume(sound, self.volume_sound)
        pygame.mixer.Sound.play(sound)

    def change_playlist(self, next, techno=False):
        if techno:
            self.current_playlist=self.playlists.index("TECHNO")
        else:
            if next:
                self.current_playlist+=1
                if self.get_current_playlist() == "TECHNO":
                    self.current_playlist+=1
            else:
                self.current_playlist-=1
                if self.get_current_playlist() == "TECHNO":
                    self.current_playlist-=1
        self.queue_musics_playlist()
        self.start_music()

    def get_current_playlist(self):
        return self.playlists[self.current_playlist%len(self.playlists)]

    def get_current_track(self):
        return self.current[(self.nbr_track-1)%len(self.current)]["name"]

    def pause_unpause_sound(self):
        self.config.set("sound", str(self.is_paused_sound))
        if self.is_paused_sound:
            self.volume_sound=1.0
            self.play_random_sound("menu", 3)
        else:
            self.volume_sound=0.0
        self.is_paused_sound=not self.is_paused_sound

    def pause_unpause_music(self):
        self.config.set("music", str(self.is_paused_music))
        if self.is_paused_music:
            self.unpause_music()
        else:
            self.pause_music()
        self.is_paused_music=not self.is_paused_music

    def pause_music(self):
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        pygame.mixer.music.unpause()

    def queue_musics_playlist(self):
        self.current=[]
        for i in range(len(self.musics[self.get_current_playlist()])):
            try:
                self.current.append(self.musics[self.get_current_playlist()][i])    
            except Exception as e:
                print(e)
        random.shuffle(self.current)
        self.nbr_track=0

    def start_music(self, next=True):
        self.is_paused_music=False
        pygame.mixer.music.unload()
        if not next:
            self.nbr_track-=2
        pygame.mixer.music.load(self.path_music+self.current[self.nbr_track%len(self.current)]["file"])
        self.nbr_track+=1
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT+1) 

