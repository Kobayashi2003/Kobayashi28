"""为应用程序 users 定义 URL 模式"""

from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    # 包含默认的身份验证 URL
    path('', include('django.contrib.auth.urls')), # 登录页面的 URL 模式与 URL http://localhost:8080/users/login/ 匹配。这个 URL 中的单词 users 让 Django 在 users/urls.py 中查找，而单词 login 让它将请求发送给 Django 的默认视图 login

    # 注册页面
    path('register/', views.register, name='register'),
]