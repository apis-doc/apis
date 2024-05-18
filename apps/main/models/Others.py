# --*--*--*--*--*--*- Create by bh at 2024/5/16 23:37 -*--*--*--*--*--*--
from django.db import models
from django.contrib.auth.models import User


class UserConfig(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    config = models.JSONField(verbose_name='配置内容')
    create_time = models.DateTimeField(auto_created=True, auto_now=False, auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_created=False, auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户配置表'
        verbose_name_plural = verbose_name
        db_table = 'user_configs'

    def __str__(self):
        return
