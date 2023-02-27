from speechLoops.speechLoop import SpeechLoop
import datetime

class WelcomeLoop(SpeechLoop):
    """This is the welcome loop. It is the first loop that is called when the program starts."""

    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        """This method is called when the loop is started. It is used to start the speech recognition and to set the next loop."""

        self.handler.imagePlayer.setImage("cat")

        if (datetime.datetime.now().hour < 10):
            self.speak_text(f'Guten Morgen {self.handler.user.name}, komm putz dir die Zähne mit mir!')
            self.handler.imagePlayer.setImage("cat2")
            #wait 3 min
            self.speak_text(f'Und jetzt noch schnell die Haare kämmen und anziehen, dann kann der Tag losgehen!')
        elif (datetime.datetime.now().hour > 12 and datetime.datetime.now().hour < 15) and datetime.date.isoweekday() in range(1, 5) :
            if self.handler.user.school:
                self.speak_text(f'Guten Tag {self.handler.user.name}, na wie war die Schule?')
                self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("gut", "toll", "schön", "super", "oke")):
                    self.handler.result = ""
                    self.speak_text(f'Das freut mich. Ich bin mir sicher nächstes Mal wird auch wieder super!')
                elif any(x in self.handler.result for x in ("naja", "schlecht", "blöd", "doof", "nicht")):
                    self.speak_text("Das tut mir leid für dich. Hoffentlich wird morgen wieder besser. Sonst solltest du mal mit einem Erwachsenen reden, damit sie dir helfen.")
                elif ("langweilig" in self.handler.result):
                    self.handler.result = ""
                    self.speak_text("Ach was es gibt doch immer etwas spannendes zu lernen.") 
                else:
                    self.handler.result = ""
                    self.speak_text("Ich habe schon viel von der Schule gehört, da wäre ich auch gerne mal.")
                
                self.speak_text(f'Hast du denn schon deine Hausaufgaben gemacht?')
                self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("ja", "klar", "genau", "schon")):
                    self.handler.result = ""
                    self.speak_text(f'Sehr gut {self.handler.user.name}, ich bin stolz auf dich!')
                elif ("nicht" in self.handler.result and "schule" in self.handler.result) or (any(x in self.handler.result for x in ("gehe", "bin")) and "kindergarten" in self.handler.result):
                    self.handler.result = ""
                    self.speak_text("Ohje da hab ich mir was falsches gemerkt, das tut mir leid. Du gehst also in den Kindergarten?") 
                    while(1):
                        self.handler.result = self.listen()
                        if any(x in self.handler.result for x in ("ja", "genau", "richtig", "klar", "sicher")):
                            self.handler.result = ""
                            self.handler.user.school = True
                            self.speak_text(f'Das ist doch auch richtig schön und auch da lernt man schon viele tolle Sachen.')
                            break
                        elif any(x in self.handler.result for x in ("nein", "falsch", "nö", "nicht", "ne")):
                            self.speak_text("Puh, dann hab ich mich doch nicht geirrt. Super, dass du zur Schule gehst!")
                            break
                        else:
                            self.handler.result = ""
                            self.speak_text("Ich habe dich leider nicht verstanden. Gehst du in den Kindergarten?")
                elif any(x in self.handler.result for x in ("naja", "nein", "ne", "nö", "nicht")):
                    self.speak_text("Das ist wichtig, komm mach die mal zuerst, danach bin ich gerne weiter für dich da!")
                elif any(x in self.handler.result for x in ("keine Lust", "langweilig", "mach ich nicht")):
                    self.handler.result = ""
                    self.speak_text("Die helfen dir aber damit du mal werden kannst, was du möchtest. Komm, mach mal deine Hausaufgaben. Danach können wir machen, was du möchtest.") 
                
                else:
                    self.handler.result = ""
                    self.speak_text("Passt doch. Was möchtest du denn jetzt gerne machen?")
            else:
                self.speak_text(f'Guten Tag {self.handler.user.name}, na wie war es im Kindergarten?')
                self.handler.result = self.listen()
                if any(x in self.handler.result for x in ("gut", "toll", "schön", "super", "oke")):
                    self.handler.result = ""
                    self.speak_text(f'Das freut mich. Ich bin mir sicher nächstes Mal wird auch wieder super!')
                elif ("nicht" in self.handler.result and "kindergarten" in self.handler.result) or (any(x in self.handler.result for x in ("gehe", "bin")) and "schule" in self.handler.result):
                    self.handler.result = ""
                    self.speak_text("Ohje da hab ich mir was falsches gemerkt, das tut mir leid. Du gehst also zur Schule?") 
                    while(1):
                        self.handler.result = self.listen()
                        if any(x in self.handler.result for x in ("ja", "genau", "richtig", "klar", "sicher")):
                            self.handler.result = ""
                            self.handler.user.school = True
                            self.speak_text(f'Ich bin beeindruckt, dann hast du bestimmt schon richtig viel gelernt. Vielleicht kann ich dir mit meinen Lernspielen mal helfen.')
                            break
                        elif any(x in self.handler.result for x in ("nein", "falsch", "nö", "nicht", "ne")):
                            self.speak_text("Im Kindergarten lernst du auch schon viele tolle Sachen und hast bestimmt auch ganz liebe Freunde.")
                            break
                        else:
                            self.handler.result = ""
                            self.speak_text("Ich habe dich leider nicht verstanden. Gehst du schon zur Schule?")
                elif any(x in self.handler.result for x in ("naja", "schlecht", "blöd", "doof", "nicht")):
                    self.speak_text("Das tut mir leid für dich. Hoffentlich wird morgen wieder besser. Sonst solltest du mal mit einem Erwachsenen reden, damit sie dir helfen.")
                elif ("langweilig" in self.handler.result):
                    self.handler.result = ""
                    self.speak_text("Ach was es gibt doch immer etwas tolles zu erleben.") 
                else:
                    self.handler.result = ""
                    self.speak_text("Ich habe schon viel vom Kindergarten gehört, da wäre ich auch gerne mal.")

        elif (datetime.datetime.now().hour > 19):
            self.speak_text(f'Guten Abend {self.handler.user.name}, komm putz dir die Zähne mit mir!')
            self.handler.imagePlayer.setImage("cat2")
            #wait 3 min
            self.speak_text(f'Und jetzt noch schnell den Schlafanzug anziehen und danach kann ich dir eine Geschichte vorlesen!')
        else:
            self.speak_text(f'Hallo {self.handler.user.name}, wie kann ich dir helfen?')
        self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))