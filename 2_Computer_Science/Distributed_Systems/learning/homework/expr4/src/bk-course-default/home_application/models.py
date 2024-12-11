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

from django.db import models


# Create your models here.


class BackupRecord(models.Model):
    """
    备份记录
    """
    bk_host_id = models.IntegerField(verbose_name="主机ID")
    bk_file_dir = models.CharField(verbose_name="备份目录", max_length=1024)
    bk_file_suffix = models.CharField(verbose_name="文件名后缀", max_length=255)
    bk_backup_name = models.CharField(verbose_name="备份文件名", max_length=1024)
    bk_file_create_time = models.CharField(verbose_name="备份时间", max_length=30)
    bk_file_operator = models.CharField(verbose_name="备份人", max_length=30)
    bk_job_link = models.CharField(verbose_name="JOB结果", max_length=100)

    class Meta:
        verbose_name = "备份记录"
        verbose_name_plural = verbose_name


class ApiRequestCount(models.Model):
    """
    API请求次数记录模型，用于运营分析
    """

    pass    # 请实现API请求次数记录数据Model
