from playsound import playsound
from pygame import mixer
import time
class AzanPlayer:
    def __init__(self, azan_path='azan3.mp3', player="pygame"):
        self.azan = azan_path
        self.player = player
        if player == "pygame":
            mixer.init()
            mixer.music.load(self.azan)

    def play(self):
        if self.player == "pygame":
            mixer.music.play()
            while mixer.music.get_busy():
                pass
        else:
            playsound(self.azan)