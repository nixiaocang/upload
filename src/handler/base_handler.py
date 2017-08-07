#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import sys
import json
import ERROR
import tornado.web
import tornado.ioloop
from tornado.web import RequestHandler
from tornado.gen import coroutine
from tornado.gen import Task
from util.tools import print_stack

reload(sys)
sys.setdefaultencoding('utf-8')


class IllegalArgumentException(Exception):
    pass


class BaseHandler(RequestHandler):

    datatype = 'json'
    error_code = ERROR
    SUCCESS_FLAG = 'success'

    @coroutine
    def get(self):
        yield Task(self.run)
        self.do_response()

    @coroutine
    def post(self):
        yield Task(self.run)
        self.do_response()

    def do_response(self):
        if self.datatype == 'json':
            self.add_header("Content-Type", "application/josn;charset=utf-8")
            data = {
                'status': str(self.status),
                'errstr': self.errstr,
                'result': self.result,
            }
            self.write(json.dumps(data))
        else:
            self.write(self.result)

    @coroutine
    def run(self, *args, **kwargs):
        try:
            self.do_action()
        except IllegalArgumentException, ie:
            self.send_error(self.error_code.MISSING_ARGUMENT, ie.message)
            print_stack()
        except Exception, e:
            self.set_error(self.error_code.UNKNOW_ERROR, e.message)
            self.ext_log_data.append(e.message)
            print_stack()

    def prepare(self):
        self.request_start_time = time.time()
        self.today = time.strftime('%Y%m%d')
        self.status = 0
        self.errstr = ''
        self.result = ''
        self.ext_log_data = []

    def set_error(self, err_code, err_str, result=''):
        self.status = '%s' % err_code
        self.errstr = err_str
        self.result = result

    def do_action(self):
        return True

    def get_log_info(self):
        try:
            real_ip = self.request.headers.get('X-Real-Ip') or self.request.remote_ip
            cost_time = int((time.time() - self.request_start_time) * 1000)
            log = '\t'.join(["%s"] * 9) % (
                real_ip,
                self.request.method,
                self.request.path,
                '&'.join(["%s=%s" % (i, self.get_argument(i)[0:1000]) for i in self.request.arguments.keys()]),
                self.request.headers['User-Agent'],
                self.status,
                self.errstr,
                cost_time,
                '|'.join(self.ext_log_data)
            )
            return log
        except Exception, e:
            return 'error when logging: %s' % repr(e)

    def get_status(self):
        return self.status

    def get_args(self, arg_list):
        kv = {}
        for arg in arg_list:
            (arg_name, arg_cast, arg_default) = arg
            v = self.get_argument(arg_name, None)
            if not v:
                if arg_default is None:
                    raise IllegalArgumentException("argument %s is missing" % arg_name)
                else:
                    kv[arg_name] = arg_default
                    continue
            if arg_cast:
                try:
                    v = arg_cast(v)
                except Exception as e:
                    raise IllegalArgumentException("argument %s type mismatch, data->(%s), exception:%s" % (arg_namem, v, e))
            kv[arg_name] = v
        return kv
