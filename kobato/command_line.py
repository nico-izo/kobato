#!/usr/bin/env python3

import os
import sys
import signal

from kobato.commands import login, post, show, subscribe, alias
from kobato.config import ConfigPrivate

from kobato.misc import terminated, usage
from kobato.plugin import kobato_plugin_dispatch

signal.signal(signal.SIGINT, lambda x, y: terminated())

def main():
    if not(sys.argv[1:]) or (sys.argv[1] in ('-h', '--help', 'help')):
        usage()

    config = ConfigPrivate
    command = sys.argv[1]
    module_args = sys.argv[2:]

    kobato_plugin_dispatch(command, module_args, config)

if __name__ == '__main__':
    main()
