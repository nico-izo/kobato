import sys
import os
from os import makedirs
from .plugin import commands
from appdirs import user_data_dir

def terminated():
    print("Plz don't kill me, it's not a nice thing to do with your"
          " imouto ﾟ｡･ﾟヾ(ﾟ｀ｪ´ﾟ)ﾉ｡ﾟ･｡\n")
    os._exit(1)

def get_data_dir():
    path = os.path.join(user_data_dir('kobato'), 'drafts')
    makedirs(path, exist_ok=True)

    return path
