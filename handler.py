from ImagePlayer import ImagePlayer
from speechLoops.gameLoop import GameLoop
from user import User
from speechLoops.speechLoop import SpeechLoop
from speechLoops.fairytaleLoop import FairytaleLoop
from speechLoops.mainLoop import MainLoop
from speechLoops.welcomeLoop import WelcomeLoop
from speechLoops.personalizeLoop import PersonalizeLoop
from speechLoops.sleepLoop import SleepLoop
import time

class Handler:
    '''
    This is the handler class for the magic mirror project.
    it contains the userdata and keeps track of the context.
    there should be an active speechLoop at any given time.
    the speechLoops itself are responsible for chaining the next Loop.
    Typical programflow is:
        Loopstart -> listen -> process -> other loop gets chained in handler -> return -> nextLoop
    '''

    def __init__(self) -> None:
        self.user = User('Steffi', 8, True, 'lila', '', 0, 0, 0, 0)
        self.context = dict()
        self.speechLoopDict = dict()
        self.speechLoop = None
        self.result = ""
        self.imagePlayer = ImagePlayer()
        self.sleeping = False
        self.lastInteraction = time.time()
        
    def setSpeechLoop(self, speechLoop:SpeechLoop) -> None:
        self.speechLoop = speechLoop
    
    def updateSpeechLoopDict(self, key:str, speechLoop:SpeechLoop) -> None:
        self.speechLoopDict.update({key: speechLoop})

    def getSpeechLoop(self, key:str) -> SpeechLoop:
        return self.speechLoopDict[key]

    def fillDict(self) -> None:
        self.updateSpeechLoopDict("welcomeLoop", WelcomeLoop(self))
        self.updateSpeechLoopDict("mainLoop", MainLoop(self))
        self.updateSpeechLoopDict("fairytaleLoop", FairytaleLoop(self))
        self.updateSpeechLoopDict("personalizeLoop", PersonalizeLoop(self))
        self.updateSpeechLoopDict("gameLoop", GameLoop(self))
        self.updateSpeechLoopDict("sleepLoop", SleepLoop(self))

    def checkForAbort(self) -> bool:
        return True if any(x in self.result for x in ("abbrechen", "ende", "stop")) else False
    
    def checkForSleep(self) -> bool:
        divTime = time.time() - self.lastInteraction
        print(f'Zeit seit letzter Interaktion: {divTime}')
        if divTime > 60:
            self.speechLoop = self.speechLoopDict["sleepLoop"]
            return True
        return False

    def start(self) -> None:
        self.fillDict()
        self.speechLoop = self.speechLoopDict["personalizeLoop"]
        # self.speechLoop = self.speechLoopDict["welcomeLoop"]
        
        while 1:
            self.speechLoop.play()