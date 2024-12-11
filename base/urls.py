from django.urls import path
from . import views 

urlpatterns = [
path('',views.index, name='index'),
path('contact/', views.contact, name='contact'),
path('apropos/', views.apropos, name='apropos'),
path('vehiculecompagnielist/', views.vehicule_compagnie_list, name='vehiculecompagnielist'),
path('vehicules/', views.vehicule_list, name='vehicule_list'),
path('users/', views.UserListView, name='user_list'),
]