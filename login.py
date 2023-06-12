from aomaker.cache import cache
from aomaker.fixture import BaseLogin
from requests import request


class Login(BaseLogin):

    def login(self):
        submit_host = self.host

        payload = {
            'lang': 'zh',
            'username': self.account['user'],
            'password': self.account['pwd'],
        }

        submit_login_url = submit_host + "/login"
        data = {
            'url': submit_login_url,
            'method': 'post',
            'json': payload
        }

        resp_submit = request(**data)

        return resp_submit

    def make_headers(self, resp_login):
        cookie_dict = resp_login.cookies.get_dict()
        found = ['%s=%s' % (name, value) for (name, value) in cookie_dict.items()]
        headers = {
            'Cookie': ';'.join(found)
        }
        return headers
