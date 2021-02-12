# Generated by Django 3.0.5 on 2020-08-16 22:27

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='#', null=True, upload_to=blog.models.image_upload),
        ),
        migrations.AddField(
            model_name='post',
            name='onlyMe',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='stuff',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
