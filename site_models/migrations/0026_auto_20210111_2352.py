# Generated by Django 3.0.9 on 2021-01-11 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_models', '0025_auto_20210111_2344'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CurrentProductStore',
            new_name='CurrentOrderStore',
        ),
    ]
