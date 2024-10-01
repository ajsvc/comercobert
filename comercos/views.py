from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404, HttpResponse

from .serializers import EstablimentSerializer
from .models import Categoria, Establiment, OpeningHours
from django.template.context import RequestContext
from django.db.models import Q
import json
from .forms import AltaEstablimentForm, FiltrarEstablimentsForm
from django.core.mail import EmailMessage

def home(request):
    context = locals()
    template = 'home.html'
        
    establiments = Establiment.objects.filter(visible=True)
    
    categoria = request.GET.get('categoria')
    entrega_domicili = request.GET.get('entrega_domicili', None)
    per_emportar = request.GET.get('per_emportar', None)
    nom = request.GET.get('nom',None)
    
    if categoria:
        establiments = establiments.filter(categories=categoria)

    if entrega_domicili:
        establiments = establiments.filter(reparteix_domicili=True)
    
    
    if per_emportar:
        establiments = establiments.filter(per_emportar=True)
    
    if nom:
        establiments = establiments.filter(nom__icontains=nom)
        
      
       
    establiments_json = EstablimentSerializer(establiments, many=True)

    context['establiments'] = establiments
    context['categories'] = Categoria.objects.all()

    
    form = FiltrarEstablimentsForm(initial={'entrega_domicili': entrega_domicili, 'per_emportar': per_emportar, 'categoria': categoria})
    context['form'] = form
    
            
    return render(request, template, context) 



def registre_ok(request):
    context = locals()
    template = 'gracies.html'
    
    form_data = json.loads(request.session.get('form', {}))
    establiment = Establiment.objects.get(id=request.session.get('id_establiment'))
    #context['butlleta'] = butlleta

    #request.session['dni'] = ''
    return render(request, template, context) 



def alta(request):
 
    context = locals()
    template = 'establiment_alta.html'
    
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AltaEstablimentForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():            
            # process the data in form.cleaned_data as required
            nou_establiment = Establiment()
            
            nou_establiment.nom_propietari = form.cleaned_data['nom_propietari']
            nou_establiment.cognoms_propietari = form.cleaned_data['cognoms_propietari']
            nou_establiment.dni = form.cleaned_data['dni_propietari']
            nou_establiment.telefon_propietari = form.cleaned_data['telefon_propietari']
            nou_establiment.email_propietari = form.cleaned_data['email_propietari']
            
            nou_establiment.nom = form.cleaned_data['nom']
            nou_establiment.email = form.cleaned_data['email']
            
            nou_establiment.telefon = form.cleaned_data['telefon']
            nou_establiment.mobil = form.cleaned_data['mobil']
            nou_establiment.whatsapp = form.cleaned_data['whatsapp']
            
            nou_establiment.web = form.cleaned_data['web']
            nou_establiment.facebook = form.cleaned_data['facebook']
            nou_establiment.instagram = form.cleaned_data['instagram']
            nou_establiment.descripcio = form.cleaned_data['horari']
            
            nou_establiment.adreca = form.cleaned_data['adreca']
            nou_establiment.location = form.cleaned_data['location']
            
            nou_establiment.reparteix_domicili = form.cleaned_data['reparteix_domicili']
            nou_establiment.per_emportar = form.cleaned_data['per_emportar']
                        
            image = request.FILES.get('image')
                        
            if image:
                nou_establiment.image = image                       
                        
            nou_establiment.save()
            
            #afegim les categories
            nou_establiment.categories.set(form.cleaned_data['categories'])


            #guardo el form a la sessió
            clean_form = json.dumps(form.cleaned_data, indent=4, sort_keys=True, default=str)
            request.session['form'] = clean_form
            request.session['id_establiment'] = nou_establiment.id
            
            
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
                                """ % (nou_establiment.nom_propietari, nou_establiment.nom)
                
                correus = [nou_establiment.email_propietari]
                if settings.PRODUCCIO:
                    correus.append('svc.comerc@svc.cat')
                    correus.append('sainzazueooj@svc.cat')
                
                email = EmailMessage('Comerç obert a Sant Vicenç de Castellet', email_body, to=correus)
                email.content_subtype = "html"
                #email.attach_file('%s/qr/%s' % (settings.MY_STATIC_ROOT, self.qr_image))
                
                email.send()
            except:
                return HttpResponse('Error enviant el correu')
            

            # redirect to a new URL:
            return redirect('gracies')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AltaEstablimentForm()
        context['form'] = form
        

    return render(request, template, context) 

def establiment_detall(request, slug_establiment):
    context = locals()
    template = 'establiment_detall.html'
    
    try:
        context['establiment'] = Establiment.objects.get(slug=slug_establiment)
    except:
        raise Http404("Aquesta establiment no existeix.") 
    
    
    
    
    return render(request, template, context)
