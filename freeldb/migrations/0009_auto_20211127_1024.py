# Generated by Django 3.0.5 on 2021-11-27 03:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('freeldb', '0008_auto_20211127_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='view',
            name='viewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views_from', to=settings.AUTH_USER_MODEL),
        ),
    ]
