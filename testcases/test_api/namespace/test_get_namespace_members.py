# -*- coding;utf-8 -*-
"""
File name : get_namespace_members.PY
Program IDE : PyCharm
Create file time: 2022/8/9 14:46
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.namespace import ns
from apis.users import user


class TestGetNsMembers(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("data", data_maker("data/api_data/namespace.yaml", "namespace", "get_ns_members"))
    def test_get_ns_members(self, data):
        test_data = data['variables']

        # 获取项目名
        ns.get_for_test(test_data)
        resp = ns.get_ns_members(test_data)
        self.assert_ge(resp.get('totalItems'), 1)
        # 获取所有成员name
        member = [members.get('metadata').get('name') for members in resp.get('items')]
        # 获取当前登录信息
        user_resp = user.get_user_info()
        username = user_resp.get('data').get('username')
        self.assert_contains(member, username)
        # 校验schema
        self.assert_schema(resp, 'get_ns_members')
