# -*- coding;utf-8 -*-
"""
File name : test_describe_policy.PY
Program IDE : PyCharm
Create file time: 2023/6/13 11:01
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.policy import policy


class TestDescribePolicy(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.policy
    @pytest.mark.parametrize("data", data_maker("data/api_data/policy.yaml", "policy", "describe_policy"))
    @pytest.mark.parametrize("policy_init", data_maker("data/api_data/policy.yaml", "policy", "create_policy"))
    def test_describe_policy(self, data, policy_init):
        policy_data = data['variables']

        po_init = policy_init['variables']
        policy.get_for_test(po_init)

        resp = policy.describe_policy(policy_data['alias-name'])

        # 断言
        self.assert_eq(resp.get('metadata').get('annotations').get('kubesphere.io/alias-name'),
                       policy_data['alias-name'])
        self.assert_schema(resp, 'describe_policy')
