# Generated by Django 3.0.5 on 2021-11-28 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freeldb', '0009_auto_20211127_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='picture',
            field=models.ImageField(blank=True, upload_to='static'),
        ),
    ]
