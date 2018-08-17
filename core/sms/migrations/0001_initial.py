# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='DateTime')),
                ('app_name', models.CharField(max_length=16, null=True, verbose_name='App Name', blank=True)),
                ('send_to', models.CharField(max_length=32, verbose_name='Send To')),
                ('content', models.CharField(max_length=255, null=True, verbose_name='Content', blank=True)),
                ('url', models.URLField(max_length=255, null=True, verbose_name='Url', blank=True)),
                ('success', models.BooleanField(default=False, verbose_name='Success')),
            ],
        ),
    ]
