# Generated by Django 2.2.10 on 2021-12-02 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0014_auto_20211201_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalidea',
            name='investment',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Inversión adicional'),
        ),
        migrations.AlterField(
            model_name='historicalidea',
            name='price_score',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Precio total leguas'),
        ),
        migrations.AlterField(
            model_name='historicalidea',
            name='total_investment',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Inversión total'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='investment',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Inversión adicional'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='price_score',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Precio total leguas'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='total_investment',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Inversión total'),
        ),
    ]
