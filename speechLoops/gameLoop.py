import random
from speechLoops.speechLoop import SpeechLoop

class GameLoop(SpeechLoop):
    """SpeechLoop for the game mode."""
    
    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        self.handler.user.name = "susi"
        self.handler.result = self.listen()

        if any(x in self.handler.result for x in ("Wort")):
        ################################################ VORSTELLUNG - Spiegel ################################################
            self.speak_text("Los geht's mit Wort für Wort.")
            wordArray = ["Spiel", "Kugel", "Frosch", "Brunnen", "Rad"]
            correctAnswers = 0
            beendeSpiel = 5
            getWordNum = random.randint(0, 4)
            guessWord = wordArray[getWordNum]
            while(beendeSpiel):
                self.speak_text("Wie heißt das angezeigte Wort?")
                self.handler.result = self.listen()
                if (guessWord.lower() in self.handler.result):
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    self.speak_text(f'Super {self.handler.user.name}! Da steht {guessWord}, das stimmt. Weiter so!')
                    getWordNum = random.randint(0, 4)
                    guessWord = wordArray[getWordNum]
                    continue
                elif any(x in self.handler.result for x in ("ende", "abbrechen", "stop")):
                    self.handler.result = ""
                    self.speak_text("Möchtest du das Spiel wirklich beenden?")
                    while(1):
                        self.handler.result = self.listen()
                        if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                            self.handler.result = ""
                            beendeSpiel = 0
                            self.speak_text("Das Spiel wurde beendet.")
                            break
                        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                            self.handler.result = ""
                            self.speak_text("Das Spiel geht weiter.")
                            break
                        else:
                            self.handler.result = ""
                            self.speak_text("Ich habe dich leider nicht verstanden. Sicher, dass du das Spiel beenden willst?")
                elif any(x in self.handler.result for x in ("weiß", "keine")) and any(x in self.handler.result for x in ("nicht", "ahnung", "plan", "lust")):
                    self.handler.result = ""
                    self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, welches Wort da steht.")
                elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                    self.handler.result = ""
                    beendeSpiel -= 1
                    self.speak_text(f'Da stand {guessWord}. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.')
                    getWordNum = random.randint(0, 4)
                    guessWord = wordArray[getWordNum]
                else:
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir das Wort verrate, dass da steht.')
                    self.handler.result = ""

            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du bist ein richtiger Profi im Lesen!')
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Du kannst mit jedem Spiel mehr.')
            print("Spiel vorbei")
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("abc", "künste", "alphabet")):
        ################################################ VORSTELLUNG - Spiegel ################################################
            self.speak_text("Los geht's mit ABC Künste.")
            alphabetArray = ["a", "b", "c", "d", "e"]
            correctAnswers = 0
            beendeSpiel = 5
            getAlphabetNum = random.randint(0, 4)
            guessAlphabet = alphabetArray[getAlphabetNum]
            while(beendeSpiel):
                self.speak_text("Wie heißt der angezeigte Buchstabe?")
                self.handler.result = self.listen()
                if (guessAlphabet.lower() in self.handler.result):
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    self.speak_text(f'Super {self.handler.user.name}! Da steht {guessAlphabet}, das stimmt. Weiter so!')
                    getAlphabetNum = random.randint(0, 4)
                    guessAlphabet = alphabetArray[getAlphabetNum]
                    continue
                elif any(x in self.handler.result for x in ("ende", "abbrechen", "stop")):
                    self.handler.result = ""
                    self.speak_text("Möchtest du das Spiel wirklich beenden?")
                    while(1):
                        self.handler.result = self.listen()
                        if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                            self.handler.result = ""
                            beendeSpiel = 0
                            self.speak_text("Das Spiel wurde beendet.")
                            break
                        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                            self.handler.result = ""
                            self.speak_text("Das Spiel geht weiter.")
                            break
                        else:
                            self.handler.result = ""
                            self.speak_text("Ich habe dich leider nicht verstanden. Sicher, dass du das Spiel beenden willst?")
                elif any(x in self.handler.result for x in ("weiß", "keine")) and any(x in self.handler.result for x in ("nicht", "ahnung", "plan", "lust")):
                    self.handler.result = ""
                    self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, welcher Buchstabe da steht.")
                elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                    self.handler.result = ""
                    beendeSpiel -= 1
                    self.speak_text(f'Das war der Buchstabe {guessAlphabet}. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.')
                    getAlphabetNum = random.randint(0, 4)
                    guessAlphabet = alphabetArray[getAlphabetNum]
                else:
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir den Buchstaben verrate, der da steht.')
                    self.handler.result = ""

            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du kennst dein Alphabet bestens! Trau dich gerne mal an das Wort für Wort Spiel.')
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Du kannst mit jedem Spiel mehr.')
            print("Spiel vorbei")
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
            self.handler.result = ""
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
              
        else:
            self.handler.result = ""
            self.speak_text("Dieses Lernspiel kenne ich leider nicht. Möchtest du wissen, welche Lernspiele ich kenne?")
            while(1):
                self.handler.result = self.listen()
                print(self.handler.result)
                if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                    self.handler.result = ""
                    self.speak_text("Ich kenne Wort für Wort, ABC Künste, Zahlenzauber, Einmaleins Meister, Tiktak Uhrenspaß")
                    break
                elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                    self.handler.result = ""
                    break
                else:
                    self.handler.result = ""
                    self.speak_text("Ich habe dich leider nicht verstanden. Welches Lernspiel möchtest du denn gerne spielen?")
            self.speak_text("Welches Märchen möchtest du denn gerne hören?")