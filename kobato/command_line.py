#!/usr/bin/env python3

import os
import sys
import signal

from kobato.commands import login, post, show, subscribe

from kobato.misc import terminated, usage
from kobato.plugin import kobato_plugin_dispatch

signal.signal(signal.SIGINT, lambda x, y: terminated())

def main():
    
    if not(sys.argv[1:]) or (sys.argv[1] in ('-h', '--help', 'help')):
        usage()
    
    command = sys.argv[1]
    module_args = sys.argv[2:]
    
    kobato_plugin_dispatch(command, module_args)

if __name__ == '__main__':
    main()
