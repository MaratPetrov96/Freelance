# Generated by Django 3.0.5 on 2021-11-27 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freeldb', '0007_auto_20211126_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
    ]
