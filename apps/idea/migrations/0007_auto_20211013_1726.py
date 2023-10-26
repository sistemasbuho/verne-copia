# Generated by Django 2.2.10 on 2021-10-13 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0006_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalidea',
            name='feedback',
            field=models.TextField(default=' ', max_length=5000, verbose_name='Observaciones'),
        ),
        migrations.AddField(
            model_name='idea',
            name='feedback',
            field=models.TextField(default=' ', max_length=5000, verbose_name='Observaciones'),
        ),
        migrations.AddField(
            model_name='task',
            name='phase',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='idea.Phase'),
        ),
        migrations.AlterField(
            model_name='historicalidea',
            name='link_documentation',
            field=models.URLField(blank=True, default=' ', max_length=1500, null=True, verbose_name='Enlace a Documentación'),
        ),
        migrations.AlterField(
            model_name='historicalphase_date',
            name='description',
            field=models.TextField(default=' ', max_length=5000, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='historicalphase_date',
            name='feedback',
            field=models.TextField(default=' ', max_length=5000, verbose_name='Comentarios'),
        ),
        migrations.AlterField(
            model_name='historicalphase_date',
            name='link_documentation',
            field=models.URLField(blank=True, default=' ', max_length=1500, null=True, verbose_name='Enlace a Documentación'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='link_documentation',
            field=models.URLField(blank=True, default=' ', max_length=1500, null=True, verbose_name='Enlace a Documentación'),
        ),
        migrations.AlterField(
            model_name='phase_date',
            name='description',
            field=models.TextField(default=' ', max_length=5000, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='phase_date',
            name='feedback',
            field=models.TextField(default=' ', max_length=5000, verbose_name='Comentarios'),
        ),
        migrations.AlterField(
            model_name='phase_date',
            name='link_documentation',
            field=models.URLField(blank=True, default=' ', max_length=1500, null=True, verbose_name='Enlace a Documentación'),
        ),
    ]
