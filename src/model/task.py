#!/usr/bin/env python
# -*- coding:utf-8 -*-

import lib.database
import util.tools as tools

class TASK():
    def __init__(self):
        self.db = lib.database.TassadarPool()

    def create(self, type, user_id, ds_id):
        task_id = tools.uniq_id('task') 
        sql = 'insert into TASK (`task_id`, `type`, `owner`, `rela_id`) values ("%s", "%d", "%s", "%s")' % (task_id, 0, user_id, ds_id)
        self.db.query(sql)
        return task_id
    def get_one(self, task_id):
        sql = 'select * from TASK where task_id="%s" and is_del=0' % task_id
        res = self.db.query(sql)
        print res
        return res[0]

    def get_all()

