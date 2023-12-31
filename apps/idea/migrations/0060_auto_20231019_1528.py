# Generated by Django 2.2.27 on 2023-10-19 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0059_auto_20230829_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalidea',
            name='innovation_estrategia',
            field=models.CharField(blank=True, choices=[('Crecimiento de mercados', 'Crecimiento de mercados'), ('Innovación', 'Innovación'), ('Sostenibilidad', 'Sostenibilidad'), ('Nuestra gente y cultura', 'Nuestra gente y cultura'), ('Productividad y mejora continua', 'Productividad y mejora continua')], max_length=40, null=True, verbose_name='¿A que pilar estratégico le apunta la idea?'),
        ),
        migrations.AddField(
            model_name='idea',
            name='innovation_estrategia',
            field=models.CharField(blank=True, choices=[('Crecimiento de mercados', 'Crecimiento de mercados'), ('Innovación', 'Innovación'), ('Sostenibilidad', 'Sostenibilidad'), ('Nuestra gente y cultura', 'Nuestra gente y cultura'), ('Productividad y mejora continua', 'Productividad y mejora continua')], max_length=40, null=True, verbose_name='¿A que pilar estratégico le apunta la idea?'),
        ),
    ]
