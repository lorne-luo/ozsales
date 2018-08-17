# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_usersession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='session',
            field=models.OneToOneField(to='sessions.Session'),
        ),
    ]
