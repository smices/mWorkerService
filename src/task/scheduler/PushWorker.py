#!/usr/bin/env python
# coding:utf-8
import sys
import imp
import redis
from rq import Queue
import random
from task.worker.PushWorker import push_messenger


def main(config, silent=False, data=None):
    """
    Job enqueue

    :param config:
    :return:
    """
    queue_dsn = config["queue"]["dsn"]
    redis_conn = redis.from_url(queue_dsn)

    q = Queue('low', connection=redis_conn)

    ret = []
    result = q.enqueue(push_messenger, data, result_ttl=60)
    ret.append(result)

    if silent is True:
        return ret
    else:
        print ret


if __name__ == '__main__':
    from lib.units import this_file_dir, config_reader

    main(config_reader("PushWorker", this_file_dir()))
