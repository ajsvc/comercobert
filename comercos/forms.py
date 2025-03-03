from django import forms
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
from leaflet.forms.widgets import LeafletWidget
from django.core.validators import validate_image_file_extension
from .models import Establiment, Categoria
from localflavor.es.forms import ESIdentityCardNumberField
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from django.forms import ModelChoiceField
from django.contrib.gis.geos import Point
from location_field.forms.spatial import LocationField
from django.template.defaultfilters import slugify
from image_cropping import ImageCropWidget





class FiltrarEstablimentsForm(forms.Form):
    categoria = forms.ModelChoiceField(required=False, queryset=Categoria.objects.all(), empty_label="seleccioni categoria")
    entrega_domicili = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'text-white' }))
    per_emportar = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'text-white' }))
    nom = forms.CharField(
        required=False,
        label="Buscar pel nom",
        widget=forms.TextInput(attrs={'placeholder': 'Nom establiment...', 'class': 'form-control'})
    )    

class MySelectDateWidget(forms.SelectDateWidget):

    def get_context(self, name, value, attrs):
        old_state = self.is_required
        self.is_required = False
        context = super(MySelectDateWidget, self).get_context(name, value, attrs)
        self.is_required = old_state
        return context


class AltaEstablimentForm(forms.Form):
    nom_propietari = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'nom del propietari...'}))
    cognoms_propietari = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'cognoms del propietari...'}))
    dni_propietari = ESIdentityCardNumberField(only_nif=True, label='', widget=forms.TextInput(attrs={'placeholder': 'dni del propietari...'}))
    telefon_propietari = forms.CharField(max_length=15, label='', widget=forms.TextInput(attrs={'placeholder': 'telèfon del propietari...'}))
    email_propietari = forms.EmailField(max_length=254, label='', widget=forms.EmailInput(attrs={'placeholder': 'correu electrònic del propietari...'}))
    email2_propietari = forms.EmailField(max_length=254, label='', widget=forms.EmailInput(attrs={'placeholder': 'repeteix correu electrònic del propietari...'}))
    
    nom = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'nom establiment...'}))
    email = forms.EmailField(max_length=254, label='', widget=forms.EmailInput(attrs={'placeholder': 'correu electrònic establiment...'}))
    email2 = forms.EmailField(max_length=254, label='', widget=forms.EmailInput(attrs={'placeholder': 'repeteix correu electrònic establiment...'}))
    
    telefon = forms.CharField(required=False, max_length=15, label='', widget=forms.TextInput(attrs={'placeholder': 'telèfon establiment...'}))
    mobil = forms.CharField(required=False, max_length=15, label='', widget=forms.TextInput(attrs={'placeholder': 'mòbil establiment...'}))
    whatsapp = forms.CharField(required=False, max_length=15, label='', widget=forms.TextInput(attrs={'placeholder': 'whatsapp establiment...'}))
    
    web = forms.URLField(required=False, label='', help_text="http://www.exemple.cat",widget=forms.TextInput(attrs={'placeholder': 'lloc web...'}))
    facebook = forms.URLField(required=False, label='', help_text="https://facebook.com/nom establiment",widget=forms.TextInput(attrs={'placeholder': 'lloc a Facebook...'}))
    instagram = forms.URLField(required=False, label='', help_text="https://instagram.com/nom establiment",widget=forms.TextInput(attrs={'placeholder': 'lloc instagram...'}))
    horari = forms.CharField(required=False, label='', help_text="Horari de dilluns a diumenge", widget=forms.Textarea(attrs={'placeholder': 'horari...'}))
    
    adreca = forms.CharField(
        max_length=100, label='',
        help_text='S\'actualitza al mapa, si no es posiciona correctament, pots moure el marcador al mapa. Adreça completa: Carrer, núm.0 , 08295 Sant Vicenç de Castellet',
        widget=forms.TextInput(attrs={
            'placeholder': 'adreça establiment...',
            'style': 'width: 80%; display: inline-block;'
        }))
    
    # Cambiar location para usar el LeafletWidget
    location = forms.CharField(
        label='',
        #widget=LeafletWidget(attrs={'map_height': '500px', })
        widget=forms.HiddenInput()
    )  
        
    reparteix_domicili = forms.BooleanField(required=False, label='Entrega a domicili', widget=forms.CheckboxInput(attrs={'placeholder': 'reparteix a domicili...' }))
    per_emportar = forms.BooleanField(required=False, label='Menjar per emportar', widget=forms.CheckboxInput(attrs={'placeholder': 'menjar per emportar...' }))
    
    image = forms.ImageField(required=False, label='Imatge', help_text='adjunta una imatge del teu establiment. No ha de tenir molta resolució.')
    
    politica_dades = forms.BooleanField(
        label="Accepto la política de privacitat d'aquest lloc web",
        widget=forms.CheckboxInput(attrs={
            'placeholder': 'accepto',
            'class': 'form-check-input'
            }
        ))
    
    
    categories = forms.MultipleChoiceField(
        label='Categories de l\'establiment:',
        help_text='Premeu la tecla "Control", o "Command" en un Mac, per seleccionar més d\'un valor.', 
        choices=Categoria.objects.all().values_list('id','nom')
    )
    
    captcha = ReCaptchaField(label='')
    
    def __init__(self, *args, **kwargs):
        super(AltaEstablimentForm, self).__init__(*args, **kwargs)
        self.fields['categories'].choices = Categoria.objects.all().values_list('id','nom')
    
    def clean_location(self):
        # Convierte la ubicación a un objeto Point antes de guardar
        location = self.cleaned_data.get('location')
        if location:
            lon, lat = map(float, location.split())
            return Point(lon, lat)
        raise forms.Validatio
    
    def clean_dni_propietari(self):
        dni = self.cleaned_data.get('dni_propietari',None)
        if dni is not None and dni != '': 
            try:
                establiment = Establiment.objects.get(dni=dni)
            except Establiment.DoesNotExist:
                return dni or None
            raise forms.ValidationError("Aquest DNI ja existeix")
        else:
            return None
    
    
    def clean_nom(self):
        #mirem que no existeixi un altre establiment amb el mateix slug
        nom = self.cleaned_data.get('nom',None)
        
        if nom is not None and nom != '': 
            try:
                establiment = Establiment.objects.get(slug=slugify(nom))
            except Establiment.DoesNotExist:
                return nom or None
            raise forms.ValidationError("Aquest nom d'establiment ja existeix")
        else:
            return None
    
    def clean(self):
        cleaned_data = super(AltaEstablimentForm, self).clean()
        
        email_propietari = self.cleaned_data.get('email_propietari', None)
        email2_propietari = self.cleaned_data.get('email2_propietari', None)
        
        if email_propietari and email2_propietari and (email_propietari != email2_propietari):
            self._errors['email2_propietari'] = self.error_class(['Els correus electrònics no coincideixen.'])
            del self.cleaned_data['email2']
        
        email = self.cleaned_data.get('email', None)
        email2 = self.cleaned_data.get('email2', None)

        if email and email2 and (email != email2):
            self._errors['email2'] = self.error_class(['Els correus electrònics no coincideixen.'])
            del self.cleaned_data['email2']
       
        return cleaned_data
    
