from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm, UpdateProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# from .models import Vehicule

 


def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte creer avec success")
            return redirect("signin")
        
    context = {"form":form}
    return render(request, "core/signup.html", context)

def signin (request):
    if request.method == 'POST':
        email = request.POST["email"]
        password= request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    context= {}
    return render(request, "core/login.html", context)

def signout(request):
    logout(request)
    return redirect("index")

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Vehicule
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Vehicule,CompagnieVehicule
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Vehicule, CompagnieVehicule,CustomUser

@login_required(login_url='signin')
def profile(request, user_id=None):
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user
    type_choisi = request.GET.get('type', 'vehicule')  # Récupérer le type (vehicule ou compagnie)

    # Filtrage des véhicules ou des compagnies
    if type_choisi == 'vehicule':
        vehicules = Vehicule.objects.filter(user=user).order_by('-created_at')
        compagnies = []  # Pas de compagnies pour ce type
    else:
        vehicules = []  # Pas de véhicules pour ce type
        compagnies = CompagnieVehicule.objects.filter(user=user, actif=True).order_by('-created_at')

    # Récupération des filtres
    nom = request.GET.get('nom', '')
    type_bien = request.GET.get('type_bien', '')
    prix_min = request.GET.get('prix_min', '')
    prix_max = request.GET.get('prix_max', '')
    description = request.GET.get('description', '')

    # Filtrer les véhicules ou compagnies en fonction des critères
    if vehicules:
        if nom:
            vehicules = vehicules.filter(nom__icontains=nom)  # Recherche insensible à la casse
        if type_bien:
            vehicules = vehicules.filter(type_bien=type_bien)
        if prix_min:
            vehicules = vehicules.filter(prix__gte=prix_min)  # Prix supérieur ou égal à prix_min
        if prix_max:
            vehicules = vehicules.filter(prix__lte=prix_max)  # Prix inférieur ou égal à prix_max
        if description:
            vehicules = vehicules.filter(description__icontains=description)  # Filtrer par description
    
    if compagnies:
        if nom:
            compagnies = compagnies.filter(nom__icontains=nom)
        if description:
            compagnies = compagnies.filter(description__icontains=description)

    # Pagination pour les véhicules
    paginator_vehicules = Paginator(vehicules, 6)  # 6 véhicules par page
    page_vehicules = request.GET.get('page')
    try:
        vehicules = paginator_vehicules.page(page_vehicules)
    except PageNotAnInteger:
        vehicules = paginator_vehicules.page(1)
    except EmptyPage:
        vehicules = paginator_vehicules.page(paginator_vehicules.num_pages)

    # Pagination pour les compagnies
    paginator_compagnies = Paginator(compagnies, 6)  # 6 compagnies par page
    page_compagnies = request.GET.get('page_compagnies')
    try:
        compagnies = paginator_compagnies.page(page_compagnies)
    except PageNotAnInteger:
        compagnies = paginator_compagnies.page(1)
    except EmptyPage:
        compagnies = paginator_compagnies.page(paginator_compagnies.num_pages)

    # Passer les véhicules et autres données au template
    context = {
        "user": user,
        "vehicules": vehicules,
        "compagnies": compagnies,
        "type": type_choisi,
        "nom": nom,
        "type_bien": type_bien,
        "prix_min": prix_min,
        "prix_max": prix_max,
        "description": description,
        "paginator_vehicules": paginator_vehicules,
        "paginator_compagnies": paginator_compagnies,
    }

    return render(request, "core/profile.html", context)



@login_required(login_url="signin")
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = UpdateProfileForm(instance=user)
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile modifier avec success")
                return redirect("profile")
                
    context = {"form": form}
    return render(request, "core/update_profile.html", context)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .forms import 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VehiculeForm
from .models import Photo

@login_required
def add_vehicule(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST, request.FILES)
        if form.is_valid():
            vehicule = form.save(commit=False)
            vehicule.user = request.user  # Assignation de l'utilisateur connecté
            vehicule.save()  # Sauvegarde du véhicule
            # Gérer l'upload des images supplémentaires (galerie)
            images = request.FILES.getlist('image_galerie')  # Récupérer la liste des fichiers envoyés pour la galerie

            for img in images:
                Photo.objects.create(vehicule=vehicule, image=img)
            return redirect('profile')  # Redirection vers le profil après ajout du véhicule
    else:
        form = VehiculeForm()

    return render(request, 'core/add_vehicule.html', {'form': form})

