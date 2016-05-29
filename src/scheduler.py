#!/usr/bin/env python
# coding:utf-8
import sys
import os
import platform
import getopt

from prettytable import PrettyTable as PTable
from lib.units import *


_dir_config = this_file_dir()+"/conf"
_dir_scheduler = this_file_dir()+"/task/scheduler"
_dir_worker = this_file_dir()+"/task/worker"

add_module_path(_dir_scheduler)
add_module_path(_dir_worker)


def usage():
    """
    Usage
    """
    print "+" + "-" * 40 + "+"
    print "| 测试执行 Worker 数据插入"
    print "+" + "-" * 40 + "+"
    print "| 请使用如下命令执行:"
    print "| ./%s -m module_name" % os.path.basename(__file__)
    print "+" + "-" * 40 + "+"

    worker_list = scan_worker(_dir_scheduler)
    h = PTable([u"可用参数", u"参数说明"])
    h.align[u"可用参数"] = "l"
    h.align[u"参数说明"] = "l"
    h.padding_width = 1
    h.add_row(["-h", u"显示帮助内容"])
    h.add_row(["-m", u"执行 Worker 导入"])
    print h

    m = PTable([u"可选模块名称", u"模块配置文件"])
    m.align[u"可选模块名称"] = "l"
    m.align[u"模块配置文件"] = "l"
    m.padding_width = 1

    for work in worker_list:
        m.add_row([work, this_file_dir() + "/conf" + os.sep + work + ".conf"])
    print m

    sys.exit(0)


def run(worker):
    """
    Run Worker Module main
    :param worker:
    :return:
    """
    os.system("clear")

    import_str = "from task.scheduler import %s as inWorker" % worker

    try:
        exec import_str
    except ImportError, ex:
        print "Import Exception:\n[COMMAND] %s" % import_str
        print "[MESSAGE] ", ex
        sys.exit(0)

    # read config
    config = get_worker_config(worker, _dir_config)
    inWorker.main(config)


def insert(worker, data=None):
    """
    insert a record to worker queue
    :param worker:
    :return:
    """

    import_str = "from task.scheduler import %s as inWorker" % worker

    try:
        exec import_str
    except ImportError, ex:
        outstr = "Import Exception:\n[COMMAND] %s" % import_str
        outstr += "[MESSAGE] ", ex
        return outstr
    except Exception, ex:
        return "[MESSAGE] ", ex

    # read config
    config = get_worker_config(worker, _dir_config)
    return inWorker.main(config, silent=True, data=data)


if __name__ == '__main__':
    if platform.system() not in ['Linux', 'Darwin']:
        print (u"\n\tSorry, not supported your (%s) system!" % platform.system())*10
        sys.exit(0)

    if len(sys.argv[1:]) == 0:
        # 没有参数就显示帮助文档
        usage()

    opts, args = getopt.getopt(sys.argv[1:], "hm:")

    for op, var in opts:
        if op == "-m":
            if var in scan_worker(_dir_scheduler):
                run(var)
            else:
                usage()
        elif op == "-h":
            usage()

