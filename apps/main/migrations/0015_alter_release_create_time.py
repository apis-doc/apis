# Generated by Django 3.2.18 on 2024-05-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_notice_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='create_time',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间'),
        ),
    ]