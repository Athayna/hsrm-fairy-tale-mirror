from speechLoops.speechLoop import SpeechLoop
import datetime

class MainLoop(SpeechLoop):
    def __init__(self, handler):
        super().__init__(handler)

    def play(self) -> None:

        self.handler.result = self.listen()

        if ( self.handler.result == "abbrechen"):
            pass

        elif any(x in self.handler.result for x in ("zeit", "uhr")):
            self.speak_text(f'Es ist {datetime.datetime.now().strftime("%H:%M Uhr")}')

        elif "datum" in self.handler.result:
            self.speak_text(f'Heute ist der {datetime.datetime.now().strftime("%d.%m.%Y")}')

        # elif "geburtstag" in self.handler.result:
        #     self.speak_text(f'Dein Geburtstag ist in {(datetime.datetime.now() - datetime.datetime.strptime(self.handler.user.birthday, "%d.%m.%Y")).days)} Tagen')

        elif any(x in self.handler.result for x in ("wetter", "temp", "regen", "kalt", "warm")):
            weather = self.find_weather()
            self.speak_text(f'Das Wetter in {weather["location"]} ist {weather["temperature"]} Grad Celsius')
            if any(x in weather["info"] for x in ("rain", "drizzle", "shower")):
                self.speak_text("Denk an deinen Regenschirm!")
            if (weather["temperature"] < 10):
                self.speak_text("Zieh dich warm an!")
        
        elif any(x in self.handler.result for x in ("erzähl", "les", "spiel", "geschichte", "märchen")):
            
            self.speak_text("Möchtest du wissen, welche Märchen ich alle kenne?")
            while(1):
                self.handler.result = self.listen()
                if (x in self.handler.result for x in ("ja", "genau", "gerne")):
                    self.speak_text("Ich kenne")
                    for name in self.get_maerchen():
                        self.speak_text(name)
                    break
                elif (x in self.handler.result for x in ("nein", "nicht", "nö")):
                    break
                else:
                    self.speak_text("Ich habe dich leider nicht verstanden. Soll ich dir auflisten, welche Märchen ich kenne?")
            self.speak_text("Welches Märchen soll ich dir vorlesen?")
            self.speak_text("Du kannst auch abbrechen, indem du keins sagst.")
            
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("fairytaleLoop"))

        
        else:
            self.speak_text("Ich bin mir nicht sicher, ob ich dich nicht richtig verstanden habe oder ich den Befhel nicht kenne. Was brauchst du?")