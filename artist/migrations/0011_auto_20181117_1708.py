# Generated by Django 2.1.1 on 2018-11-17 08:08

import artist.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0010_auto_20181112_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='work',
        ),
        migrations.AddField(
            model_name='work',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=artist.models.upload_to),
        ),
        migrations.AddField(
            model_name='work',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=artist.models.upload_to),
        ),
        migrations.AddField(
            model_name='work',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=artist.models.upload_to),
        ),
        migrations.AddField(
            model_name='work',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to=artist.models.upload_to),
        ),
        migrations.AddField(
            model_name='work',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to=artist.models.upload_to),
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]
