# Generated by Django 2.2.27 on 2023-03-15 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0042_auto_20230313_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalidea',
            name='region',
        ),
        migrations.RemoveField(
            model_name='idea',
            name='region',
        ),
        migrations.AddField(
            model_name='idea',
            name='region',
            field=models.ManyToManyField(blank=True, related_name='region_implementacion', to='idea.Subregion', verbose_name='Regiones de aplicación de la idea'),
        ),
    ]
