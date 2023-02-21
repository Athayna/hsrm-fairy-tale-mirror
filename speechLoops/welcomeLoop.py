from speechLoops.speechLoop import SpeechLoop
import datetime

class WelcomeLoop(SpeechLoop):
    """This is the welcome loop. It is the first loop that is called when the program starts."""

    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        """This method is called when the loop is started. It is used to start the speech recognition and to set the next loop."""

        self.handler.result = self.listen()
                            
        if "spiegel" in self.handler.result:
            if (datetime.datetime.now().hour < 10):
                self.speak_text(f'Guten Morgen {self.handler.user.name}, komm putz dir die Zähne mit mir!')
            elif (datetime.datetime.now().hour > 18):
                self.speak_text(f'Guten Abend {self.handler.user.name}, komm putz dir die Zähne mit mir und danach kann ich dir eine Geschichte vorlesen!')
            else:
                self.speak_text(f'Hallo {self.handler.user.name}, wie kann ich dir helfen?')
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))