from django.shortcuts import render
from .models import WebsiteLink
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import VehiculeCompagnie,Vehicule,CustomUser,CompagnieVehicule
# Create your views here.
def index(request):

    websites = WebsiteLink.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        websites = websites.filter(name__icontains=search_query) | websites.filter(description__icontains=search_query)

    # Pagination des WebsiteLinks
    paginator = Paginator(websites, 3)  # 3 WebsiteLinks par page
    page = request.GET.get('page')

    try:
        websites = paginator.page(page)
    except PageNotAnInteger:
        websites = paginator.page(1)
    except EmptyPage:
        websites = paginator.page(paginator.num_pages)

    vehiculecompagnie = VehiculeCompagnie.objects.all().order_by('-created_at')[:3]
    vehicules = Vehicule.objects.all().order_by('-created_at')[:3]
    compagnies = CompagnieVehicule.objects.all().order_by('-created_at')[:3]
                

    return render(request, 'base/index.html', {  
        'vehiculecompagnie': vehiculecompagnie, 
        'compagnies': compagnies, 
        'vehicules': vehicules, 
        'websites': websites,  # Passer les WebsiteLinks à la vue
        'paginator': paginator,  # Passer le paginator à la vue
    })

def apropos(request):
    return render(request,'base/apropos.html')

def contact(request):
    return render(request,'base/contact.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from core.models import VehiculeCompagnie,Vehicule,CustomUser,CompagnieVehicule

# def CompagnieVehiculeList(request):
    
#     # Récupération des filtres depuis l'URL
#     pays = request.GET.get('pays', '')  # Filtre par pays
#     nom = request.GET.get('nom', '')    # Filtre par nom

#     # Filtrage des véhicules selon les paramètres reçus
#     vehicules = CompagnieVehicule.objects.all()

#     # Filtre par pays
#     if pays:
#         vehicules = vehicules.filter(pays=pays)

#     # Filtre par nom (insensible à la casse)
#     if nom:
#         vehicules = vehicules.filter(nom__icontains=nom)

#     # Pagination
#     paginator = Paginator(vehicules, 6)  # 6 véhicules par page
#     page = request.GET.get('page')

#     try:
#         vehicules = paginator.page(page)
#     except PageNotAnInteger:
#         vehicules = paginator.page(1)  # Si la page demandée n'est pas un entier
#     except EmptyPage:
#         vehicules = paginator.page(paginator.num_pages)  # Si la page demandée est vide

#     # Passage des données à la template
#     return render(request, 'base/compagnievehiculelist.html', {
#         'vehicules': vehicules,
#         'pays': pays,
#         'nom': nom,
#     })


def vehicule_compagnie_list(request):
    # Filtrer les véhicules de la compagnie
    
    vehicules = VehiculeCompagnie.objects.filter().order_by('-created_at')

    # Filtre par type de véhicule
    type_bien = request.GET.get('type_bien', '')
    if type_bien:
        vehicules = vehicules.filter(type_bien=type_bien)

    # Filtre par nom
    nom = request.GET.get('nom', '')
    if nom:
        vehicules = vehicules.filter(nom__icontains=nom)  # Recherche insensible à la casse

    # Filtre par prix (minimum et maximum)
    prix_min = request.GET.get('prix_min', '')
    prix_max = request.GET.get('prix_max', '')
    if prix_min:
        vehicules = vehicules.filter(prix__gte=prix_min)  # Prix supérieur ou égal à prix_min
    if prix_max:
        vehicules = vehicules.filter(prix__lte=prix_max)  # Prix inférieur ou égal à prix_max

    # Pagination
    paginator = Paginator(vehicules, 6)  # 6 véhicules par page
    page = request.GET.get('page')

    try:
        vehicules = paginator.page(page)
    except PageNotAnInteger:
        vehicules = paginator.page(1)
    except EmptyPage:
        vehicules = paginator.page(paginator.num_pages)

    # Passer les véhicules et autres données au template
    context = {
        
        'vehicules': vehicules,
        'paginator': paginator,
        'type_bien': type_bien,
        'nom': nom,
        'prix_min': prix_min,
        'prix_max': prix_max,
    }

    return render(request, 'base/vehicule_compagnie_list.html', context)


 # Cette vue est protégée par l'authentification
def vehicule_list(request):
    # Récupérer les paramètres GET
    nom = request.GET.get('nom', '')
    type_bien = request.GET.get('type_bien', '')
    prix_min = request.GET.get('prix_min', '')
    prix_max = request.GET.get('prix_max', '')
    description = request.GET.get('description', '')

    # Récupérer tous les véhicules, sans filtrer par utilisateur
    vehicules = Vehicule.objects.all().order_by('-created_at')

    # Appliquer les filtres si les paramètres sont présents
    if nom:
        vehicules = vehicules.filter(nom__icontains=nom)
    if type_bien:
        vehicules = vehicules.filter(type_bien=type_bien)
    if prix_min:
        vehicules = vehicules.filter(prix__gte=prix_min)  # Prix supérieur ou égal à prix_min
    if prix_max:
        vehicules = vehicules.filter(prix__lte=prix_max)  # Prix inférieur ou égal à prix_max
    if description:
        vehicules = vehicules.filter(description__icontains=description)

    # Pagination des véhicules
    paginator_vehicules = Paginator(vehicules, 6)  # 6 véhicules par page
    page_vehicules = request.GET.get('page')
    try:
        vehicules = paginator_vehicules.page(page_vehicules)
    except PageNotAnInteger:
        vehicules = paginator_vehicules.page(1)
    except EmptyPage:
        vehicules = paginator_vehicules.page(paginator_vehicules.num_pages)

    # Passer les véhicules et les filtres au template
    context = {
        "vehicules": vehicules,
        "nom": nom,
        "type_bien": type_bien,
        "prix_min": prix_min,
        "prix_max": prix_max,
        "description": description,
        "paginator_vehicules": paginator_vehicules,
    }

    return render(request, "base/vehicule_list.html", context)



def UserListView(request):
    # Récupération des filtres depuis l'URL
    username = request.GET.get('username', '')  # Filtre par nom d'utilisateur

    # Filtrage des utilisateurs selon le nom d'utilisateur
    users = CustomUser.objects.all()

    # Filtre par nom d'utilisateur
    if username:
        users = users.filter(username__icontains=username)  # Insensible à la casse

    # Pagination
    paginator = Paginator(users, 6)  # 6 utilisateurs par page
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)  # Si la page demandée n'est pas un entier
    except EmptyPage:
        users = paginator.page(paginator.num_pages)  # Si la page demandée est vide

    # Passage des données à la template
    return render(request, 'base/user_list.html', {
        'users': users,
        'username': username,
    })

