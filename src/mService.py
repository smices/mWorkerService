#!/usr/bin/env python
# coding:utf-8
import getopt
import logging
import signal
from prettytable import PrettyTable
import multiprocessing
from lib.units import *
import cPickle as serialize
from termcolor import colored
import psutil

worker_list = []
worker_config_list = {}
master_pid = 0


def sigint_handler(signum, frame):
    stop()
    """
    for i in pid_list:
        os.kill(i, signal.SIGKILL)
    logging.info("exit...")
    """
    sys.exit()

# bind signal SIGINT process func
signal.signal(signal.SIGINT, sigint_handler)
#signal.signal(signal.SIGTERM, sigint_handler)


def usage():
    """
    显示 使用帮助
    """
    h = PrettyTable([u"可用参数", u"参数说明"])
    h.align[u"可用参数"] = "l"
    h.align[u"参数说明"] = "l"
    h.padding_width = 1
    h.add_row(["-h", u"显示帮助内容"])
    h.add_row(["-d", u"守护模式启动程序"])
    h.add_row(["-s", u"服务配置项 可用参数{start|stop|status|restart}"])

    print h
    sys.exit(0)


def master_pid(action="r", pid=None):
    action = action.lower()
    if action not in ["c", "r", "w", "d", "k"]:
        raise ValueError, "Action undefined!"
    pid_file = "./tmp/master_processor.pid"

    if action == "c":
        if os.path.isfile(pid_file):
            with open(pid_file) as fp:
                pid = int(fp.read().strip())
                try:
                    return psutil.Process(pid).is_running()
                except psutil.NoSuchProcess:
                    return False
        else:
            return False
    elif action == "r":
        try:
            with open(pid_file, 'r') as fp:
                pid = int(fp.read().strip())
                return pid
        except IOError:
            pid = None
        except ValueError:
            pid = None
        except SystemExit:
            pid = None
        return pid
    elif action == "w":
        if pid is None:
            pid = os.getpid()
        try:
            with open(pid_file, 'w+') as fp:
                fp.write(str(pid)+"\n")
                fp.flush()
            return pid
        except IOError:
            return None
    elif action == "k":
        psutil.Process(pid).terminal()
    elif action == "d":
        return os.remove(pid_file)


def processors_list(action="r", pid_list=None):
    action = action.lower()
    pfile = this_file_dir() + "/tmp/sub_processor.pid"
    if action == "r":
        if os.path.exists(pfile) is False:
            return False
        with open(pfile, 'r') as fp:
            result = serialize.load(fp)
        return result
    elif action == "w":
        if pid_list is None:
            return False
        try:
            with open(pfile, 'w+') as fp:
                fp.write(serialize.dump(pid_list, fp))
                fp.flush()
            return True
        except Exception:
            return False
    elif action == "k":
        if pid_list is not None:
            for pid in pid_list:
                psutil.Process(pid).terminal()

    elif action == "d":
        os.remove(pfile)


def enabled_worker():
    """
    scan enabled worker
    :return:list
    """
    worker_list = scan_worker("./conf", ".conf")
    try:
        for w in worker_list:
            worker_config_list[w] = config_reader(w, "./conf")
    except AttributeError:
        worker_list.remove(w)
        pass
    return worker_list, worker_config_list


def exec_worker(worker):
    #qdebug(worker)
    #return True
    import_str = "from task.worker import %s as inWorker" % worker



    try:
        exec import_str
    except ImportError, ex:
        print "Import Exception:\n[COMMAND] %s" % import_str
        print "[MESSAGE] ", ex
        sys.exit(0)

    # read config
    config = get_worker_config(worker, "./conf")
    print config
    inWorker.main(config)


