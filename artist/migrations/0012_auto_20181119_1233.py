# Generated by Django 2.1.1 on 2018-11-19 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0011_auto_20181117_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='work',
            options={'ordering': ['-created_at']},
        ),
    ]