# Generated by Django 3.0.9 on 2021-01-11 21:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('site_models', '0019_auto_20210111_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentproductstore',
            name='date_received',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 11, 21, 26, 56, 341618, tzinfo=utc)),
            preserve_default=False,
        ),
    ]