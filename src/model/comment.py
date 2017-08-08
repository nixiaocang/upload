#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.database import MySQLHelper
import util.tools as tools

class Comment():
    def __init__(self):
        self.db = MySQLHelper()

    def create(self, bag):
        cmt_id = tools.uniq_id('cmt')
        sql = "INSERT INTO `comment` (`text_id`, `cmt_id`, `email`, `subject`, `comment`) VALUES ('%s', '%s', '%s', '%s', '%s');" % (bag['text_id'], cmt_id, bag['email'], bag['subject'], bag['comment'])
        self.db.query(sql)
        return cmt_id

    def get_all(self, text_id):
        sql = 'select * from comment where text_id="%s" and is_del=0' % text_id
        res = self.db.query(sql)
        return res


if __name__=='__main__':
    print Blog().get_list('jiaogf')

