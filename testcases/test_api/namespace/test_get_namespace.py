# -*- coding;utf-8 -*-
"""
File name : test_get_namespace.PY
Program IDE : PyCharm
Create file time: 2022/8/3 17:22
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.namespace import ns


class TestGetNameSpace(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("data", data_maker("data/api_data/namespace.yaml", "namespace", "get_namespace"))
    def test_get_all_namespace(self, data):
        resp = ns.get_all_namespace()
        init_total = resp.get('totalItems')
        page = 1
        while page * 10 < init_total:
            page += 1
            ns.get_all_namespace(page)
        self.assert_gt(init_total, 0)

        # schema断言
        self.assert_schema(resp, 'get_all_namespace')
