# Generated by Django 2.2.27 on 2022-08-24 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0024_auto_20220824_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalidea',
            name='state',
            field=models.CharField(blank=True, choices=[('APROBADO', 'Aprobado'), ('RECHAZADO', 'Rechazado'), ('POR DEFINIR', 'Por definir')], default='POR DEFINIR', max_length=20, null=True, verbose_name='Estado'),
        ),
    ]
