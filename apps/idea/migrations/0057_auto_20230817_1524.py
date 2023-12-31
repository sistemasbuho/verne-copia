# Generated by Django 2.2.27 on 2023-08-17 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0056_auto_20230421_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalidea',
            name='state',
            field=models.CharField(blank=True, choices=[('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado'), ('En revisión', 'En revisión'), ('Por definir', 'Por definir')], default='Por definir', max_length=20, null=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='historicalidea',
            name='state',
            field=models.CharField(blank=True, choices=[('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado'), ('En revisión', 'En revisión'), ('Por definir', 'Por definir')], default='Sí', max_length=20, null=True, verbose_name='Proposito'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='idea_externa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='idea.ExternalIdea', verbose_name='Idea Externa'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='state',
            field=models.CharField(blank=True, choices=[('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado'), ('En revisión', 'En revisión'), ('Por definir', 'Por definir')], default='Sí', max_length=20, null=True, verbose_name='Proposito'),
        ),
    ]
