# Generated by Django 2.2.27 on 2023-03-30 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0049_auto_20230317_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalidea',
            name='solucion',
            field=models.TextField(default=1, max_length=5000, verbose_name='Solución'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='idea',
            name='solucion',
            field=models.TextField(default=1, max_length=5000, verbose_name='Solución'),
            preserve_default=False,
        ),
    ]
