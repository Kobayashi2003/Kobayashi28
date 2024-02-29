from django.contrib import admin

# Register your models here.

from .models import Topic, Entry
# 首先要导入要注册的模型 Topic。models 前面的句点让 Django 在 admin.py 所在的目录中查找 models.py

admin.site.register(Topic) # admin.site.register() 让 Django 通过管理网站管理模型
admin.site.register(Entry) 