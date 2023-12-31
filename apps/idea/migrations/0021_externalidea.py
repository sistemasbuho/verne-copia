# Generated by Django 2.2.27 on 2022-08-22 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0020_auto_20220526_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalIdea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('description', models.TextField(max_length=5000, verbose_name='Descripción')),
                ('title', models.CharField(max_length=150, verbose_name='Título')),
                ('is_active', models.BooleanField(default=True, verbose_name='¿Está activa?')),
                ('external_name', models.CharField(max_length=150, verbose_name='Título')),
                ('external_email', models.CharField(max_length=150, verbose_name='Título')),
            ],
        ),
    ]
