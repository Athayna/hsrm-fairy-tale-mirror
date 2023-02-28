from speechLoops.speechLoop import SpeechLoop
import datetime

watchListWords = ["zeit", "uhr", "wetter", "temp", "regen", "kalt", "warm", "heiß", "erzähl", "geschichte", "märchen", "spiel", "lern", "wer", "schönst"]
class MainLoop(SpeechLoop):
    """MainLoop is the main loop of the program. It is the second loop that is started and the last one that is stopped."""

    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:

        if self.handler.result == "":
            self.handler.result = self.listen()

        if not self.handler.result:
            return
        
        if self.handler.checkForAbort():
            pass

        elif any(x in self.handler.result for x in ("zeit", "uhr")):
            self.handler.result = ""
            self.speak_text(f'Es ist {datetime.datetime.now().strftime("%H:%M Uhr")}')

        elif "datum" in self.handler.result:
            self.handler.result = ""
            self.speak_text(f'Heute ist der {datetime.datetime.now().strftime("%d.%m.%Y")}')

        elif any(x in self.handler.result for x in ("wetter", "temp", "regen", "kalt", "warm", "heiß")):
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
                    self.speak_text("Ich habe dich leider nicht verstanden. Soll ich dir auflisten, welche Märchen ich kenne?")
            self.speak_text("Welches Märchen soll ich dir vorlesen?")
            
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("fairytaleLoop"))

        elif any(x in self.handler.result for x in ("spiel", "lern")):
            self.handler.result = ""
            self.speak_text("Welches Lernspiel möchstest du spielen?")
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("gameLoop"))

        elif "wer" in self.handler.result and "schönst" in self.handler.result:
            self.handler.result = ""
            self.speak_text(f'{self.handler.user.name}, Du bist am Schönsten! Selbst das Schneewittchen, ueber den Bergen, bei den sieben Zwergen, ist nicht schoener als du.')

        else:
            self.handler.result = ""
            self.speak_text("Ich habe dich nicht verstanden. Möchtest du wissen, was ich alles kann?")
            while(1):
                self.handler.result = self.listen()
                if not self.handler.result:
                    return
                if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                    self.handler.result = ""
                    self.speak_text("Ich kann dir ein Märchen erzählen, mit dir Lernspiele spielen, herausfinden wer am Schönsten im ganzen Land ist, dir die Uhrzeit sagen, das Datum nennen oder das Wetter vorhersagen.", watchListWords)
                    break
                elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                    self.handler.result = ""
                    break
                else:
                    self.handler.result = ""
                    self.speak_text("Ich habe dich leider nicht verstanden. Soll ich dir auflisten, was ich alles kann?")

            if self.handler.result == "":
                self.speak_text("Was möchtest du gerne machen?")