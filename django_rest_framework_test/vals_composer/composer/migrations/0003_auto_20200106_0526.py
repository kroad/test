# Generated by Django 3.0 on 2020-01-06 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('composer', '0002_auto_20200106_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bpm',
            name='bpm',
            field=models.IntegerField(),
        ),
    ]
