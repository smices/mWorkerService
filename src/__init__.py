#!/usr/bin/env python
# coding:utf-8
import sys
import os


def current_file_path():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

_APP_DIR_ROOT = current_file_path()
_APP_DIR_LIB = _APP_DIR_ROOT + os.sep + "lib"
_APP_DIR_TASK = _APP_DIR_ROOT + os.sep + "task"
_APP_DIR_SCHEDULER = _APP_DIR_TASK + os.sep + "scheduler"
_APP_DIR_WORKER = _APP_DIR_TASK + os.sep + "worker"

sys.path.append(_APP_DIR_ROOT)
sys.path.append(_APP_DIR_LIB)
sys.path.append(_APP_DIR_TASK)
sys.path.append(_APP_DIR_SCHEDULER)
sys.path.append(_APP_DIR_WORKER)

