from speechLoops.speechLoop import SpeechLoop
from text_to_num import alpha2digit

watchListSkip = ["weiter", "überspringen"]
watchListConfirmation = ["ja", "genau", "richtig", "nein", "nö", "falsch"]
watchListConfirmationExt = ["ja", "genau", "richtig", "klar", "sicher", "nein", "nö", "falsch", "nicht"]
watchListSpiegel = ["egal", "abbrechen", "stop", "ja", "genau", "richtig", "vielleicht", "eventuell", "nein", "falsch", "nö", "lösung", "sag es mir", "ergebnis", "schneewittchen", "sieben zwerg", "7 zwerg"]
watchListMenu = ["zeit", "uhr", "wetter", "temp", "regen", "kalt", "warm", "heiß", "erzähl", "geschichte", "märchen", "spiel", "lern", "wer", "schönst", "weiter", "überspringen"]

class PersonalizeLoop(SpeechLoop):
    """SpeechLoop for user personalization."""

    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        ################################################ KENNENLERNEN - NAME ################################################
        # Name? -> String -> Richtig/Falsch; alt: "Sag ich nicht"
        
        self.speak_text("Hallo, ich bin dein magischer Märchenspiegel. Ich kann dir eine Geschichte vorlesen, mit dir Lernspiele spielen, das Wetter vorhersagen, dir die Zeit oder das Datum sagen und herausfinden, wer am schönsten in diesem Land ist."\
                        "Um mit mir zu sprechen, sag einfach: Hallo Spiegel, Spieglein, Spieglein oder trete vor mich." \
                        "Zuerst möchte ich dich ein wenig kennenlernen.", watchListSkip)
        self.speak_text("Wie heißt du denn?", watchListSkip)
        while(1):
            #self.handler.result = self.listen()
            self.handler.result = "stefanie"
            print(f'result ist: {self.handler.result}')
            tempName = self.handler.result
            if not self.handler.result:
                print("no result")
                return
            self.handler.result = ""
            if ("Sag ich nicht" in tempName):
                print("sag ich nicht?")
                self.handler.result = ""
                self.speak_text("Das finde ich aber schade. Dann nenn mir einfach einen Spitznamen mit dem ich dich ansprechen kann.", watchListSkip)
                tempName = self.listen()
            print("bestätige name")
            self.speak_text("Habe ich dich richtig verstanden?")
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
                self.speak_text("Tut mir leid. Wie heißt du denn?", watchListSkip)
            else:
                self.handler.result = ""
                self.speak_text("Ich habe dich leider nicht verstanden. Wie heißt du? Du kannst mir auch nur einen Spitznamen nennen mit dem ich dich ansprechen kann.", watchListSkip)
        
        # ################################################ KENNENLERNEN - ALTER ################################################
        # Alter? -> Zahl -> Richtig/Falsch; alt: "Sag ich nicht"
        
        self.speak_text("Sag mal, wie alt bist du denn eigentlich?", watchListSkip)

        while(1):
            self.handler.result = self.listen()
            if not self.handler.result:
                return
            checkStringForNum = alpha2digit(self.handler.result, "de")
            if any(word.isdigit() for word in checkStringForNum.split()):
                tempAge = ""
                for word in checkStringForNum.split():
                    if word.isdigit():
                        tempAge = word
                        break
                self.handler.result = ""
                self.speak_text(f'Du bist also {tempAge} Jahre, stimmt das?', watchListConfirmation)
                if self.handler.result == "":
                    self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                    self.handler.result = ""
                    self.handler.user.age = int(tempAge)
                    self.speak_text("Du bist ja schon richtig groß.")
                    break
                elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                    self.handler.result = ""
                    self.speak_text("Tut mir leid. Wie alt bist du denn?", watchListSkip)
            elif ("Sag ich nicht" in self.handler.result):
                self.handler.result = ""
                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal dein Alter.", watchListSkip)
                break 
            else:
                self.handler.result = ""
                self.speak_text("Ich habe dich leider nicht verstanden. Wie alt bist du?", watchListSkip)

        # ################################################ KENNENLERNEN - ALTER ################################################
        # Schule? -> Richtig/Falsch; alt: "Sag ich nicht"
        
        self.speak_text("Gehst du denn schon zur Schule?", watchListConfirmationExt)

        while(1):
            if self.handler.result == "":
                self.handler.result = self.listen()
            if not self.handler.result:
                return
            if any(x in self.handler.result for x in ("ja", "genau", "richtig", "klar", "sicher")):
                self.handler.result = ""
                self.handler.user.school = True
                self.speak_text(f'Ich bin beeindruckt, dann hast du bestimmt schon richtig viel gelernt. Vielleicht kann ich dir mit meinen Lernspielen mal helfen.', watchListSkip)
                break
            elif any(x in self.handler.result for x in ("nein", "falsch", "nö", "nicht")):
                self.handler.result = ""
                self.speak_text(f'Dann gehst du also noch in den Kindergarten?', watchListConfirmationExt)
                if self.handler.result == "":
                    self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("ja", "genau", "richtig", "klar", "sicher")):
                    self.handler.result = ""
                    self.speak_text("Im Kindergarten lernst du auch schon viele tolle Sachen und hast bestimmt auch ganz liebe Freunde.", watchListSkip)
                    break
                elif any(x in self.handler.result for x in ("nein", "falsch", "nö", "nicht")):
                    self.handler.result = ""
                    self.speak_text(f'Dann gehst du also doch zur Schule?', watchListConfirmationExt)
                    if self.handler.result == "":
                        self.handler.result = self.listen()
            elif ("Sag ich nicht" in self.handler.result):
                self.handler.result = ""
                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir das nächstes Mal.", watchListSkip)
                break 
            else:
                self.handler.result = ""
                self.speak_text("Ich habe dich leider nicht verstanden. Gehst du schon zur Schule?", watchListConfirmationExt)

        # ################################################ KENNENLERNEN - Lieblingsfarbe ################################################
        # # Lieblingsfarbe? -> Zahl -> Richtig/Falsch; alt: "Sag ich nicht"

        self.speak_text(f'Und was ist deine Lieblingsfarbe {self.handler.user.name}?', watchListSkip)

        while(1):
            self.handler.result = self.listen()
            tempLieblingsfarbe = self.handler.result
            if not self.handler.result:
                return
            self.handler.result = ""
            if ("Sag ich nicht" in tempLieblingsfarbe):
                self.handler.result = ""
                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal deine Lieblingsfarbe.", watchListSkip)
                break
            self.speak_text(f'Ist es richtig, dass {tempLieblingsfarbe} deine Lieblingsfarbe ist?', watchListConfirmation)
            if self.handler.result == "":
                self.handler.result = self.listen()
            if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                self.handler.result = ""
                self.handler.user.color = tempLieblingsfarbe
                self.speak_text("Die Farbe finde ich auch total schön.")
                break
            elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.handler.result = ""
                self.speak_text("Tut mir leid. Was ist denn deine Lieblingsfarbe?", watchListSkip)
            else:
                self.handler.result = ""
                self.speak_text("Ich habe dich leider nicht verstanden. Was ist deine Lieblingsfarbe?", watchListSkip)

        self.speak_text("Dann weiß ich jetzt die wichtigsten Sachen über dich.", watchListSkip)

