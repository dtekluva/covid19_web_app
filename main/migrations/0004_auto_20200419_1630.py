# Generated by Django 3.0.5 on 2020-04-19 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200413_0211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='name',
            new_name='state_name',
        ),
    ]
