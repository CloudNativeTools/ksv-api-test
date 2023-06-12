# -*- coding;utf-8 -*-
"""
File name : users.PY
Program IDE : PyCharm
Create file time: 2022/8/8 17:19
File Create By Author : qiaoshilu
"""

from aomaker.base.base_api import BaseApi


class Users(BaseApi):
    """
    用户信息
    """

    def get_user_info(self):
        """
        获取当前用户信息
        :return:
        """
        http_data = {
            "api_path": "/userInfo",
            "method": "get"
        }
        response = self.send_http(http_data)
        return response

    def create_user(self, test_data: dict):
        """
        创建用户，不加入项目
        :param test_data: 用户信息
        :return:
        """
        body = {
            "apiVersion": "iam.kubesphere.io/v1alpha2",
            "kind": "KsvUser",
            "metadata": {
                "name": test_data['name'],
                "annotations": {
                    "iam.kubesphere.io/uninitialized": "true",
                    "iam.kubesphere.io/loginFirst": "true",
                    "kubesphere.io/creator": "admin"
                }
            },
            "spec": {
                "email": test_data['email'],
                "password": test_data['password']
            }
        }
        http_data = {
            "method": "post",
            "api_path": "/kapis/iam.kubesphere.io/v1alpha2/users",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    def get_all_user(self, page=1, limit=10):
        """获取用户列表
        :param page: 页码，默认为1
        :param limit: 每页条数，10
        :return:
        """
        http_data = {
            "api_path": "/kapis/iam.kubesphere.io/v1alpha2/users",
            'method': 'get',
            'params': {'limit': limit, 'page': page, 'sortBy': 'createTime'}
        }
        response = self.send_http(http_data)
        return response

    def delete_user(self, test_data: dict):
        """
        删除用户
        :param test_data:用户信息
        :return:
        """
        body = {}
        http_data = {
            "api_path": f"/kapis/iam.kubesphere.io/v1alpha2/users/{test_data['name']}",
            "method": "delete",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    def get_for_test(self, user_data: dict):
        """
        获取测试用户资源，有直接返回，没有需创建
        :param user_data: 用户数据
        :return:
        """
        user_list = self.user_filter_by_name(user_data['name'])
        if len(user_list) > 0:
            return user_list[0]
        self.create_user(user_data)
        return None

    @staticmethod
    def user_filter_by_name(username):
        """通过username获取用户list
        :param username: 查询条件
        :return:
        """
        resp = user.get_all_user()
        init_total = resp.get('totalItems')
        page = 0
        user_list = []
        while page * 10 < init_total:
            page += 1
            resp = user.get_all_user(page)
            user_list = [users for users in resp.get('items')
                         if users.get('metadata').get('name') == username]
        return user_list


user = Users()
