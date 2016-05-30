#!/usr/bin/env python
# coding:utf-8
import os
import sys
import redis
import logging
from rq import Worker, Queue, Connection
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    from lib.units import *
except ImportError:
    pass


worker_config = None

def push_messenger(message_body):
    global worker_config
    try:
        from baidubce.services.sms import sms_client as sms
        from baidubce import exception as ex
        from baidubce.bce_client_configuration import BceClientConfiguration
        from baidubce.auth.bce_credentials import BceCredentials
    except ImportError:
        print "Path error!!"
        print sys.path
        sys.exit()

    if worker_config is not None:
        app_path = get_app_path()
        worker_config = get_worker_config("SMSWorker", app_path['conf'])

    HOST = worker_config['app']['HOST']
    AK = worker_config['app']['AK']
    SK = worker_config['app']['SK']

    logger = logging.getLogger('baidubce.services.sms.smsclient')
    fh = logging.FileHandler('sms_sample.log')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    bce_config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
    logging.basicConfig(level=logging.DEBUG, filename='./sms.log', filemode='w')
    LOG = logging.getLogger(__name__)

    sms_client = sms.SmsClient(bce_config)
    try:
        """
        # query template list
        LOG.debug('Query template list')
        response = sms_client.get_template_list()
        valid_template_id = None
        valid_template_content = None
        for temp in response.template_list:
            print temp.template_id, temp.name, temp.content, \
                    temp.status, temp.create_time, temp.update_time
            if temp.status == u'VALID':
                valid_template_id = temp.template_id
                valid_template_content = temp.content
        """

        LOG.debug('Send Message')
        response = sms_client.send_message('smsTpl:8504139f-2b8e-49f3-adc4-957b8b3bfa67',
                                           [message_body],
                                           {'username': "睡你大爷起来嗨,Python~"})
        message_id = response.message_id
        return message_id

        """
        #query message
        LOG.debug('query Message')
        response = sms_client.query_message_detail(message_id)

        print response.message_id, response.receiver, response.content, response.send_time
        """

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, msg: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)


def main(config):
    global worker_config
    worker_config = config

    listen = config["listen"].values()

    queue_dsn = config["queue"]["dsn"]

    conn = redis.from_url(queue_dsn)

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


if __name__ == '__main__':
    sys.path.append("../../")
    from lib.units import *
    app_path = get_app_path()
    app_path.pop("tmp")
    app_path['baidubce'] = app_path['lib'] + os.sep + 'baidubce'
    for key in app_path:
        add_module_path(app_path[key])
    worker_name = os.path.splitext(__file__)[0]
    config = get_worker_config(worker_name, "../../conf")
    print config["listen"]
    main(config)
