from speechLoops.speechLoop import SpeechLoop

class PersonalizeLoop(SpeechLoop):

    def __init__(self, handler):
        super().__init__(handler)

    def play(self) -> None:
        ################################################ KENNENLERNEN - NAME ################################################
        # Name? -> String -> Richtig/Falsch; alt: "Sag ich nicht"
        
        #self.speak_text("Hallo, ich bin dein magischer Märchenspiegel. Ich kann dir die Zeit sagen, das Wetter vorhersagen, dir eine Geschichte vorlesen und vieles mehr."\
        #                "Zuerst möchte ich dich ein wenig kennenlernen."\
        #                "Wie heißt du denn?")
        self.speak_text("Sag Name")
        while(1):
            tempName = self.listen()
            self.speak_text(f'Habe ich dich richtig verstanden? Du heißt also {tempName}')
            self.handler.result = self.listen()
            if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                self.handler.user.name = tempName
                self.speak_text(f'Hallo {self.handler.user.name}, es freut mich dich kennenzulernen!')
                break
            elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.speak_text("Tut mir leid. Wie heißt du denn?")
            elif ("Sag ich nicht" in self.handler.result):
                self.speak_text("Das finde ich aber schade. Dann nenn mir einfach einen Spitznamen mit dem ich dich ansprechen kann.")
            else:
                self.speak_text("Ich habe dich leider nicht verstanden. Wie heißt du? Du kannst mir auch nur einen Spitznamen nennen mit dem ich dich ansprechen kann.")
        
        ################################################ KENNENLERNEN - ALTER ################################################
        # Alter? -> Zahl -> Richtig/Falsch; alt: "Sag ich nicht"
        
        self.speak_text("Sag mal, wie alt bist du denn eigentlich?")

        while(1):
            tempAge = self.listen()
            if not tempAge.isdecimal():
                self.speak_text(f'Du bist {tempAge} Jahre, stimmt das?')
                self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                    self.handler.user.age = tempAge
                    self.speak_text("Du bist ja schon richtig groß.")
                    break
                elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                    self.speak_text("Tut mir leid. Wie alt bist du denn?")
            elif ("Sag ich nicht" in tempAge):
                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal dein Alter.")
                break 
            else:
                self.speak_text("Ich habe dich leider nicht verstanden. Wie alt bist du? Wenn du mir das nicht verraten möchtest, sag einfach: Sag ich nicht.")

        
        ################################################ KENNENLERNEN - Lieblingsfarbe ################################################
        # Lieblingsfarbe? -> Zahl -> Richtig/Falsch; alt: "Sag ich nicht"

        self.speak_text(f'Und was ist deine Lieblingsfarbe {self.handler.user.name}?')

        while(1):
            tempLieblingsfarbe = self.listen()
            self.speak_text(f'Ist es richtig, dass {tempLieblingsfarbe} deine Lieblingsfarbe ist?')
            self.handler.result = self.listen()
            if any(x in self.handler.result for x in ("ja", "genau", "richtig")):
                self.handler.user.color = tempLieblingsfarbe
                self.speak_text("Die Farbe finde ich auch total schön.")
                break
            elif any(x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.speak_text("Tut mir leid. Was ist denn deine Lieblingsfarbe?")
            elif ("Sag ich nicht" in self.handler.result):
                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal deine Lieblingsfarbe.")
                break 
            else:
                self.speak_text("Ich habe dich leider nicht verstanden. Was ist deine Lieblingsfarbe?")

        self.speak_text("Dann weiß ich jetzt die wichtigsten Sachen über dich. Viel Spaß!")
        self.speak_text("Um mit mir zu sprechen, sag einfach: Hallo Spiegel oder trete vor mich.")
