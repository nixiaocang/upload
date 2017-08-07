#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests
from requests.exceptions import ConnectionError
from util.config import Configuration
class OverloadException(Exception):

    def __init__(self, status, errstr, uri=""):
        self.status = status
        self.errstr = errstr
        self.uri = uri

    def __str__(self):
        return self.errstr


class OpendsToken():

    def _request(self, url, data):
        retry = 0
        while retry < 5:
            try:
                res = requests.post(url, data=data)
                break
            except ConnectionError as e:
                retry += 1
                time.sleep(2)
                if retry == 5:
                    raise e

        try:
            result = res.json()
        except:
            raise OverloadException('500', 'no result returned from overload server', url)

        if result['status'] != 0:
            raise OverloadException(result['status'], result['errstr'], url)

        return result['result']

    def get_token(self, user_id):
        url = Configuration.get('overlord', 'url')
        data = {"user_id":user_id}
        res = self._request(url, data)
        return res.get('token')




