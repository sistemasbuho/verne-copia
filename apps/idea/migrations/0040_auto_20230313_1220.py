# Generated by Django 2.2.27 on 2023-03-13 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0039_auto_20230313_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='complete',
            field=models.BooleanField(default=False, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='taskbyidea',
            name='complete',
            field=models.CharField(blank=True, choices=[('Por hacer', 'Por hacer'), ('En ejecución', 'En ejecución'), ('Completado', 'Completado')], default='Por hacer', max_length=20, null=True, verbose_name='Estado'),
        ),
    ]
