#!/usr/bin/env python3

import os
import sys
import signal
import argparse
import shlex

from kobato.commands import login, post, show, subscribe, alias, feed
from kobato.config import ConfigPrivate

from kobato.misc import terminated
from kobato.plugin import kobato_subparsers_register, kobato_format

signal.signal(signal.SIGINT, lambda x, y: terminated())


def main():
    parser = argparse.ArgumentParser(description='Kobato — Command line interface for microblogging platform point.im.',
                                     usage='%(prog)s [-h] COMMAND [-h] [options...]')  # because default usage is crap

    config = ConfigPrivate()

    subparsers = parser.add_subparsers(help='subcommands help', metavar='')
    kobato_subparsers_register(subparsers, config)

    aliases = []
    if 'aliases' in config:
        aliases = config['aliases']

    sysargs = sys.argv[1:] if len(sys.argv) > 1 else ['-h']

    # TODO: I just do not want to create dummy subparser "help"
    if sysargs[0] == 'help':
        sysargs[0] = '--help'

    if sysargs[0] in aliases:
        command = sysargs[0]
        try:
            result = kobato_format(aliases[command], *sysargs[1:])
        except IndexError:
            print("ERROR: not enough arguments for alias")
            sys.exit(1)

        print("Alias resolved:", result)
        print("Executing...")
        result = shlex.split(result)

        sysargs = result

    args = parser.parse_args(sysargs)

    # TODO: sometimes we need to show help in case of no parameters
    args.func(vars(args))

if __name__ == '__main__':
    main()
