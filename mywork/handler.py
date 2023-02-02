import user
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
        self.user = user.User()
        self.context = dict()
        self.speechLoopDict = dict()
        self.speechLoop = None
        self.response =""
        
    def setSpeechLoop(self, speechLoop: speechLoop.SpeechLoop)-> None:
        self.speechLoop = speechLoop
    
    def updateSpeechLoopDict(self,key:str, speechLoop:speechLoop.SpeechLoop) -> None:
        self.responseDict.update({key, speechLoop})

    def getSpeechLoop(self, key:str) -> speechLoop.SpeechLoop:
        return self.responseDict[key]

    def fillDict(self) -> None:
        self.responseDict.update({"startLoop", speechLoop.StartLoop()})
        self.responseDict.update({"mainLoop", speechLoop.MainLoop()})
        self.responseDict.update({"storyLoop", speechLoop.StoryLoop()})

    def start(self) -> None:
        self.fillDict()
        self.speechLoop = self.responseDict["startLoop"]
        while(1):
            self.speechLoop.play()