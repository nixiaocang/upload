#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.database import MySQLHelper
import util.tools as tools

class Blog():
    def __init__(self):
        self.db = MySQLHelper()

    def create(self, args):
        text_id = tools.uniq_id('text')
        sql = "INSERT INTO `blog` (`user_id`, `text_id`, `content`, `title`, `subtitle`) VALUES ('%s', '%s', '%s', '%s', '%s')" % (args['user_id'], text_id, args['content'], args['title'], args['subtitle'])
        self.db.query(sql)
        return text_id

    def modify(self, text_id, args):
        sql = "update blog set content='%s', title='%s', subtitle='%s' where text_id='%s'" % (args['content'], args['title'], args['subtitle'], text_id)
        res = self.db.query(sql)
        return text_id
    def get_one(self, text_id):
        sql = 'select * from blog where text_id="%s" and is_del=0' % text_id
        res = self.db.query(sql)
        return res[0]

    def get_list(self, user_id):
        sql = 'select * from blog where user_id="%s" and is_del=0' % user_id
        res = self.db.query(sql)
        return res

    def update_read(self, text_id, read):
         sql = "update blog set `read`=%s where text_id='%s'" % (read, text_id)
         res = self.db.query(sql)
         return text_id

if __name__=='__main__':
    print Blog().get_list('jiaogf')

