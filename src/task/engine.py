#!/usr/bin/env python
# -*- coding:utf-8 -*-

from util.logger import task_logger
from helper.token_helper import OpendsToken
from helper.sync_data import SyncData

class KstEngine(object):
    def __init__(self, info):
        self.task_info = info
        self.logger = task_logger()

    def do(self):
        user_id = self.task_info['owner']
        token = "05be5244dbbe5ce45eaac6eb8adccf39" #OpendsToken().get_token(user_id)
        SyncData(user_id, token).run()
