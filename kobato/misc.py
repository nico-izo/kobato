import sys
import os
import requests

from os import makedirs
from appdirs import user_data_dir
from decorating import animated
from requests.exceptions import RequestException, SSLError


def terminated():
    print("Plz don't kill me, it's not a nice thing to do with your"
          " imouto ﾟ｡･ﾟヾ(ﾟ｀ｪ´ﾟ)ﾉ｡ﾟ･｡\n")
    os._exit(1)


def get_data_dir():
    path = os.path.join(user_data_dir('kobato'), 'drafts')
    makedirs(path, exist_ok=True)

    return path


def kobato_request(url,
                   method='get',
                   result='json',  # json|text
                   ssl_check=True,
                   animated_request=True,
                   animated_text='Doin\' all the things...',
                   **kwargs):
    named_parameters = {}

    if not ssl_check:
        named_parameters['verify'] = False

    for key in kwargs:
        named_parameters[key] = kwargs[key]

    method = getattr(requests, method)

    # TODO: in fact, there are a lot of exceptions
    # http://docs.python-requests.org/en/master/_modules/requests/exceptions/?highlight=exception
    # maybe I can handle them better?
    error = False
    with animated(animated_text):
        try:
            r = method(url, **named_parameters)
        except SSLError as e:
            print("ERROR: something wrong with SSL:", type(e).__name__)
            # TODO TODO TODO!!!
            print("However, you can execute kobato config --set meta.verify_ssl false to suppress this error.")
            error = True
        except RequestException as e:
            print("ERROR: something went wrong:", type(e).__name__)
            print("Exiting...")
            error = True

    if error:  # something wrong with animated() and sys.exit
        sys.exit(127)

    if result == 'json':
        try:
            result = r.json()
        except Exception as e:
            print("JSON decoding failed:", type(e).__name__)
            print("Exiting...")
            sys.exit(1)
    else:
        result = r.text

    return result
