#pip install speechrecognition pyaudio gtts beautifulsoup4 requests pillow
#WARNING: not the latest playsound version, use pip install playsound==1.2.2
#python -m pip install pyaudio
from handler import Handler
import threading

def main() -> None:
    """Main function"""
    handler = Handler()
    threading.Thread(target=handler.start, daemon=True).start()
    handler.imagePlayer.start()

if __name__ == "__main__":
    main()