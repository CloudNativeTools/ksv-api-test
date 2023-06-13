# -*- coding;utf-8 -*-
"""
File name : test_edit_policy.PY
Program IDE : PyCharm
Create file time: 2023/6/13 10:44
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.policy import policy


class TestEditPolicy(BaseTestcase):
    @allure.title('{policy_data[title]}')
    @pytest.mark.policy
    @pytest.mark.parametrize("policy_data", data_maker("data/api_data/policy.yaml", "policy", "edit_policy"))
    @pytest.mark.parametrize("policy_init", data_maker("data/api_data/policy.yaml", "policy", "create_policy"))
    def test_edit_policy(self, policy_data, policy_init):
        po_data = policy_data['variables']
        po_init = policy_init['variables']

        # 获取策略名
        policy.get_for_test(po_init)

        resp = policy.edit_policy(po_data)
        self.assert_eq(resp.get('metadata').get('annotations').get('kubesphere.io/alias-name'), po_data['alias-name'])
        self.assert_eq(resp.get('spec').get('deltas'), po_data['deltas'])
        self.assert_eq(resp.get('spec').get('time'), po_data['time'])
        self.assert_eq(resp.get('spec').get('type'), po_data['type'])

        # 校验schema
        self.assert_schema(resp, 'edit_policy')
