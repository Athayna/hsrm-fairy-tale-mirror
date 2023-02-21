from speechLoops.speechLoop import SpeechLoop

class FairytaleLoop(SpeechLoop):
    """SpeechLoop for the fairytale mode."""
    
    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:

        self.handler.result = self.listen()

        if any(fairytale in self.handler.result for fairytale in self.get_maerchen() ):

            for fairytale in self.get_maerchen():
                    if fairytale in self.handler.result:
                        self.handler.result = fairytale
            self.speak_text(f'Hier ist die Geschichte von {self.handler.result}:')
            print(self.handler)
            self.read_fairy_tale(self.handler.result)
            print("Märchen vorbei")
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
              
        else:
            self.speak_text("Dieses Märchen kenne ich leider nicht. Möchtest du wissen, welche Märchen ich kenne?")
            while(1):
                self.handler.result = self.listen()
                print(self.handler.result)
                if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                    self.speak_text("Ich kenne")
                    alleMaerchen = ""
                    for name in self.get_maerchen():
                        alleMaerchen += name + ", "
                    self.speak_text(alleMaerchen)
                    break
                elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                    break
                else:
                    self.speak_text("Ich habe dich leider nicht verstanden. Welches Märchen möchtest du denn gerne hören?")
            self.speak_text("Welches Märchen möchtest du denn gerne hören?")