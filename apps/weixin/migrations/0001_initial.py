# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WxApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('app_id', models.CharField(max_length=128, verbose_name='App ID')),
                ('app_secret', models.CharField(max_length=128, verbose_name='App Secret')),
                ('access_token', models.CharField(max_length=512, null=True, verbose_name='Access Token', blank=True)),
                ('token_expiry', models.DateTimeField(null=True, verbose_name='Token Expiry', blank=True)),
                ('jsapi_ticket', models.CharField(max_length=512, null=True, verbose_name='JsApi Ticket', blank=True)),
                ('ticket_expiry', models.DateTimeField(null=True, verbose_name='Ticket Expiry', blank=True)),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update At', null=True)),
            ],
            options={
                'verbose_name': 'Weixin App',
                'verbose_name_plural': 'Weixin Apps',
            },
        ),
    ]
