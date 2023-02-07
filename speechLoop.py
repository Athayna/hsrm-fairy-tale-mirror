import speech_recognition as sr
import handler
from gtts import gTTS
from playsound import playsound
from tempfile import NamedTemporaryFile
import datetime
import requests
import os
from bs4 import BeautifulSoup

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
                    self.handler.result = r.recognize_google(audio, language="de-DE").lower()
                    print("Understood {0}, returning self.handler.result".format(self.handler.result))
                    return self.handler.result.lower()
                except sr.RequestError as e:
                    print("Could not request self.handler.results; {0}".format(e))
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
        for file in os.listdir(os.getcwd() + "/maerchen"):
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
            with open(os.getcwd() + "/maerchen/" + title + ".txt") as file:
                line = file.readline()
                while (line):
                    self.speak_text(file.readline())
        except FileNotFoundError:
            print ("File not found")

######################################## DIFFERENT LOOPS ########################################

class FirstTimeLoop(SpeechLoop):

    def __init__(self, handler):
        super().__init__(handler)

    def play(self) -> None:
        # self.speak_text("Hallo, ich bin dein magischer Märchenspiegel. Ich kann dir die Zeit sagen, das Wetter vorhersagen, dir eine Geschichte vorlesen und vieles mehr.")
        # self.speak_text("Zuerst möchte ich dich kennenlernen.")
        self.speak_text("Wer bist du?")
        self.handler.result = self.listen()
        self.handler.user.name = self.handler.result
        self.speak_text("Hallo {0}".format(self.handler.user.name))
        self.speak_text("Wann hast du Geburtstag?")
        self.handler.result = self.listen()
        self.handler.user.birthday = self.handler.result
        self.handler.user.age = datetime.datetime.now().year - int(self.handler.user.birthday.split(".")[2])
        self.speak_text("Du bist also {0} Jahre alt.".format(self.handler.user.age))

        # self.speak_text("Das war alles was ich über dich wissen wollte. Ich wünsche dir viel Spaß mit mir.")
        # self.speak_text("Um mit mir zu sprechen, sag einfach: Hallo Spiegel oder trete vor mich.")

        self.handler.setSpeechLoop(self.handler.getSpeechLoop("startLoop"))


class StartLoop(SpeechLoop):

    def __init__(self, handler):
        super().__init__(handler)

    def play(self) -> None:

        self.handler.result = self.listen()
                            
        if "spiegel" in self.handler.result:
            if (datetime.datetime.now().hour < 10):
                self.speak_text("Guten Morgen {0}, komm putz dir die Zähne mit mir!".format(self.handler.user.name))
            elif (datetime.datetime.now().hour > 18):
                self.speak_text("Guten Abend {0}, komm putz dir die Zähne mit mir und danach kann ich dir eine Geschichte vorlesen!".format(self.handler.user.name))
            else:
                self.speak_text("Hallo {0}, wie kann ich dir helfen?".format(self.handler.user.name))
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
            

class MainLoop(SpeechLoop):
    def __init__(self, handler):
        super().__init__(handler)

    def play(self) -> None:

        self.handler.result = self.listen()

        if any(x in self.handler.result for x in ("zeit", "uhr")):
            self.speak_text("Es ist {0}".format(datetime.datetime.now().strftime("%H:%M Uhr")))

        elif "datum" in self.handler.result:
            self.speak_text("Heute ist der {0}".format(datetime.datetime.now().strftime("%d.%m.%Y")))

        elif "geburtstag" in self.handler.result:
            self.speak_text("Dein Geburtstag ist in {0} Tagen".format((datetime.datetime.now() - datetime.datetime.strptime(self.handler.user.birthday, "%d.%m.%Y")).days))

        elif any(x in self.handler.result for x in ("wetter", "temp", "regen", "kalt", "warm")):
            weather = self.find_weather()
            self.speak_text("Das Wetter in {0} ist {1} Grad Celsius".format(weather["location"], weather["temperature"]))
            if any(x in weather["info"] for x in ("rain", "drizzle", "shower")):
                self.speak_text("Denk an deinen Regenschirm!")
            if (weather["temperature"] < 10):
                self.speak_text("Zieh dich warm an!")
        
        elif any(x in self.handler.result for x in ("erzähl", "les", "spiel", "geschichte", "märchen")):
            
            self.speak_text("Welches Märchen soll ich dir vorlesen? Ich kenne:")
            for name in self.get_maerchen():
                self.speak_text(name)
            self.speak_text("Du kannst auch abbrechen indem du keins sagst.")
            
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("storyLoop"))
            

class StoryLoop(SpeechLoop):
    
    def __init__(self, handler):
        super().__init__(handler)

    def play(self) -> None:

        self.handler.result = self.listen()

        if (self.handler.result in self.get_maerchen()):
            self.speak_text("Hier ist die Geschichte von {0}:".format(self.handler.result))
            self.read_fairy_tale(self.handler.result)
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
            
        
        elif ("kein" in self.handler.result):
            self.handler.setSpeechLoop(self.handler.getSpeechLoop("mainLoop"))
           
        
        else:
            self.speak_text("Dieses Märchen kenne ich leider nicht. Ich kenne:")
            for name in self.get_maerchen():
                self.speak_text(name)
            self.speak_text("Du kannst auch abbrechen indem du keins sagst.")
                
            
