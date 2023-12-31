# Generated by Django 2.2.27 on 2022-06-24 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0005_auto_20220526_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluservotes',
            name='vote',
            field=models.CharField(choices=[('1', 'Avanza de fase'), ('2', 'Se mantiene en fase'), ('3', 'Sube de prioridad'), ('4', 'Baja de prioridad'), ('5', 'Banco de Ideas'), ('6', 'Se mantiene en prioridad')], max_length=100, verbose_name='Voto de la Idea'),
        ),
        migrations.AlterField(
            model_name='uservotes',
            name='vote',
            field=models.CharField(choices=[('1', 'Avanza de fase'), ('2', 'Se mantiene en fase'), ('3', 'Sube de prioridad'), ('4', 'Baja de prioridad'), ('5', 'Banco de Ideas'), ('6', 'Se mantiene en prioridad')], max_length=100, verbose_name='Voto de la Idea'),
        ),
    ]
