# Generated by Django 4.0.4 on 2022-06-05 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_item_comment_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('book', 'Books'), ('video', 'Videos'), ('audio', 'Audios'), ('img', 'Images'), ('other', 'Other')], default='book', max_length=64),
        ),
    ]
