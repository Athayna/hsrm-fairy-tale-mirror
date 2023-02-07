from handler import Handler
from speechLoop import SpeechLoop
import datetime

class FirstTimeLoop(SpeechLoop):

    def __init__(self, handler: Handler):
        super().__init__(handler)

    def play(self) -> None:
        self.speak_text("Hallo, ich bin dein magischer Märchenspiegel. Ich kann dir die Zeit sagen, das Wetter vorhersagen, dir eine Geschichte vorlesen und vieles mehr."\
                        "Zuerst möchte ich dich ein wenig kennenlernen."\
                        "Wie heißt du denn?")

        # Name -> Geburtsdatum -> Wenn Nein: Alter? -> Monat? - Tag?
        while(1):
            self.handler.result = self.listen()
            self.handler.user.name = self.handler.result
            self.speak_text("Habe ich dich richtig verstanden? Du heißt also {0}".format(self.handler.user.name))
            self.handler.result = self.listen()
            if (x in self.handler.result for x in ("ja", "genau", "richtig")):
                self.speak_text("Hallo {0}, es freut mich dich kennenzulernen!".format(self.handler.user.name))
                break
            elif (x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.speak_text("Tut mir leid. Wie heißt du denn?")
            elif ("Sag ich nicht" in self.handler.result):
                self.handler.user.name = ""
                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal deinen Namen.")
                break
            else:
                self.speak_text("Ich habe dich leider nicht verstanden. Wie heißt du? Wenn du mir das nicht verraten möchtest, sag einfach: Sag ich nicht.")
        
        self.speak_text("Dann fehlt noch dein Geburtstag. Wenn du mir das verrätst, kann ich dir auch gratulieren. Möchtest du das?")
        self.handler.result = self.listen()
        while(1):
            if ("ja" in self.handler.result):
                self.speak_text("Da bin ich gespannt. In welchem Monat hast du Geburtstag?")
                while(1):
                    self.handler.result = self.listen()
                    self.speak_text("Du hast im {0} Geburtstag?".format(self.handler.result))
                    if (x in self.handler.result for x in ("ja", "genau", "richtig")):
                        self.handler.user.birthday = self.handler.result
                        self.speak_text("Das ist ein richtig schöner Monat. Und an welchem Tag hast du Geburtstag?")
                        while(1):
                            self.handler.result = self.listen()
                            self.speak_text("Du hast am {0} Geburtstag?".format(self.handler.result))
                            if (x in self.handler.result for x in ("ja", "genau", "richtig")):
                                self.handler.user.birthday = self.handler.result + "." + self.handler.user.birthday + "."
                                self.handler.user.birthday += datetime.datetime.now().year + int(self.handler.user.age)
                                self.speak_text("So ein schönes Datum. Ich freue mich schon dir zu gratulieren!")
                                break
                            elif (x in self.handler.result for x in ("nein", "falsch", "nö")):
                                self.speak_text("Tut mir leid. An welchem Tag hast du denn Geburtstag?")
                            elif ("Sag ich nicht" in self.handler.result):
                                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal deinen Geburtstag.")
                                break
                            else:
                                self.speak_text("Ich habe dich leider nicht verstanden. An welchem Tag hast du denn Geburtstag?")
                        break
                    elif (x in self.handler.result for x in ("nein", "falsch", "nö")):
                        self.speak_text("Tut mir leid. In welchem Monat hast du denn Geburtstag?")
                    elif ("Sag ich nicht" in self.handler.result):
                        self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal deinen Geburtstag.")
                        break
                    else:
                        self.speak_text("Ich habe dich leider nicht verstanden. In welchem Monat hast du denn Geburtstag?")
            elif (x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.speak_text("Das hätte ich gerne macht, wie schade. Vielleicht sagst du mir nächstes Mal, wann du Geburtstag hast.")
                break
            else:
                self.speak_text("Ich habe dich leider nicht verstanden. Möchtest du, dass ich dir zum Geburtstag gratuliere?")
        
        self.speak_text("Magst du mir auch sagen, wie alt du bist?")
        while(1):
            self.handler.result = self.listen()
            self.handler.user.age = self.handler.result
            if (x in self.handler.result for x in ("ja", "genau", "richtig")):
                self.speak_text("Wie alt bist du denn?")
                self.handler.result = self.listen()
                while(1):
                    self.handler.user.age = self.handler.result
                    self.speak_text("Du bist {0} Jahre?".format(self.handler.user.age))
                    self.handler.result = self.listen()
                    if (x in self.handler.result for x in ("ja", "genau", "richtig")):
                        self.speak_text("Du bist ja schon richtig groß.")
                        break
                    elif (x in self.handler.result for x in ("nein", "falsch", "nö")):
                        self.speak_text("Tut mir leid. Wie alt bist du denn?")
                    elif ("Sag ich nicht" in self.handler.result):
                        self.handler.user.age = ""
                        self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal dein Alter.")
                        break 
                    else:
                        self.speak_text("Ich habe dich leider nicht verstanden. Wie alt bist du?")
                break
            elif (x in self.handler.result for x in ("nein", "falsch", "nö")):
                self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal dein Alter.")
            else:
                while(1):
                    self.handler.user.age = self.handler.result
                    self.speak_text("Du bist {0} Jahre?".format(self.handler.user.age))
                    self.handler.result = self.listen()
                    
                    if (x in self.handler.result for x in ("ja", "genau", "richtig")):
                        self.speak_text("Du bist ja schon richtig groß.")
                        break
                    elif (x in self.handler.result for x in ("nein", "falsch", "nö")):
                        self.speak_text("Tut mir leid. Wie alt bist du denn?")
                    elif ("Sag ich nicht" in self.handler.result):
                        self.handler.user.age = ""
                        self.speak_text("Das finde ich aber schade. Vielleicht verrätst du mir nächstes Mal dein Alter.")
                        break 
                    else:
                        self.speak_text("Ich habe dich leider nicht verstanden. Wie alt bist du?")
                break
        
        self.speak_text("Du bist also {0} Jahre alt.".format(self.handler.user.age))
        self.speak_text("Das war alles was ich über dich wissen wollte. Ich wünsche dir viel Spaß mit mir.")
        self.speak_text("Um mit mir zu sprechen, sag einfach: Hallo Spiegel oder trete vor mich.")
