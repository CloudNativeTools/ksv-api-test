# -*- coding;utf-8 -*-
"""
File name : test_create_task.PY
Program IDE : PyCharm
Create file time: 2023/6/17 23:59
File Create By Author : qiaoshilu
"""
import allure
import pytest
from aomaker.aomaker import data_maker
from aomaker.base.base_testcase import BaseTestcase

from apis.task import task


class TestCreateTask(BaseTestcase):
    @allure.title('{data[title]}')
    @pytest.mark.task
    @pytest.mark.parametrize("data", data_maker("data/api_data/task.yaml", "task", "create_task"))
    def test_create_policy(self, data):
        task_data = data['variables']

        # 查询是否数据存在，存在则删除

        resp = task.create_task(task_data)
