import os
import speech_recognition as sr
from string import punctuation
from txtai.pipeline import TextToSpeech
import sounddevice as sd
import re

from Config import Config
from util import Functions, Arguments


class CommandHandler:
    def __init__(self, config: Config) -> None:
        if config.loaderror is not None:
            raise Exception(config.loaderror)
        self.finished = False
        self.tts = TextToSpeech()
        self.config = config
        if config.parser == 'whisperapi':
            self.recognizer = 'recognize_whisper_api'
        elif config.parser == 'whisper':
            self.recognizer = 'recognize_whisper'
        elif config.parser == 'google':
            self.recognizer = 'recognize_google'
        else:
            raise Exception('Invalid parser specified')

    def handle(self, recog: sr.Recognizer, audio):
        try:
            command = self.get_transcript(recog, audio, clean=True)
            if command is None:
                return
            if len(self.config.middleware_stt_order):
                for middleware in self.config.middleware_stt_order:
                    command = middleware(command)
            self.manage(command)
        except Exception as e:
            print(e)
            return

    def get_transcript(self, recog: sr.Recognizer, audio, clean=False):
        try:
            transcript = getattr(recog, self.recognizer)(audio)
            command = self.clean(transcript)
            if len(command) == 0:
                return None
            # print("I heard: " + command)
            # self.say(transcript)
            return command if clean else transcript
        except sr.UnknownValueError:
            raise Exception("I didn't understand")
        except sr.RequestError as e:
            raise Exception(f"Bad request ({self.recognizer} - {e})")

    def clean(self, input: str):
        return input.lower().strip(punctuation).strip()

    def say(self, script):
        if len(self.config.middleware_tts_order):
            for middleware in self.config.middleware_tts_order:
                script = middleware(script)
        if self.config.verbose_tts:
            print(script)
        sd.play(self.tts(str(script)), 22050, blocking=True)

    def prompt(self, prompt):
        if self.talk_thread is not None:
            self.talk_thread.join()
        self.say(prompt)
        return self.wait_for_response()

    def exit(self):
        self.finished = True

    def manage(self, command):
        if self.config.verbose_stt:
            print(command)
        for cmd in self.config.mods:
            params = re.findall('\{(.+?)\}', cmd['command'])
            if not params and command == cmd['command']:
                root_dir = os.getcwd()
                os.chdir(f"{root_dir}\\{cmd['directory']}")
                cmd['function']({}, Functions(
                    say=self.say,
                    exit=self.exit,
                    prompt=self.prompt
                ))
                os.chdir(root_dir)
                return
            if not params:
                continue
            matchStr = re.sub('{.+?}', '(.+)', cmd['command'])
            args = re.match(matchStr, command)
            if args:
                root_dir = os.getcwd()
                os.chdir(f"{root_dir}\\{cmd['directory']}")
                cmd['function'](
                    Arguments(
                        {param: args.groups()[i] for i, param in enumerate(params)}),
                    Functions(
                        say=self.say,
                        exit=self.exit,
                        prompt=self.prompt
                    )
                )
                os.chdir(root_dir)
                return