class EstablimentForm(forms.ModelForm):
    class Meta:
        model = Establiment
        fields = (
            "nom_propietari",
            "cognoms_propietari",
            "tel_propietari",
            "email_propietari",
            "dni",
            "nom",
            "categories",
            "email",
            "telefon",
            "mobil",
            "whatsapp",
            "reparteix_domicili",
            "per_emportar",
            "web",
            "facebook",
            "instagram",
            "descripcio",
            "horaris",            
            "cropping",            
            "adreca",
            "location",
            "visible"
        )
    image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple":False}),
        label=("Afegir imatge"),
        required=False
    )
        
    def clean_location(self):
        location_value = self.cleaned_data.get('location')

        if isinstance(location_value, str):
            try:
                # Convierte la cadena WKT en un objeto GEOSGeometry
                point = GEOSGeometry(location_value)
                if not point.geom_type == 'Point':
                    raise ValidationError("La ubicación debe ser un punto.")
                return point
            except Exception as e:
                raise ValidationError(f"Error al procesar la ubicación: {e}")
        
        return location_value  # Si ya es un objeto Point

    def clean_imatges(self):
        """Asegúrate de que solo se suban imágenes."""
        for upload in self.files.getlist("imatges"):
            validate_image_file_extension(upload)
'''
class RegistreForm(forms.Form):
	#id_butlleta = forms.IntegerField(widget=forms.HiddenInput())
	id_acte = forms.IntegerField(widget=forms.HiddenInput())
	tipus = forms.CharField(widget=forms.HiddenInput())
'''
