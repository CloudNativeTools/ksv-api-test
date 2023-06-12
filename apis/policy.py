# -*- coding;utf-8 -*-
"""
File name : policy.PY
Program IDE : PyCharm
Create file time: 2023/5/1 22:37
File Create By Author : qiaoshilu
"""
import random
import string

from aomaker.aomaker import dependence
from aomaker.base.base_api import BaseApi

from apis.common.random_func import get_name_id
from apis.namespace import ns


class Policy(BaseApi):
    @dependence(ns.get_all_namespace, 'namespace_list')
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


policy = Policy()
