# Generated by Django 2.2.27 on 2022-08-22 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0021_externalidea'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='externalidea',
            options={'verbose_name': 'Ideas Externas', 'verbose_name_plural': 'Ideas Externas'},
        ),
        migrations.AddField(
            model_name='externalidea',
            name='conditions',
            field=models.BooleanField(default=True, verbose_name='Términos y condiciones'),
        ),
        migrations.AlterField(
            model_name='externalidea',
            name='external_email',
            field=models.CharField(max_length=150, verbose_name='Email externo'),
        ),
        migrations.AlterField(
            model_name='externalidea',
            name='external_name',
            field=models.CharField(max_length=150, verbose_name='Nombre externo'),
        ),
    ]
