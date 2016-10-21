#!/usr/bin/env python3

import os
import sys
import signal
import argparse
import shlex

from kobato.commands import (
    login,
    post,
    show,
    subscribe,
    alias,
    feed,
    delete,
    comment,
    whitelist
)
import kobato.commands.config

from kobato.config import ConfigPrivate

from kobato.misc import terminated
from kobato.plugin import kobato_subparsers_register, kobato_format

from kobato import __version__

signal.signal(signal.SIGINT, lambda x, y: terminated())


def main():
    parser = argparse.ArgumentParser(description='Kobato — Command line interface for microblogging platform point.im.')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))

    config = ConfigPrivate()
    aliases = config.get('aliases', {})
    aliases = aliases.copy()

    subparsers = parser.add_subparsers(help='subcommands help', metavar='<command>')
    kobato_subparsers_register(subparsers, config, aliases)

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
