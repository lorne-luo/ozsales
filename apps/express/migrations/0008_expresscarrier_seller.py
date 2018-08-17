# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0011_auto_20171107_1104'),
        ('express', '0007_auto_20171106_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='expresscarrier',
            name='seller',
            field=models.ForeignKey(blank=True, to='member.Seller', null=True),
        ),
    ]
