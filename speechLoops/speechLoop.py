import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import requests
import os
from bs4 import BeautifulSoup
import re
import multiprocessing
from signal import SIGINT

######################################## BASE LOOP - ABSTRACT ########################################

class SpeechLoop():
    """Abstract class for speech loops"""

    def __init__(self, handler) -> None:
        self.handler = handler

    def listen(self) -> str:
        """Abstract method for listening to user input"""
        
        with sr.Microphone() as source:
            r = sr.Recognizer()
            while(1):
                try:
                    print("Adjusting ambient noise")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening...")
                    self.handler.imagePlayer.setImage("dog")
                    audio = r.listen(source)
                    print("Interpreting input")
                    self.handler.imagePlayer.setImage("cat")
                    result = r.recognize_google(audio, language="de-DE").lower()
                    print(f'Understood {result}, returning self.handler.result')
                    return result.lower()
                except sr.RequestError as e:
                    print(f'Could not request self.handler.results; {e}')
                except sr.UnknownValueError:
                    print("unknown error occurred")        

    def speak_text(self, command) -> None:
        readProcess = multiprocessing.Process(target=speak_tale, args=[command])          
        readProcess.start()
        conn1, conn2 = multiprocessing.Pipe()
        listenProcess = multiprocessing.Process(target=listenToKill, args=[readProcess.pid, conn2])
        listenProcess.start()
        while(readProcess.is_alive()):
            if conn1.poll(0.1):
                print("found word")
                self.handler.result = conn1.recv()
                break
        else:
            listenProcess.terminate()

    def play(self) -> None:
        pass

    def get_maerchen(self) -> list:
        list = []
        for file in os.listdir(os.getcwd() + "\\maerchen"):
            if file.endswith(".txt"):
                list.append(file[:-4])
        return list

    def find_weather(self) -> dict:
        city_name = 'Wiesbaden'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        res = requests.get(
            f'https://www.google.com/search?q={city_name}&oq={city_name}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
        
        soup = BeautifulSoup(res.text, 'html.parser')
        return dict(
            location = soup.select('#wob_loc')[0].getText().strip(),
            time = soup.select('#wob_dts')[0].getText().strip(),
            info = soup.select('#wob_dc')[0].getText().strip(),
            temperature = soup.select('#wob_tm')[0].getText().strip()
        )

    def read_fairy_tale(self, title) -> None:
        try:
            with open(os.getcwd() + "\\maerchen\\" + title + ".txt") as file:
                lines = file.readlines()
                for line in lines:
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
        for word in line.split():
            word = re.sub("[^A-Za-z]","",word.lower())
            if word in self.handler.imagePlayer.imageDict and word != self.handler.imagePlayer.imageTxt:
                self.handler.imagePlayer.setImage(word)
                return

######################################## DIFFERENT LOOPS ########################################

watchListWords = {
    "abbruch": ["abbruch", "abbrechen", "stop"]
}

def speak_tale(command) -> None:
    tts = gTTS(text=command, lang='de', slow=False)
    tts.save('tts.mp3')
    playsound('tts.mp3')
    os.remove('tts.mp3')

def listenToKill(thread, pipeconnection:multiprocessing.Pipe, killswitch=None, watchListWords=watchListWords["abbruch"]) -> None:
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
                pipeconnection.send(word)
                if killswitch:
                    killswitch.set()
                try:
                    while(pipeconnection.poll(0.100)):
                        pass
                finally:
                    os.kill(thread, SIGINT)
                    return
