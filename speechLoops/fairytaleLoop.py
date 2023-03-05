from speechLoops.speechLoop import SpeechLoop

watchListConfirmation = ["ja", "genau", "gern", "ok", "klar", "nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen"]
watchListMenu = ["zeit", "uhr", "wetter", "temp", "regen", "kalt", "warm", "heiß", "erzähl", "geschichte", "märchen", "spiel", "lern", "wer", "schönst"]

class FairytaleLoop(SpeechLoop):
    """SpeechLoop for the fairytale mode."""
    
    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:

        if self.handler.result == "":
            self.handler.result = self.listen()

        if not self.handler.result:
            return

        if any(fairytale in self.handler.result for fairytale in self.get_maerchen() ):
            for fairytale in self.get_maerchen():
                    if fairytale in self.handler.result:
                        self.handler.result = ""
                        readFairytale = fairytale
            self.speak_text(f'Hier ist die Geschichte von {readFairytale}:')
            self.read_fairy_tale(readFairytale)
            self.handler.imagePlayer.setImage("gesicht-lachen")
            self.handler.result = ""
            self.speak_text(f'Das Märchen ist zu Ende. Was möchtest du gerne machen?', watchListMenu)
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
            self.handler.result = ""
            self.speak_text(f'Die Märchenauswahl wurde abgebrochen. Was möchtest du gerne machen?', watchListMenu)
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
              
        else:
            self.handler.result = ""
            self.speak_text("Dieses Märchen kenne ich leider nicht. Möchtest du wissen, welche Märchen ich kenne?", watchListConfirmation)
            while(1):
                if self.handler.result == "":
                    self.handler.result = self.listen()
                if not self.handler.result:
                    return
                if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                    self.handler.result = ""
                    self.speak_text("Ich kenne")
                    alleMaerchen = ""
                    for name in self.get_maerchen():
                        alleMaerchen += name + ", "
                    self.speak_text(alleMaerchen, self.get_maerchen())
                    break
                elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                    self.handler.result = ""
                    break
                else:
                    self.handler.result = ""
                    self.speak_text("Ich habe dich leider nicht verstanden. Möchtest du wissen, welche Märchen ich kenne?", watchListConfirmation)
            
            if self.handler.result == "":
                self.speak_text("Welches Märchen möchtest du denn gerne hören?", self.get_maerchen())