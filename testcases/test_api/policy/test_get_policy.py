# -*- coding;utf-8 -*-
"""
File name : test_get_policy.PY
Program IDE : PyCharm
Create file time: 2023/6/13 23:05
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.policy import policy


class TestGetPolicy(BaseTestcase):
    @allure.title('{policy_data[title]}')
    @pytest.mark.policy
    @pytest.mark.parametrize("policy_init", data_maker("data/api_data/policy.yaml", "policy", "create_policy"))
    @pytest.mark.parametrize("policy_data", data_maker("data/api_data/policy.yaml", "policy", "get_policy"))
    def test_get_policy_all_pro(self, policy_data, policy_init):
        po_init = policy_init['variables']
        # 获取policy资源
        policy.get_for_test(po_init)

        resp = policy.get_all_policy()
        init_total = resp.get('totalItems')
        page = 1
        while page * 10 < init_total:
            page += 1
            policy.get_all_policy(page=page)
        self.assert_gt(init_total, 0)

        # schema断言
        self.assert_schema(resp, 'get_all_policy')

    @allure.title('{policy_data[title]}')
    @pytest.mark.policy
    @pytest.mark.parametrize("policy_data", data_maker("data/api_data/policy.yaml", "policy", "get_policy"))
    def test_get_policy_by_pro(self, policy_data):

        resp = policy.get_policy_by_pro()
        init_total = resp.get('totalItems')
        page = 1
        while page * 10 < init_total:
            page += 1
            policy.get_policy_by_pro(page=page)
        self.assert_gt(init_total, 0)

        # schema断言
        self.assert_schema(resp, 'get_policy_by_pro')
