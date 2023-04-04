from util import Arguments, Functions


def reminder(args: Arguments, funcs: Functions):
    funcs.say('Reminder created!')


def goodbye(args: Arguments, funcs: Functions):
    funcs.say('Goodbye!')
    funcs.exit()


def get_name(args: Arguments, funcs: Functions):
    name = None
    while name is None:
        name = funcs.prompt('What is your name?')
    funcs.say(f'Hello, {name}!')
