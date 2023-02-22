from speechLoops.speechLoop import SpeechLoop
import datetime

class MainLoop(SpeechLoop):
    """MainLoop is the main loop of the program. It is the second loop that is started and the last one that is stopped."""

    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        self.handler.result = self.listen()

        if self.handler.checkForAbort():
            pass

        elif any(x in self.handler.result for x in ("zeit", "uhr")):
            self.handler.result = ""
            self.speak_text(f'Es ist {datetime.datetime.now().strftime("%H:%M Uhr")}')

        elif "datum" in self.handler.result:
            self.handler.result = ""
            self.speak_text(f'Heute ist der {datetime.datetime.now().strftime("%d.%m.%Y")}')

        elif any(x in self.handler.result for x in ("wetter", "temp", "regen", "kalt", "warm")):
            self.handler.result = ""
            weather = self.find_weather()
            self.speak_text(f'Das Wetter in {weather["location"]} ist {weather["temperature"]} Grad Celsius')
            if any(x in weather["info"] for x in ("rain", "drizzle", "shower")):
                self.speak_text("Denk an deinen Regenschirm!")
            if (weather["temperature"] < 10):
                self.speak_text("Zieh dich warm an!")
        
        elif any(x in self.handler.result for x in ("erzähl", "geschichte", "märchen")):
            self.handler.result = ""
            self.speak_text("Möchtest du wissen, welche Märchen ich kenne?")
            while(1):
                self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                    self.handler.result = ""
                    self.speak_text("Ich kenne")
                    alleMaerchen = ""
                    for name in self.get_maerchen():
                        alleMaerchen += name + ", "
                    self.speak_text(alleMaerchen)
                    break
                elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                    self.handler.result = ""
                    break
                else:
                    self.handler.result = ""
                    self.speak_text("Ich habe dich leider nicht verstanden. Soll ich dir auflisten, welche Märchen ich kenne?")
            self.speak_text("Welches Märchen soll ich dir vorlesen?")
            
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("fairytaleLoop"))

        else:
            self.handler.result = ""
            self.speak_text("Ich habe dich nicht verstanden. Möchtest du wissen, was ich alles kann?")
            while(1):
                self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                    self.handler.result = ""
                    self.speak_text("Ich kann Geschichten erzählen, die Uhrzeit, das Datum oder das Wetter sagen, ...")
                    break
                elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                    self.handler.result = ""
                    break
                else:
                    self.handler.result = ""
                    self.speak_text("Ich habe dich leider nicht verstanden. Soll ich dir auflisten, was ich alles kann?")