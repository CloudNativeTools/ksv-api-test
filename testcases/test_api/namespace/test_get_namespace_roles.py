# -*- coding;utf-8 -*-
"""
File name : test_get_namespace_roles.PY
Program IDE : PyCharm
Create file time: 2022/8/8 17:51
File Create By Author : qiaoshilu
"""
from collections import Counter

import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.namespace import ns


class TestGetNsRoles(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("data", data_maker("data/api_data/namespace.yaml", "namespace", "get_ns_role"))
    def test_get_ns_roles(self, data):
        test_data = data['variables']

        # 获取项目名
        ns.get_for_test(test_data)
        resp = ns.get_ns_roles(test_data)
        role = [roles.get('metadata').get('name') for roles in resp.get('items')]
        self.assert_eq(resp.get('totalItems'), 3)
        self.assert_eq(Counter(role), Counter(['viewer', 'admin', 'operator']))
        self.assert_schema(resp, 'get_ns_roles')
