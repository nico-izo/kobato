import sys
import os
from os import makedirs
from .plugin import commands
from .config import config_sync
from appdirs import user_data_dir

def terminated():
    print("Plz don't kill me, it's not a nice thing to do with your"
          " imouto ﾟ｡･ﾟヾ(ﾟ｀ｪ´ﾟ)ﾉ｡ﾟ･｡\n")
    config_sync()
    os._exit(n)    

def usage():
    columns = 13
    compiled_desc = ""
    # let's just assume that we'll never have command longer than 13 symbols
    for key, value in sorted(commands.items()):
        compiled_desc += "   " + key + (" " * (columns - len(key))) + value['description'] + "\n"
        if len(value['aliases']):
            compiled_desc += " "*16 + "Aliases: " + ", ".join(value['aliases']) + "\n"

    print(
    "Kobato — Command line interface for microblogging platform point.im\n"
    "\n"
    "Usage: kobato [--help] <command> [parameters | --help]\n\n"
    "Available commands: \n" + compiled_desc + "\n"
    )

    sys.exit(0)

def get_data_dir():
    path = os.path.join(user_data_dir('kobato'), 'drafts')
    makedirs(path, exist_ok=True)

    return path
