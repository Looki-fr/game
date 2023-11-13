import pygame
import json
import random

class Audio:
    def __init__(self, directory, playlist):
        self.path=directory+"\\audio\\musics\\"
        self.musics = json.load(open(directory+"\\audio\\musics.json"))
        self.playlists=list(self.musics.keys())
        self.is_paused_music=False
        self.current=[]
        self.nbr_track=0
        self.current_playlist=self.playlists.index(playlist)
        pygame.mixer.init()

        self.queue_musics_playlist()
        self.start_music()

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

    def pause_unpause_music(self):
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
        pygame.mixer.music.load(self.path+self.current[self.nbr_track%len(self.current)]["file"])
        self.nbr_track+=1
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT+1) 

