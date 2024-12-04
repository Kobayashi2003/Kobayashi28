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
from django.http import JsonResponse
from django.shortcuts import render

from blueking.component.shortcuts import get_client_by_request


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


# 开发样例，在这里实现了【查询业务列表接口】
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


def get_sets_list(request):
    """
    根据业务 ID，查询业务下的集群列表
    """
    client = get_client_by_request(request)
    # 请求参数
    kwargs = {
        "bk_biz_id": request.GET.get('bk_biz_id'),  # 从 request.GET 中获取传递的查询参数
        "fields": ["bk_set_id", "bk_set_name", "bk_biz_id", 
                  "bk_created_at", "bk_supplier_account"],
    }
    result = client.cc.search_set(kwargs)
    return JsonResponse(result)


def get_modules_list(request):
    """
    根据业务 ID 和集群 ID，查询对应下的模块列表
    """
    client = get_client_by_request(request)
    # 构造请求参数
    kwargs = {
        "bk_biz_id": request.GET.get('bk_biz_id'),
        "bk_set_id": request.GET.get('bk_set_id'),
        "fields": ["bk_module_id", "bk_module_name", "bk_set_id",
                  "bk_biz_id", "bk_created_at", "bk_supplier_account"],
    }
    result = client.cc.search_module(kwargs)
    return JsonResponse(result)


def get_hosts_list(request):
    """
    根据传递的查询条件，包括但不限于（业务 ID、集群 ID、模块 ID、主机 ID、主机维护人）
    查询主机列表
    """
    client = get_client_by_request(request)
    # 构造请求参数
    kwargs = {
        "bk_biz_id": request.GET.get("bk_biz_id"),
        # TODO 待优化项: 学有余力的同学可尝试实现分页
        "page": {
            "start": 0,
            "limit": 100,
        },
        "fields": [
            "bk_host_id",      # 主机ID
            "bk_cloud_id",     # 云区域ID
            "bk_host_innerip", # 主机内网IP
            "bk_os_type",      # 操作系统类型
            "bk_mac",          # 主机MAC地址
            "operator",        # 操作人
            "bk_bak_operator"  # 备份维护人
        ]
    }

    # 添加可选参数，包括但不限于主机ID、集群ID、模块ID...
    if request.GET.get("bk_set_id"):
        # kwargs["bk_set_id"] = request.GET.get("bk_set_id")
        # 错误写法，注意数据结构和数据结构约束已文档为准
        kwargs["bk_set_ids"] = [int(request.GET.get("bk_set_id"))]  # 注意这里的数据结构，仔细阅读接口文档

    if request.GET.get("bk_module_id"):
        # kwargs["bk_set_id"] = request.GET.get("bk_set_id")
        # 错误写法，注意数据结构和数据结构约束已文档为准
        kwargs["bk_module_ids"] = [int(request.GET.get("bk_module_id"))]  # 注意这里的数据结构，仔细阅读接口文档

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