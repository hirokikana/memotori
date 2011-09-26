#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import logging

import tornado.locale
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.autoreload import start as restarter

import datetime
import ConfigParser

import logging

sys.path.append('lib/')
import memotori.handlers

class Application(tornado.web.Application):
    def __init__(self):
        settings = self.__load_config()
        handlers = [
            (r'/', memotori.handlers.TopHandler),
            (r'/login', memotori.handlers.LoginHandler),
            (r'/logout', memotori.handlers.LogoutHandler),
            (r'/user/(.*)', memotori.handlers.UserHandler),
            # (r'/category/(.*)', CategoryHandler),
            (r'/memo/(.*)', memotori.handlers.MemoHandler),
            # (r'/friend/(.*)', FriendHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            ]
        tornado.web.Application.__init__(self, handlers, **settings)

    def __load_config(self):
        # 読み込み
        config_path = '%s/memotori.config' % os.path.abspath(os.path.dirname(__file__))
        parser = ConfigParser.ConfigParser()
        parser.read(config_path)

        ## evalして実行後の値があるものについては実行後の値を入れる
        config_dict = parser._sections['global']
        config = {}
        for key in config_dict.keys():
            try:
                value = eval(config_dict[key])
            except Exception,e:
                value = config_dict[key]
            config[key] = value

        return config

    def setup_logger(self):
        settings = self.settings
        logger = logging.getLogger()
        handler = logging.FileHandler('%s/memotori.log' % settings['log_dir'], 'a')
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.log = logger

if __name__ == '__main__':
    application = Application()
    application.listen(application.settings['listen_port'])
    loop = tornado.ioloop.IOLoop.instance()
    tornado.options.parse_command_line()
    application.setup_logger()
    restarter(loop)
    loop.start()
    
