# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OzbarginTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('includes', models.CharField(max_length=255, verbose_name='includes')),
                ('excludes', models.CharField(max_length=255, verbose_name='excludes')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Create at', null=True)),
            ],
        ),
    ]
