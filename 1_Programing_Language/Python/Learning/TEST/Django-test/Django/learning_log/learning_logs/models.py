from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 这里导入了模块 models，并让我们创建自己的模型。
# 模型告诉 Django 如何处理应用程序中存储的数据。
# 在代码层面，模型就是一个类，包含属性和方法


class Topic(models.Model): # 我们创建了一个名为 Topic 的类，它继承 Model，即 Django 中定义了模型基本功能的类
    """用户学习的主题"""
    text = models.CharField(max_length=200) # 属性 text 是一个 CharField——由字符组成的数据，即文本。
                                            # 需要存储少量文本时可使用 CharField
                                            # 定义 CharField 属性时，必须告诉 Django 该在数据库中预留多少空间
    date_added = models.DateTimeField(auto_now_add=True) # 属性 date_added 是一个 DateTimeField——记录日期和时间的数据。
                                                        # 我们传递了实参 auto_now_add=True，每当用户创建新主题时，Django 都会将这个属性自动设置为当前日期和时间

    owner = models.ForeignKey(User, on_delete=models.CASCADE) # 这将建立到模型 User 的外键关系。用户被删除时，所有与之相关联的主题也会被删除

    def __str__(self): # 需要告诉 Django，默认使用哪个属性来显示有关主题的信息。Django 调用方法 __str__() 来显示模型的简单表示
        """返回模型的字符串表示。"""
        return self.text


class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) # 属性 topic 是个 ForeignKey 实例。
                                                                # 外键（ForeiKey）是一个数据库术语，它指向数据库中的另一条记录，这里是将每个条目关联到特定主题
                                                                # 创建每个主题时，都分配了一个键（ID）。需要在两项数据之间建立联系时，Django 使用与每项信息相关联的键
                                                                # 实参 on_delete=models.CASCADE 让 Django 在删除主题的同时删除所有与之相关联的条目，这成为 级联删除（cascading delete）

    text = models.TextField() # 属性 text 是一个 TextField 实例。这种字段的长度不受限制
    date_added = models.DateTimeField(auto_now_add=True) # 属性 date_added 让我们能够按创建顺序呈现条目，并在每个条目旁边放置时间戳

    class Meta: # Meta 类存储用于管理模型的额外信息。在这里，它让我们能够设置一个特殊属性，让 Django 在需要时使用 Entries 来表示多个条目。
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        return f"{self.text[:50]}..." # 返回条目中的一部分文本
