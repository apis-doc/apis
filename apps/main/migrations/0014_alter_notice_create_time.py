# Generated by Django 3.2.18 on 2024-05-17 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_notice_release_userconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='create_time',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间'),
        ),
    ]
