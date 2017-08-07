#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import time
from lib.database import TassadarPool
from helper.kst_helper import KstHelper

reload(sys)
sys.setdefaultencoding('utf-8')

def get_url():
    sql = "select * from KST_INFO where is_del=0 and is_create=1"
    res = TassadarPool().query(sql)
    print res
    for kst in res:
        yield kst


def main():
    for kst in get_url():
        KstHelper().req_again(kst)

if __name__ == '__main__':
    print "start request kst: %s" % time.time()
    main()
    print "end request kst: %s" % time.time() 
