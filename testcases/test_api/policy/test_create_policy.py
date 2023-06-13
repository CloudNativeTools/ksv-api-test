# -*- coding;utf-8 -*-
"""
File name : test_create_policy.PY
Program IDE : PyCharm
Create file time: 2023/5/1 22:31
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.namespace import ns
from apis.policy import policy


class TestCreatePolicy(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.policy
    @pytest.mark.parametrize("data", data_maker("data/api_data/policy.yaml", "policy", "create_policy"))
    def test_create_policy(self, data):
        policy_data = data['variables']

        resp = policy.create_policy(policy_data)

        self.assert_eq(resp.get('metadata').get('annotations').get('kubesphere.io/alias-name'),
                       policy_data['alias-name'])
        self.assert_eq(resp.get('spec').get('time'), policy_data['time'])
        self.assert_eq(resp.get('spec').get('type'), policy_data['type'])
        # schema断言
        self.assert_schema(resp, 'create_policy')

        # 查看列表，匹配该数据
        self.assert_gt(len(policy.policy_filter_by_alias(policy_data['alias-name'])), 0)
