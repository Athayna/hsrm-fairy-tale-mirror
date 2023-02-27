from speechLoops.speechLoop import SpeechLoop
from text_to_num import alpha2digit

class PersonalizeLoop(SpeechLoop):
    """SpeechLoop for user personalization."""

    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        ################################################ KENNENLERNEN - NAME ################################################
        # Name? -> String -> Richtig/Falsch; alt: "Sag ich nicht"
        
        self.speak_text("Hallo, ich bin dein magischer Märchenspiegel. Ich kann dir eine Geschichte vorlesen, das Wetter vorhersagen, dir die Zeit sagen und vieles mehr."\
                        "Um mit mir zu sprechen, sag einfach: Hallo Spiegel oder trete vor mich." \
                        "Zuerst möchte ich dich ein wenig kennenlernen."\
                        "Wie heißt du denn?")
        while(1):
            tempName = self.listen()
            if ("Sag ich nicht" in tempName):
                self.handler.result = ""
                self.speak_text("Das finde ich aber schade. Dann nenn mir einfach einen Spitznamen mit dem ich dich ansprechen kann.")
                tempName = self.listen()
            self.speak_text(f'Habe ich dich richtig verstanden? Du heißt also {tempName}')
            self.handler.result = self.listen()
            if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                self.handler.result = ""
                self.handler.user.name = tempName
                self.speak_text(f'Hallo {self.handler.user.name}, es freut mich dich kennenzulernen!')
                break
            elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.handler.result = ""
                self.speak_text("Tut mir leid. Wie heißt du denn?")
            else:
                self.handler.result = ""
                self.speak_text("Ich habe dich leider nicht verstanden. Wie heißt du? Du kannst mir auch nur einen Spitznamen nennen mit dem ich dich ansprechen kann.")
        
        # ################################################ KENNENLERNEN - ALTER ################################################
        # Alter? -> Zahl -> Richtig/Falsch; alt: "Sag ich nicht"
        
        self.speak_text("Sag mal, wie alt bist du denn eigentlich?")

        while(1):
            self.handler.result = self.listen()
            checkStringForNum = alpha2digit(self.handler.result, "de")
            if any(word.isdigit() for word in checkStringForNum.split()):
                tempAge = ""
                for word in checkStringForNum.split():
                    if word.isdigit():
                        tempAge = word
                        break
                self.handler.result = ""
                self.speak_text(f'Du bist also {tempAge} Jahre, stimmt das?')
                self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                    self.handler.result = ""
                    self.handler.user.age = int(tempAge)
                    self.speak_text("Du bist ja schon richtig groß.")
                    break
                elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                    self.handler.result = ""
                    self.speak_text("Tut mir leid. Wie alt bist du denn?")
            elif ("Sag ich nicht" in tempAge):
                self.handler.result = ""
                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal dein Alter.")
                break 
            else:
                self.handler.result = ""
                self.speak_text("Ich habe dich leider nicht verstanden. Wie alt bist du? Wenn du mir das nicht verraten möchtest, sag einfach: Sag ich nicht.")

        # ################################################ KENNENLERNEN - Lieblingsfarbe ################################################
        # # Lieblingsfarbe? -> Zahl -> Richtig/Falsch; alt: "Sag ich nicht"

        self.speak_text(f'Und was ist deine Lieblingsfarbe {self.handler.user.name}?')

        while(1):
            tempLieblingsfarbe = self.listen()
            if ("Sag ich nicht" in tempLieblingsfarbe):
                self.handler.result = ""
                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal deine Lieblingsfarbe.")
                break
            self.speak_text(f'Ist es richtig, dass {tempLieblingsfarbe} deine Lieblingsfarbe ist?')
            self.handler.result = self.listen()
            if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                self.handler.result = ""
                self.handler.user.color = tempLieblingsfarbe
                self.speak_text("Die Farbe finde ich auch total schön.")
                break
            elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.handler.result = ""
                self.speak_text("Tut mir leid. Was ist denn deine Lieblingsfarbe?")
            else:
                self.handler.result = ""
                self.speak_text("Ich habe dich leider nicht verstanden. Was ist deine Lieblingsfarbe?")

        self.speak_text("Dann weiß ich jetzt die wichtigsten Sachen über dich.")

################################################ VORSTELLUNG - Spiegel ################################################
        self.speak_text("Weißt du eigentlich aus welchem Märchen du mich kennst?")

        while(1):
            self.handler.result = self.listen()
            if any(x in self.handler.result for x in ("egal", "abbrechen", "stop")):
                self.handler.result = ""
                self.speak_text(f'Ich verrate es dir trotzdem, ich stamme aus Schneewittchen und die sieben Zwerge. Und jetzt wünsche ich dir viel Spaß {self.handler.user.name}! Was möchtest du machen?')
                break
            elif any(x in self.handler.result for x in ("ja", "genau", "richtig", "vielleicht", "eventuell")):
                self.handler.result = ""
                self.speak_text("Aus welchem Märchen denkst du, kennst du mich?")
                self.handler.result = self.listen()
            elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.handler.result = ""
                self.speak_text("Dann rate doch einfach mal und ich sage dir, ob es das richtige war oder sag Lösung und ich verrate dir direkt, welches Märchen es ist.")
                self.handler.result = self.listen()
            elif any(x in self.handler.result for x in ("lösung", "sag es mir", "ergebnis")):
                self.handler.result = ""
                self.speak_text(f'Ich stamme aus Schneewittchen und die sieben Zwerge. Wenn du das Märchen hören möchtest, dann sag Märchen. Ansonsten viel Spaß {self.handler.user.name}! Was möchtest du jetzt machen?')
                break
            if any(x in self.handler.result for x in ("schneewittchen", "sieben zwerg", "7 zwerg")):
                self.handler.result = ""
                self.speak_text(f'Richtig, das hast du super erraten {self.handler.user.name}. Ich stamme aus Schneewittchen und die sieben Zwerge. Wenn du das Märchen mal von mir hören möchtest, dann sag Märchen. Ansonsten viel Spaß! Was möchtest du jetzt machen?')
                break
            else:
                self.speak_text(f'{self.handler.result} stimmt nicht. Entweder du rätst nochmal oder du sagst Lösung, damit ich dir das Märchen verrate von dem ich stamme.')
                self.handler.result = ""
            
