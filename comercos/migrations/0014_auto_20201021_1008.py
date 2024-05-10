# Generated by Django 3.0.8 on 2020-10-21 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercos', '0013_auto_20201021_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='establiment',
            name='dni',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='establiment',
            name='enviar_correu',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='establiment',
            name='nom',
            field=models.CharField(max_length=100, verbose_name='Nom Establiment'),
        ),
    ]