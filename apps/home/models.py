from django.db import models

def custom_upload_to_logo(instance, filename):
    old_instance = MenuLogo.objects.get(pk=instance.pk)
    old_instance.logo.delete()
    return 'home/' + filename

class MenuLogo(models.Model):
    logo = models.ImageField( verbose_name=u'Imagen Logo',upload_to=custom_upload_to_logo)

        
    class Meta:
        verbose_name = "Logo Principal"
        verbose_name_plural = "Logo Principal"


class Menu(models.Model):
    items= models.CharField(max_length=20, verbose_name=u'Items Menú')

    def __str__(self):
        return self.items
        
    class Meta:
        ordering = ["id"]
        verbose_name = "Item Menú"
        verbose_name_plural = "Items Menú"


def custom_upload_to_banner(instance, filename):
    old_instance = BannerHeader.objects.get(pk=instance.pk)
    old_instance.image_banner.delete()
    return 'home/' + filename

class BannerHeader(models.Model):
    header_title = models.CharField(max_length=100, verbose_name=u'Título Banner')
    description = models.CharField(max_length=100, verbose_name=u'Descripción Banner')
    image_banner =  models.ImageField( verbose_name=u'Imagen Banner',upload_to=custom_upload_to_banner)

    def __str__(self):
        return self.header_title
        
    class Meta:
        verbose_name = "Banner Inicio"
        verbose_name_plural = "Banner Inicio"


class HeaderExploreSection(models.Model):
    title =  models.CharField(max_length=100, verbose_name=u'Título Sección Explora')
    description = models.CharField(max_length=100, verbose_name=u'Descripción Sección Explora')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Título Sección Explora"
        verbose_name_plural = "Título Sección Explora"



class ExploreSection(models.Model):
    card_image = models.ImageField( verbose_name=u'Imagen Card Sección Explora')
    card_title = models.CharField(max_length=100, verbose_name=u'Título Card Sección Explora')
    card_description = models.CharField(max_length=100, verbose_name=u'Descripción Card Sección Explora')

    def __str__(self):
        return self.card_title
        
    class Meta:
        verbose_name = "Card Sección Explora"
        verbose_name_plural = "Cards Sección Explora"


class ProcessSection(models.Model):
    card_image = models.ImageField(verbose_name=u'Imagen Sección Procesos')
    card_title = models.CharField(max_length=100, verbose_name=u'Título Sección Procesos')
    card_description = models.TextField(max_length=1000, verbose_name=u'Descripción Sección Procesos')
    card_description_two = models.TextField(max_length=1000, null =True, blank= True,verbose_name=u'Descripción Sección Procesos')

    def __str__(self):
        return self.card_title
        
    class Meta:
        verbose_name = "Card Sección Procesos"
        verbose_name_plural = "Cards Sección Procesos"


class Metrics(models.Model):
    conter_data = models.IntegerField(verbose_name=u'Contador Métricas')
    title_counter = models.CharField(max_length=100, verbose_name=u'Título Métricas')

    def __str__(self):
        return self.title_counter
        
    class Meta:
        verbose_name = "Métrica"
        verbose_name_plural = "Métricas"

        
class HeaderTeamSection(models.Model):
    title =  models.CharField(max_length=100, verbose_name=u'Título Sección Equipo')
    description = models.CharField(max_length=100, verbose_name=u'Descripción Sección Equipo')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Título Sección Equipo"
        verbose_name_plural = "Título Sección Equipo"

class HeaderMovilizadoresSection(models.Model):
    title =  models.CharField(max_length=100, verbose_name=u'Título Sección Movilizadores')
    description = models.CharField(max_length=100, verbose_name=u'Descripción Sección Movilizadores')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Título Sección Movilizadores"
        verbose_name_plural = "Título Sección Movilizadores"

class HeaderValoresSection(models.Model):
    title =  models.CharField(max_length=100, verbose_name=u'Título Nuestros Valores de Innovación')
    description = models.CharField(max_length=100, verbose_name=u'Descripción Nuestros Valores de Innovación')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Título Nuestros Valores de Innovación"
        verbose_name_plural = "Título Nuestros Valores de Innovación"




class TeamSection(models.Model):
    team_image = models.ImageField( verbose_name=u'Imagen Miembro Equipo Innovación')
    team_name = models.CharField(max_length=100, verbose_name=u'Nombre Miembro Equipo Innovación')
    team_role = models.CharField(max_length=100, verbose_name=u'Cargo Miembro Equipo Innovación')

    def __str__(self):
        return self.team_name
        
    class Meta:
        verbose_name = "Miembro Equipo"
        verbose_name_plural = "Miembros Equipo"


class Footer(models.Model):
    logo_footer =  models.ImageField( verbose_name=u'Logo Footer')
    description_footer =  models.CharField(max_length=100, verbose_name=u'Descripción')
    link_facebook = models.URLField(max_length=1500,null =True, blank = True, verbose_name=u'Link Facebook', unique = True)
    link_twitter = models.URLField(max_length=1500, null =True, blank = True,  verbose_name=u'Link Twitter', unique = True)
    link_linkedin = models.URLField(max_length=1500, null =True, blank = True,  verbose_name=u'Link Linkedin', unique = True)
    link_youtube = models.URLField(max_length=1500, null =True, blank = True,  verbose_name=u'Link Youtube', unique = True)
    address =  models.CharField(max_length=100, verbose_name=u'Dirección')
    location =  models.CharField(max_length=100, verbose_name=u'Ubicación')
    telephone = models.CharField(max_length=100,verbose_name=u'Teléfono')
    url_website =  models.URLField(max_length=1500, verbose_name=u'Link Página Web')
    terms_conditions =  models.FileField( null=True, blank= True, verbose_name=u'Términos y condiciones', unique = True)
    manifiesto =  models.FileField( null=True, blank= True, verbose_name=u'Manifiesto de Innovación', unique = True)

    def __str__(self):
        return self.description_footer
        
    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"


class MovilizadoresSection(models.Model):
    team_image = models.ImageField( verbose_name=u'Imagen Miembro Movilizador Innovación')
    team_name = models.CharField(max_length=100, verbose_name=u'Nombre Miembro Movilizador Innovación')
    team_role = models.CharField(max_length=100, verbose_name=u'Cargo Miembro Movilizador Innovación')

    def __str__(self):
        return self.team_name
        
    class Meta:
        verbose_name = "Movilizador de Innovación"
        verbose_name_plural = "Movilizadores de Innovación"


class ValoressSection(models.Model):
    team_image = models.ImageField( verbose_name=u'Imagen Nuestros Valores de Innovación')
    team_name = models.CharField(max_length=100, verbose_name=u'Nombre Nuestros Valores de Innovación')
    team_role = models.CharField(max_length=100, verbose_name=u'Cargo Nuestros Valores de Innovación')

    def __str__(self):
        return self.team_name
        
    class Meta:
        verbose_name = "Nuestros Valores de Innovación"
        verbose_name_plural = "Nuestros Valores de Innovación"


    