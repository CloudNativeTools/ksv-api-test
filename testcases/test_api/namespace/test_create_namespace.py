# -*- coding;utf-8 -*-
"""
File name : test_create_namespace.PY
Program IDE : PyCharm
Create file time: 2022/8/1 17:32
File Create By Author : qiaoshilu
"""

import allure
import pytest
from aomaker.aomaker import data_maker, genson
from aomaker.base.base_testcase import BaseTestcase

from apis import ResourceStatus
from apis.namespace import ns


class TestCreateNamespace(BaseTestcase):

    @allure.title('{data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("data", data_maker("data/api_data/namespace.yaml", "namespace", "create_namespace"))
    def test_create_namespace(self, data):
        # 先查询是否已存在该项目
        test_data = data['variables']
        ns_list = ns.namespace_filter_by_name(test_data['name'])
        if len(ns_list) > 0:
            # 删除该项目，重新创建
            ns.delete_namespace(test_data)
        resp = ns.create_namespace(test_data)
        self.assert_eq(resp.get('metadata').get('name'), test_data['name'])
        self.assert_eq(resp.get('status').get('phase'), ResourceStatus.ACTIVE.value)
        # schema断言
        self.assert_schema(resp, 'create_namespace')

        # 查看列表，匹配该数据
        self.assert_gt(len(ns.namespace_filter_by_name(test_data['name'])), 0)