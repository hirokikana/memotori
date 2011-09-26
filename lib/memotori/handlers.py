# -*- coding:utf-8 -*-
from tornado.web import RequestHandler,authenticated
from memotori.userauth import RedisAuthMixin, AuthenticateLogic
import memotori.model
import json
import logging

from xml.etree.ElementTree import Element, SubElement, Comment, tostring

class BaseHandler(RedisAuthMixin, RequestHandler):
    def initialize(self):
        ## 必要なパラメーターをすべて入れておく
        key_list = ['next', 'username', 'password', 'userid', 'userinfo']
        self.param = {}
        for key in key_list:
            self.param[key] = self.get_argument(key, '')
        self.param['userid'] = self.get_current_user()
            
        # ユーザー情報を入れる
        if self.param['userid']:
            self.user_model = memotori.model.UserModel(self.settings)
            self.param['userinfo'] = self.user_model.find_by_id(self.param['userid'])
        else:
            self.param['userinfo'] = {}


class LogoutHandler(BaseHandler):
    def get(self):
        auth_logic = AuthenticateLogic(self.settings)

        authcookie = self.get_cookie('auth')
        auth_logic.logout(authcookie)
        
        self.set_cookie('auth', '')
        self.redirect('/')
        
        
class LoginHandler(BaseHandler):
    def get(self):
        # ログイン画面表示
        param = self.param
        self.render('login.html',**param)

    def post(self):
        # ログイン処理
        param = self.param

        auth_logic = AuthenticateLogic(self.settings)
        authcookie = auth_logic.auth(param['username'], param['password'])
        if authcookie:
            self.set_cookie('auth', authcookie)
            self.redirect('/');
        else:
            self.render('login.html',**param)


class TopHandler(BaseHandler):
    def get(self):
        userid = self.get_current_user()
        param = self.param
        if (userid):
            # 認証済み
            pass
        else:
            # 認証していない
            pass
        
        self.render('top.html',**param)
            

class UserHandler(BaseHandler):
    def get(self, path):
        param = self.param
        self.render('user.html', **param)

    def post(self, path):
        # ユーザー登録
        auth_logic = AuthenticateLogic(self.settings)
        
        mail = self.get_argument('mail', None)
        name = self.get_argument('name', '')
        password = self.get_argument('password', None)
        password_confirm = self.get_argument('password_confirm', None)

        # TODO 確認画面
        
        if (password == password_confirm):
            # 登録開始
            data = {}
            data['mail'] = mail
            data['password'] = password
            data['name'] = name
            auth_logic.register(data)
            self.redirect('/login')
        else:
            # 登録しない(エラー画面)
            pass
            
        
class MemoHandler(BaseHandler):
    def get(self, path):
        # 表示
        param = self.param
        memo_model = memotori.model.MemoModel(self.settings)
        
        if (path):
            # 詳細表示
            pass
        else:
            userid = self.get_current_user()
            param['memo_list'] = []
            for row in memo_model.find_by_userid(userid):
                row['content'] = row['content'].replace('/r','');
                row['content'] = row['content'].replace('/n','<BR>');
                param['memo_list'].append(row);
            self.render('memo.html', **param)
            # # 一覧表示(json)
            # self.set_header('Content-Type', 'application/json')
            # userid = self.get_current_user()
            # resultset = []
            # for rows in memo_model.find_by_userid(userid):
            #     result = {}
            #     result['create_date'] = rows.create_date.isoformat()
            #     result['content'] = rows.content
            #     resultset.append(result)
            
            # self.finish(json.dumps(resultset))

    def post(self, path):
        # 投稿
        data = {}
        data['content'] = self.get_argument('memo', None)
        data['uid'] = uid = self.get_current_user()
        memo_model = memotori.model.MemoModel(self.settings)
        memo_model.insert_memo(data)

        if (path == 'xml'):
            # レスポンスをXMLで返す
            self.set_header('Content-Type', 'application/xml')
            response = Element('response')
            status = SubElement(response, 'status')
            status.text = 'ok'
            response_str = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
            response_str += tostring(response)
            self.write(response_str)
            self.flush()
        else:
            # それ以外はTOPページへリダイレクト
            self.redirect('/')
        
        
        

