
from config import *

import requests
import json

class AccessToken(object):

    def __init__(self, AppID=AppID, AppSecret=AppSecret, Redirect_uri=Redirect_uri):
        self.AppID= AppID
        self.AppSecret = AppSecret
        self.Redirect_uri = Redirect_uri
        self.__state = STATE
        
        self.__access_token = None
        self.__user_id = None
        self.__expire_time = None

        __url = BASE_URL + "oauth/authorize?client_id=%s&redirect_uri=%s&state=%s"
        self.init_url = __url % (self.AppID, self.Redirect_uri, self.__state)

    def set_token(self, code):
        url = BASE_URL + "oauth/access_token"
        data = {
                "client_id": self.AppID,
                "client_secret": self.AppSecret, 
                "code": code, 
                "redirect_uri":self.Redirect_uri
                }
        res = requests.post(url, data)
        ctn = json.loads(res.content)
        self.__access_token = ctn["access_token"]
        self.__user_id = ctn["userid"]
        self.__expire_time = ctn["expires"]

    def get_token(self):
        return self.__access_token

    def access_by_token(self, procd, *args , **kwargs):
        def f(*args, **kwargs):
            res = procd(*args, access_token=self.__access_token, **kwargs)
            return res
        return f

at = AccessToken()


class ApiError(AttributeError):
    def __init__(self, attr):
        self.message = "api has no attribute '%s'"%'.'.join(attr)
        self.args = (self.message,)

class ApiFramework(object):

    def __init__(self, attr=[]):
        self.attr = attr

    def __getattr__(self, s):
        af = ApiFramework(self.attr+[s])
        return af

    @at.access_by_token
    def __call__(self, *args, **kwargs):
        
        path = self.attr[0:-1]
        method = self.attr[-1]
        url = BASE_URL + "/".join(path)
        print(self.attr, "===========")
        print(method == "get")
        res_ctn =None
        
        # res_ctn = requests.get(url, params=kwargs).content
        if(method == "get"):
            res_ctn = requests.get(url, params=kwargs).content
        elif(method == "post"):
            res_ctn = requests.post(url, data=kwargs).content
        else:
            raise Exception("wrong http method")
        return res_ctn
        

api = ApiFramework()








    
