# -*- coding;utf-8 -*-
"""
File name : test_get_namespace_detail.PY
Program IDE : PyCharm
Create file time: 2022/8/8 17:39
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis import ResourceStatus
from apis.namespace import ns


class TestGetNsDetail(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("data", data_maker("data/api_data/namespace.yaml", "namespace", "describe_namespace"))
    def test_get_ns_detail(self, data):
        test_data = data['variables']
        ns_name = test_data['name']

        # 获取项目名
        ns.get_for_test(test_data)
        resp = ns.get_ns_detail(ns_name)
        self.assert_eq(resp.get('metadata').get('name'), ns_name)
        self.assert_eq(resp.get('status').get('phase'), ResourceStatus.ACTIVE.value)
        self.assert_schema(resp, 'get_ns_detail')
