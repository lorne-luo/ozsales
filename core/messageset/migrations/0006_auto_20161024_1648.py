# -*- coding: utf-8 -*-


from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('messageset', '0005_auto_20160222_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationcontent',
            name='contents',
            field=tinymce.models.HTMLField(verbose_name='\u5185\u5bb9'),
        ),
        migrations.AlterField(
            model_name='sitemailcontent',
            name='contents',
            field=tinymce.models.HTMLField(verbose_name='\u5185\u5bb9'),
        ),
    ]
