# Generated by Django 2.1.1 on 2018-11-11 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20181102_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='user',
            field=models.OneToOneField(limit_choices_to={'is_artist': True}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