from .models import Vehicule

def vehicule_detail(request, id):
    # Get the vehicle object based on its ID
    vehicule = get_object_or_404(Vehicule, id=id)

    # Pass the vehicle and its owner (user) to the template
    return render(request, 'core/vehicule_detail.html', {
        'vehicule': vehicule,
        'owner': vehicule.user  # Pass the user associated with the vehicle
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Vehicule
from .forms import ContactVehiculeForm

def contact_vehicule(request, id):  # Le paramètre 'id' fait référence au véhicule
    vehicule = get_object_or_404(Vehicule, id=id)  # Récupérer le véhicule par son id

    if request.method == 'POST':
        form = ContactVehiculeForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)  # Crée un objet contact mais ne le sauvegarde pas encore
            contact.vehicule = vehicule  # Associe le contact au véhicule
            contact.save()  # Sauvegarde le contact dans la base de données

            # Ajout d'un message de succès
            messages.success(request, "Votre demande de contact a bien été envoyée !")

            # Redirection vers la page de détail du véhicule
            return redirect('vehicule_detail', id=vehicule.id)
    else:
        form = ContactVehiculeForm()  # Crée un formulaire vide si la requête est GET

    return render(request, 'core/contact_vehicule.html', {
        'form': form,
        'vehicule': vehicule,
    })


from .forms import CompagnieVehiculeForm

@login_required  # Assurer que l'utilisateur est authentifié
def create_compagnie_vehicule(request):
    if request.method == 'POST':
        form = CompagnieVehiculeForm(request.POST, request.FILES, initial={'user': request.user})
        if form.is_valid():
            compagnie_vehicule = form.save(commit=False)
            compagnie_vehicule.user = request.user  # Associer l'utilisateur à cette compagnie
            compagnie_vehicule.save()

            messages.success(request, "Votre compagnie de véhicule a été créée avec succès !")
            return redirect('profile')  # Redirection après succès
    else:
        form = CompagnieVehiculeForm(initial={'user': request.user})

    return render(request, 'core/create_compagnie_vehicule.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CompagnieVehicule
from .forms import CompagnieVehiculeForm
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CompagnieVehicule, VehiculeCompagnie

def compagnie_detail(request, compagnie_slug):
    # Récupérer la compagnie de véhicules
    compagnie_vehicule = get_object_or_404(CompagnieVehicule, slug=compagnie_slug)
    
    # Récupérer les véhicules associés à la compagnie
    vehicules = VehiculeCompagnie.objects.filter(compagnie=compagnie_vehicule).order_by('-created_at')

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
        'compagnie_vehicule': compagnie_vehicule,
        'vehicules': vehicules,
        'paginator': paginator,
        'type_bien': type_bien,
        'nom': nom,
        'prix_min': prix_min,
        'prix_max': prix_max,
    }

    return render(request, 'core/compagnie_detail.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CompagnieVehicule, VehiculeCompagnie, PhotoCompagnie
from .forms import VehiculeCompagnieForm ,ContactVehiculeCompagnieForm
def create_vehicule_compagnie(request, compagnie_slug):
    # Récupérer la compagnie de véhicules en fonction du slug
    compagnie = get_object_or_404(CompagnieVehicule, slug=compagnie_slug)

    # Vérifier que l'utilisateur est celui qui a créé la compagnie
    if compagnie.user != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à ajouter des véhicules à cette compagnie.")
        return redirect('compagnie_detail', compagnie_slug=compagnie.slug)


    # Traitement du formulaire lorsque la requête est de type POST
    if request.method == 'POST':
        form = VehiculeCompagnieForm(request.POST, request.FILES)

        if form.is_valid():
            # Créer une instance de VehiculeCompagnie sans la sauvegarder immédiatement
            vehicule = form.save(commit=False)
            vehicule.compagnie = compagnie  # Associer la compagnie de véhicules au véhicule
            vehicule.user = request.user  # Associer l'utilisateur au véhicule
            vehicule.save()  # Enregistrer le véhicule dans la base de données

            # Gérer l'upload des images supplémentaires pour la galerie
            images = request.FILES.getlist('image_galerie')  # Récupérer la liste des fichiers envoyés pour la galerie

            for img in images:
                PhotoCompagnie.objects.create(vehicule_compagnie=vehicule, image=img)  # Créer une photo associée au véhicule

            # Message de succès
            messages.success(request, f"Le véhicule a été ajouté avec succès à la compagnie {compagnie.nom}.")
            return redirect('compagnie_detail', compagnie_slug=compagnie.slug)


    else:
        form = VehiculeCompagnieForm()

    return render(request, 'core/create_vehicule_compagnie.html', {
        'form': form,
        'compagnie_vehicule': compagnie,
    })

from django.shortcuts import render, get_object_or_404
from .models import CompagnieVehicule, VehiculeCompagnie

from django.shortcuts import render, get_object_or_404
from .models import VehiculeCompagnie

from django.shortcuts import render, get_object_or_404
from .models import VehiculeCompagnie

def vehiculecompagnie_detail(request, id):
    # Récupère le véhicule spécifique basé sur l'id
    vehicule_compagnie = get_object_or_404(VehiculeCompagnie, id=id)

    # Récupère la compagnie propriétaire du véhicule
    compagnie_vehicule = vehicule_compagnie.compagnie

    # Passe le véhicule et la compagnie au template
    return render(request, 'core/vehiculecompagnie_detail.html', {
        'vehicule_compagnie': vehicule_compagnie,  # Passe l'objet 'vehicule_compagnie' au template
        'compagnie_vehicule': compagnie_vehicule   # Passe l'objet 'compagnie_vehicule' au template
    })


def contact_vehiculecompagnie(request, id):  # Le paramètre 'id' fait référence au véhicule
    vehicule_compagnie = get_object_or_404(VehiculeCompagnie, id=id)  # Récupérer le véhicule par son id

    if request.method == 'POST':
        form = ContactVehiculeCompagnieForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)  # Crée un objet contact mais ne le sauvegarde pas encore
            contact.vehicule_compagnie = vehicule_compagnie # Associe le contact au véhicule
            contact.save()  # Sauvegarde le contact dans la base de données

            # Ajout d'un message de succès
            messages.success(request, "Votre demande de contact a bien été envoyée !")

            # Redirection vers la page de détail du véhicule
            return redirect('vehiculecompagnie_detail', id=vehicule_compagnie.id)
    else:
        form = ContactVehiculeCompagnieForm()  # Crée un formulaire vide si la requête est GET

    return render(request, 'core/contact_vehiculecompagnie.html', {
        'form': form,
        'vehicule': vehicule_compagnie,
    })

from .models import CompagnieVehicule,VehiculeCompagnie,Vehicule,CustomUser
from django.shortcuts import render, get_object_or_404
from .models import CompagnieVehicule

def CompagnieVehiculeList(request, compagnie_slug=None):
    # Récupération des filtres depuis l'URL
    pays = request.GET.get('pays', '')
    nom = request.GET.get('nom', '')

    # Filtrage des véhicules selon les paramètres reçus
    vehicules = CompagnieVehicule.objects.all()

    # Filtre par pays
    if pays:
        vehicules = vehicules.filter(pays=pays)

    # Filtre par nom (insensible à la casse)
    if nom:
        vehicules = vehicules.filter(nom__icontains=nom)

   
    # Pagination
    paginator = Paginator(vehicules, 6)  # 6 véhicules par page
    page = request.GET.get('page')
    try:
        vehicules = paginator.page(page)
    except PageNotAnInteger:
        vehicules = paginator.page(1)
    except EmptyPage:
        vehicules = paginator.page(paginator.num_pages)

    # Passage des données à la template
    return render(request, 'core/compagnievehiculelist.html', {
        'vehicules': vehicules,
        'pays': pays,
        'nom': nom,
          # Passez le slug à la template
    })
