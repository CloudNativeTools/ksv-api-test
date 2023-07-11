# -*- coding;utf-8 -*-
"""
File name : test_delete_namespace.PY
Program IDE : PyCharm
Create file time: 2022/8/2 15:54
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis import ResourceStatus
from apis.namespace import ns


class TestDeleteNameSpace(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("data", data_maker("data/api_data/namespace.yaml", "namespace", "delete_namespace"))
    def test_delete_namespace(self, data):
        test_data = data['variables']
        # 先查询是否已存在该项目
        ns.get_for_test(test_data)

        resp = ns.delete_namespace(test_data)
        self.assert_eq(resp.get('metadata').get('name'), test_data['name'])
        self.assert_eq(resp.get('status').get('phase'), ResourceStatus.TERMINATING.value)
        # schema断言
        self.assert_schema(resp, 'delete_namespace')
