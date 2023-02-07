from user import User
import speechLoop
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
        self.user = User('hans', 4, "01.01.2005")
        self.context = dict()
        self.speechLoopDict = dict()
        self.speechLoop = None
        self.response =""
        
    def setSpeechLoop(self, speechLoop: speechLoop.SpeechLoop)-> None:
        self.speechLoop = speechLoop
    
    def updateSpeechLoopDict(self,key:str, speechLoop:speechLoop.SpeechLoop) -> None:
        self.speechLoopDict.update({key: speechLoop})

    def getSpeechLoop(self, key:str) -> speechLoop.SpeechLoop:
        return self.speechLoopDict[key]

    def fillDict(self) -> None:
        self.updateSpeechLoopDict("startLoop", speechLoop.StartLoop(self))
        self.updateSpeechLoopDict("mainLoop", speechLoop.MainLoop(self))
        self.updateSpeechLoopDict("storyLoop", speechLoop.StoryLoop(self))
        self.updateSpeechLoopDict("firstTimeLoop", speechLoop.FirstTimeLoop(self))

    def start(self) -> None:
        self.fillDict()
        self.speechLoop = self.speechLoopDict["firstTimeLoop"]
        while(1):
            self.speechLoop.play()