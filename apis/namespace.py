# -*- coding;utf-8 -*-
"""
File name : api_namespace.PY
Program IDE : PyCharm
Create file time: 2022/8/1 17:34
File Create By Author : qiaoshilu
"""
import time

from aomaker.aomaker import update
from aomaker.aomaker import async_api, dependence
from aomaker.base.base_api import BaseApi
from aomaker.log import logger

from apis import ResourceStatus


def wait_delete_ns_task(ns_name):
    """删除项目，加入轮循函数
    :param ns_name: 项目名
    :return:
    """
    retry = 0
    while retry < 20:
        res_list = ns.namespace_filter_by_name(ns_name, native=True)
        if len(res_list) > 0:
            ns_status = res_list[0].get('status').get('phase')
            if ns_status in [ResourceStatus.TERMINATING.value, ResourceStatus.ACTIVE.value]:
                logger.info(f'ns资源状态： {ns_status}')
                time.sleep(10)
                retry += 1
        else:
            return res_list


class NameSpace(BaseApi):
    """
    项目namespace
    """

    def create_namespace(self, test_data: dict):
        """创建项目
        :param test_data:项目数据
        :return:
        """
        body = {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "labels": {
                    "kubesphere.io/visibility": "private",
                    "virtualization.kubesphere.io/enable": "true"
                },
                "name": test_data['name'],
                "annotations": {
                    "kubesphere.io/creator": "admin"
                }
            }
        }
        http_data = {
            "method": "post",
            "api_path": "/api/v1/namespaces",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    @async_api(wait_delete_ns_task, 'metadata.name')
    def delete_namespace(self, test_data: dict):
        """删除项目
        因删除后，会有5-10s等待，直接查询get list会出现schema错误；故等待删除完毕
        :param test_data: 项目数据
        :return:
        """
        body = {}
        http_data = {
            "method": "delete",
            "api_path": f"/api/v1/namespaces/{test_data['name']}",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    def get_all_namespace(self, limit=10):
        """获取项目列表
        :param limit: 每页条数，10
        :return:
        """
        http_data = {
            "api_path": "/kapis/iam.kubesphere.io/v1alpha2/users/admin/namespaces",
            'method': 'get',
            'params': {'sortBy': 'createTime',
                       'limit': limit}
        }
        response = self.send_http(http_data)
        return response

    def get_all_k8s_ns(self):
        """获取k8s原生项目列表
        :return:
        """
        http_data = {
            "api_path": "/api/v1/namespaces",
            'method': 'get'
        }
        response = self.send_http(http_data)
        return response

    def check_namespace_exist(self, test_data: dict):
        """检验项目名是否存在
        :param test_data
        :return:
        """
        http_data = {
            "api_path": f"/api/v1/namespaces/{test_data['name']}",
            "method": "get"
        }
        http_data.update({"headers": {"x-check-exist": "true"}})
        response = self.send_http(http_data)
        return response

    def get_for_test(self, test_data: dict):
        """获取资源，有直接返回，无则创建后返回
        :param test_data:
        :return:
        """
        ns_list = self.namespace_filter_by_name(test_data['name'])
        if len(ns_list) > 0:
            return ns_list[0]
        self.create_namespace(test_data)
        return self.namespace_filter_by_name(test_data['name'])[0]

    def get_namespace_current_info(self, ns_name, login_info):
        """
        获取namespace下当前登录信息
        :param ns_name: 项目名
        :param login_info: 登录账号，如admin
        :return:
        """
        http_data = {
            "api_path": f"/kapis/iam.kubesphere.io/v1alpha2"
                        f"/namespaces/{ns_name}/members/{login_info}",
            "method": "get"
        }
        response = self.send_http(http_data)
        return response

    def get_ns_detail(self, ns_name):
        """
        获取项目详情
        :param ns_name 项目名
        :return:
        """
        http_data = {
            "api_path": f"/api/v1/namespaces/{ns_name}",
            "method": "get"
        }
        response = self.send_http(http_data)
        return response

    def get_ns_roles(self, test_data: dict, page=1, limit=-1):
        """
        获取项目角色
        :param test_data: 项目数据
        :param page: 页码，默认1
        :param limit: 每页条数，默认-1全部
        :return:
        """
        http_data = {
            "api_path": f"/kapis/iam.kubesphere.io/v1alpha2/namespaces/{test_data['name']}/roles",
            "method": "get",
            "params": {"limit": limit,
                       "sortBy": "createTime",
                       "page": page,
                       "annotation": "kubesphere.io/creator"}
        }
        response = self.send_http(http_data)
        return response

    def get_ns_members(self, test_data: dict, limit=-1):
        """
        获取项目下成员信息
        :param test_data:项目数据
        :param page: 页码，默认1
        :param limit: 每页条数，默认-1全部
        :return:
        """
        http_data = {
            "api_path": f"/kapis/iam.kubesphere.io/v1alpha2/namespaces/{test_data['name']}/members",
            "method": "get",
            "params": {"limit": limit, "sortBy": "createTime"}
        }
        response = self.send_http(http_data)
        return response

    @dependence("ns.get_ns_detail", "ns_detail", imp_module="apis.namespace", ns_name="auto-test")
    @update("ns_detail", ns_name="auto-test")
    def edit_namespace(self, test_data: dict):
        """
        编辑项目
        :param test_data
        :return:
        """
        resource_version = self.cache.get_by_jsonpath('ns_detail', jsonpath_expr='$..resourceVersion')

        body = {
            "kind": "Namespace",
            "apiVersion": "v1",
            "metadata": {
                "name": f"{test_data['name']}",
                "labels": {
                    "kubernetes.io/metadata.name": f"{test_data['name']}",
                    "kubesphere.io/namespace": f"{test_data['name']}",
                    "kubesphere.io/visibility": "private",
                    "virtualization.kubesphere.io/enable": "true"
                },
                "annotations": {
                    "ksvm.number": "0",
                    "kubesphere.io/alias-name": test_data['alias_name'],
                    "kubesphere.io/creator": "admin",
                    "ovn.kubernetes.io/cidr": "10.233.64.0/18",
                    "ovn.kubernetes.io/exclude_ips": "10.233.64.1",
                    "ovn.kubernetes.io/logical_switch": "ovn-default",
                    "project.kubesphere.io/role": "admin",
                    "user.number": "1",
                    "kubesphere.io/description": test_data['description']
                },
                "resourceVersion": resource_version
            },
            "spec": {
                "finalizers": [
                    "kubernetes"
                ]
            }
        }

        http_data = {
            "api_path": f"/api/v1/namespaces/{test_data['name']}",
            "method": "put",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    def join_namespace(self, ns_data: dict):
        """
        邀请用户加入项目
        :param ns_data: 项目数据
        :param user_data: 项目数据
        :return:
        """
        body = [
            {
                "username": ns_data['username'],
                "roleRef": ns_data['role']
            }
        ]
        http_data = {
            "api_path": f"/kapis/iam.kubesphere.io/v1alpha2/namespaces/{ns_data['name']}/members",
            "method": "post",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    def delete_ns_member(self, ns_data: dict):
        """
        删除项目下用户
        :param ns_data:项目数据
        :param user_data:用户数据
        :return:
        """
        body = {}
        http_data = {
            "api_path": f"/kapis/iam.kubesphere.io/v1alpha2"
                        f"/namespaces/{ns_data['name']}/members/{ns_data['username']}",
            "method": "delete",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    def change_ns_role(self, ns_data: dict):
        """
        变更项目下用户角色
        :param ns_data:项目数据
        :param user_data:项目数据
        :return:
        """
        body = {
            "username": ns_data['username'],
            "roleRef": ns_data['user_role']
        }
        http_data = {
            "api_path": f"/kapis/iam.kubesphere.io/v1alpha2"
                        f"/namespaces/{ns_data['name']}/members/{ns_data['username']}",
            "method": "put",
            "json": body
        }
        response = self.send_http(http_data)
        return response

    def namespace_filter_by_name(self, ns_name, native=False):
        """通过ns_name获取项目list
        :param ns_name: 项目名
        :param native: 是否获取原生接口
        :return:
        """
        if native:
            resp = self.get_all_k8s_ns()
        else:
            resp = self.get_all_namespace()

        ns_list = [ns_list for ns_list in resp.get('items')
                   if ns_list.get('metadata').get('name') == ns_name]
        return ns_list

    @staticmethod
    def ns_member_filter_by_name(ns_data: dict):
        """
        通过项目名和用户筛选ns
        :param ns_data: 项目数据
        :return:
        """
        resp = ns.get_ns_members(ns_data)

        ns_member_list = [ns_member for ns_member in resp.get('items')
                          if ns_member.get('metadata').get('name') == ns_data['username']]

        return ns_member_list


ns = NameSpace()
