# Generated by Django 2.2.10 on 2021-10-14 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0008_auto_20211014_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalphase_date',
            name='phase',
        ),
        migrations.RemoveField(
            model_name='phase_date',
            name='phase',
        ),
        migrations.AddField(
            model_name='phase_date',
            name='task',
            field=models.ManyToManyField(to='idea.Task', verbose_name='Tareas'),
        ),
    ]
