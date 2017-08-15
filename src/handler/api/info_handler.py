#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handler.base_handler import BaseHandler
from model.blog import Blog
from model.comment import Comment


class InfoHandler(BaseHandler):

    def do_action(self):
        args = self.get_args([
            ('text_id', str, None),
        ])
        text_id = args.get('text_id')
        res = Blog().get_one(text_id)
        comment = Comment().get_all(text_id)
        res['comment'] = comment
        read = res['read'] + 1
        Blog().update_read(text_id, read)
        self.result = res
        return True
