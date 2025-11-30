from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from . import views

urlpatterns = [
    path('set_language/', set_language, name='set_language'),
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
