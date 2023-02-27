from handler import Handler
import threading

def main() -> None:
    """Main function"""
    handler = Handler()
    threading.Thread(target=handler.start, daemon=True).start()
    handler.imagePlayer.start()

if __name__ == "__main__":
    main()