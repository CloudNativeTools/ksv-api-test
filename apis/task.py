# -*- coding;utf-8 -*-
"""
File name : task.py.PY
Program IDE : PyCharm
Create file time: 2023/6/18 0:01
File Create By Author : qiaoshilu
"""
from aomaker.aomaker import dependence
from aomaker.base.base_api import BaseApi

from apis.common.random_func import get_name_id
from apis.namespace import ns


class Task(BaseApi):
    @dependence(ns.get_all_namespace, 'namespace_list')
    def create_task(self, task_data: dict):
        ns_name = self.cache.get_by_jsonpath('namespace_list', jsonpath_expr='$..name')
        body = {
            "apiVersion": "virtualization.kubesphere.io/v1alpha1",
            "kind": "VirtualMachineTimerTask",
            "metadata": {
                "namespace": ns_name,
                "name": get_name_id("vmtask-", 8),
                "annotations": {
                    "kubesphere.io/alias-name": task_data['alias-name'],
                    "virtualization.kubesphere.io/type": task_data['type'],
                    "kubesphere.io/creator": "admin"
                },
                "labels": {
                    f"timerpolicy.kubesphere.io/{ns_name}": "vmpolicy-e1otnz88"
                }
            },
            "spec": {
                "targets": [
                    {
                        "name": "i-d338598f",
                        "namespace": f"{ns_name}",
                        "aliasName": "test-vm",
                        "ips": [

                        ],
                        "type": task_data['target_type'],
                        "action": task_data['target_action']
                    }
                ],
                "policy": {
                    "name": "vmpolicy-e1otnz88"
                },
                "disable": False,
                "failedTimes": task_data['failed_times'],
                "failedStop": task_data['failed_stop']
            }
        }

        http_data = {
            "method": "post",
            "api_path": f"/apis/virtualization.kubesphere.io/v1alpha1/namespaces/{ns_name}/virtualmachinetimertasks",
            "json": body
        }
        response = self.send_http(http_data)
        return response


task = Task()
