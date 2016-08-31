Kobato — Point.im Command Line Interface
=============

[![Build Status](https://travis-ci.org/nico-izo/kobato.svg?branch=master)](https://travis-ci.org/nico-izo/kobato)

## Description
`kobato` is a command-line interface for [Point.im](https://point.im/) microblogging platform. It uses official API, so you can do all the things that are there. But for now you can only do only limited set of things.

## Demo

![cool gif](http://i.imgur.com/yZjgNy7.gif)

## Requirements

- Python 3.5 (haven't tested it under anything else, but it should be fine down to 3.3)
- requests
- decorating
- appdirs

## Installation

- From pipy:
    * `sudo pip3 install kobato`
- Manual
    * `git clone https://github.com/nico-izo/kobato.git`
    * `cd kobato`
    * `virtualenv ~/.virtualenvs/kobato`
    * `source ~/.virtualenvs/kobato/bin/activate`
    * `pip3 install .`



## Dive into Point

- Login:
    * `kobato login`
- Post
    * `kobato post`
- Quick post
    * `kobato post -t tag -t tag2 -m 'message' -f`
- Show post
    * `kobato show -p#da`
- Show post with replies
    * `kobato show -p#vhbne -r | less`
- Show user
    * `kobato show -u@arts`
- Aliases
    * `kobato alias --create anime_art "post -fy -t anime_art -m'{0}' {...}"`
- Exit point and remove your login/password from config
    * `kobato login --reset`

## License

GPLv3. All hail Stallman!
