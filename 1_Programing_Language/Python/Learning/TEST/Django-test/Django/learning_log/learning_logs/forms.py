from django import forms

from .models import Topic, Entry

# 首先导入模块 forms 以及要使用的模型

class TopicForm(forms.ModelForm):
    class Meta: # 最简单的 ModelForm 版本只包含一个内嵌的 Meta 类，它告诉 Django 根据哪个模型创建表单以及在表单中包含哪些字段
        model = Topic
        fields = ['text'] # 表单中只需包含字段 text
        labels = {'text': ''} # 让 Django 不要为字段 text 生成标签


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ' '} # 这里给字段 'text' 制定了标签 'Entry:'
        widgets = {'text': forms.Textarea(attrs={'cols': 80})} # 小部件（widget）是一个 HTML 表单元素。通过设置属性 widgets，可覆盖 Django 选择的默认小部件。通过让 Django 使用 forms.Textarea，我们定制了字段 'text' 的输入小部件，将文本区域的宽度设置为 80 列，而不是默认的 40 列
