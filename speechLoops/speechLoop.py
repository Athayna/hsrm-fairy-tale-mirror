import speech_recognition as sr
import handler
from gtts import gTTS
from playsound import playsound
from tempfile import NamedTemporaryFile
import datetime
import requests
import os
from bs4 import BeautifulSoup
import re
import multiprocessing
import subprocess
from signal import SIGINT

######################################## BASE LOOP - ABSTRACT ########################################

class SpeechLoop():

    def __init__(self, handler):
        self.handler = handler

    def listen(self):
        with sr.Microphone() as source:
            r = sr.Recognizer()
            while(1):
                try:
                    print("Adjusting ambient noise")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening...")
                    audio = r.listen(source)
                    print("Interpreting input")
                    result = r.recognize_google(audio, language="de-DE").lower()
                    print(f'Understood {result}, returning self.handler.result')
                    return result.lower()
                except sr.RequestError as e:
                    print(f'Could not request self.handler.results; {e}')
                except sr.UnknownValueError:
                    print("unknown error occurred")        

    def speak_text(self, command):
        tts = gTTS(text=command, lang='de', slow=False)
        tts.save('tts.mp3')
        playsound('tts.mp3')
        os.remove('tts.mp3')

    def play(self) -> None:
        pass

    def get_maerchen(self):
        list = []
        for file in os.listdir(os.getcwd() + "\\maerchen"):
            if file.endswith(".txt"):
                list.append(file[:-4])
        return list

    def find_weather(self):
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

    def read_fairy_tale(self, title):
        try:
            with open(os.getcwd() + "\\maerchen\\" + title + ".txt") as file:
                lines = file.readlines()
                for line in lines:
                    self.findPicture(line)
                    readProcess = multiprocessing.Process(target=speak_tale, args=[line])          
                    readProcess.start()
                    killswitch = multiprocessing.Event()
                    listenProcess = multiprocessing.Process(target=listenToKill, args=[readProcess.pid, killswitch])
                    listenProcess.start()
                    readProcess.join()
                    if listenProcess.is_alive():
                        listenProcess.terminate()
                    if killswitch.is_set():
                        break

 
                    
        except FileNotFoundError:
            print ("File not found")


    def findPicture(self, line:str)-> None:
        for word in line.split():
            word = re.sub("[^A-Za-z]","",word.lower())
            if word in self.handler.imagePlayer.imageDict and word != self.handler.imagePlayer.imageTxt:
                self.handler.imagePlayer.setImage(word)
                return

######################################## DIFFERENT LOOPS ########################################

def speak_tale(command):
    tts = gTTS(text=command, lang='de', slow=False)
    tts.save('tts.mp3')
    playsound('tts.mp3')
    os.remove('tts.mp3')

def listenToKill(thread, killswitch):
    def listenWithoutClass():
        with sr.Microphone() as source:
            r = sr.Recognizer()
            while(1):
                try:
                    print("Adjusting ambient noise")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening...")
                    audio = r.listen(source)
                    print("Interpreting input")
                    result = r.recognize_google(audio, language="de-DE").lower()
                    print(f'Understood {result}, returning self.handler.result')
                    return result.lower()
                except sr.RequestError as e:
                    print(f'Could not request self.handler.results; {e}')
                except sr.UnknownValueError:
                    print("unknown error occurred")    
    
    while(1):
        result = listenWithoutClass()
        if "stop" in result or "abbrechen" in result:
            os.kill(thread, SIGINT)
            killswitch.set()
            return
            
class FirstTimeLoop(SpeechLoop):

    def __init__(self, handler):
        super().__init__(handler)

    def play(self) -> None:
        # self.speak_text("Hallo, ich bin dein magischer Märchenspiegel. Ich kann dir die Zeit sagen, das Wetter vorhersagen, dir eine Geschichte vorlesen und vieles mehr.")
        # self.speak_text("Zuerst möchte ich dich kennenlernen.")
        self.speak_text("Wer bist du?")
        self.handler.result = self.listen()
        self.handler.user.name = self.handler.result
        self.speak_text(f'Hallo {self.handler.user.name}')
        self.speak_text("Wann hast du Geburtstag?")
        self.handler.result = self.listen()
        self.handler.user.birthday = self.handler.result
        self.handler.user.age = datetime.datetime.now().year - int(self.handler.user.birthday.split(".")[2])
        self.speak_text(f'Du bist also {self.handler.user.age} Jahre alt.')

        # self.speak_text("Das war alles was ich über dich wissen wollte. Ich wünsche dir viel Spaß mit mir.")
        # self.speak_text("Um mit mir zu sprechen, sag einfach: Hallo Spiegel oder trete vor mich.")

        self.handler.setSpeechLoop(self.handler.getSpeechLoop("startLoop"))



            


            


                
            
