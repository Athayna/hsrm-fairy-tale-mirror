import random
from speechLoops.speechLoop import SpeechLoop
from text_to_num import alpha2digit

watchListWords = ["wort", "abc", "künste", "zahl", "zauber", "einmaleins", "meister", "tiktak", "uhr", "weiter", "überspringen"]
watchListWordsGame = ["ende", "abbrechen", "stop", "weiter", "überspringen"]
watchListWordsGameSol= ["lösung", "ende", "abbrechen", "stop", "weiter", "überspringen"]
watchListConfirmation = ["ja", "genau", "gern", "ok", "klar", "nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen"]
watchListMenu = ["zeit", "uhr", "wetter", "temp", "regen", "kalt", "warm", "heiß", "erzähl", "geschichte", "märchen", "spiel", "lern", "wer", "schönst"]


class GameLoop(SpeechLoop):
    """SpeechLoop for the game mode."""
    
    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        
        if self.handler.result == "":
            self.handler.result = self.listen()

        if not self.handler.result:
            return

        if "wort" in self.handler.result:
        ################################################ SPIEL - Wort für Wort ################################################
            self.handler.result = ""
            self.speak_text("Los geht's mit Wort für Wort.")
            wordArray = [["du", "so", "es", "da", "ja"], 
                         ["mit", "Kuh", "war", "rot", "Tal"], 
                         ["Hund", "Mund", "klug", "wenn", "dort"],
                         ["Spiel", "Kugel", "essen", "gehen", "lesen"],
                         ["Frosch", "Brunnen", "schlau", "rennen", "lustig"]]
            level = self.handler.user.wordGame//5
            correctAnswers = 0
            beendeSpiel = 5
            usedArray = wordArray[level].copy()
            getWordNum = random.randint(0, (len(usedArray))-1)
            guessWord = usedArray[getWordNum]
            self.handler.imagePlayer.setTextImage(guessWord)
            print(guessWord)
            while(beendeSpiel):
                if self.handler.result == "":
                    self.speak_text("Wie heißt das angezeigte Wort?")
                    self.handler.result = self.listen(showPictures=False)
                if not self.handler.result:
                    return
                if any(x == guessWord.lower() for x in self.handler.result.split()):
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    usedArray.remove(guessWord)
                    if beendeSpiel:
                        self.speak_text(f'Super {self.handler.user.name}! Da steht {guessWord}, das stimmt. Weiter so!', watchListWordsGame)
                        getWordNum = random.randint(0, (len(usedArray))-1)
                        guessWord = usedArray[getWordNum]
                        self.handler.imagePlayer.setTextImage(guessWord)
                    print(guessWord)
                    continue
                elif any(x in self.handler.result for x in ("ende", "abbrechen", "stop")):
                    self.handler.result = ""
                    self.speak_text("Möchtest du das Spiel wirklich beenden?", watchListConfirmation)
                    while(1):
                        if self.handler.result == "":
                            self.handler.result = self.listen()
                        if not self.handler.result:
                            return
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
                            self.speak_text("Ich habe dich leider nicht verstanden. Sicher, dass du das Spiel beenden willst?", watchListConfirmation)
                elif any(x in self.handler.result for x in ("weiß", "keine")) and any(x in self.handler.result for x in ("nicht", "ahnung", "plan", "lust")):
                    self.handler.result = ""
                    self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, welches Wort da steht.", watchListWordsGameSol)
                elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                    self.handler.result = ""
                    beendeSpiel -= 1
                    self.speak_text(f'Da stand {guessWord}. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.', watchListWordsGame)
                    if beendeSpiel:
                        tempWord = guessWord
                        while tempWord == guessWord:
                            getWordNum = random.randint(0, (len(usedArray))-1)
                            guessWord = usedArray[getWordNum]
                        self.handler.imagePlayer.setTextImage(guessWord)
                    print(guessWord)
                else:
                    tempVal = self.handler.result
                    self.handler.result = ""
                    self.speak_text(f'{tempVal} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir das Wort verrate, dass da steht.', watchListWordsGameSol)

            self.handler.imagePlayer.setImage("cat")
            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du bist ein richtiger Profi im Lesen!', ["weiter", "überspringen"])
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Du kannst mit jedem Spiel mehr.', ["weiter", "überspringen"])
            print("Spiel vorbei")
            self.handler.user.wordGame += correctAnswers
            self.speak_text(f'Wenn du nochmal spielen möchtest, musst du Lernspiel sagen. Was möchtest du gerne machen?', watchListMenu)
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("abc", "künste", "alphabet")):
        ################################################ SPIEL - ABC Künste ################################################
            self.handler.result = ""
            self.speak_text("Los geht's mit ABC Künste. Um den Buchstaben zu erraten sag ein davor. Zum Beispiel, wenn da a steht, musst du ein a sagen, sonst verstehe ich dich leider nicht.", ["weiter", "überspringen"])
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
                if self.handler.result == "":
                    self.speak_text("Wie heißt der angezeigte Buchstabe?")
                    self.handler.result = self.listen(showPictures=False)
                if not self.handler.result:
                    return
                if any(x in self.handler.result for x in ("ende", "abbrechen", "stop")):
                    self.handler.result = ""
                    self.speak_text("Möchtest du das Spiel wirklich beenden?", watchListConfirmation)
                    while(1):
                        if self.handler.result == "":
                            self.handler.result = self.listen()
                        if not self.handler.result:
                            return
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
                            self.speak_text("Ich habe dich leider nicht verstanden. Sicher, dass du das Spiel beenden willst?", watchListConfirmation)
                elif any(x in self.handler.result for x in ("weiß", "keine")) and any(x in self.handler.result for x in ("nicht", "ahnung", "plan", "lust")):
                    self.handler.result = ""
                    self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, welcher Buchstabe da steht.", watchListWordsGameSol)
                elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                    self.handler.result = ""
                    beendeSpiel -= 1
                    self.speak_text(f'Das war der Buchstabe {guessAlphabet}. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.', watchListWordsGame)
                    if beendeSpiel:
                        getAlphabetNum = random.randint(0, (len(alphabetArray)*2-1))
                        if getAlphabetNum > 25:
                            guessAlphabet = alphabetArray[getAlphabetNum-26].upper()
                        else:
                            guessAlphabet = alphabetArray[getAlphabetNum]
                        self.handler.imagePlayer.setTextImage(guessAlphabet)
                        print(guessAlphabet)
                elif any(x == "ein" for x in self.handler.result.split()) and guessAlphabet.lower() in self.handler.result:
                    foundLetter = 0
                    for word in self.handler.result.split():
                        if foundLetter:
                            letter = word[0]
                            if letter == guessAlphabet:
                                break
                            elif letter != guessAlphabet:
                                foundLetter = 0
                                break
                        if word == "ein":
                            foundLetter = 1

                #elif "ein" in self.handler.result and guessAlphabet.lower() in self.handler.result:
                    if foundLetter:
                        self.handler.result = ""
                        correctAnswers += 1
                        beendeSpiel -= 1
                        alphabetArray.remove(guessAlphabet.lower())
                        self.speak_text(f'Super {self.handler.user.name}! Da steht {guessAlphabet}, das stimmt. Weiter so!', watchListWordsGame)
                        if beendeSpiel:
                            getAlphabetNum = random.randint(0, (len(alphabetArray)*2-1))
                            if getAlphabetNum > 25:
                                guessAlphabet = alphabetArray[getAlphabetNum-26].upper()
                            else:
                                guessAlphabet = alphabetArray[getAlphabetNum]
                            self.handler.imagePlayer.setTextImage(guessAlphabet)
                            print(guessAlphabet)
                        continue
                    else:  
                        self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir den Buchstaben verrate, der da steht.', watchListWordsGameSol)
                        self.handler.result = ""
                else:
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir den Buchstaben verrate, der da steht.', watchListWordsGameSol)
                    self.handler.result = ""

            self.handler.imagePlayer.setImage("cat")
            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du kennst dein Alphabet bestens! Trau dich gerne mal an das Wort für Wort Spiel.', ["weiter", "überspringen"])
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Bald kannst du das ganze ABC.', ["weiter", "überspringen"])
            print("Spiel vorbei")
            self.speak_text(f'Wenn du nochmal spielen möchtest, musst du Lernspiel sagen. Was möchtest du gerne machen?', watchListMenu)
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))

        elif any(x in self.handler.result for x in ("zahl", "zauber")):
        ################################################ SPIEL - Zahlenzauber ################################################
            self.handler.result = ""
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
                if self.handler.result == "":
                    self.speak_text("Was ist das Ergebnis der angezeigten Rechnung?")
                    self.handler.result = self.listen(showPictures=False)
                if not self.handler.result:
                    return
                if str(guessSolution) in alpha2digit(self.handler.result, "de"):
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    self.speak_text(f'Super {self.handler.user.name}! Das Ergebnis ist {guessSolution}, das stimmt. Weiter so!', watchListWordsGame)
                    if beendeSpiel:
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
                    self.speak_text("Möchtest du das Spiel wirklich beenden?", watchListConfirmation)
                    while(1):
                        if self.handler.result == "":
                            self.handler.result = self.listen()
                        if not self.handler.result:
                            return
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
                            self.speak_text("Ich habe dich leider nicht verstanden. Sicher, dass du das Spiel beenden willst?", watchListConfirmation)
                elif any(x in self.handler.result for x in ("weiß", "keine")) and any(x in self.handler.result for x in ("nicht", "ahnung", "plan", "lust")):
                    self.handler.result = ""
                    self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, was das Ergebnis ist.", watchListWordsGameSol)
                elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                    self.handler.result = ""
                    beendeSpiel -= 1
                    self.speak_text(f'Das Ergebnis war {guessSolution}. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.', watchListWordsGame)
                    if beendeSpiel:
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
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir das Ergebnis verrate.', watchListWordsGameSol)
                    self.handler.result = ""

            self.handler.imagePlayer.setImage("cat")
            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du bist ein Rechengenie!.', ["weiter", "überspringen"])
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Du kannst mit jedem Spiel mehr.', ["weiter", "überspringen"])
            print("Spiel vorbei")
            self.handler.user.numberGame += correctAnswers
            self.speak_text(f'Wenn du nochmal spielen möchtest, musst du Lernspiel sagen. Was möchtest du gerne machen?', watchListMenu)
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("multi", "meister", "einmal")):
        ################################################ SPIEL - Einmaleins Meister ################################################
            self.handler.result = ""
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
                if self.handler.result == "":
                    self.speak_text("Was ist das Ergebnis der angezeigten Rechnung?")
                    self.handler.result = self.listen(showPictures=False)
                if not self.handler.result:
                    return
                if str(guessSolution) in alpha2digit(self.handler.result, "de"):
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    self.speak_text(f'Super {self.handler.user.name}! Das Ergebnis ist {guessSolution}, das stimmt. Weiter so!', watchListWordsGame)
                    if beendeSpiel:
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
                    self.speak_text("Möchtest du das Spiel wirklich beenden?", watchListConfirmation)
                    while(1):
                        if self.handler.result == "":
                            self.handler.result = self.listen()
                        if not self.handler.result:
                            return
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
                            self.speak_text("Ich habe dich leider nicht verstanden. Sicher, dass du das Spiel beenden willst?", watchListConfirmation)
                elif any(x in self.handler.result for x in ("weiß", "keine")) and any(x in self.handler.result for x in ("nicht", "ahnung", "plan", "lust")):
                    self.handler.result = ""
                    self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, was das Ergebnis ist.", watchListWordsGameSol)
                elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                    self.handler.result = ""
                    beendeSpiel -= 1
                    self.speak_text(f'Das Ergebnis war {guessSolution}. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.', watchListWordsGame)
                    if beendeSpiel:
                        print(level)
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
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir das Ergebnis verrate.', watchListWordsGameSol)
                    self.handler.result = ""

            self.handler.imagePlayer.setImage("cat")
            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du bist ein Rechengenie!.', ["weiter", "überspringen"])
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Du kannst mit jedem Spiel mehr.', ["weiter", "überspringen"])
            print("Spiel vorbei")
            self.handler.user.numberGame += correctAnswers
            self.speak_text(f'Wenn du nochmal spielen möchtest, musst du Lernspiel sagen. Was möchtest du gerne machen?', watchListMenu)
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))

        elif any(x in self.handler.result for x in ("tik", "tak", "uhr")):
        ################################################ SPIEL - TikTak Uhrenspaß ################################################
            self.handler.result = ""
            self.speak_text("Los geht's mit TikTak Uhrenspaß.")
            correctAnswers = 0
            beendeSpiel = 5
            level = self.handler.user.numberGame//5
            level = 2
            getTimeHour = 0
            getTimeMinute = 0
            if level == 0:
                getTimeHour = random.randint(1, 12)
            elif level == 1:
                # normally until 12 but pictures only until hour 4 -> getTimeHour = random.randint(1, 12)
                getTimeHour = random.randint(1, 4)
                getTimeMinute = random.randint(0, 3)*15
            elif level >=2:
                getTimeHour = random.randint(1, 12)
                getTimeMinute = random.randint(0, 12)*5                
                # normally all hours with all 5min options but not all pictures included so switch case for available options
                # 5 10 35 40
                interimSolution = getTimeHour//4 + 1
                if interimSolution == 1:
                    getTimeHour = 5
                    getTimeMinute = 10
                elif interimSolution == 2:
                    getTimeHour = 8
                    getTimeMinute = 5
                elif interimSolution == 3:
                    getTimeHour = 5
                    getTimeMinute = 35
                elif interimSolution == 4:
                    getTimeHour = 8
                    getTimeMinute = 40
            if getTimeMinute:
                self.handler.imagePlayer.setTimeImage(f'{getTimeHour}{getTimeMinute}')
            else:
                self.handler.imagePlayer.setTimeImage(getTimeHour)
            print(f'{getTimeHour}{getTimeMinute}')
            while(beendeSpiel):
                if self.handler.result == "":
                    self.speak_text("Welche Uhrzeit wird hier angezeigt?")
                    self.handler.result = self.listen(showPictures=False)
                if not self.handler.result:
                    return
                if getTimeMinute == 0:
                    self.handler.result += " 0"
                if str(getTimeHour) in alpha2digit(self.handler.result, "de") and (str(getTimeMinute) in alpha2digit(self.handler.result, "de") or getTimeMinute == 15 and "viertel nach" in self.handler.result or getTimeMinute == 30 and "halb" in self.handler.result or getTimeMinute == 45 and "viertel vor" in self.handler.result):
                    self.handler.result = ""
                    correctAnswers += 1
                    beendeSpiel -= 1
                    if getTimeMinute:
                        if getTimeMinute == 15:
                            self.speak_text(f'Super {self.handler.user.name}! Die Uhr zeigt {getTimeHour} Uhr {getTimeMinute}, auch viertel nach {getTimeHour} genannt, das stimmt. Weiter so!', watchListWordsGame)
                        elif getTimeMinute == 30:
                            self.speak_text(f'Super {self.handler.user.name}! Die Uhr zeigt {getTimeHour} Uhr {getTimeMinute}, auch halb {getTimeHour} genannt, das stimmt. Weiter so!', watchListWordsGame)
                        elif getTimeMinute == 45:
                            self.speak_text(f'Super {self.handler.user.name}! Die Uhr zeigt {getTimeHour} Uhr {getTimeMinute}, auch viertel vor {getTimeHour+1} genannt, das stimmt. Weiter so!', watchListWordsGame)
                        else:
                            self.speak_text(f'Super {self.handler.user.name}! Die Uhr zeigt {getTimeHour} Uhr {getTimeMinute}, das stimmt. Weiter so!', watchListWordsGame)
                    else:
                        self.speak_text(f'Super {self.handler.user.name}! Die Uhr zeigt {getTimeHour} Uhr, das stimmt. Weiter so!', watchListWordsGame)

                    if beendeSpiel:
                        if level == 0:
                            getTimeHour = random.randint(1, 12)
                        elif level == 1:
                            # normally until 12 but pictures only until hour 4 -> getTimeHour = random.randint(1, 12)
                            getTimeHour = random.randint(1, 4)
                            getTimeMinute = random.randint(0, 3)*15
                        elif level >=2:
                            getTimeHour = random.randint(1, 12)
                            getTimeMinute = random.randint(0, 12)*5                
                            # normally all hours with all 5min options but not all pictures included so switch case for available options
                            # 5 10 35 40
                            interimSolution = getTimeHour//4 + 1
                            if interimSolution == 1:
                                getTimeHour = 5
                                getTimeMinute = 10
                            elif interimSolution == 2:
                                getTimeHour = 8
                                getTimeMinute = 5
                            elif interimSolution == 3:
                                getTimeHour = 5
                                getTimeMinute = 35
                            elif interimSolution == 4:
                                getTimeHour = 8
                                getTimeMinute = 40
                        if getTimeMinute:
                            self.handler.imagePlayer.setTimeImage(f'{getTimeHour}{getTimeMinute}')
                        else:
                            self.handler.imagePlayer.setTimeImage(getTimeHour)
                    continue
                elif any(x in self.handler.result for x in ("ende", "abbrechen", "stop")):
                    self.handler.result = ""
                    self.speak_text("Möchtest du das Spiel wirklich beenden?", watchListConfirmation)
                    while(1):
                        if self.handler.result == "":
                            self.handler.result = self.listen()
                        if not self.handler.result:
                            return
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
                            self.speak_text("Ich habe dich leider nicht verstanden. Sicher, dass du das Spiel beenden willst?", watchListConfirmation)
                elif any(x in self.handler.result for x in ("weiß", "keine")) and any(x in self.handler.result for x in ("nicht", "ahnung", "plan", "lust")):
                    self.handler.result = ""
                    self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, was das Ergebnis ist.", watchListWordsGameSol)
                elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                    self.handler.result = ""
                    beendeSpiel -= 1
                    if getTimeMinute:
                        if getTimeMinute == 15:
                            self.speak_text(f'Die Uhr zeigt {getTimeHour} Uhr {getTimeMinute}, auch viertel nach {getTimeHour} genannt. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.', watchListWordsGame)
                        elif getTimeMinute == 30:
                            self.speak_text(f'Die Uhr zeigt {getTimeHour} Uhr {getTimeMinute}, auch halb {getTimeHour} genannt. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.', watchListWordsGame)
                        elif getTimeMinute == 45:
                            self.speak_text(f'Die Uhr zeigt {getTimeHour} Uhr {getTimeMinute}, auch viertel vor {getTimeHour+1} genannt. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.', watchListWordsGame)
                        else:
                            self.speak_text(f'Die Uhr zeigt {getTimeHour} Uhr {getTimeMinute}. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.', watchListWordsGame)
                    else:
                        self.speak_text(f'Die Uhr zeigt {getTimeHour} Uhr. Versuch es immer weiter {self.handler.user.name}, du wirst immer besser je mehr du übst.', watchListWordsGame)

                    if beendeSpiel:
                        if level == 0:
                            getTimeHour = random.randint(1, 12)
                        elif level == 1:
                            # normally until 12 but pictures only until hour 4 -> getTimeHour = random.randint(1, 12)
                            getTimeHour = random.randint(1, 4)
                            getTimeMinute = random.randint(0, 3)*15
                        elif level >=2:
                            getTimeHour = random.randint(1, 12)
                            getTimeMinute = random.randint(0, 12)*5                
                            # normally all hours with all 5min options but not all pictures included so switch case for available options
                            # 5 10 35 40
                            interimSolution = getTimeHour//4 + 1
                            if interimSolution == 1:
                                getTimeHour = 5
                                getTimeMinute = 10
                            elif interimSolution == 2:
                                getTimeHour = 8
                                getTimeMinute = 5
                            elif interimSolution == 3:
                                getTimeHour = 5
                                getTimeMinute = 35
                            elif interimSolution == 4:
                                getTimeHour = 8
                                getTimeMinute = 40
                        if getTimeMinute:
                            self.handler.imagePlayer.setTimeImage(f'{getTimeHour}{getTimeMinute}')
                        else:
                            self.handler.imagePlayer.setTimeImage(getTimeHour)
                else:
                    self.speak_text(f'{self.handler.result} ist falsch. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir die Uhrzeit verrate.', watchListWordsGameSol)
                    self.handler.result = ""

            self.handler.imagePlayer.setImage("cat")
            if correctAnswers >= 4:
                self.speak_text(f'Wahnsinn {self.handler.user.name}, du kennst deine Zeit!.', ["weiter", "überspringen"])
            elif correctAnswers < 4:
                self.speak_text(f'Immer weiter so {self.handler.user.name}. Du kannst mit jedem Spiel mehr.', ["weiter", "überspringen"])
            print("Spiel vorbei")
            self.handler.user.numberGame += correctAnswers
            self.speak_text(f'Wenn du nochmal spielen möchtest, musst du Lernspiel sagen. Was möchtest du gerne machen?', watchListMenu)
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
        
        elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
            self.handler.result = ""
            self.speak_text(f'Die Spielauswahl wurde abgebrochen. Was möchtest du gerne machen?', watchListMenu)
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
              
        else:
            self.handler.result = ""
            self.speak_text("Dieses Lernspiel kenne ich leider nicht. Möchtest du wissen, welche Lernspiele ich kenne?", watchListConfirmation)
            while(1):
                if self.handler.result == "":
                    self.handler.result = self.listen()
                if not self.handler.result:
                    return
                print(self.handler.result)
                if any(x in self.handler.result for x in ("ja", "genau", "gern", "ok", "klar")):
                    self.handler.result = ""
                    self.speak_text("Ich kenne Wort für Wort, ABC Künste, Zahlenzauber, Einmaleins Meister und Tiktak Uhrenspaß.", watchListWords)
                    break
                elif any(x in self.handler.result for x in ("nein", "nicht", "nö", "kein", "stop", "ende", "abbrechen")):
                    self.handler.result = ""
                    break
                else:
                    self.handler.result = ""
                    self.speak_text("Ich habe dich leider nicht verstanden. Soll ich dir auflisten, welche Lernspiele ich kenne?", watchListConfirmation)
            
            if self.handler.result == "":
                self.speak_text("Welches Lernspiel möchtest du denn gerne spielen?", watchListWords)