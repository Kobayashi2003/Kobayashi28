"""learning_log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # 注意此处需要导入 include 函数

urlpatterns = [ # 变量 urlpatterns 包含项目中应用程序的 URL
    path('admin/', admin.site.urls), # 模块 admin.site.urls定义了可在管理网站中请求的所有 URL
    path('users/', include('users.urls')),
    path('', include('learning_logs.urls')), # 默认的 urls.py 包含在文件夹 learning_log 中，现在需要在文件夹 learning_logs 中再创建一个 urls.py 文件
]
