#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import time

import requests
from requests.exceptions import ConnectionError

from helper.task_queue import TaskQueue
from model.task import TASK
from util.config import Configuration
from util.logger import runtime_logger


class KstHelper():
    def _request(self, url, params):
        res = None
        retry = 0
        while retry < 5:
            try:
                res = requests.post(url, data=params)
                break
            except ConnectionError as e:
                retry += 1
                time.sleep(2)
                if retry == 5:
                    runtime_logger().error("请求url:%s历史数据时出现错误:%s" % (url, e.message))
                    raise e
        return res

    def sync_data(self, user_id, token, ds_id):
        # token = OpendsToken().get_token(user_id)
        task_id = TASK().create(TASK.KST_TYPE, user_id, ds_id)
        TaskQueue().push(task_id, TaskQueue.KST_TYPE)
        return task_id

    def req_hdata(self, user_id, compId, ak, kst_url, data):
        tt = int(time.time() * 10000)
        data['tt'] = str(tt)
        hprefix = Configuration().get('url_prefix', 'hprefix')
        pu = hprefix + '?user_id="%s"&compId="%s"' % (user_id, compId)
        params = {
            "ak": ak,
            "tt": str(tt),
            "pu": pu,
            "pt": "HISTORYDATA",
        }
        kssign = self.gen_sign(data)
        params['kssign'] = kssign
        res = self._request(kst_url, params)
        result = json.loads(res.content)
        runtime_logger().info("用户:%s请求历史访客信息返回结果:%s" % (user_id, res.content))
        conn_res = self.deal_res(result)
        return conn_res

    def req_vdata(self, user_id, compId, ak, kst_url, data):
        tt = int(time.time() * 10000)
        data['tt'] = str(tt)
        vprefix = Configuration().get('url_prefix', 'vprefix')
        pu = vprefix + '?user_id="%s"&compId="%s"' % (user_id, compId)
        params = {
            "ak": ak,
            "tt": str(tt),
            "pu": pu,
            "pt": "VISITORCARD",
        }
        kssign = self.gen_sign(data)
        params['kssign'] = kssign
        res = self._request(kst_url, params)
        result = json.loads(res.content)
        runtime_logger().info("用户:%s请求历史名片信息返回结果:%s" % (user_id, res.content))
        conn_res = self.deal_res(result)
        return conn_res

    def deal_res(self, result):
        conn_res = {}
        if result.get('statusCode') == 8:
            conn_res['status'] = 0
        else:
            conn_res['status'] = result.get('statusCode')
            conn_res['msg'] = result.get('msg')
        print conn_res
        return conn_res

    def gen_sign(self, data):
        vs = [data['ak'], data['as'], data['at'], data['tt']]
        vs.sort()
        s = vs[0] + vs[1] + vs[2] + vs[3]
        sha1obj = hashlib.sha1()
        sha1obj.update(s)
        s = sha1obj.hexdigest()
        return s

    def req_again(self, kst):
        kst_url = kst['url'] + '/bs/ksapi/repush.do'
        data = {
            "ak": kst['ak'],
            "as": kst['as'],
            "at": kst['at'],
            "vt": "MD5",
        }
        self.req_hdata(kst['user_id'], kst['compId'], kst['ak'], kst_url, data)
        self.req_vdata(kst['user_id'], kst['compId'], kst['ak'], kst_url, data)


