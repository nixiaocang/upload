#!/usr/bin/python

import os
import sys
import commands

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT = 'kst'

def set_env():
    cur_dir = sys.path[0]
    os.sys.path.append(os.path.join(cur_dir, 'src'))
    os.environ['PROJECT'] = PROJECT
    os.environ['CONF'] = os.path.join(cur_dir, 'conf')
    os.environ['SRC'] = os.path.join(cur_dir, 'src')

if __name__ == '__main__':
    set_env()
