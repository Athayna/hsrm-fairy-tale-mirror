#pip install speechrecognition pyaudio gtts beautifulsoup4 requests pillow
#WARNING: not the latest playsound version, use pip install playsound==1.2.2
#python -m pip install pyaudio
from handler import Handler
import tkinter as tk
from PIL import ImageTk, Image
import sys
import threading
from ImagePlayer import ImagePlayer

def main():
    handler = Handler()
    threading.Thread(target=handler.start, daemon=True).start()
    imageHandler = ImagePlayer()
    imageHandler.start()

if __name__ == "__main__":
    main()