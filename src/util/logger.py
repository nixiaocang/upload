#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import os
import logging
import logging.config
from config import Configuration
log_path = Configuration().get('global', 'log_path')
conf_file = os.path.join(os.getenv('CONF'), 'logging.conf')
logging.config.fileConfig(conf_file, defaults = {'log_path': log_path})


def sync_logger():
    return logging.getLogger('sync')


def receive_logger():
    return logging.getLogger('receive')


def task_logger():
    return logging.getLogger('task')


def runtime_logger():
    return logging.getLogger('runtime')

def api_logger():
    return  logging.getLogger('api')
