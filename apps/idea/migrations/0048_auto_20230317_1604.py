# Generated by Django 2.2.27 on 2023-03-17 16:04

import apps.idea.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0047_auto_20230317_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='primer_documento',
            field=models.FileField(blank=True, null=True, upload_to=apps.idea.models.Idea.custom_upload_to_documento, verbose_name='Documentación de Evolución 1'),
        ),
    ]
