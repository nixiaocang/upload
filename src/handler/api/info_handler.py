#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handler.base_handler import BaseHandler
from model.blog import Blog


class InfoHandler(BaseHandler):

    def do_action(self):
        args = self.get_args([
            ('text_id', str, None),
        ])
        text_id = args.get('text_id')
        self.result = Blog().get_one(text_id)
        return True
