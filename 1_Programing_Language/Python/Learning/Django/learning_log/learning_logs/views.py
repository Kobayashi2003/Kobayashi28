from django.shortcuts import render, redirect, get_object_or_404 # 函数 render()，它根据视图提供的数据渲染响应
                                            # 我们导入了函数 redirect，用户提交主题后将使用这个函数重定向到页面 topics。函数 redirect 将视图名作为参数，并将用户重定向到这个视图。

from django.contrib.auth.decorators import login_required

from django.http import Http404 # 服务器上没有请求的资源时，标准的做法时返回 404 响应。这里导入了异常 Http404，并在用户请求其不应查看的主题时引发这个异常

from .models import Topic, Entry # 首先导入与需数据相关联的模型

from .forms import TopicForm, EntryForm # 导入表单

# Create your views here.


def index(request):
    """学习笔记的主页。"""
    return render(request, 'learning_logs/index.html') # URL 请求与刚才定义的模式匹配时，Django 将在文件 views.py 中查找函数 index()，再将对象 request 传递给这个视图函数
                                                        # 这里不需要处理任何数据，因此这个函数只包含调用 render() 的代码
                                                        # 这里向函数 render() 提供了两个实参：对象 request 以及一个可用于创建页面的模板

@login_required # 将 login_required 作为修饰器应用于视图函数 topics()，让 Python 在运行 topics() 的代码之前先运行 login_required() 的代码。login_required() 的代码检查用户是否已登录，仅当用户已登录时，Django  才运行 topics() 的代码。如果用户未登录，就重定向到登录页面。为实现这种重定向，需要修改 settings.py
def topics(request): # 函数 topics() 包含一个形参：Django 从服务器那里收到的 request 对象。
    """显示所有主题"""
    # topics = Topic.objects.order_by('date_added') # 查询数据库，请求提供 Topic 对象，并根据属性 date_added 紧密型排序。返回的查询集被存储在 topics 中
    topics = Topic.objects.filter(owner=request.user).order_by('date_added') # 用户登录后，request 对象将会有一个 user 属性，其中存储了有关该用户的信息。查询 TOpic.objects.filter(owner=request.user) 让 Django 只从数据库中获取 owner 属性为当前用户的 Topic 对象。
    context = {'topics': topics} # 定义一个发送给模板的上下文。上下文是一个字典，其中的键是将在模板中用来访问数据的名称，而值是要发送给模板的数据。
    return render(request, 'learning_logs/topics.html', context) # 创建使用数据的页面时，除了对象 request 和模板的路径外，还将变量 context 传递给 render

@login_required
def topic(request, topic_id): # 这个函数接受表达式 /<int:topic_id>/ 捕获的值，并肩齐存储到 topic_id 中
    """显示单个主题及其所有的条目"""
    # topic = Topic.objects.get(id=topic_id) # 使用 get() 来获取指定的主题
    topic = get_object_or_404(Topic, id=topic_id)
    # 确认请求的主题属于当前用户。
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added') # 获取与该主题相关联的条目，并根据 date_added 进行排序；date_added 前面的减号指定按降序排列
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request): # 函数 new_topic() 将请求对象作为参数。用户初次请求该页面时，其浏览器将发送 GET 请求；用户填写并提交表单时，其浏览器将发送 POST 请求。根据请求的类型，可确定用户请求的是空表单含税要求对填写好的表单进行处理
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm() # 当请求类型不是 POST 时，创建一个 TopicForm 实例，由于实例化 TopicForm 时没有指定任何实参，Django 将创建一个空表单，供用户填写后，将其赋给变量 form，再通过上下文字典将这个表单发给模板
    else:
        # POST 提交的数据：对数据进行处理
        form = TopicForm(data=request.POST) # 我们使用用户输入的数据（存储在 request.POST 中）创建一个 TopicForm 实例，这样对象 form 将包含用户提交的信息
        if form.is_valid(): # 要将提交的信息保存到数据库，必须先通过检查确定它们是有效的。方法 is_valid() 核实用户填写了所有必不可少的字段（表单字段默认都是必不可少的），且输入的数据与要求的字段类型一致。这种自动验证避免了我们去做大量的工作
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # form.save() # 如果所有的字段都有效，就可调用 save() ，将数据写入数据库
            return redirect('learning_logs:topics') # 保存数据后，使用 redirect() 将用户的浏览器重定向到页面 topics

    # 显示空表单或指出表单数据无效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id): # new_entry() 的定义包含形参 topic_id，用于存储从 URL 中获得的值。渲染页面和处理表单数据时，都需要知道针对的是哪个主题，因此使用 topic_id 来获得正确的主题
    """在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据：创建一个表单
        form = EntryForm()
    else:
        # POST 提交的数据：对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # 调用 save() 时，传递实参 commit=False，让 Django 创建一个新的条目对象，并将其赋给 new_entry，但不保存到数据库中
            new_entry.topic = topic # 将 new_entry 的属性 topic 设置为在这个函数开头从数据库中获取的主题，将其与正确的主题相关联
            new_entry.save() # 调用 save() 且不指定任何实参，将条目保存到数据库中
            return redirect('learning_logs:topic', topic_id=topic_id)

    # 显示空表单或指出表单数据无效
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    # 获取用户要修改的条目对象以及与其关联的主题
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单。
        form = EntryForm(instance=entry) # 使用实参 instance=entry 创建一个 EntryForm 实例。这个实参让 Django 创建一个表单，并使用既有条目对象中的信息填充它。用户看到既有的数据，并且能够编辑
    else:
        # POST 提交的数据：对数据进行处理.
        form = EntryForm(instance=entry, data=request.POST) # 传递实参 instance=entry 和 data=reqest.POST，让 Django 根据既有条目对象创建一个表单实例，并根据 request.POST 中的相关数据对其进行修改。
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)