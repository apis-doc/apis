# Generated by Django 3.2.18 on 2023-10-08 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestlog',
            name='err',
            field=models.TextField(default='', verbose_name='异常信息'),
        ),
        migrations.AlterField(
            model_name='requestlog',
            name='content_type',
            field=models.IntegerField(choices=[(0, 'application/json'), (1, 'text/html'), (2, 'multipart/form-data'), (3, 'text/plain'), (4, 'application/xml'), (5, 'application/x-www-form-urlencoded')], default=0, verbose_name='请求体类型'),
        ),
    ]