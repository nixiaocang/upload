#!/usr/bin/env python
# -*- coding:utf-8 -*-

from util.config import Configuration
from util.tools import print_stack
from util.logger import api_logger
import MySQLdb


class MySQLHelper:
    def __init__(self):
        self.logger = api_logger()
        try:
            self.conf = Configuration().get_section('blog')
            self.db = MySQLdb.connect(host=self.conf['host'], user=self.conf['user'], passwd=self.conf['passwd'], db=self.conf['db'], charset=self.conf['charset'])
        except Exception,e:
            self.logger.error(e.message)
            raise e

    def query(self, sql):
        cur =  self.db.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        res = cur.fetchall()
        result = []
        for item in res:
            if 'ctime' in item.keys():
                item['ctime'] = str(item['ctime'])
            result.append(item)
        cur.close()
        self.db.commit()
        self.db.close()
        return result

    def query_one(self, sql):
        res = self.query(sql)
        result = [item  for item in res]
        return result.pop() if result else {}

    def update(self, sql):
        try:
            cur = self.db.cursor()
            cur.execute(sql)
            cur.close()
            self.db.commit()
        except:
            return False
        finally:
            self.db.close()
        return True

