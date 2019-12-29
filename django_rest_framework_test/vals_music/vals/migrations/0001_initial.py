# Generated by Django 3.0 on 2019-12-28 14:26

from django.db import migrations, models
import uuid
import vals.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=256, upload_to='')),
                ('filename', models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.IntegerField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='UploadVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=256, upload_to=vals.models.filename_manager)),
                ('filename', models.CharField(blank=True, max_length=256)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('uploaded_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]