#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handler.base_handler import BaseHandler
from model.blog import Blog
from model.comment import Comment


class SaveHandler(BaseHandler):

    def do_action(self):
        args = self.get_args([
            ('content', str, None),
            ('user_id', str, None),
        ])
        text_id = self.get_argument('text_id', None)
        if text_id:
            Blog().modify(text_id, args['content'])
        else:
            text_id = Blog().create(args)
        self.result = text_id
        return True
