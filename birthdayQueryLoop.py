import handler
import speechLoop
import datetime

class FirstTimeLoop(speechLoop.SpeechLoop):

    def __init__(self, handler: handler.Handler):
        super().__init__(handler)

    def play(self) -> None:
        