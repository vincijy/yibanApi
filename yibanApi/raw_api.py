class AccessToken(object):

    def __init__(self, AppID=AppID, AppSecret=AppSecret, Redirect_uri=Redirect_uri):
        self.AppID= AppID
        self.AppSecret = AppSecret
        self.Redirect_uri = Redirect_uri
        self.__state = STATE
        
        self.__access_token = "access_token_str"
        self.__user_id = None
        self.__expire_time = None

        __url = BASE_URL + "oauth/authorize?client_id=%s&redirect_uri=%s&state=%s"
        self.init_url = __url % (self.AppID, self.Redirect_uri, self.__state)

    def _set_token(self, code):
        url = BASE_URL + "oauth/access_token"
        data = {
                "client_id": self.AppID,
                "client_secret": self.AppSecret, 
                "code": code, 
                "redirect_uri":self.redirect_uri
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

class ApiFramework(object):

    def __init__(self, path=[]):
        self.path = path

    def __getattr__(self, s):
        af = ApiFramework(self.path+[s])
        return af

    @at.access_by_token
    def __call__(self, *args, **kwargs):
        access_token = kwargs.get("access_token", "")
        url = BASE_URL + "/".join(self.path)
        #res_ctn = requests.get(url, params=kwargs).content
        print(kwargs)



api = ApiFramework()

x = api.friend.me_list.get(page=1, count=2)


    
