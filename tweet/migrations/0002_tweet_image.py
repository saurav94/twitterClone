# Generated by Django 3.1.2 on 2020-10-13 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='image',
            field=models.ImageField(blank=True, upload_to='tweet_pics'),
        ),
    ]
