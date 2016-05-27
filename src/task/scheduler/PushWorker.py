#!/usr/bin/env python
# coding:utf-8
import sys
import imp
import redis
from rq import Queue
import random
from task.worker.PushWorker import push_messenger


def main(config, silent=False):
    """
    Job enqueue

    :param config:
    :return:
    """
    queue_dsn = config["queue"]["dsn"]
    redis_conn = redis.from_url(queue_dsn)

    q = Queue('low', connection=redis_conn)

    in_count = 0
    in_max = 99

    ret = []
    while in_count < in_max:
        result = q.enqueue(push_messenger, random.randint(1, 9999), result_ttl=60)
        ret.append(result)
        in_count += 1

    if silent is True:
        return ret
    else:
        print ret


if __name__ == '__main__':
    from lib.units import this_file_dir, config_reader

    main(config_reader("PushWorker", this_file_dir()))
