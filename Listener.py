from time import sleep
import speech_recognition as sr
from dotenv import load_dotenv
import yaml

from CommandHandler import CommandHandler
from Config import Config

class Listener:
    def __init__(self, handler: CommandHandler):
        handler.wait_for_response = self.wait_for_response
        self.handler = handler
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.paused = False
        self.pauseBfr = False
        print("Capturing ambient noise")
        # self.r.pause_threshold = 0.5
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
        print("Done capturing ambient noise")

    def start_listening(self):
        print("Now listening")
        self.stop_listening = self.r.listen_in_background(self.mic, self.handler.handle)

    def wait_for_response(self, timeout=None, opts=None):
        # self.stop_listening(True)
        self.paused = True
        audio = self.r.listen(self.mic, timeout=10)
        try:
            captured = self.handler.get_transcript(self.r, audio)
        except Exception as e:
            captured = None
        self.paused = False
        if captured is None:
            self.handler.internal_say("I'm sorry, I didn't understand.")
            return None
        if opts is None:
            # self.start_listening()
            return captured

paused = False
def start(handler):
    listener = Listener(handler)
    listener.start_listening()
    global paused
    while not listener.handler.finished:
        if listener.paused and not paused:
            listener.stop_listening(True)
            listener.pauseBfr = True
            paused = True
        elif paused:
            listener.pauseBfr = False
            paused = False
            listener.start_listening()
        sleep(0.1)
        pass
    listener.stop_listening(True)
    return

if __name__ == "__main__":
    with open('config.yml', 'r') as config_file:
        config = Config(yaml.safe_load(config_file))
        try:
            handler = CommandHandler(config)
        except Exception as e:
            print(e)
            exit(0)
    load_dotenv()
    start(handler)