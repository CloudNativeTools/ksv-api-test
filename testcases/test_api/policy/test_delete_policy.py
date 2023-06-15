# -*- coding;utf-8 -*-
"""
File name : test_delete_policy.PY
Program IDE : PyCharm
Create file time: 2023/6/14 22:54
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.policy import policy


class TestDeletePolicy(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.policy
    @pytest.mark.parametrize("data", data_maker("data/api_data/policy.yaml", "policy", "delete_policy"))
    @pytest.mark.parametrize("policy_init", data_maker("data/api_data/policy.yaml", "policy", "create_policy"))
    def test_delete_policy(self, data, policy_init):
        po_init = policy_init['variables']
        policy_obj = policy.get_for_test(po_init)
        po_name = policy_obj['metadata']['name']

        resp = policy.delete_policy(policy_obj)
        self.assert_eq(resp.get('details').get('name'), po_name)
        self.assert_eq(resp.get('status'), 'Success')
        # schema断言
        self.assert_schema(resp, 'delete_policy')
