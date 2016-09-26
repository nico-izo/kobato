import sys
import os

from os import makedirs
from appdirs import user_data_dir
from decorating import animated


def terminated():
    print("Plz don't kill me, it's not a nice thing to do with your"
          " imouto ﾟ｡･ﾟヾ(ﾟ｀ｪ´ﾟ)ﾉ｡ﾟ･｡\n")
    sys.exit(1)


def get_data_dir():
    path = os.path.join(user_data_dir('kobato'), 'drafts')
    makedirs(path, exist_ok=True)

    return path
