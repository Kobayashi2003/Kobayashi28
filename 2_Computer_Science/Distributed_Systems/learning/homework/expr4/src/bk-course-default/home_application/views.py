# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import json
import time

from django.http import JsonResponse
from django.shortcuts import render

from blueking.component.shortcuts import get_client_by_request
from home_application.constants import MAX_ATTEMPTS, JOB_RESULT_ATTEMPTS_INTERVAL, JOB_BK_BIZ_ID, BK_JOB_HOST, \
    WEB_SUCCESS_CODE, SEARCH_FILE_PLAN_ID, WAITING_CODE, SUCCESS_CODE, BACKUP_FILE_PLAN_ID
from home_application.models import BackupRecord


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, "home_application/index_home.html")


def dev_guide(request):
    """
    开发指引
    """
    return render(request, "home_application/dev_guide.html")


def contact(request):
    """
    联系页
    """
    return render(request, "home_application/contact.html")


def get_bizs_list(request):
    """
    获取业务列表
    """
    # 从环境配置获取APP信息，从request获取当前用户信息
    client = get_client_by_request(request)
    # 请求参数
    kwargs = {
        "fields": [
            "bk_biz_id",
            "bk_biz_name"
        ],
        # 社区版环境中业务数量有限，故不考虑分页情况
        "page": {
            "start": 0,
            "limit": 10,
            "sort": ""
        }
    }
    # 这里需要填写对应的组件API的入口地址
    result = client.cc.search_business(kwargs)
    return JsonResponse(result)


# 请仿照此前的接口，实现查询集群列表接口
def get_sets_list(request):
    """
    根据业务ID，查询业务下的集群列表
    """
    client = get_client_by_request(request)
    # 请求参数
    kwargs = {
        "bk_biz_id": request.GET.get('bk_biz_id'),  # 从request.GET中获取传递的查询参数
        "fields": ["bk_set_id", "bk_set_name", "bk_biz_id", "bk_created_at", "bk_supplier_account"],
    }
    result = client.cc.search_set(kwargs)
    return JsonResponse(result)


def get_modules_list(request):
    """
    根据业务ID和集群ID，查询对应下辖的模块列表
    """
    client = get_client_by_request(request)
    # 构造请求参数
    kwargs = {
        "bk_biz_id": request.GET.get('bk_biz_id'),
        "bk_set_id": request.GET.get("bk_set_id"),
        "fields": ["bk_module_id", "bk_module_name", "bk_set_id", "bk_biz_id", "bk_created_at", "bk_supplier_account"],
    }
    result = client.cc.search_module(kwargs)
    return JsonResponse(result)


def get_hosts_list(request):
    """
    根据传递的查询条件，包括但不限于（业务ID、集群ID、模块ID、主机ID、主机维护人）
    查询主机列表
    """
    client = get_client_by_request(request)
    # 构造请求参数
    kwargs = {
        "bk_biz_id": request.GET.get("bk_biz_id"),
        # TODO 待优化项：学有余力的同学可尝试实现分页
        "page": {
            "start": 0,
            "limit": 100,
        },
        "fields": [
            "bk_host_id",  # 主机ID
            "bk_cloud_id",  # 云区域ID
            "bk_host_innerip",  # 主机内网IP
            "bk_os_type",  # 操作系统类型
            "bk_mac",  # 主机MAC地址
            "operator",  # 操作人
            "bk_bak_operator"  # 备份维护人
        ]
    }

    # 添加可选参数，包括但不限于主机ID、集群ID、模块ID...
    if request.GET.get("bk_set_id"):
        # kwargs["bk_set_id"] = request.GET.get("bk_set_id")    // 错误写法，注意数据结构数据结构与接口文档保持一致
        kwargs["bk_set_ids"] = [int(request.GET.get("bk_set_id"))]  # 注意这里的数据结构，仔细阅读接口文档

    if request.GET.get("bk_module_id"):
        # kwargs["bk_set_id"] = request.GET.get("bk_set_id")    // 错误写法，注意数据结构数据结构与接口文档保持一致
        kwargs["bk_module_ids"] = [int(request.GET.get("bk_module_id"))]  # 注意这里的数据结构，仔细阅读接口文档

    rules = []  # 额外查询参数，配置查询规则
    if request.GET.get("operator"):
        rules.append({
            "field": "operator",
            "operator": "equal",
            "value": request.GET.get("operator")
        })

    # TODO：添加额外查询参数

    if rules:
        kwargs["host_property_filter"] = {
            "condition": "AND",
            "rules": rules
        }

    result = client.cc.list_biz_hosts(kwargs)
    return JsonResponse(result)


def get_host_detail(request):
    """
    根据主机ID，查询主机详情信息
    """
    client = get_client_by_request(request)

    kwargs = {
        "bk_host_id": request.GET.get("bk_host_id")
    }

    result = client.cc.get_host_base_info(kwargs)
    return JsonResponse(result)


