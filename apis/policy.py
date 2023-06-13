# -*- coding;utf-8 -*-
"""
File name : policy.PY
Program IDE : PyCharm
Create file time: 2023/5/1 22:37
File Create By Author : qiaoshilu
"""

from aomaker.aomaker import dependence
from aomaker.aomaker import update
from aomaker.base.base_api import BaseApi

from apis.common.random_func import get_name_id
from apis.namespace import ns


class Policy(BaseApi):
    @dependence(ns.get_all_namespace, 'namespace_list')
    @update("policy_list")
    def create_policy(self, policy_data: dict):
        ns_name = self.cache.get_by_jsonpath('namespace_list', jsonpath_expr='$..name')
        body = {
            "apiVersion": "virtualization.kubesphere.io/v1alpha1",
            "kind": "VirtualMachineTimerPolicy",
            "metadata": {
                "namespace": ns_name,
                "name": get_name_id("vmpolicy-", 8),
                "annotations": {
                    "kubesphere.io/alias-name": policy_data['alias-name'],
                    "kubesphere.io/creator": "admin"
                }
            },
            "spec": {
                "disable": False,
                "type": policy_data['type'],
                "time": policy_data['time'],
                "deltas": [

                ]
            }
        }
        http_data = {
            "method": "post",
            "api_path": f"/apis/virtualization.kubesphere.io/v1alpha1/namespaces/{ns_name}/virtualmachinetimerpolicies",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    def get_all_policy(self, limit=10):
        """获取定时策略列表
        :param limit: 每页条数，10
        :return:
        """
        http_data = {
            "api_path": "/kapis/resources.kubesphere.io/v1alpha3/virtualmachinetimerpolicies",
            'method': 'get',
            'params': {'sortBy': 'createTime',
                       'limit': limit}
        }
        response = self.send_http(http_data)
        return response

    @dependence("policy.get_all_policy", "policy_list", imp_module="apis.policy")
    def policy_filter_by_alias(self, policy_alias):
        """通过policy_name获取项目list
        :param policy_alias: 策略别名
        :return:
        """
        # 获取依赖接口返回数据
        policy_list = self.cache.get("policy_list")
        po_list = [po_list for po_list in policy_list.get('items')
                   if po_list.get('metadata').get('annotations').get('kubesphere.io/alias-name') == policy_alias]
        return po_list

    @dependence("policy.describe_policy", "describe_policy", imp_module="apis.policy")
    def edit_policy(self, policy_data: dict):
        po_namespace = self.cache.get_by_jsonpath('describe_policy', jsonpath_expr='$..namespace')
        po_name = self.cache.get_by_jsonpath('describe_policy', jsonpath_expr='$..name')
        resource_version = self.cache.get_by_jsonpath('describe_policy', jsonpath_expr='$..resourceVersion')
        body = {
            "apiVersion": "virtualization.kubesphere.io/v1alpha1",
            "kind": "VirtualMachineTimerPolicy",
            "metadata": {
                "annotations": {
                    "kubesphere.io/alias-name": policy_data['alias-name'],
                    "kubesphere.io/creator": "admin"
                },
                "name": po_name,
                "namespace": po_namespace,
                "resourceVersion": resource_version
            },
            "spec": {
                "deltas": policy_data['deltas'],
                "disable": False,
                "time": policy_data['time'],
                "type": policy_data['type']
            }

        }
        http_data = {
            "method": "put",
            "api_path": f"/apis/virtualization.kubesphere.io/v1alpha1/namespaces/auto-test/virtualmachinetimerpolicies/{po_name}",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    @dependence("policy.policy_filter_by_alias", "policy_filter", policy_alias='auto-policy', imp_module="apis.policy")
    def describe_policy(self):
        """
        获取策略详情
        :return:
        """
        policy_name = self.cache.get_by_jsonpath('policy_filter', jsonpath_expr='$..name')
        http_data = {
            "method": "get",
            "api_path": f"/apis/virtualization.kubesphere.io/v1alpha1/namespaces/auto-test/virtualmachinetimerpolicies/{policy_name}",
        }
        response = self.send_http(http_data)
        return response

    def get_for_test(self, test_data: dict):
        """获取资源，有直接返回，无则创建后返回
        :param test_data:
        :return:
        """
        policy_list = self.policy_filter_by_alias(test_data['alias-name'])
        if len(policy_list) > 0:
            return policy_list[0]
        self.create_policy(test_data)
        return self.policy_filter_by_alias(test_data['alias-name'])[0]


policy = Policy()
