import multiprocessing
from speechLoops.speechLoop import SpeechLoop
import datetime
from text_to_num import alpha2digit

watchListConfirmation = ["ja", "genau", "gern", "ok", "klar", "nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen"]
watchListWords = ["zeit", "uhr", "wetter", "temp", "regen", "kalt", "warm", "heiß", "erzähl", "geschichte", "märchen", "spiel", "lern", "wer", "schönst"]
watchListSkip = ["weiter", "überspringen"]
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
            self.speak_text(f'Es ist {datetime.datetime.now().strftime("%H:%M Uhr")}', watchListSkip)

        elif "wecker" in self.handler.result:
            self.handler.result = ""
            while 1:
                if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                    self.speak_text(f'Der Wecker ist gestellt.', watchListSkip)
                    wecker = f'{getTimeHour}:{getTimeMinute}'
                    timerProcess = multiprocessing.Process(target=set_Timer, args=[wecker])
                    timerProcess.start()
                    break
                getTimeHour = 0
                getTimeMinute = 0
                hourSet = False
                self.speak_text(f'Auf wieviel Uhr soll ich den Wecker stellen?', watchListSkip)
                if self.handler.result == "":
                    self.handler.result = self.listen()
                if not self.handler.result:
                    return
                checkStringForNum = alpha2digit(self.handler.result, "de")
                checkStringForNum = checkStringForNum.replace(":", " ")
                if any(word.isdigit() for word in checkStringForNum.split(" ")):
                    for word in checkStringForNum.split(" "):
                        if hourSet:
                            if word.isdigit():
                                getTimeMinute = word
                                break
                        if word.isdigit():
                            getTimeHour = word
                            hourSet = True
                    if getTimeMinute:
                        self.speak_text(f'Möchtest du den Wecker auf {getTimeHour} Uhr {getTimeMinute} stellen?', watchListConfirmation)
                    else:
                        self.speak_text(f'Möchtest du den Wecker auf {getTimeHour} Uhr stellen?', watchListConfirmation)
                    while(1):
                        if self.handler.result == "":
                            self.handler.result = self.listen()
                        if not self.handler.result:
                            print("no result")
                            return
                        if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                            break
                        elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                            self.handler.result = ""
                            break
                        else:
                            self.handler.result = ""
                            self.speak_text("Ich habe dich leider nicht verstanden.")
                            if getTimeMinute:
                                self.speak_text(f'Möchtest du den Wecker auf {getTimeHour} Uhr {getTimeMinute} stellen?', watchListConfirmation)
                            else:
                                self.speak_text(f'Möchtest du den Wecker auf {getTimeHour} Uhr stellen?', watchListConfirmation)                


        elif "datum" in self.handler.result:
            self.handler.result = ""
            self.speak_text(f'Heute ist der {datetime.datetime.now().strftime("%d.%m.%Y")}', watchListSkip)

        elif "name" in self.handler.result:
            self.handler.result = ""
            self.speak_text("Wie soll ich dich denn nennen?", watchListSkip)
            while(1):
                self.handler.result = self.listen()
                tempName = self.handler.result
                if not self.handler.result:
                    print("no result")
                    return
                self.handler.result = ""
                print("bestätige name")
                self.speak_text(f'Habe ich dich richtig verstanden? Du heißt also {tempName}', watchListConfirmation)
                if self.handler.result == "":
                    print("name richtig?")
                    self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                    self.handler.result = ""
                    self.handler.user.name = tempName
                    self.speak_text(f'Hallo {self.handler.user.name}, es freut mich dich kennenzulernen!', watchListSkip)
                    break
                elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                    self.handler.result = ""
                    self.speak_text("Tut mir leid. Wie soll ich dich nennen?", watchListSkip)
                else:
                    self.handler.result = ""
                    self.speak_text("Ich habe dich leider nicht verstanden. Wie soll ich dich nennen? Du kannst mir auch nur einen Spitznamen nennen mit dem ich dich ansprechen kann.", watchListSkip)

        elif any(x in self.handler.result for x in ("wetter", "temp", "regen", "kalt", "warm", "heiß")):
            self.handler.result = ""
            weather = self.find_weather()
            self.speak_text(f'Das Wetter in {weather["location"]} ist {weather["temperature"]} Grad Celsius', watchListSkip)
            if any(x in weather["info"] for x in ("rain", "drizzle", "shower")):
                self.speak_text("Denk an deinen Regenschirm!", watchListSkip)
            if (weather["temperature"] < 15):
                self.speak_text("Zieh dich schön warm an!", watchListSkip)
            elif (weather["temperature"] > 15 and weather["temperature"] < 20):
                self.speak_text("Etwas langärmliges oder ein Tshirt mit Jäckchen und eine lange Hose sind heute ganz gut!", watchListSkip)
            elif (weather["temperature"] > 20 and weather["temperature"] < 25):
                self.speak_text("Ein Tshirt mit Jäckchen und lange Hose reichen heute aus!")
            elif (weather["temperature"] > 25):
                self.speak_text("Es ist sehr warm, ein Tshirt und eine kurze Hose reichen bestimmt! Denk daran genug zu trinken.", watchListSkip)
        
        elif any(x in self.handler.result for x in ("erzähl", "geschichte", "märchen")):
            self.handler.result = ""
            self.speak_text("Möchtest du wissen, welche Märchen ich kenne?", watchListConfirmation)
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
                    self.speak_text("Ich habe dich leider nicht verstanden. Soll ich dir auflisten, welche Märchen ich kenne?", watchListConfirmation)
            self.speak_text("Welches Märchen soll ich dir vorlesen?", self.get_maerchen())
            
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("fairytaleLoop"))

        elif any(x in self.handler.result for x in ("spiel", "lern")):
            self.handler.result = ""
            self.speak_text("Welches Lernspiel möchstest du spielen?")
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("gameLoop"))

        elif "wer" in self.handler.result and "schönst" in self.handler.result:
            self.handler.result = ""
            self.speak_text(f'{self.handler.user.name}, Du bist am Schönsten! Selbst das Schneewittchen, ueber den Bergen, bei den sieben Zwergen, ist nicht schoener als du.', watchListSkip)

        else:
            self.handler.result = ""
            self.speak_text("Ich habe dich nicht verstanden. Möchtest du wissen, was ich alles kann?", watchListConfirmation)
            while(1):
                if self.handler.result == "":
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
                    self.speak_text("Ich habe dich leider nicht verstanden. Soll ich dir auflisten, was ich alles kann?", watchListConfirmation)

            if self.handler.result == "":
                self.speak_text("Was möchtest du gerne machen?", watchListWords)


def set_Timer(time) -> None:
    """Method for setting a timer."""
    print("in timer")
    while not time in datetime.datetime.now().strftime("%H:%M Uhr"):
        time.sleep(30)
    if time in datetime.datetime.now().strftime("%H:%M Uhr"):
        SpeechLoop.speak_text("wecker klingeln")