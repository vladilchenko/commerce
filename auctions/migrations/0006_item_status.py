# Generated by Django 4.0.4 on 2022-06-08 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_item_watching'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(default='open', max_length=6),
        ),
    ]
