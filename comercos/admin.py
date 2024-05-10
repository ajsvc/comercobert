from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import Categoria, Establiment, OpeningHours
from ordered_model.admin import OrderedModelAdmin


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id','nom','admin_icona',)
    list_display_links = ('id','nom',)
    class Media:
        css = {
        'all': (
                '/static/fontawesome_5/css/django-fontawesome.css',
                '/static/fontawesome_5/css/all.min.css', 
                ),
        }




class EstablimentAdmin(ImageCroppingMixin, admin.ModelAdmin):
    default_lon = 41.6684
    default_lat = 1.8646
    default_zoom = 16
    list_display = ('id','nom',)
    list_display_links = ('id','nom',)
    


class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('id','weekday','from_hour','to_hour',)





admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Establiment,EstablimentAdmin)
admin.site.register(OpeningHours,OpeningHoursAdmin)