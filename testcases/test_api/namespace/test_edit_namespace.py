# -*- coding;utf-8 -*-
"""
File name : test_edit_namespace.PY
Program IDE : PyCharm
Create file time: 2022/8/9 17:32
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.namespace import ns


class TestEditNamespace(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("data", data_maker("data/api_data/namespace.yaml", "namespace", "edit_namespace"))
    def test_edit_namespace(self, data):
        test_data = data['variables']

        # 获取项目名
        ns.get_for_test(test_data)
        resp = ns.edit_namespace(test_data)
        self.assert_eq(resp.get('metadata').get('annotations').get('kubesphere.io/alias-name'), test_data['alias_name'])
        self.assert_eq(resp.get('metadata').get('annotations').get('kubesphere.io/description'),
                       test_data['description'])
        # 校验schema
        self.assert_schema(resp, 'edit_namespace')
