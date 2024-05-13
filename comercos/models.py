# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from fontawesome_5.fields import IconField
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.contrib.gis.db import models as geomodels
from image_cropping import ImageRatioField
from django.core.mail import EmailMessage
import urllib

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField


class Categoria(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=255, editable = False)
    icona = IconField()
    
    def admin_icona(self):
        if self.icona:
            return mark_safe('<span style="font-size: 1.7rem;">%s</span>' % (self.icona.as_html()))
        else:
            return 'no disponible'
    
    admin_icona.allow_tags = True
    
    def __unicode__(self):
        return "%s" % (self.nom)
    def __str__(self):
        return "%s" % (self.nom)
    class Meta:
        verbose_name_plural = "Categories comerç"
        ordering = ['nom']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super(Categoria, self).save(*args, **kwargs)

WEEKDAYS = [
    (1, "Dilluns"),
    (2, "Dimarts"),
    (3, "Dimecres"),
    (4, "Dijous"),
    (5, "Divendres"),
    (6, "Dissabte"),
    (7, "Diumenge"),
]

class OpeningHours(models.Model):
    #user = models.ForeignKey(Establiment,on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    
    def __unicode__(self):
        return "%s: De %s a %s" % (self.get_weekday_display(),self.from_hour,self.to_hour)
    def __str__(self):
        return "%s: De %s a %s" % (self.get_weekday_display(),self.from_hour,self.to_hour)
    
    class Meta:
        verbose_name_plural = "Horaris"
        ordering = ['weekday']
    


class Establiment(models.Model):
    '''Dades del propietari'''
    nom_propietari = models.CharField(max_length=100)
    cognoms_propietari = models.CharField(max_length=100)
    tel_propietari = models.CharField(max_length=15, blank=True)
    email_propietari = models.EmailField(max_length=254, blank=True)
    dni = models.CharField(unique=False, max_length=10, null=True, blank=True, default=None)
    
    '''Dades de l'establiment'''
    nom = models.CharField(max_length=100, verbose_name='Nom Establiment')
    slug = models.SlugField(unique=True, max_length=255, editable = False)
    categories = models.ManyToManyField(Categoria)
    email = models.EmailField(max_length=254, blank=True)
    telefon = models.CharField(max_length=15, blank=True)
    mobil = models.CharField(max_length=15, blank=True)
    whatsapp = models.CharField(max_length=15, blank=True)
    
    reparteix_domicili = models.BooleanField(default=False)
    per_emportar = models.BooleanField(default=False)
    web = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    descripcio = models.TextField(blank=True)
    horaris = models.ManyToManyField(OpeningHours)
    
    image = models.ImageField(blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '340x200')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    adreca = models.CharField(max_length=255)
    location = LocationField(based_fields=['adreca'], zoom=15, default=Point(1.8610, 41.6674))
    
    
    visible = models.BooleanField(default=False)
    enviar_correu = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s" % (self.nom)
    def __str__(self):
        return "%s" % (self.nom)
    
    class Meta:
        verbose_name_plural = "Establiments"
        ordering = ['nom']
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        
        super(Establiment, self).save(*args, **kwargs)
        
        
        if self.enviar_correu==True:
            try:
                #enviem el correu amb el QR
                email_body = """\
                                <html>
                                  <head></head>
                                  <body>
                                    <h2>Benvingut %s, al lloc web comerç obert de l'Ajuntament de Sant Vicenç de Castellet</h2>
                                    <p>S'ha procedit a donar d'alta l'establiment "%s" a la nostra base de dades.</p>
                                    <h5></h5>
                                  </body>
                                </html>
                                """ % (self.nom_propietari, self.nom)

                email = EmailMessage('Comerç obert a Sant Vicenç de Castellet', email_body, to=[self.email_propietari])
                email.content_subtype = "html"
                #email.attach_file('%s/qr/%s' % (settings.MY_STATIC_ROOT, self.qr_image))

                email.send()
            except:
                return HttpResponse('Error enviant el correu')
        
        self.enviar_correu = False
        super(Establiment, self).save(*args, **kwargs)
    
