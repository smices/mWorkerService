#!/usr/bin/env python
# coding:utf-8
import sys
import os
from termcolor import cprint


def this_file_dir():
    """
    get file current path
    """
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def get_app_path(root_path=None):
    if root_path is None:
        root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path = dict()
    path['root'] = root_path
    path['conf'] = root_path + os.sep + "conf"
    path['task'] = root_path + os.sep + "task"
    path['lib'] = root_path + os.sep + "lib"
    path['3rd'] = root_path + os.sep + "3rd"
    path['tmp'] = root_path + os.sep + "tmp"

    return path


def qdebug(msg, debug=False):
    if debug is False:
        print "[DEBUG]", msg


def add_module_path(path):
    """
    Add path to module find path
    :param path:str
    :return:void
    """
    real_path = os.path.abspath(path)
    if os.path.isdir(real_path):
        if path not in sys.path:
            sys.path.append(real_path)


def isset(v):
    try:
        type(eval(v))
    except:
        return False
    else:
        return True


def config_reader(config_file, path):
    """
    Read config to dict
    :param config_file:
    :param path:
    :return:
    """
    from configobj import ConfigObj
    config_file = path + os.sep + config_file + ".conf"

    if os.path.isfile(config_file) is False:
        raise IOError, ("Config file (%s) not find,exit!" % config_file)

    config = ConfigObj(config_file, encoding='UTF8')

    if isset(config["setup"]["enable"]) and config["setup"]["enable"] == "0":
        raise AttributeError, "config setup enable is off"

    return config


def get_worker_config(worker_name, config_path=None):
    """
    Get worker config
    :param worker_name:str
    :param config_path:str
    :return:ConfigObj
    """
    try:
        if config_path is None:
            config = config_reader(worker_name, os.path.dirname(this_file_dir()) + os.sep + "conf")
        else:
            config = config_reader(worker_name, config_path)
    except IOError, ex:
        print "[FATAL ERROR]", ex
        sys.exit(0)
    except AttributeError, ex:
        print "[NOTICE ERROR]", ex
        sys.exit(0)
    return config


def scan_worker(directory, ext=".py"):
    """
    Scan Worker directory, fetch all worker class
    """
    worker_list = []
    for parent, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if os.path.splitext(filename)[1] == ext and os.path.splitext(filename)[0].endswith('Worker'):
                worker_list.append(os.path.splitext(filename)[0])
    return worker_list


def cmsg(message, type="normal", attrs=[]):
    type = type.lower()
    attrs.append("bold")
    if type in ["normal", "n"]:
        cprint(message, attrs=attrs)
    elif type in ["error", "e"]:
        cprint(message, "yellow", "on_red", attrs=attrs)
    elif type in ["warn", "w"]:
        cprint(message, "magenta", "on_yellow", attrs=attrs)
    elif type in ["info", "i"]:
        cprint(message, "white", "on_cyan", attrs=attrs)

