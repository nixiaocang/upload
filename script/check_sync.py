#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import time
from lib.database import TassadarPool
from helper.kst_helper import KstHelper

reload(sys)
sys.setdefaultencoding('utf-8')


def get_kstds():
    sql = "select user_id, ds_id, token from KST_INFO where is_del=0"
    res = TassadarPool().query(sql)
    for kst in res:
        yield  kst


def main():

    for kst in get_kstds():
        task_id = KstHelper.sync_data(kst['user_id'], kst['token'], kst['ds_id'])

if __name__ == '__main__':
    print "start exec: %s" % time.time()
    main()
    print "end exec: %s" % time.time()


