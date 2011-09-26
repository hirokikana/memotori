# -*- coding: utf-8 -*-
import tornado.database
import redis

import sha
import random

##
# DB接続用Model
##
class DBModel(object):
    def __init__(self,settings):
        self.settings = settings
        self.connection = tornado.database.Connection(self.settings['db_host'],
                                                      self.settings['db_name'],
                                                      self.settings['db_user'],
                                                      self.settings['db_password'])
        self.table_name = self._get_table_name()
        
    def __del__(self):
        self.connection.close()

    def _get_table_name(self):
        raise NotImplementedError, 'require __get_table_name method in DBModel'

    def find_by_id(self, id):
        query = 'SELECT * FROM %s WHERE id = %%s;' % self.table_name
        return self.connection.get(query, id)

    def get_all(self):
        query = 'SELECT * FROM %s;' % self.table_name
        return self.connection.query(query)


class UserModel(DBModel):
    def _get_table_name(self):
        return 'user'

    def find_by_mail(self, mail):
        query = 'SELECT * FROM %s WHERE mail = %%s LIMIT 1' % self.table_name
        return self.connection.get(query, mail)

    def register(self, data):
        # data['name']/data['mail']/data['password']
        query = 'INSERT INTO %s (name, mail, password, create_date, update_date) VALUE (%%s, %%s, %%s, now(), now());' % self.table_name
        return self.connection.execute(query, data['name'], data['mail'], data['password'])

class MemoModel(DBModel):
    def _get_table_name(self):
        return 'memo'

    def insert_memo(self, data):
        # data['uid']/data['content']
        query = 'INSERT INTO %s (uid, content, create_date, update_date) VALUES (%%s, %%s, now(), now());' % self.table_name
        return self.connection.execute(query, data['uid'], data['content'])

    def find_by_userid(self, userid):
        query = 'SELECT * FROM %s WHERE uid = %%s;' % self.table_name
        return self.connection.query(query, userid)
        

class RedisModel(object):
    def __init__(self, settings):
        self.settings = settings
        self.connection = redis.Redis(host=self.settings['redis_host'],
                                      port=self.settings['redis_port'])

    def set_auth_cookie(self, uid):
        authcookie = sha.sha(str(random.random())).hexdigest() # TODO
        self.__set_auth(uid, authcookie);
        self.__set_user_auth(uid, authcookie)
        return authcookie

    def get_userid(self, authcookie):
        userid = self.__get_user_id(authcookie)
        if (userid and self.__get_user_authcookie(userid) == authcookie):
            return userid
        else:
            return None

    def __get_user_id(self, authcookie):
        key = '%s:%s' % (self.__get_redis_key('auth'), authcookie)
        return self.connection.get(key)

    def __get_user_authcookie(self, uid):
        key = '%s:%s' % (self.__get_redis_key('user_auth'), uid)
        return self.connection.get(key)

    def __set_user_auth(self, uid, authcookie):
        key = '%s:%s' % (self.__get_redis_key('user_auth'), uid)
        return self.connection.set(key, authcookie)
        
    def __set_auth(self, uid, authcookie):
        key = '%s:%s' % (self.__get_redis_key('auth'), authcookie)
        return self.connection.set(key, uid)
    
    def __get_redis_key(self, key):
        prefix = self.settings['redis_prefix']
        if (key == 'auth'):
            return '%sauth' % prefix
        elif (key == 'user_auth'):
            return '%suser_auth' % prefix
        return None
