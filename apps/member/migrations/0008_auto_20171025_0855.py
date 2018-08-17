# -*- coding: utf-8 -*-


from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('member', '0007_auto_20161115_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersession',
            name='session',
        ),
        migrations.RemoveField(
            model_name='usersession',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='seller',
            options={},
        ),
        migrations.AlterModelManagers(
            name='seller',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='seller',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='password',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='username',
        ),
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address', blank=True),
        ),
        migrations.DeleteModel(
            name='UserSession',
        ),
    ]
