# Generated by Django 2.2.10 on 2021-10-04 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerheader',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descripción Banner'),
        ),
        migrations.AlterField(
            model_name='bannerheader',
            name='header_title',
            field=models.CharField(max_length=100, verbose_name='Título Banner'),
        ),
        migrations.AlterField(
            model_name='bannerheader',
            name='image_banner',
            field=models.ImageField(upload_to='', verbose_name='Imagen Banner'),
        ),
        migrations.AlterField(
            model_name='exploresection',
            name='card_description',
            field=models.CharField(max_length=100, verbose_name='Descripción Card Sección Explora'),
        ),
        migrations.AlterField(
            model_name='exploresection',
            name='card_image',
            field=models.ImageField(upload_to='', verbose_name='Imagen Card Sección Explora'),
        ),
        migrations.AlterField(
            model_name='exploresection',
            name='card_title',
            field=models.CharField(max_length=100, verbose_name='Título Card Sección Explora'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='description_footer',
            field=models.CharField(max_length=100, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='link_facebook',
            field=models.URLField(max_length=1500, unique=True, verbose_name='Link Facebook'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='link_linkedin',
            field=models.URLField(max_length=1500, unique=True, verbose_name='Link Linkedin'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='link_twitter',
            field=models.URLField(max_length=1500, unique=True, verbose_name='Link Twitter'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='location',
            field=models.CharField(max_length=100, verbose_name='Ubicación'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='logo_footer',
            field=models.ImageField(upload_to='', verbose_name='Logo Footer'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='telephone',
            field=models.IntegerField(verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='terms_conditions',
            field=models.URLField(blank=True, max_length=1500, null=True, unique=True, verbose_name='Términos y condiciones'),
        ),
        migrations.AlterField(
            model_name='footer',
            name='url_website',
            field=models.URLField(max_length=1500, verbose_name='Link Página Web'),
        ),
        migrations.AlterField(
            model_name='headerexploresection',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descripción Sección Explora'),
        ),
        migrations.AlterField(
            model_name='headerexploresection',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Título Sección Explora'),
        ),
        migrations.AlterField(
            model_name='headerteamsection',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descripción Sección Equipo'),
        ),
        migrations.AlterField(
            model_name='headerteamsection',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Título Sección Equipo'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='items',
            field=models.CharField(max_length=20, verbose_name='Itmes Menú'),
        ),
        migrations.AlterField(
            model_name='menulogo',
            name='logo',
            field=models.ImageField(upload_to='', verbose_name='Imagen Logo'),
        ),
        migrations.AlterField(
            model_name='metrics',
            name='conter_data',
            field=models.IntegerField(verbose_name='Contador Métricas'),
        ),
        migrations.AlterField(
            model_name='metrics',
            name='title_counter',
            field=models.CharField(max_length=100, verbose_name='Título Métricas'),
        ),
        migrations.AlterField(
            model_name='processsection',
            name='card_description',
            field=models.TextField(max_length=1000, verbose_name='Descripción Sección Procesos'),
        ),
        migrations.AlterField(
            model_name='processsection',
            name='card_description_two',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Descripción Sección Procesos'),
        ),
        migrations.AlterField(
            model_name='processsection',
            name='card_image',
            field=models.ImageField(upload_to='', verbose_name='Imagen Sección Procesos'),
        ),
        migrations.AlterField(
            model_name='processsection',
            name='card_title',
            field=models.CharField(max_length=100, verbose_name='Título Sección Procesos'),
        ),
        migrations.AlterField(
            model_name='teamsection',
            name='team_image',
            field=models.ImageField(upload_to='', verbose_name='Imagen Miembro Equipo Innovación'),
        ),
        migrations.AlterField(
            model_name='teamsection',
            name='team_name',
            field=models.CharField(max_length=100, verbose_name='Nombre Miembro Equipo Innovación'),
        ),
        migrations.AlterField(
            model_name='teamsection',
            name='team_role',
            field=models.CharField(max_length=100, verbose_name='Cargo Miembro Equipo Innovación'),
        ),
    ]
