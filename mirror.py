#pip install speechrecognition pyaudio gtts playsound beautifulsoup4 requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from bs4 import BeautifulSoup
import requests
from tempfile import NamedTemporaryFile
import os
import datetime

def listen():
    r = sr.Recognizer()
    while(1):
        try:
            print("Adjusting ambient noise")
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = r.listen(source)
            print("Interpreting input")
            result = r.recognize_google(audio, language="de-DE").lower()
            print("Understood {0}, returning result".format(result))
            return result.lower()
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")        

def get_maerchen():
    list = []
    for file in os.listdir(os.getcwd() + "/maerchen"):
        if file.endswith(".txt"):
            list.append(file[:-4])
    return list

def speak_text(command):
    gTTS(text=command, lang='de').write_to_fp(voice := NamedTemporaryFile())
    playsound(voice.name)
    voice.close()

def read_fairy_tale(title):
    try:
        with open(os.getcwd() + "/maerchen/" + title + ".txt") as file:
            line = file.readline()
            while (line):
                speak_text(file.readline())
    except FileNotFoundError:
        print ("File not found")

def find_weather():
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


def welcome():
    speak_text("Hallo, ich bin dein magischer Märchenspiegel. Ich kann dir die Zeit sagen, das Wetter vorhersagen, dir eine Geschichte vorlesen und vieles mehr.")
    speak_text("Zuerst möchte ich dich kennenlernen.")
    speak_text("Wer bist du?")
    result = listen()
    user["name"] = result
    speak_text("Hallo {0}".format(user["name"]))
    speak_text("Wann hast du Geburtstag?")
    result = listen()
    user["birthday"] = result
    user["age"] = datetime.datetime.now().year - int(user["birthday"].split(".")[2])
    speak_text("Du bist also {0} Jahre alt.".format(user["age"]))
    speak_text("Das war alles was ich über dich wissen wollte. Ich wünsche dir viel Spaß mit mir.")
    speak_text("Um mit mir zu sprechen, sag einfach: Hallo Spiegel oder trete vor mich.")

user = dict(
    name = "",
    age = 0,
    birthday = ""
)

welcome()

while(1):
    with sr.Microphone() as source: 
        result = listen()
                            
        if "spiegel" in result:
            if (datetime.datetime.now().hour < 10):
                speak_text("Guten Morgen {0}, komm putz dir die Zähne mit mir!".format(user["name"]))
            elif (datetime.datetime.now().hour > 18):
                speak_text("Guten Abend {0}, komm putz dir die Zähne mit mir und danach kann ich dir eine Geschichte vorlesen!".format(user["name"]))
            else:
                speak_text("Hallo {0}, wie kann ich dir helfen?".format(user["name"]))
                            
            while("wiedersehen" not in result):
                result = listen()

                if any(x in result for x in ("zeit", "uhr")):
                    speak_text("Es ist {0}".format(datetime.datetime.now().strftime("%H:%M Uhr")))

                elif "datum" in result:
                    speak_text("Heute ist der {0}".format(datetime.datetime.now().strftime("%d.%m.%Y")))

                elif "geburtstag" in result:
                    speak_text("Dein Geburtstag ist in {0} Tagen".format((datetime.datetime.now() - datetime.datetime.strptime(user["birthday"], "%d.%m.%Y")).days))

                elif any(x in result for x in ("wetter", "temp", "regen", "kalt", "warm")):
                    weather = find_weather()
                    speak_text("Das Wetter in {0} ist {1} Grad Celsius".format(weather["location"], weather["temperature"]))
                    if any(x in weather["info"] for x in ("rain", "drizzle", "shower")):
                        speak_text("Denk an deinen Regenschirm!")
                    if (weather["temperature"] < 10):
                        speak_text("Zieh dich warm an!")
                
                elif any(x in result for x in ("erzähl", "les", "spiel", "geschichte", "märchen")):
                    
                    speak_text("Welches Märchen soll ich dir vorlesen? Ich kenne:")
                    for name in get_maerchen():
                        speak_text(name)
                    speak_text("Du kannst auch abbrechen indem du keins sagst.")
                    
                    result = listen()
                    
                    while(1):
                        if (result in get_maerchen()):
                            speak_text("Hier ist die Geschichte von {0}:".format(result))
                            read_fairy_tale(result)
                            break
                        
                        elif ("kein" in result):
                            break
                        
                        else:
                            speak_text("Dieses Märchen kenne ich leider nicht. Ich kenne:")
                            for name in get_maerchen():
                                speak_text(name)
                            speak_text("Du kannst auch abbrechen indem du keins sagst.")
                            
                        result = listen()
