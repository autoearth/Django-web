# Generated by Django 3.0 on 2020-06-22 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproduct',
            name='imageurl',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
