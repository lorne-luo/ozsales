# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0002_auto_20171106_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='mobile',
            field=models.CharField(unique=True, max_length=30, verbose_name='mobile', blank=True),
        ),
    ]
