# https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
# Thanks to user derek73

from typing import Callable
from word2number import w2n


class dotdict(dict):
    __getattr__ = dict.get


class Arguments(dotdict):
    pass


class Functions:
    def __init__(self, say: Callable[[str], None], exit: Callable[[], None], prompt: Callable[[str], str]):
        self.say = say
        self.exit = exit
        self.prompt = prompt


def checkNum(arg, integer=True):
    try:
        num = int(arg)
    except:
        try:
            num = w2n.word_to_num(arg)
        except:
            return None
    if integer and not isinstance(num, int):
        return None
    return num
