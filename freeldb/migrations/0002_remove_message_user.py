# Generated by Django 3.0.5 on 2021-11-15 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freeldb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='user',
        ),
    ]
