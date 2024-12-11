from django.urls import path
from . import views 

urlpatterns = [
path('signup',views.signup, name='signup'),
path('signin',views.signin, name='signin'),
path('signout',views.signout, name='signout'),
path('profile/', views.profile, name='profile'),
path('profile/<int:user_id>/', views.profile, name='user_profile'),
path('update_profile',views.update_profile, name='update_profile'),
path('add_vehicule/', views.add_vehicule, name='add_vehicule'),
path('vehicule/<int:id>/', views.vehicule_detail, name='vehicule_detail'),
path('vehicule/<int:id>/contact/', views.contact_vehicule, name='contact_vehicule'),
path('vehiculecompagnie/<int:id>/contact/', views.contact_vehiculecompagnie, name='contact_vehiculecompagnie'),
path('create_compagnie_vehicule/', views.create_compagnie_vehicule, name='create_compagnie_vehicule'),
path('compagnie/<slug:compagnie_slug>/', views.compagnie_detail, name='compagnie_detail'),
# path('user/compagnie/<int:compagnie_id>/', views.compagnie_detail, name='compagnie_detail'),
path('compagnie-vehicule/<slug:compagnie_slug>/vehicule/ajouter/', views.create_vehicule_compagnie, name='create_vehicule_compagnie'),
path('user/vehiculecompagnie/<int:id>/', views.vehiculecompagnie_detail, name='vehiculecompagnie_detail'),
path('compagnie_list/', views.CompagnieVehiculeList, name='compagnie_vehiculelist'),
]
