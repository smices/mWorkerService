#!/usr/bin/env python
# coding:utf-8
import sys
import imp
import redis
from rq import Queue
import random
from task.worker.PushWorker import push_messenger


def main(msg, config, silent=False):
    """
    Job enqueue
    :param msg:str
    :param config:
    :return:
    """
    queue_dsn = config["queue"]["dsn"]
    redis_conn = redis.from_url(queue_dsn)

    q = Queue('low', connection=redis_conn)

    ret = q.enqueue(push_messenger, msg, result_ttl=60)

    if silent is True:
        return ret
    else:
        print ret


if __name__ == '__main__':
    from lib.units import this_file_dir, config_reader

    main(config_reader("mServiceWorker", "PushWorker", this_file_dir()))
