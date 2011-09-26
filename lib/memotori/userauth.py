# -*- coding: utf-8 -*-
import redis
import memotori.model
import sha

class RedisAuthMixin(object):
    def get_current_user(self):
        authcookie = self.get_cookie('auth', None)
        if authcookie:
            redis_model = memotori.model.RedisModel(self.settings)
            userid = redis_model.get_userid(authcookie)
            return userid


class AuthenticateLogic(object):
    def __init__(self, settings):
        self.settings = settings
        self.user_model = memotori.model.UserModel(self.settings)
        self.redis_model = memotori.model.RedisModel(self.settings)

    def auth(self, mail, password):
        if self.__get_password_hash(mail) == self.__generate_password_hash(password):
            # 認証成功
            result = self.user_model.find_by_mail(mail)
            uid = int(result['id'])
            # authcookieをセット
            authcookie = self.redis_model.set_auth_cookie(uid)
            # authcookieをcookieにセット
            return authcookie
        else:
            # 認証失敗
            return None

    def logout(self, authcookie):
        if authcookie:
            self.redis_model

    def register(self, data):
        data['password'] = self.__generate_password_hash(data['password'])
        return self.user_model.register(data)

    def __get_password_hash(self, mail):
        result = self.user_model.find_by_mail(mail)
        
        if (result):
            return result['password']
        return None

    def __generate_password_hash(self, password):
        password_hash = sha.sha(password + self.settings['password_salt']).hexdigest()
        return password_hash
