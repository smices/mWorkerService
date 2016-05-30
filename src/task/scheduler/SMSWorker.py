#!/usr/bin/env python
# coding:utf-8
import redis
from rq import Queue
from task.worker.SMSWorker import push_messenger


def main(msg, config=None, silent=False):
    """
    Job enqueue
    :param msg:str
    :param config:object
    :return:
    """
    queue_dsn = config["queue"]["dsn"]
    redis_conn = redis.from_url(queue_dsn)

    q = Queue('high', connection=redis_conn)
    ret = q.enqueue(push_messenger, msg, result_ttl=60)
    print ret
    return ret


if __name__ == '__main__':
    from lib.units import this_file_dir, config_reader, _app_root_dir
    print _app_root_dir

    main("13751015906", config_reader("SMSWorker", this_file_dir()))
