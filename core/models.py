from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify # type: ignore

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    
    def __str__(self):
        return self.email

# Choix pour les communes


TYPE_VEHICULE_CHOICES = [
    ('voiture', 'Voiture'),
    ('moto', 'Moto'),
    ('camion', 'Camion'),
    ('bus', 'Bus'),
    ('utilitaire', 'Véhicule utilitaire'),
    ('autres', 'Autres'),
]
class Vehicule(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    devise = models.CharField(max_length=3, choices=[('USD', 'USD'), ('CDF', 'CDF')], default='CDF', verbose_name="Devise")
    motif = models.CharField(max_length=8, choices=[('LOCATION', 'LOCATION'), ('VENTE', 'VENTE')], default='LOCATION', verbose_name="Motif")
    description = models.TextField(verbose_name="Description détaillée")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    image_profile = models.ImageField(upload_to='vehicule/images/', null=True, blank=True, verbose_name="Image principale")
    image_galerie = models.ImageField(upload_to='vehicule/galerie/', null=True, blank=True, verbose_name="Image galerie")
    contacté = models.BooleanField(default=False, verbose_name="Contacté")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="vehicules")
    type_bien = models.CharField(max_length=50, choices=TYPE_VEHICULE_CHOICES, default='voiture', verbose_name="Type de bien")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    def save(self, *args, **kwargs):
        # Plus besoin de générer le 'slug'
        super(Vehicule, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom



class Photo(models.Model):
    vehicule = models.ForeignKey(Vehicule, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicule/galerie/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.vehicule.type_bien} - {self.image.name}"


class ContactVehicule(models.Model):
    # Lien vers l'immobilier concerné
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name='contacts', verbose_name="Bien immobilier")

    # Informations sur la personne qui contacte
    nom = models.CharField(max_length=255, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    description = models.TextField(verbose_name="Message ou description", blank=True, null=True)

    # Statut de la demande (si elle a été contactée ou pas)
    contacté = models.BooleanField(default=False, verbose_name="Contacté")

    # Date de la demande
    date_contact = models.DateTimeField(auto_now_add=True, verbose_name="Date de la demande")

    def __str__(self):
        return f"Contact de {self.nom} pour {self.immobilier.type_bien} à {self.immobilier.commune}"

    class Meta:
        verbose_name = "Demande de Contact"
        verbose_name_plural = "Demandes de Contact"
        ordering = ['-date_contact']

from django.db import models
from django.utils.text import slugify
from django.conf import settings

# Définir les choix pour les pays
PAYS_CHOICES = [
    ('kinshasa', 'Kinshasa'),
    ('chine', 'Chine'),
    ('japon', 'Japon'),
    ('korea', 'Corée'),
    ('usa', 'États-Unis'),
    ('france', 'France'),
    ('allemagne', 'Allemagne'),
    ('italie', 'Italie'),
    ('autres', 'Autres'),
]

# Modèle CompagnieVehicule
from django.utils.text import slugify

class CompagnieVehicule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="compagnies_vehicule")
    nom = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="img/compagnie_vehicule", null=True, blank=True, verbose_name="Image de la Compagnie")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    pays = models.CharField(max_length=100, choices=PAYS_CHOICES, default='kinshasa', verbose_name="Pays")
    description = models.TextField(null=True, blank=True, verbose_name="Description de la Compagnie")
    actif = models.BooleanField(default=False, verbose_name="Actif")

    def save(self, *args, **kwargs):
        if not self.slug and self.nom:  # Si le slug est vide et que le nom existe
            self.slug = slugify(self.nom)
        super(CompagnieVehicule, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom

    

class VehiculeCompagnie(models.Model):
    compagnie = models.ForeignKey(CompagnieVehicule, on_delete=models.CASCADE, related_name='vehicules', verbose_name="Compagnie")
    nom = models.CharField(max_length=50, unique=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    devise = models.CharField(max_length=3, choices=[('USD', 'USD'), ('CDF', 'CDF')], default='CDF', verbose_name="Devise")
    motif = models.CharField(max_length=8, choices=[('LOCATION', 'LOCATION'), ('VENTE', 'VENTE')], default='LOCATION', verbose_name="Motif")
    description = models.TextField(verbose_name="Description détaillée")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    image_profile = models.ImageField(upload_to='vehicule_compagnie/images/', null=True, blank=True, verbose_name="Image principale")
    image_galerie = models.ImageField(upload_to='vehicule_compagnie/galerie/', null=True, blank=True, verbose_name="Image galerie")
    contacté = models.BooleanField(default=False, verbose_name="Contacté")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="vehicule_compagnies")
    type_bien = models.CharField(max_length=50, choices=TYPE_VEHICULE_CHOICES, default='voiture', verbose_name="Type de bien")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    def save(self, *args, **kwargs):
        # Plus besoin de générer le 'slug'
        super(VehiculeCompagnie, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom

class PhotoCompagnie(models.Model):
    vehicule_compagnie = models.ForeignKey(VehiculeCompagnie, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicule_compagnie/galerie/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo pour {self.vehicule_compagnie.nom} - {self.image.name}"

class ContactVehiculeCompagnie(models.Model):
    vehicule_compagnie = models.ForeignKey(VehiculeCompagnie, on_delete=models.CASCADE, related_name='contacts', verbose_name="Compagnie de véhicules")
    nom = models.CharField(max_length=255, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    description = models.TextField(verbose_name="Message ou description", blank=True, null=True)
    contacté = models.BooleanField(default=False, verbose_name="Contacté")
    date_contact = models.DateTimeField(auto_now_add=True, verbose_name="Date de la demande")

    def __str__(self):
        return f"Contact de {self.nom} pour {self.vehicule_compagnie.nom} dans {self.vehicule_compagnie.pays}"

    class Meta:
        verbose_name = "Demande de Contact"
        verbose_name_plural = "Demandes de Contact"
        ordering = ['-date_contact']
