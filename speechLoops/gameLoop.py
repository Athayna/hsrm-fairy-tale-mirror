import random
from speechLoops.speechLoop import SpeechLoop
from text_to_num import alpha2digit

class GameLoop(SpeechLoop):
    """SpeechLoop for the game mode."""
    
    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        self.handler.user.name = "susi"
        self.handler.user.wordGame = 6
        self.handler.user.numberGame = 2
        self.handler.user.multGame = 2
        #self.handler.result = self.listen()
        self.handler.result = "zahl"

        if "wort" in self.handler.result:
        ################################################ SPIEL - Wort für Wort ################################################
            self.speak_text("Los geht's mit Wort für Wort.")
            wordArray = [["du", "so", "es", "da", "ja"], 
                         ["mit", "Kuh", "war", "rot", "Tal"], 
                         ["Hund", "Mund", "klug", "wenn", "dort"],
                         ["Spiel", "Kugel", "essen", "gehen", "lesen"],
                         ["Frosch", "Brunnen", "schlau", "rennen", "lustig"]]
            level = self.handler.user.wordGame//5
            correctAnswers = 0
            beendeSpiel = 3
            usedArray = wordArray[level].copy()
            getWordNum = random.randint(0, (len(usedArray))-1)
            guessWord = usedArray[getWordNum]
            self.handler.imagePlayer.setTextImage(guessWord)
            print(guessWord)
            while(beendeSpiel):
                self.speak_text("Wie heißt das angezeigte Wort?")
                self.handler.result = self.listen(showPictures=False)
                if (guessWord.lower() in self.handler.result):
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    usedArray.remove(guessWord)
                    if beendeSpiel:
                        self.speak_text(f'Super {self.handler.user.name}! Da steht {guessWord}, das stimmt. Weiter so!')
                        getWordNum = random.randint(0, (len(usedArray))-1)
                        guessWord = usedArray[getWordNum]
                        self.handler.imagePlayer.setTextImage(guessWord)
                    print(guessWord)
                    continue
                elif any(x in self.handler.result for x in ("ende", "abbrechen", "stop")):
                    self.handler.result = ""
                    self.speak_text("Möchtest du das Spiel wirklich beenden?")
                    while(1):
                        self.handler.result = self.listen()
                        if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                            self.handler.result = ""
                            beendeSpiel = 0
                            self.speak_text("Beenden...")
                            break
                        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                            self.handler.result = ""
                            self.speak_text("Das Spiel geht weiter.")
                            self.handler.imagePlayer.setTextImage(guessWord)
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
                    if beendeSpiel:
                        tempWord = guessWord
                        while tempWord == guessWord:
                            getWordNum = random.randint(0, (len(usedArray))-1)
                            guessWord = usedArray[getWordNum]
                        self.handler.imagePlayer.setTextImage(guessWord)
                    print(guessWord)
                else:
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir das Wort verrate, dass da steht.')
                    self.handler.result = ""

            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du bist ein richtiger Profi im Lesen!')
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Du kannst mit jedem Spiel mehr.')
            print("Spiel vorbei")
            self.handler.user.wordGame += correctAnswers
            self.speak_text(f'Das Spiel ist zu Ende. Was möchtest du gerne machen?')
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("abc", "künste", "alphabet")):
        ################################################ SPIEL - ABC Künste ################################################
            self.speak_text("Los geht's mit ABC Künste. Um den Buchstaben zu erraten sag ein davor. Zum Beispiel, wenn da a steht, musst du ein a sagen, sonst verstehe ich dich leider nicht.")
            alphabetArray = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            correctAnswers = 0
            beendeSpiel = 5
            getAlphabetNum = random.randint(0, 51)
            if getAlphabetNum > 25:
                guessAlphabet = alphabetArray[getAlphabetNum-26].upper()
            else:
                guessAlphabet = alphabetArray[getAlphabetNum]
            self.handler.imagePlayer.setTextImage(guessAlphabet)
            print(guessAlphabet)
            while(beendeSpiel):
                self.speak_text("Wie heißt der angezeigte Buchstabe?")
                self.handler.result = self.listen(showPictures=False)
                if any(x in self.handler.result for x in ("ende", "abbrechen", "stop")):
                    self.handler.result = ""
                    self.speak_text("Möchtest du das Spiel wirklich beenden?")
                    while(1):
                        self.handler.result = self.listen()
                        if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                            self.handler.result = ""
                            beendeSpiel = 0
                            self.speak_text("Beenden...")
                            break
                        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                            self.handler.result = ""
                            self.speak_text("Das Spiel geht weiter.")
                            self.handler.imagePlayer.setTextImage(guessAlphabet)
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
                    getAlphabetNum = random.randint(0, (len(alphabetArray)*2-1))
                    if getAlphabetNum > 25:
                        guessAlphabet = alphabetArray[getAlphabetNum-26].upper()
                    else:
                        guessAlphabet = alphabetArray[getAlphabetNum]
                    self.handler.imagePlayer.setTextImage(guessAlphabet)
                    print(guessAlphabet)
                elif "ein" in self.handler.result and guessAlphabet.lower() in self.handler.result:
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    alphabetArray.remove(guessAlphabet.lower())
                    self.speak_text(f'Super {self.handler.user.name}! Da steht {guessAlphabet}, das stimmt. Weiter so!')
                    getAlphabetNum = random.randint(0, (len(alphabetArray)*2-1))
                    if getAlphabetNum > 25:
                        guessAlphabet = alphabetArray[getAlphabetNum-26].upper()
                    else:
                        guessAlphabet = alphabetArray[getAlphabetNum]
                    self.handler.imagePlayer.setTextImage(guessAlphabet)
                    print(guessAlphabet)
                    continue
                else:
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir den Buchstaben verrate, der da steht.')
                    self.handler.result = ""

            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du kennst dein Alphabet bestens! Trau dich gerne mal an das Wort für Wort Spiel.')
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Bald kannst du das ganze ABC.')
            print("Spiel vorbei")
            self.speak_text(f'Das Spiel ist zu Ende. Was möchtest du gerne machen?')
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))

        elif any(x in self.handler.result for x in ("zahl", "zauber")):
        ################################################ SPIEL - Zahlenzauber ################################################
            self.speak_text("Los geht's mit Zahlenzauber.")
            correctAnswers = 0
            beendeSpiel = 5
            level = self.handler.user.numberGame//5
            if level == 0:
                getNum1 = random.randint(0, 5)
                getNum2 = random.randint(0, 5)
                guessSolution = getNum1 + getNum2
                displayCalc = f'{getNum1} + {getNum2} ='
            elif level == 1:
                getNum1 = random.randint(0, 10)
                getNum2 = random.randint(0, (10-getNum1))
                guessSolution = getNum1 + getNum2
                displayCalc = f'{getNum1} + {getNum2} ='
            elif level >=2:
                chooseArithmetic = random.randint(0, 1)
                if chooseArithmetic:
                    getNum1 = random.randint(0, (5*level))
                    getNum2 = random.randint(0, getNum1)
                    guessSolution = getNum1 - getNum2
                    displayCalc = f'{getNum1} - {getNum2} ='
                else:
                    getNum1 = random.randint(0, (5*level))
                    getNum2 = random.randint(0, (5*level))
                    guessSolution = getNum1 + getNum2
                    displayCalc = f'{getNum1} + {getNum2} ='
            self.handler.imagePlayer.setTextImage(displayCalc)
            print(displayCalc)
            while(beendeSpiel):
                self.speak_text("Was ist das Ergebnis der angezeigten Rechnung?")
                self.handler.result = self.listen(showPictures=False)
                if str(guessSolution) in alpha2digit(self.handler.result, "de"):
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    self.speak_text(f'Super {self.handler.user.name}! Das Ergebnis ist {guessSolution}, das stimmt. Weiter so!')
                    if level == 0:
                        getNum1 = random.randint(0, 5)
                        getNum2 = random.randint(0, 5)
                        guessSolution = getNum1 + getNum2
                        displayCalc = f'{getNum1} + {getNum2} ='
                    elif level == 1:
                        getNum1 = random.randint(0, 10)
                        getNum2 = random.randint(0, (10-getNum1))
                        guessSolution = getNum1 + getNum2
                        displayCalc = f'{getNum1} + {getNum2} ='
                    elif level >=2:
                        chooseArithmetic = random.randint(0, 1)
                        if chooseArithmetic:
                            getNum1 = random.randint(0, (5*level))
                            getNum2 = random.randint(0, getNum1)
                            guessSolution = getNum1 - getNum2
                            displayCalc = f'{getNum1} - {getNum2} ='
                        else:
                            getNum1 = random.randint(0, (5*level))
                            getNum2 = random.randint(0, (5*level))
                            guessSolution = getNum1 + getNum2
                            displayCalc = f'{getNum1} + {getNum2} ='
                    print(displayCalc)
                    self.handler.imagePlayer.setTextImage(displayCalc)
                    continue
                elif any(x in self.handler.result for x in ("ende", "abbrechen", "stop")):
                    self.handler.result = ""
                    self.speak_text("Möchtest du das Spiel wirklich beenden?")
                    while(1):
                        self.handler.result = self.listen()
                        if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                            self.handler.result = ""
                            beendeSpiel = 0
                            self.speak_text("Beenden...")
                            break
                        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                            self.handler.result = ""
                            self.speak_text("Das Spiel geht weiter.")
                            self.handler.imagePlayer.setTextImage(displayCalc)
                            break
                        else:
                            self.handler.result = ""
                            self.speak_text("Ich habe dich leider nicht verstanden. Sicher, dass du das Spiel beenden willst?")
                elif any(x in self.handler.result for x in ("weiß", "keine")) and any(x in self.handler.result for x in ("nicht", "ahnung", "plan", "lust")):
                    self.handler.result = ""
                    self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, was das Ergebnis ist.")
                elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                    self.handler.result = ""
                    beendeSpiel -= 1
                    self.speak_text(f'Das Ergebnis war {guessSolution}. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.')
                    if level == 0:
                        getNum1 = random.randint(0, 5)
                        getNum2 = random.randint(0, 5)
                        guessSolution = getNum1 + getNum2
                        displayCalc = f'{getNum1} + {getNum2} ='
                    elif level == 1:
                        getNum1 = random.randint(0, 10)
                        getNum2 = random.randint(0, (10-getNum1))
                        guessSolution = getNum1 + getNum2
                        displayCalc = f'{getNum1} + {getNum2} ='
                    elif level >=2:
                        chooseArithmetic = random.randint(0, 1)
                        if chooseArithmetic:
                            getNum1 = random.randint(0, (5*level))
                            getNum2 = random.randint(0, getNum1)
                            guessSolution = getNum1 - getNum2
                            displayCalc = f'{getNum1} - {getNum2} ='
                        else:
                            getNum1 = random.randint(0, (5*level))
                            getNum2 = random.randint(0, (5*level))
                            guessSolution = getNum1 + getNum2
                            displayCalc = f'{getNum1} + {getNum2} ='
                    print(displayCalc)
                    self.handler.imagePlayer.setTextImage(displayCalc)
                else:
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir das Ergebnis verrate.')
                    self.handler.result = ""

            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du bist ein Rechengenie!.')
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Du kannst mit jedem Spiel mehr.')
            print("Spiel vorbei")
            self.handler.user.numberGame += correctAnswers
            self.speak_text(f'Das Spiel ist zu Ende. Was möchtest du gerne machen?')
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("multi", "meister", "einmal")):
        ################################################ SPIEL - Einmaleins Meister ################################################
            self.speak_text("Los geht's mit Einmaleins Meister.")
            correctAnswers = 0
            beendeSpiel = 5
            level = self.handler.user.multGame//5
            if level <= 5:
                getNum1 = random.randint(1, level + 1)
                getNum2 = random.randint(1, 10)
                guessSolution = getNum1 * getNum2
                displayCalc = f'{getNum1} x {getNum2} ='
            elif level > 5:
                chooseArithmetic = random.randint(0, 1)
                if chooseArithmetic:
                    getNum2 = random.randint(1, level + 1)
                    tempNum = random.randint(1, 10)
                    getNum1 = tempNum * getNum2
                    guessSolution = tempNum
                    displayCalc = f'{getNum1} : {getNum2} ='
                else:
                    getNum1 = random.randint(1, level + 1)
                    getNum2 = random.randint(1, level + 1)
                    guessSolution = getNum1 * getNum2
                    displayCalc = f'{getNum1} x {getNum2} ='
            self.handler.imagePlayer.setTextImage(displayCalc)
            print(displayCalc)
            while(beendeSpiel):
                self.speak_text("Was ist das Ergebnis der angezeigten Rechnung?")
                self.handler.result = self.listen(showPictures=False)
                if str(guessSolution) in alpha2digit(self.handler.result, "de"):
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    self.speak_text(f'Super {self.handler.user.name}! Das Ergebnis ist {guessSolution}, das stimmt. Weiter so!')
                    if level <= 5:
                        getNum1 = random.randint(1, level + 1)
                        getNum2 = random.randint(1, 10)
                        guessSolution = getNum1 * getNum2
                        displayCalc = f'{getNum1} x {getNum2} ='
                    elif level > 5:
                        chooseArithmetic = random.randint(0, 1)
                        if chooseArithmetic:
                            getNum2 = random.randint(1, level + 1)
                            tempNum = random.randint(1, 10)
                            getNum1 = tempNum * getNum2
                            guessSolution = tempNum
                            displayCalc = f'{getNum1} : {getNum2} ='
                        else:
                            getNum1 = random.randint(1, level + 1)
                            getNum2 = random.randint(1, level + 1)
                            guessSolution = getNum1 * getNum2
                            displayCalc = f'{getNum1} x {getNum2} ='
                    print(displayCalc)
                    self.handler.imagePlayer.setTextImage(displayCalc)
                    continue
                elif any(x in self.handler.result for x in ("ende", "abbrechen", "stop")):
                    self.handler.result = ""
                    self.speak_text("Möchtest du das Spiel wirklich beenden?")
                    while(1):
                        self.handler.result = self.listen()
                        if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                            self.handler.result = ""
                            beendeSpiel = 0
                            self.speak_text("Beenden...")
                            break
                        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                            self.handler.result = ""
                            self.speak_text("Das Spiel geht weiter.")
                            self.handler.imagePlayer.setTextImage(displayCalc)
                            break
                        else:
                            self.handler.result = ""
                            self.speak_text("Ich habe dich leider nicht verstanden. Sicher, dass du das Spiel beenden willst?")
                elif any(x in self.handler.result for x in ("weiß", "keine")) and any(x in self.handler.result for x in ("nicht", "ahnung", "plan", "lust")):
                    self.handler.result = ""
                    self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, was das Ergebnis ist.")
                elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                    self.handler.result = ""
                    beendeSpiel -= 1
                    self.speak_text(f'Das Ergebnis war {guessSolution}. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.')
                    if level <= 5:
                        getNum1 = random.randint(1, level + 1)
                        getNum2 = random.randint(1, 10)
                        guessSolution = getNum1 * getNum2
                        displayCalc = f'{getNum1} x {getNum2} ='
                    elif level > 5:
                        chooseArithmetic = random.randint(0, 1)
                        if chooseArithmetic:
                            getNum2 = random.randint(1, level + 1)
                            tempNum = random.randint(1, 10)
                            getNum1 = tempNum * getNum2
                            guessSolution = tempNum
                            displayCalc = f'{getNum1} : {getNum2} ='
                        else:
                            getNum1 = random.randint(1, level + 1)
                            getNum2 = random.randint(1, level + 1)
                            guessSolution = getNum1 * getNum2
                            displayCalc = f'{getNum1} x {getNum2} ='
                    print(displayCalc)
                    self.handler.imagePlayer.setTextImage(displayCalc)
                else:
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir das Ergebnis verrate.')
                    self.handler.result = ""

            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du bist ein Rechengenie!.')
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Du kannst mit jedem Spiel mehr.')
            print("Spiel vorbei")
            self.handler.user.numberGame += correctAnswers
            self.speak_text(f'Das Spiel ist zu Ende. Was möchtest du gerne machen?')
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
            self.handler.result = ""
            self.speak_text(f'Die Spielauswahl wurde abgebrochen. Was möchtest du gerne machen?')
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
                    self.speak_text("Ich habe dich leider nicht verstanden. Soll ich dir auflisten, welche Lernspiele ich kenne?")
            self.speak_text("Welches Lernspiel möchtest du denn gerne spielen?")