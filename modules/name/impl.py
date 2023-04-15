from util import Arguments, Functions
from string import punctuation

name = ''


def init():
    global name
    with open('name.txt', 'r') as f:
        name = f.readline()
    if not name:
        name = input('Please input a name for me: ')
        with open('name.txt', 'w') as f:
            f.write(name)


def stt(transcript: str):
    if not transcript.startswith(name.lower()):
        return None
    return transcript[len(name):].strip(punctuation).strip()
