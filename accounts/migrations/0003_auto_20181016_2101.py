# Generated by Django 2.1.1 on 2018-10-16 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_artist_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='name',
            new_name='profile',
        ),
    ]
