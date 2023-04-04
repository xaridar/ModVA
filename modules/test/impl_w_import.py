from util import Functions, Arguments, checkNum


def countdown(args: Arguments, funcs: Functions):
    num = checkNum(args.start)

    if num is None:
        funcs.say(f'Number could not be parsed.')
        return

    if num == 0:
        funcs.say(f'I cannot count down from 0...')
        return

    for i in reversed(range(num + 1)):
        funcs.say(i)
