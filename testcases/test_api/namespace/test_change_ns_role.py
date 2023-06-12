# -*- coding;utf-8 -*-
"""
File name : test_change_ns_role.PY
Program IDE : PyCharm
Create file time: 2022/8/12 14:36
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.namespace import ns
from apis.users import user


class TestChangeNsRole(BaseTestcase):
    @allure.title('{ns_data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("ns_data", data_maker("data/api_data/namespace.yaml", "namespace", "change_ns_role"))
    @pytest.mark.parametrize("user_data", data_maker("data/api_data/user.yaml", "user", "create_user"))
    def test_change_ns_role(self, ns_data, user_data):
        ns_data = ns_data['variables']
        user_data = user_data['variables']

        # 获取项目名
        ns.get_for_test(ns_data)
        # 获取用户
        user.get_for_test(user_data)
        # 获取项目成员列表,不存在先邀请加入
        ns_member_list = ns.ns_member_filter_by_name(ns_data)
        if len(ns_member_list) == 0:
            ns.join_namespace(ns_data)
        resp = ns.change_ns_role(ns_data)

        self.assert_eq(resp.get('roleRef'), ns_data['user_role'])
        self.assert_schema(resp, 'change_ns_role')

        # 校验项目下用户列角色是否变更
        ns_member_list = ns.ns_member_filter_by_name(ns_data)
        self.assert_eq(ns_member_list[0].get('metadata').get('annotations').get('iam.kubesphere.io/role'),
                       ns_data['user_role'])
