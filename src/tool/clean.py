#!/usr/bin/env python
import os
import sys
import glob


def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def find_cruft(path, extensions=['.pyc', '.pyo', '.log']):
    for cfile in glob.glob(os.path.join(path, '*')):
        if os.path.isdir(cfile):
            for cruft in find_cruft(cfile):
                yield cruft
        fname, ext = os.path.splitext(cfile)
        if ext in extensions:
            yield cfile


def main(path):
    for i in find_cruft(path):
        os.unlink(i)

if __name__ == '__main__':
    path = os.path.dirname(cur_file_dir())
    print path
    main(path)
