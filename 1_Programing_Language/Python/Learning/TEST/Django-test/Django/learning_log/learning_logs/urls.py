"""定义 learning_logs 的 URL 模式"""

from django.urls import path # 导入函数 path，因为需要使用它将 URL 映射到视图

from . import views # 导入模块 views，其中的句点让 Python 从当前 urls.py 模块所在的文件夹导入 views.py

app_name = 'learning_logs' # 变量 app_name 让 Django 能够将这个 urls.py 文件同项目内其它应用程序中的同名文件区分开来

urlpatterns = [ # 列表，包含可在应用程序 learning_logs 中请求的也页面
    # 主页
    path('', views.index, name='index'), # 实际的 URL 模式是对函数 path() 的调用，这个函数接受三个实参
                                        # 第一个是一个字符串，帮助 Django 正确地路由（route）请求
                                        # 接收到请求的 URL 后，Django 力图将请求路由给一个视图。为此，它搜索所有的 URL 模式，找到与当前请求匹配的哪个。
                                        # Django 忽略项目的基础 URL（http://localhost:8000/）,因此空字符串（''）与基础 URL 匹配，而其它的 URL 都与这个模式不匹配
                                        # 如果请求的 URL 与任何既有的 URL 模式都不匹配，Django 将返回一个错误页面

                                        # path() 的第二个实参指定了要调用 view.py 中的哪个函数。
                                        # 请求的 URL 与前述的正则表达式匹配时，Django 将调用 view.py 中的函数 index()

                                        # 第三个实参将这个 URL 模式的名称指定为 index，让我们能够再代码的其它地方引用它。每当需要提供到这个主页的链接时，都将使用这个名称，而不编写 URL
    # 显示所有主题
    path('topics/', views.topics, name='topics'),

    # 特定主题的详细页面
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # /<int:topic_id>/ 与包含在两个斜杠内的整数匹配，并将这个整数存储在一个名为 topic_id 的实参中

    # 用于添加新主题的页面
    path('new_topic/', views.new_topic, name='new_topic'),

    # 用于添加新条目的页面
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

    # 用于编辑条目的页面
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
]