# Generated by Django 3.0 on 2020-07-08 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20200706_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproduct',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
    ]
