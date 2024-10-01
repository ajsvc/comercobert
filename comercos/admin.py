from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin
from django.contrib.gis.geos import Point
from .models import Categoria, Establiment, OpeningHours
from .forms import EstablimentForm
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

class LeafletWidget(forms.TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)

        # Coordenadas predeterminadas
        lat = 41.6674  
        lng = 1.8610   

        # Manejo del valor actual de location
        if isinstance(value, Point):
            lat = value.y
            lng = value.x
        elif value:
            # Convertir el valor a coordenadas
            coords = value.replace("SRID=4326;POINT (", "").replace(")", "").split(" ")
            if len(coords) == 2:
                lng = float(coords[0])
                lat = float(coords[1])

        # Bounding box ajustado para Sant Vicenç de Castellet
        min_lat = 41.6590  # Límite sur del municipio
        max_lat = 41.6790  # Límite norte del municipio
        min_lon = 1.8510    # Límite oeste del municipio
        max_lon = 1.8710    # Límite este del municipio

        return mark_safe(f'''
            <div id="map" style="height: 400px;"></div>
            <script>
                var map = L.map('map').setView([{lat}, {lng}], 15);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors'
                }}).addTo(map);

                var marker = L.marker([{lat}, {lng}], {{draggable: true}}).addTo(map);

                // Actualizar el campo location al hacer clic en el mapa
                map.on('click', function(e) {{
                    marker.setLatLng(e.latlng);
                    var lng = e.latlng.lng.toFixed(10);
                    var lat = e.latlng.lat.toFixed(10);
                    document.getElementById("{name}").value = "SRID=4326;POINT (" + lng + " " + lat + ")";
                }});

                // Actualizar el campo location al arrastrar el marcador
                marker.on('dragend', function(e) {{
                    var latlng = marker.getLatLng();
                    var lng = latlng.lng.toFixed(10);
                    var lat = latlng.lat.toFixed(10);
                    document.getElementById("{name}").value = "SRID=4326;POINT (" + lng + " " + lat + ")";
                }});

                // Crear el botón de búsqueda y añadirlo al contenedor del input
                var searchButton = document.createElement('button');
                searchButton.innerHTML = '🔍';
                searchButton.onclick = function(e) {{
                    e.preventDefault();  // Evitar que el botón dispare el submit
                    // Obtener el valor del campo adreca directamente
                    var address = document.getElementById('id_adreca').value;  // Tomar el valor directamente
                    if (address) {{
                        // Limitar la búsqueda con el bounding box
                        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${{address}}&bounded=1&viewbox={min_lon},{max_lat},{max_lon},{min_lat}`)
                            .then(response => response.json())
                            .then(data => {{
                                if (data.length > 0) {{
                                    var lat = data[0].lat;
                                    var lng = data[0].lon;
                                    map.setView([lat, lng], 15);
                                    marker.setLatLng([lat, lng]);
                                    document.getElementById("{name}").value = "SRID=4326;POINT (" + lng + " " + lat + ")";
                                }} else {{
                                    console.warn('Dirección no encontrada.');
                                }}
                            }})
                            .catch(error => {{
                                console.error('Error en la geocodificación:', error);
                            }});
                    }} else {{
                        console.warn('Por favor, introduce una dirección.');
                    }}
                }};
                
                // Modificar el div que contiene el input id_adreca
                var adrecaInput = document.getElementById('id_adreca');
                var divAdreca = adrecaInput.parentNode;  // Obtener el div contenedor
                divAdreca.classList.add('button-group');  // Agregar la clase 'button-group'
                divAdreca.appendChild(searchButton);  // Añadir el botón al div contenedor

                // Mostrar la ubicación si ya existe en el campo location
                var locationFieldValue = document.getElementById("{name}").value;
                if (locationFieldValue) {{
                    var coords = locationFieldValue.replace("SRID=4326;POINT (", "").replace(")", "").split(" ");
                    if (coords.length == 2) {{
                        var lng = parseFloat(coords[0]);
                        var lat = parseFloat(coords[1]);
                        marker.setLatLng([lat, lng]);
                        map.setView([lat, lng], 15);
                    }}
                }}
            </script>
            {html}
        ''')


class EstablimentAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('id','nom','email','adreca')
    list_display_links = ('id','nom')
    list_filter = ('nom',)
    form = EstablimentForm

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)        

    class Media:
        css = {
            'all': (
                '/static/fontawesome_5/css/django-fontawesome.css',
                '/static/fontawesome_5/css/all.min.css',
                'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css',  # Leaflet CSS
            ),
        }
        js = (
            'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js',  # Leaflet JS
        )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'location':
            field.widget = LeafletWidget()  # Usamos el widget personalizado
        return field
    


class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('id','weekday','from_hour','to_hour',)





admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Establiment,EstablimentAdmin)
admin.site.register(OpeningHours,OpeningHoursAdmin)