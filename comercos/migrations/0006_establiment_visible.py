# Generated by Django 3.0.8 on 2020-10-18 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercos', '0005_establiment_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='establiment',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]