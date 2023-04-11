import webbrowser as wb
from util import Arguments, Functions
import json

aliases = {}


def init():
    global aliases
    with open('aliases.json', 'r') as f:
        aliases = json.load(f)


def open_site(args: Arguments, funcs: Functions):
    global aliases
    if args.site in aliases:
        wb.open(aliases[args.site])
    else:
        wb.open(args.site)


def add_alias(args: Arguments, funcs: Functions):
    global aliases
    if args.alias_name in aliases:
        funcs.say(f'An alias with the name {args.alias_name} already exists.')
    else:
        aliases[args.alias_name] = args.site
        with open('aliases.json', 'w') as f:
            f.write(json.dumps(aliases, indent=4))
        funcs.say('Added!')


def del_alias(args: Arguments, funcs: Functions):
    global aliases
    if args.alias not in aliases:
        funcs.say(f'An alias with the name {args.alias_name} does not exist.')
    else:
        aliases.pop(args.alias)
        with open('aliases.json', 'w') as f:
            f.write(json.dumps(aliases, indent=4))
        funcs.say('Removed!')
