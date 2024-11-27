from django.db import models

from django.db import models
from blueapps.account.models import User

class WeChatUser(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    email = models.EmailField(unique=True, null=True)
    motto = models.CharField(max_length=100, null=True, blank=True)
    pic = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Status(models.Model):
    user = models.ForeignKey(WeChatUser, models.CASCADE)
    text = models.CharField(max_length=280)
    pics = models.CharField(max_length=100, null=True, blank=True)
    pub_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-id']