

## 介绍
yibanApi 是一个易班app开发接口框架。主要是为了愉快地调用API。

## 开始

+ <code>pip install yibanApi</code>
+ 配置应用基本配置Config
+ 请求用户授权获取令牌code
+ 利用code 和 Config 实例化AccessToken
+ 开始根据API文档愉快地定义自己的API函数

以下通过一个应用flask例子具体说明

## 例子

```
#获取用户信息的例子

#coding=utf-8
#获取用户信息的例子


class Config(object):

	AppID = ""
	AppSecret = ""
	Redirect_uri = "myhost/redirect"
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

```

## 说明
与易班开发文档API接口具有一致性，即：

如果接口地址为：

https://openapi.yiban.cn/path

请求方法为： method

请求参数除了access_token为：

arg1

arg2

那么在实例化AccessToken后可以通过这样定义函数：
```
@at.access_by_token
def my_func(access_token):
	return api.path.method(access_token=access_token,
                    	   arg1=value1,
                    	   arg2=value2)

```                    

以下通过几个示例说明：
eg：

1.
```
接口说明：
    获取当前用户基本信息。

接口地址：
https://openapi.yiban.cn/user/me
GET请求
返回json
接口限制：
    授权需要：是
    访问权限：无限制
    频次限制：是

请求参数：
access_token	必填	用户授权凭证
```

```
根据接口地址和请求方式，可以这样写：
    @at.access_by_token
    def user_me(access_token):
    	return api.user.me.get(access_token=access_token)

```
2.
```
接口说明：
    开发者主动取消指定用户的授权。

接口地址：
https://openapi.yiban.cn/oauth/revoke_token
POST请求（form-data方式）
返回json
接口限制：
    授权需要：否
    访问权限：无限制
    频次限制：无限制

请求参数：
client_id	必填	应用appkey
access_token	必填	待注销的授权凭证
```

```
根据接口地址和请求方式，可以这样写：
    @at.access_by_token
    def revoke(access_token):
    	return api.oauth.revoke_token.post(access_token=access_token,
    	                                   client_id="填写你的client_id")

```

3
```
接口说明：
    删除指定好友。

接口地址：
https://openapi.yiban.cn/friend/remove
GET请求
返回json
接口限制：
    授权需要：是
    访问权限：无限制
    频次限制：是

请求参数：
access_token	必填	用户授权凭证
yb_friend_uid	必填	待删除好友的易班用户ID    	                                   
```

```
根据接口地址和请求方式，可以这样写：
    @at.access_by_token
    def remove(access_token):
    	return api.friend.remove.get(access_token=access_token,
    	                         yb_friend_uid="待删除好友的易班用户ID")
```    	                         