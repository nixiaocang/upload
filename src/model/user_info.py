#!/usr/bin/env python
# -*- coding:utf-8 -*-

import lib.database


class UserInfoModel():

    def __init__(self):
        self.db = lib.database.TassadarPool()

    def get(self, user_id):
        sql = 'select * from KST_INFO where user_id="%s" is_del=0' % user_id
        return self.db.query(sql)
