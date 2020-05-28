import requests
from urllib.parse import urljoin
import json
import pprint

class ApiResponseError(BaseException):
    pass

class Wiz:

    AsUrl = 'https://as.wiz.cn'

    def __init__(self,username: str,password: str):
        self.LoginResult = {}
        self.token = ""
        self.username = username
        self.password = password

    def __execRequest(self,method: str,url: str,body={},**kwargs):
        if self.token != "":
            header = {"X-Wiz-Token":self.token}
        else:
            header = {}
        resp = requests.request(method=method.lower(),url=url,data=body,headers=header,**kwargs)
        ret = resp.json()
        if ret["returnCode"] != 200:
            raise ApiResponseError(ret["returnMessage"])
        return ret

    def Login(self):
        url = urljoin(Wiz.AsUrl,"/as/user/login")
        body = {
            "userId": self.username,
            "password": self.password
        }
        ret = self.__execRequest("post",url,body)
        self.LoginResult = ret["result"]
        self.token = self.LoginResult.get("token","")
        return self

    def Exit(self):
        url = urljoin(Wiz.AsUrl,"/as/user/logout")
        ret = self.__execRequest(method="get",url=url)
        return ret

    def __createNote(self,kbServer, kbGuid, title, folder, html):
        url = urljoin(kbServer,"/ks/note/create",kbGuid)
        note = {
              "kbGuid":kbGuid,
              "html":html,
              "title":title,
              "category": folder,
            }
        return self.__execRequest("post",url,note)

    def LoadMarkdownWithImage(self,kbServer,kbGuid,folder,token):
        pass


    def __enter__(self):
        return self.Login()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.Exit()




if __name__ == '__main__':
    username = "xxx"
    password = "xxx"
    with Wiz(username,password) as w:
        pass