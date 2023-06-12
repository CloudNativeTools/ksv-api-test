# -*- coding;utf-8 -*-
"""
File name : test_create_user.PY
Program IDE : PyCharm
Create file time: 2022/8/11 17:07
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.users import user


class TestCreateUser(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.user
    @pytest.mark.parametrize("data", data_maker("data/api_data/user.yaml", "user", "create_user"))
    def test_create_user(self, data):
        test_data = data['variables']

        # 先查询是否已存在该用户
        user_list = user.user_filter_by_name(test_data['name'])
        if len(user_list) > 0:
            # 删除该用户，重新创建
            user.delete_user(test_data)
        resp = user.create_user(test_data)
        self.assert_eq(resp.get('metadata').get('name'), test_data['name'])
        self.assert_eq(resp.get('spec').get('email'), test_data['email'])
        self.assert_schema(resp, 'create_user')
