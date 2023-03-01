from speechLoops.speechLoop import SpeechLoop

class SleepLoop(SpeechLoop):
    """This is the sleep loop. It is the first loop that is called when the program starts."""

    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        """This method is called when the loop is started. It is used to start the speech recognition and to set the next loop."""

        if not self.handler.sleeping:
            self.handler.sleeping = True
            self.handler.imagePlayer.setImage("gesicht-schlafen")

        self.handler.result = self.listen(showPictures=False)

        print('sleepy sleepy')

        if any(x in self.handler.result for x in ("spiegel", "spieglein")):
            self.handler.result = ""
            self.handler.sleeping = False
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("welcomeLoop"))