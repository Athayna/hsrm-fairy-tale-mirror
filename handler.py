from ImagePlayer import ImagePlayer
from user import User
from speechLoops.speechLoop import SpeechLoop
from speechLoops.fairytaleLoop import FairytaleLoop
from speechLoops.mainLoop import MainLoop
from speechLoops.welcomeLoop import WelcomeLoop
from speechLoops.personalizeLoop import PersonalizeLoop


'''
This is the handler class for the magic mirror project.
it contains the userdata and keeps track of the context.
there should be an active speechLoop at any given time.
the speechLoops itself are responsible for chaining the next Loop.
Typical programflow is:
    Loopstart -> listen -> process -> other loop gets chained in handler -> return -> nextLoop
'''

class Handler:

    def __init__(self):
        self.user = User('', 0, '')
        self.context = dict()
        self.speechLoopDict = dict()
        self.speechLoop = None
        self.response =""
        self.imagePlayer = ImagePlayer()
        
    def setSpeechLoop(self, speechLoop: SpeechLoop)-> None:
        self.speechLoop = speechLoop
    
    def updateSpeechLoopDict(self,key:str, speechLoop:SpeechLoop) -> None:
        self.speechLoopDict.update({key: speechLoop})

    def getSpeechLoop(self, key:str) -> SpeechLoop:
        return self.speechLoopDict[key]

    def fillDict(self) -> None:
        self.updateSpeechLoopDict("welcomeLoop", WelcomeLoop(self))
        self.updateSpeechLoopDict("mainLoop", MainLoop(self))
        self.updateSpeechLoopDict("fairytaleLoop", FairytaleLoop(self))
        self.updateSpeechLoopDict("personalizeLoop", PersonalizeLoop(self))

    def start(self) -> None:
        self.fillDict()
        self.speechLoop = self.speechLoopDict["mainLoop"]
        while(self.response != "abbruch"):
            self.speechLoop.play()