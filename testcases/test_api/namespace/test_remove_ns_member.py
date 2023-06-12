# -*- coding;utf-8 -*-
"""
File name : test_remove_ns_member.PY
Program IDE : PyCharm
Create file time: 2022/8/12 14:27
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.namespace import ns
from apis.users import user


class TestRemoveNsMember(BaseTestcase):
    @allure.title('{ns_data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("ns_data", data_maker("data/api_data/namespace.yaml", "namespace", "left_namespace"))
    @pytest.mark.parametrize("user_data", data_maker("data/api_data/user.yaml", "user", "create_user"))
    def test_remove_ns_member(self, ns_data, user_data):
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
        resp = ns.delete_ns_member(ns_data)
        self.assert_eq(resp.get('message'), 'success')
        self.assert_schema(resp, 'delete_ns_member')

        # 移除后，项目下不再显示该用户列
        ns_member_list = ns.ns_member_filter_by_name(ns_data)
        self.assert_eq(len(ns_member_list), 0)
