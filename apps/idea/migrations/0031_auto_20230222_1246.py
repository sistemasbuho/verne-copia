# Generated by Django 2.2.27 on 2023-02-22 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0030_auto_20230220_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalidea',
            name='proposito',
            field=models.CharField(blank=True, choices=[('Sí', 'Sí'), ('No', 'No')], default='Sí', max_length=20, null=True, verbose_name='Proposito'),
        ),
        migrations.AlterField(
            model_name='externalidea',
            name='state',
            field=models.CharField(blank=True, choices=[('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado'), ('Por definir', 'Por definir')], default='Por definir', max_length=20, null=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='historicalidea',
            name='state',
            field=models.CharField(blank=True, choices=[('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado'), ('Por definir', 'Por definir')], default='Sí', max_length=20, null=True, verbose_name='Proposito'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='state',
            field=models.CharField(blank=True, choices=[('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado'), ('Por definir', 'Por definir')], default='Sí', max_length=20, null=True, verbose_name='Proposito'),
        ),
    ]
