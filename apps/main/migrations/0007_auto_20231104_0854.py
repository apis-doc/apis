# Generated by Django 3.2.18 on 2023-11-04 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_api_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='params',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.params', verbose_name='父级参数'),
        ),
        migrations.AlterField(
            model_name='api',
            name='api_type',
            field=models.IntegerField(choices=[(0, 'Gateway'), (1, 'Restful')], default=0, verbose_name='接口类型'),
        ),
        migrations.AlterField(
            model_name='params',
            name='param_type',
            field=models.CharField(choices=[('str', 'str'), ('int', 'integer'), ('bool', 'boolean'), ('datetime', 'datetime'), ('array', 'array'), ('dict', 'object')], default='str', max_length=15, verbose_name='参数类型'),
        ),
        migrations.AlterField(
            model_name='requestlog',
            name='api_type',
            field=models.IntegerField(choices=[(0, 'Gateway'), (1, 'Restful')], default=0, verbose_name='接口类型'),
        ),
    ]