################################################ VORSTELLUNG - Spiegel ################################################
        self.speak_text("Weißt du eigentlich aus welchem Märchen du mich kennst?", watchListSpiegel)

        while(1):
            if self.handler.result == "":
                self.handler.result = self.listen()
            if not self.handler.result:
                return
            if any(x in self.handler.result for x in ("egal", "abbrechen", "stop")):
                self.handler.result = ""
                self.speak_text(f'Ich verrate es dir trotzdem, ich stamme aus Schneewittchen und die sieben Zwerge. Und jetzt wünsche ich dir viel Spaß {self.handler.user.name}! Was möchtest du machen?', watchListMenu)
                break
            elif any(x in self.handler.result for x in ("ja", "genau", "richtig", "vielleicht", "eventuell")):
                self.handler.result = ""
                self.speak_text("Aus welchem Märchen denkst du, kennst du mich?", watchListSpiegel)
                if self.handler.result == "":
                    self.handler.result = self.listen()
            elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.handler.result = ""
                self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, welches Märchen es ist.", watchListSpiegel)
                if self.handler.result == "":
                    self.handler.result = self.listen()
            elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                self.handler.result = ""
                self.speak_text(f'Ich stamme aus Schneewittchen und die sieben Zwerge. Wenn du das Märchen hören möchtest, dann sag Märchen. Ansonsten viel Spaß {self.handler.user.name}! Was möchtest du jetzt machen?', watchListMenu)
                break
            if any(x in self.handler.result for x in ("schneewittchen", "sieben zwerg", "7 zwerg")):
                self.handler.result = ""
                self.speak_text(f'Richtig, das hast du super erraten {self.handler.user.name}. Ich stamme aus Schneewittchen und die sieben Zwerge. Wenn du das Märchen mal von mir hören möchtest, dann sag Märchen. Ansonsten viel Spaß! Was möchtest du jetzt machen?', watchListMenu)
                break
            else:
                tempVal = self.handler.result
                self.handler.result = ""
                self.speak_text(f'{tempVal} stimmt nicht. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir das Märchen verrate von dem ich stamme.', watchListSpiegel)

        self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
            
