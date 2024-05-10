from django.urls import path

from . import views
from django.conf.urls import url

urlpatterns = [
	path('', views.home, name='home'),
	url(r'^alta/$',views.alta, name='alta'),
    url(r'^gracies/$',views.registre_ok, name='gracies'),
	#url( r'^search/$', views.search, name = 'search' ),
	url(r'^(?P<slug_establiment>[0-9a-zA-Z-_]+)/$', views.establiment_detall, name='establiment_detall'),
    #url(r'^(?P<slug_categoria>[0-9a-zA-Z-_]+)/(?P<slug_tramit>[0-9a-zA-Z-_]+)/$', views.tramit_detall, name='tramit_detall'),
    
]