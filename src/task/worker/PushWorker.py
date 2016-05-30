#!/usr/bin/env python
# coding:utf-8
import redis
from rq import Worker, Queue, Connection
import fcntl


def push_messenger(message_body):
    fp = open("./push_messenger.log", "a")
    fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
    fp.write(str(message_body) + "\n")
    fp.close()
    return message_body


def main(config=None):

    listen = config["listen"].values()

    queue_dsn = config["queue"]["dsn"]

    conn = redis.from_url(queue_dsn)

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


if __name__ == '__main__':
    import os
    import sys
    sys.path.append("../../")
    from lib.units import get_worker_config

    worker_name = os.path.splitext(__file__)[0]

    config = get_worker_config(worker_name, "../../conf")
    print config["listen"]
    main(config)
