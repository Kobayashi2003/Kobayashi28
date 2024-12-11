# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
import logging
from django.db.models import F


from home_application.models import ApiRequestCount

logger = logging.getLogger(__name__)

# 这里的CMDB和JOB对应的名称应该同你的URL定义的前缀，详见 /home_application/urls.py

CMDB_BEHAVIORS = [
    'biz-list',
    'set-list',
    'module-list',
    'host-list',
    'host-detail'
]

JOB_BEHAVIORS = [
    'search-file',
    'backup-file',
    'backup-record'
]


class RecordUserBehaviorMiddleware(MiddlewareMixin):
    """
    自定义中间件-记录用户行为，进行埋点
    """

    def process_request(self, request):
        pass    # 请实现你的中间件
