from speechLoops.speechLoop import SpeechLoop
import threading
import os
from gtts import gTTS
from playsound import playsound
import multiprocessing
import re
import copy


class FairytaleLoop(SpeechLoop):
    
    def __init__(self, handler):
        super().__init__(handler)

    def play(self) -> None:

        self.handler.result = self.listen()

        if (self.handler.result in self.get_maerchen()):
            self.speak_text(f'Hier ist die Geschichte von {self.handler.result}:')
            print(self.handler)
            self.read_fairy_tale(self.handler.result)
            print("Märchen vorbei")
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
            
        
        elif ("kein" in self.handler.result):
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
           
        
        else:
            self.speak_text("Dieses Märchen kenne ich leider nicht. Möchtest du wissen, welche Märchen ich kenne?")
            while(1):
                self.handler.result = self.listen()
                print(self.handler.result)
                if any(x in self.handler.result for x in ("ja", "genau", "gerne")):
                    self.speak_text("Ich kenne")
                    for name in self.get_maerchen():
                        self.speak_text(name)
                    break
                elif any(x in self.handler.result for x in ("nein", "nicht", "nö")):
                    break
                else:
                    self.speak_text("Was meine Mutter?")
                    #self.speak_text("Ich habe dich leider nicht verstanden. Welches Märchen möchtest du denn gerne hören?")
            self.speak_text("Welches Märchen möchtest du denn gerne hören?")