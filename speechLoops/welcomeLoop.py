from speechLoops.speechLoop import SpeechLoop
import datetime

class WelcomeLoop(SpeechLoop):

    def __init__(self, handler):
        super().__init__(handler)

    def play(self) -> None:

        self.handler.result = self.listen()
                            
        if "spiegel" in self.handler.result:
            if (datetime.datetime.now().hour < 10):
                self.speak_text(f'Guten Morgen {self.handler.user.name}, komm putz dir die Zähne mit mir!')
            elif (datetime.datetime.now().hour > 18):
                self.speak_text(f'Guten Abend {self.handler.user.name}, komm putz dir die Zähne mit mir und danach kann ich dir eine Geschichte vorlesen!')
            else:
                self.speak_text(f'Hallo {self.handler.user.name}, wie kann ich dir helfen?')
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))