# Generated by Django 2.2.27 on 2024-01-02 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0063_auto_20231109_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalidea',
            name='innovation_type',
            field=models.CharField(blank=True, choices=[('Incremental', 'Incremental'), ('Producto', 'Producto'), ('Procesos', 'Procesos')], max_length=20, null=True, verbose_name='¿En qué etapa se encuentra ia idea?'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='innovation_type',
            field=models.CharField(blank=True, choices=[('Incremental', 'Incremental'), ('Producto', 'Producto'), ('Procesos', 'Procesos')], max_length=20, null=True, verbose_name='¿En qué etapa se encuentra ia idea?'),
        ),
    ]
