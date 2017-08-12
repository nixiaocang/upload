#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.database import MySQLHelper
import util.tools as tools

class Blog():
    def __init__(self):
        self.db = MySQLHelper()

    def create(self, args):
        text_id = tools.uniq_id('text')
        sql = "INSERT INTO `blog` (`user_id`, `text_id`, `content`) VALUES ('%s', '%s', '%s')" % (args['user_id'], text_id, args['content'])
        self.db.query(sql)
        return text_id
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