def search_file(request):
    """
    根据主机IP、文件目录和文件后缀，查询符合条件的主机文件
    """

    # 注意：先在constants.py中替换SEARCH_FILE_PLAN_ID为你自己在作业平台上新建的方案的ID
    host_id_list_str = request.GET.get("host_id_list")
    host_id_list = [int(bk_host_id) for bk_host_id in host_id_list_str.split(",")]
    kwargs = {
        "bk_scope_type": "biz",
        "bk_scope_id": JOB_BK_BIZ_ID,
        "job_plan_id": SEARCH_FILE_PLAN_ID,
        # TODO 修改为你创建的执行方案的全局变量
        "global_var_list": [
            {
                "name": "host_list",
                "server": {
                    "host_id_list": host_id_list,
                },
            },
            {
                "name": "search_path",
                "value": request.GET.get("search_path"),
            },
            {
                "name": "suffix",
                "value": request.GET.get("suffix"),
            },
        ],
    }

    # 调用执行方案
    client = get_client_by_request(request)
    job_instance_id = client.jobv3.execute_job_plan(**kwargs).get("data").get("job_instance_id")

    kwargs = {
        "bk_scope_type": "biz",
        "bk_scope_id": JOB_BK_BIZ_ID,
        "job_instance_id": job_instance_id,
    }

    attempts = 0
    while attempts < MAX_ATTEMPTS:
        # 获取执行方案执行状态
        step_instance_list = client.jobv3.get_job_instance_status(**kwargs).get("data").get("step_instance_list")
        if step_instance_list[0].get("status") == WAITING_CODE:
            time.sleep(JOB_RESULT_ATTEMPTS_INTERVAL)
        elif step_instance_list[0].get("status") != SUCCESS_CODE:
            res_data = {
                "result": False,
                "code": WEB_SUCCESS_CODE,
                "message": "search failed",
            }
            return JsonResponse(res_data)
        elif step_instance_list[0].get("status") == SUCCESS_CODE:
            break
        attempts += 1

    step_instance_id = step_instance_list[0].get("step_instance_id")

    log_list = []
    for bk_host_id in host_id_list:
        data = {
            "bk_scope_type": "biz",
            "bk_scope_id": JOB_BK_BIZ_ID,
            "job_instance_id": job_instance_id,
            "step_instance_id": step_instance_id,
            "bk_host_id": bk_host_id,
        }

        # 查询执行日志
        response = client.jobv3.get_job_instance_ip_log(**data).get("data")
        step_res = response.get("log_content")
        json_step_res = json.loads(step_res)

        json_step_res["bk_host_id"] = response.get("bk_host_id")
        log_list.append(json_step_res)

    res_data = {
        "result": True,
        "code": WEB_SUCCESS_CODE,
        "data": log_list,
    }
    return JsonResponse(res_data)


def backup_file(request):
    """
    根据主机IP、文件目录和文件后缀，备份符合条件的主机文件到指定目录
    """

    # 注意：先在constants.py中替换BACKUP_FILE_PLAN_ID为你自己在作业平台上新建的方案的ID
    host_id_list_str = request.GET.get("host_id_list")
    host_id_list = [int(bk_host_id) for bk_host_id in host_id_list_str.split(",")]
    search_path = request.GET.get("search_path")
    suffix = request.GET.get("suffix")
    kwargs = {
        "bk_scope_type": "biz",
        "bk_scope_id": JOB_BK_BIZ_ID,
        "job_plan_id": BACKUP_FILE_PLAN_ID,
        # TODO 修改为你创建的执行方案的全局变量
        "global_var_list": [
            {
                "name": "host_list",
                "server": {
                    "host_id_list": host_id_list,
                },
            },
            {
                "name": "search_path",
                "value": search_path
            },
            {
                "name": "suffix",
                "value": suffix
            },
            {
                "name": "backup_path",
                "value": request.GET.get("backup_path"),
            },
        ],
    }

    # 调用执行方案
    client = get_client_by_request(request)
    job_instance_id = client.jobv3.execute_job_plan(**kwargs).get("data").get("job_instance_id")

    kwargs = {
        "bk_scope_type": "biz",
        "bk_scope_id": JOB_BK_BIZ_ID,
        "job_instance_id": job_instance_id,
    }
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        # 获取执行方案执行状态
        step_instance_list = client.jobv3.get_job_instance_status(**kwargs).get("data").get("step_instance_list")
        if step_instance_list[0].get("status") == WAITING_CODE:
            time.sleep(JOB_RESULT_ATTEMPTS_INTERVAL)
        elif step_instance_list[0].get("status") != SUCCESS_CODE:
            res_data = {
                "result": False,
                "code": WEB_SUCCESS_CODE,
                "message": "backup failed",
            }
            return JsonResponse(res_data)
        elif step_instance_list[0].get("status") == SUCCESS_CODE:
            break
        attempts += 1

    step_instance_id = step_instance_list[0].get("step_instance_id")

    for bk_host_id in host_id_list:
        data = {
            "bk_scope_type": "biz",
            "bk_scope_id": JOB_BK_BIZ_ID,
            "job_instance_id": job_instance_id,
            "step_instance_id": step_instance_id,
            "bk_host_id": bk_host_id,
        }

        # 查询执行日志
        response = client.jobv3.get_job_instance_ip_log(**data).get("data")
        step_res = response.get("log_content")
        json_step_res = json.loads(step_res)

        for step_res in json_step_res:
            # 创建备份记录
            step_res["bk_host_id"] = bk_host_id
            step_res["bk_file_dir"] = search_path
            step_res["bk_file_suffix"] = suffix
            step_res["bk_file_operator"] = request.user.username
            step_res["bk_job_link"] = "{}/biz/{}/execute/task/{}".format(
                BK_JOB_HOST,
                JOB_BK_BIZ_ID,
                job_instance_id,
            )
            BackupRecord.objects.create(**step_res)

    res_data = {
        "result": True,
        "data": "success",
        "code": WEB_SUCCESS_CODE,
    }
    return JsonResponse(res_data)


def get_backup_record(request):
    """
    查询备份记录
    """
    res_data = {
        "result": True,
        "data": list(BackupRecord.objects.all().order_by("-id").values()),
        "code": WEB_SUCCESS_CODE,
    }
    return JsonResponse(res_data)
