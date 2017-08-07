#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime

from pymongo import MongoClient
from util.config import Configuration


class MongoModel(object):
    def __init__(self):
        conf = Configuration()
        self.connect_string = conf.get("mongo", "connect_string")
        self.db_name = conf.get("mongo", "database")
        self.conn = MongoClient(self.connect_string)
        self.db = self.conn[self.db_name]

    def __init_conn(self):
        return MongoClient(self.connect_string)

    def save(self, table, data):
        tdata = self.db[table]
        tdata.insert(data)
        return True

    def find(self, table, user_id):
        res = self.db[table].find({"user_id": user_id})
        return res

    def find_visitorId(self, user_id, compId, start_date, end_date):
        date_list = self.date_list(start_date, end_date)
        visitor = set()
        for date in date_list:
            tbname = 'vdata_%s' % date
            res = self.db[tbname].find({"user_id": user_id, "compId": compId})
            for item in res:
                visitor.add(item.get('visitorId'))
        return list(visitor)

    def date_list(self, start_date, end_date):
        date_list = []
        if start_date == end_date:
            res = start_date.replace('-', "")
            date_list.append(res)
        else:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            days = (end_date - start_date).days
            for i in range(days + 1):
                res = str(start_date + datetime.timedelta(days=i)).replace('-', "")
                date_list.append(res)
        return date_list
