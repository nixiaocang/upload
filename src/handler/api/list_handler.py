#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handler.base_handler import BaseHandler
from model.blog import Blog


class ListHandler(BaseHandler):

    def do_action(self):
        args = self.get_args([
            ('user_id', str, None),
        ])
        user_id = args.get('user_id')
        self.result = Blog().get_list(user_id)
        return True
