# -*- coding;utf-8 -*-
"""
File name : test_namespace_exist.PY
Program IDE : PyCharm
Create file time: 2022/8/5 16:56
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.namespace import ns


class TestNameSpaceExist(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.todo
    @pytest.mark.parametrize("data", data_maker("data/api_data/namespace.yaml", "namespace", "check_ns_exist"))
    def test_namespace_exist(self, data):
        test_data = data['variables']
        ns.get_for_test(test_data)
        resp = ns.check_namespace_exist(test_data)
        self.assert_eq(resp.get('exist'), True)
        self.assert_schema(resp, 'check_namespace_exist')
