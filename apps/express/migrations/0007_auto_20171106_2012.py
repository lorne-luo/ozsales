# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0006_expresscarrier_track_id_regex'),
    ]

    operations = [
        migrations.AddField(
            model_name='expresscarrier',
            name='id_upload_url',
            field=models.URLField(verbose_name='upload url', blank=True),
        ),
        migrations.AlterField(
            model_name='expresscarrier',
            name='name_en',
            field=models.CharField(default='', max_length=50, verbose_name='name_en', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expresscarrier',
            name='search_url',
            field=models.URLField(default='', verbose_name='Search url', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expresscarrier',
            name='track_id_regex',
            field=models.CharField(max_length=512, verbose_name='ID regex', blank=True),
        ),
        migrations.AlterField(
            model_name='expresscarrier',
            name='website',
            field=models.URLField(default='', verbose_name='Website', blank=True),
            preserve_default=False,
        ),
    ]
