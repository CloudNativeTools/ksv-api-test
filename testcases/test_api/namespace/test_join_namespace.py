# -*- coding;utf-8 -*-
"""
File name : test_join_namespace.PY
Program IDE : PyCharm
Create file time: 2022/8/11 16:58
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.namespace import ns
from apis.users import user


class TestJoinNameSpace(BaseTestcase):
    @allure.title('{ns_data[title]}')
    @pytest.mark.namespace
    @pytest.mark.parametrize("ns_data", data_maker("data/api_data/namespace.yaml", "namespace", "join_namespace"))
    @pytest.mark.parametrize("user_data", data_maker("data/api_data/user.yaml", "user", "create_user"))
    def test_join_namespace(self, ns_data, user_data):
        ns_data = ns_data['variables']
        user_data = user_data['variables']

        # 获取项目名
        ns.get_for_test(ns_data)
        # 获取用户
        user.get_for_test(user_data)
        # 获取项目成员列表,已存在则移除
        ns_member_list = ns.ns_member_filter_by_name(ns_data)
        if len(ns_member_list) > 0:
            ns.delete_ns_member(ns_data)
        resp = ns.join_namespace(ns_data)
        self.assert_eq(resp[0].get('roleRef'), ns_data['role'])
        self.assert_schema(resp, 'join_namespace')

        # 获取项目成员列表
        ns_member_list = ns.ns_member_filter_by_name(ns_data)
        # 加入成功，校验ns下用户信息>=1
        self.assert_eq(len(ns_member_list), 1)
        self.assert_eq(ns_member_list[0].get('metadata').get('annotations').get('iam.kubesphere.io/role'),
                       ns_data['role'])
