#coding=utf-8
#-*-coding:utf-8-*-
#!/usr/bin/env python3


class Config(object):

	AppID = ""
	AppSecret = ""
	Redirect_uri = ""
	STATE = "any_random_str"

from flask import Flask, request, redirect

from yibanApi import AccessToken, api

app = Flask(__name__)

@app.route('/')
def index():
    at = AccessToken(code=None, Config=Config)
    return redirect(at.init_url)


@app.route('/redirect')
def user_info():
    
    #获取令牌code
    __code = request.args.get("code")

    #利用code 和 Config 实例化AccessToken
    at = AccessToken(code=__code, Config=Config)

    #开始使用装饰器@at.access_by_token 和api定义自己的函数
    @at.access_by_token
    def user_me(access_token):
    	return api.user.me.get(access_token=access_token)

    return user_me()

if __name__ == '__main__':
    app.run()