def start(debug=False):
    #check master running
    if master_pid("c") is True:
        cmsg("Service master is running..., start action exit.", "error")
        sys.exit(0)

    try:
        worker_list, worker_config_list = enabled_worker()

        process_num = multiprocessing.cpu_count()*2

        pid_list = []
        pool = multiprocessing.Pool(processes=process_num)

        # worker_max = [int(worker_config_list[w]["setup"]["process_num"]) for w in worker_list]

        for w in worker_list:

            if int(worker_config_list[w]["setup"]["process_num"]) < process_num:
                max_worker = int(worker_config_list[w]["setup"]["process_num"])
            else:
                max_worker = process_num

            for i in xrange(max_worker):
                pool.apply_async(exec_worker, args=(w,))

            for i in multiprocessing.active_children():
                pid_list.append(i.pid)

        pid_list.append(os.getpid())

        write_master_pid = master_pid("w", os.getpid())
        write_subproc_pid = processors_list("w", pid_list)

        if (write_master_pid is None) or (write_subproc_pid is False):
            print "Have error, write master/subproc pid fail!"
            processors_list("k", pid_list)
            master_pid("k", os.getpid())
        else:
            pool.close()
            pool.join()
    except Exception, ex:
        print ex


def stop(debug=False):
    try:
        pid_list = processors_list("r")
        if pid_list is False:
            processors_list("d")
            master_pid("d")
            cmsg("Service not running.", "warn")
            sys.exit(0)

        for pid in pid_list:
            try:
                cmsg("Service (pid:%s) stopping...." % pid, "info")
                if psutil.Process(pid).is_running():
                    os.kill(pid, signal.SIGTERM)
                    os.kill(pid, signal.SIGINT)
                    os.kill(pid, signal.SIGKILL)
                    psutil.Process(pid).terminal()
            except psutil.NoSuchProcess:
                cmsg("Service (pid:%s) not running!" % pid, "warn")
        processors_list("d")
        master_pid("k")
        if master_pid("c") is False:
            master_pid("d")
        cmsg("Service all stoped!", "info")
    except IOError:
        cmsg("Service not running.", "error")
    except OSError:
        cmsg("Service not running.", "error")


def restart(debug=False):
    logging.info("restart...")


def status():
    """
    Fetch service status
    :return:
    """
    if master_pid("c") is True:
        print colored(" SERVICE IS RUNNING... ", "white", "on_blue")
        h = PrettyTable([u"进程ID", u"运行状态"])
        h.align[u"进程ID"] = "l"
        h.align[u"运行状态"] = "l"
        h.padding_width = 1
        pid_list = processors_list("r")
        for pid in pid_list:
            try:
                if psutil.Process(pid).is_running():
                    h.add_row([pid, colored("RUNNING...",attrs=["bold"])])
                else:
                    h.add_row([colored(pid, "magenta", "on_yellow", attrs=["bold"]),
                               colored("STOPED", "magenta", "on_yellow", attrs=["bold"])])
            except psutil.NoSuchProcess:
                h.add_row([colored(pid, "yellow", attrs=["bold", "blink"]),
                           colored("LOSTED", "red", attrs=["bold", "blink"])])
        print h
    else:
        cmsg("SERVICE IS STOPED!", "e")

def main(action, debug=False):
    action = action.lower()
    if action == "stop":
        stop()
    elif action == "start":
        start()
    elif action == "status":
        status()
    elif action == "restart":
        restart()
    else:
        cmsg("UNDEFINED ACTION", "error")

if __name__ == "__main__":
    import platform
    if platform.system() not in ['Linux', 'Darwin']:
        cmsg(u"\n\tSorry, not supported your (%s) system!" % platform.system(), "error")
        sys.exit(0)

    if len(sys.argv[1:]) == 0:
        usage()

    opts, args = getopt.getopt(sys.argv[1:], "hms:n:")

    for op, action in opts:
        if op == "-s":
            if action in ['start', 'stop', 'restart', 'status']:
                if "-m" in sys.argv:
                    cmsg("---"*10 + "DEBUGGING OPEN" + "---"*10, "i")
                    cmsg("[DO ACTION] %s" % str(action).upper(), "warn")
                    main(action)
                else:
                    main(action)
        elif op == "-h":
            usage()
            sys.exit()
