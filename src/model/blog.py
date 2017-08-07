#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.database import MySQLHelper
import util.tools as tools

class Blog():
    def __init__(self):
        self.db = MySQLHelper()

    def create(self, type, user_id, ds_id):
        task_id = tools.uniq_id('txt')
        sql = 'insert into blog (`task_id`, `type`, `owner`, `rela_id`) values ("%s", "%d", "%s", "%s")' % (task_id, 0, user_id, ds_id)
        self.db.query(sql)
        return task_id
    def get_one(self, text_id):
        sql = 'select * from blog where text_id="%s" and is_del=0' % text_id
        res = self.db.query(sql)
        return res[0]

    def get_list(self, user_id):
        sql = 'select * from blog where user_id="%s"' % user_id
        res = self.db.query(sql)
        return res


if __name__=='__main__':
    print Blog().get_list('jiaogf')

