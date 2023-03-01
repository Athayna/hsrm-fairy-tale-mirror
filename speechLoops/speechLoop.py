import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import requests
import os
import re
import time
import multiprocessing
#from signal import SIGKILL, 
from signal import SIGINT

######################################## BASE LOOP - ABSTRACT ########################################
watchListWords = {
    "abbruch": ["abbruch", "abbrechen", "stop"]
}

class SpeechLoop():
    """Abstract class for speech loops"""

    def __init__(self, handler) -> None:
        self.handler = handler

    def listen(self, showPictures=True) -> str:
        """Method for listening to user input"""
        
        with sr.Microphone() as source:
            r = sr.Recognizer()
            while(1):
                try:
                    print(f'sleeping: {self.handler.sleeping}')
                    if not self.handler.sleeping and self.handler.checkForSleep():
                        return ''
                    print("Adjusting ambient noise")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening...")
                    if showPictures:
                        self.handler.imagePlayer.setImage("gesicht-denken")
                    audio = r.listen(source, timeout=5)
                    print("Interpreting input")
                    if showPictures:
                        self.handler.imagePlayer.setImage("gesicht-lachen")
                    result = r.recognize_google(audio, language="de-DE").lower()
                    print(f'Understood {result}, returning self.handler.result')
                    self.handler.lastInteraction = time.time()
                    if any(x in result.lower() for x in ("tschüss", "gute nacht", "ausschalten")):
                        result = ""
                        self.handler.setSpeechLoop(self.handler.getSpeechLoop("sleepLoop"))
                    return result.lower()
                except sr.RequestError as e:
                    print(f'Could not request self.handler.results; {e}')
                except sr.UnknownValueError:
                    print("unknown error occurred")
                except sr.WaitTimeoutError:
                    print("Listen Timeout")

    def speak_text(self, command, watchListWords=watchListWords["abbruch"]) -> None:
        print("in speak text")
        print(f'speaktext array: {watchListWords}')
        readProcess = multiprocessing.Process(target=speak_tale, args=[command])          
        readProcess.start()
        conn1, conn2 = multiprocessing.Pipe()
        listenProcess = multiprocessing.Process(target=listenToKill, args=[readProcess.pid, conn2, None, watchListWords])
        listenProcess.start()
        while(readProcess.is_alive()):
            if conn1.poll(0.1):
                print("found word")
                self.handler.result = conn1.recv()
                break
        else:
            listenProcess.terminate()

    def play(self) -> None:
        """Method for playing the loop"""
        
        pass

    def get_maerchen(self) -> list:
        """Method for getting a list of all fairy tales in the maerchen folder"""       
        
        list = []
        for file in os.listdir(os.getcwd() + "\\maerchen"):
            if file.endswith(".txt"):
                list.append(file[:-4])
        return list

    def find_weather(self) -> dict:
        """Method for finding the weather in a city. Returns a dictionary with the temperature, the weather description and the city name."""

        API_KEY = 'e9bed519ef99f64f1873e3e42118989f'
        city_name = 'Wiesbaden'
        GEO_URL = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}'
        geolocation = requests.get(GEO_URL)
        geo_json = geolocation.json()
        lat = geo_json[0]["lat"]
        lon = geo_json[0]["lon"]
        REQUEST_URL = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        res = requests.get(REQUEST_URL)
        response = res.json()
        if(response["cod"] != "404"):
            body = response["main"]
            current_weather = response["weather"]
            return dict(
                temperature = int(body["temp"]),
                info = current_weather[0]["description"],
                location = city_name
            )
        else:
            return None

    def read_fairy_tale(self, title) -> None:
        """Method for reading a fairy tale from the maerchen folder"""

        try:
            with open(os.getcwd() + "\\maerchen\\" + title + ".txt") as file:
                lines = file.readlines()
                for line in lines:
                    self.handler.lastInteraction = time.time()
                    self.findPicture(line)
                    readProcess = multiprocessing.Process(target=speak_tale, args=[line])          
                    readProcess.start()
                    killswitch = multiprocessing.Event()
                    conn1, conn2 = multiprocessing.Pipe()
                    listenProcess = multiprocessing.Process(target=listenToKill, args=[readProcess.pid, conn2, killswitch])
                    listenProcess.start()
                    while(readProcess.is_alive()):
                        if conn1.poll(0.100):
                            print("got connection result")
                            self.handler.result = conn1.recv()
                            break
                    else:
                        print("kill listen process")
                        listenProcess.terminate()
                    if killswitch.is_set():
                        break  
                    
        except FileNotFoundError:
            print ("File not found")

    def findPicture(self, line:str) -> None:
        print(line)
        for word in line.split():
            word = re.sub("[^A-Za-z]","",word.lower())
            if word in self.handler.imagePlayer.imageDict and word != self.handler.imagePlayer.imageTxt:
                print(word)
                self.handler.imagePlayer.setImage(word)
                return

######################################## DIFFERENT LOOPS ########################################

def speak_tale(command) -> None:
    """Method for speaking a text with Google's text-to-speech API."""
    print("in speak tale sprachausgabe")
    tts = gTTS(text=command, lang='de', slow=False)
    tts.save('tts.mp3')
    playsound('tts.mp3')
    os.remove('tts.mp3')

def listenToKill(thread, pipeconnection:multiprocessing.Pipe, killswitch=None, watchListWords=watchListWords["abbruch"]) -> None:
    print(f'listenkill array: {watchListWords}')
    def listenWithoutClass():
        with sr.Microphone() as source:
            r = sr.Recognizer()
            while(1):
                try:
                    print("Adjusting ambient noise in kill")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening...")
                    audio = r.listen(source)
                    print("Interpreting input in kill")
                    result = r.recognize_google(audio, language="de-DE").lower()
                    print(f'Understood {result}, returning self.handler.result in kill')
                    return result.lower()
                except sr.RequestError as e:
                    print(f'Could not request self.handler.results; {e} in kill')
                except sr.UnknownValueError:
                    print("unknown error occurred in kill")    
    
    while(1):
        result = listenWithoutClass()
        print (result)
        print (watchListWords)
        for word in watchListWords:
            if word in result:
                print("found matching word")
                if word == "weiter" or word == "überspringen":
                    pipeconnection.send("")
                else:
                    pipeconnection.send(word)
                if killswitch:
                    killswitch.set()
                try:
                    while(pipeconnection.poll(0.100)):
                        pass
                finally:
                    os.kill(thread, SIGINT)
                    #os.kill(thread, SIGKILL)
                    return
