from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'profile_pic', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "profile_pic"),
            },
        ),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from .models import Vehicule, ContactVehicule
from django.utils.html import format_html

# Inline pour afficher les contacts associés à un bien immobilier
class ContactVehiculeInline(admin.TabularInline):
    model = ContactVehicule
    extra = 1
    fields = ('nom', 'email', 'telephone', 'description', 'contacté', 'date_contact')
    readonly_fields = ('date_contact',)

# Admin pour le modèle ContactImmobilier
class ContactVehiculeAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans l'admin pour ContactImmobilier
    list_display = ('nom', 'email', 'telephone', 'vehicule', 'contacté', 'date_contact')
    
    # Filtres dans l'interface d'administration
    list_filter = ('contacté', 'date_contact')

    # Ajout de la recherche sur certains champs
    search_fields = ['nom', 'email', 'telephone', 'vehicule__type_bien', 'vehicule__commune']

    # Rendre le lien vers l'immobilier cliquable
    def vehicule_link(self, obj):
        return format_html('<a href="{}">{}</a>', admin.site.urls + 'vehicule/' + str(obj.vehicule.id), obj.vehicule)
    vehicule_link.short_description = 'Bien vehicule'



# Enregistrement du modèle ContactImmobilier avec son admin personnalisé
admin.site.register(ContactVehicule, ContactVehiculeAdmin)

# Admin pour le modèle Immobilier
from .models import Vehicule,Photo
class PhotoInline(admin.TabularInline):  # Tu peux aussi utiliser StackInline si tu préfères
    model = Photo
    extra = 1  # Affiche un champ vide de formulaire supplémentaire pour ajouter une photo
    fields = ('image',) 

def marquer_comme_actif(modeladmin, request, queryset):
    queryset.update(actif=True)

marquer_comme_actif.short_description = "Marquer comme actif"

class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('type_bien', 'prix', 'devise', 'contacté', 'user', 'motif', 'actif', 'created_at', 'image_profile_tag')
    list_filter = ('type_bien',  'contacté', 'devise', 'motif', 'actif')
    search_fields = ['type_bien',  'prix', 'user__username', 'motif']
    inlines = [ContactVehiculeInline, PhotoInline]
    actions = [marquer_comme_actif]
    # Le champ 'slug' doit être en lecture seule
     # Champs en lecture seule
    
    # Champs pré-remplis
   

    def image_profile_tag(self, obj):
        if obj.image_profile:
            return format_html('<img src="{}" width="50" height="50" />', obj.image_profile.url)
        return "Pas d'image"
    
    image_profile_tag.short_description = 'Image Profil'

# Enregistrement du modèle Vehicule avec son admin personnalisé
admin.site.register(Vehicule, VehiculeAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'image', 'uploaded_at')
    search_fields = ('vehicule',)
    list_filter = ('vehicule',)

# Enregistrer les modèles dans l'admin
admin.site.register(Photo, PhotoAdmin)



from .models import CompagnieVehicule,VehiculeCompagnie,PhotoCompagnie,ContactVehiculeCompagnie

class CompagnieVehiculeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nom",)}
    # list_display = ['nom', 'pays', 'actif', 'created_at', 'updated_at']  # Affichez la colonne "actif" dans la liste
    # list_filter = ['actif', 'pays']  # Permet de filtrer par "actif" et "pays"
    # search_fields = ['nom', 'description']  # Permet de rechercher par nom ou description

admin.site.register(CompagnieVehicule, CompagnieVehiculeAdmin)

class PhotoCompagnieInline(admin.TabularInline):
    model = PhotoCompagnie
    extra = 1  # Affiche un champ vide de formulaire supplémentaire pour ajouter une photo

class ContactVehiculeCompagnieInline(admin.TabularInline):
    model = ContactVehiculeCompagnie
    extra = 1

class VehiculeCompagnieAdmin(admin.ModelAdmin):
    list_filter = ('compagnie', 'type_bien', 'contacté', 'devise', 'motif', 'actif')
    search_fields = ['nom',  'type_bien', 'user__username', 'motif']
    inlines = [ContactVehiculeCompagnieInline, PhotoCompagnieInline]
    list_display = ('compagnie_vehicule', 'nom', 'type_bien', 'prix', 'devise', 'contacté', 'user', 'motif', 'actif', 'created_at')

    def compagnie_vehicule(self, obj):
        return f'{obj.compagnie.nom} - {obj.nom}'  # ou ce que vous voulez afficher
    compagnie_vehicule.admin_order_field = 'compagnie__nom'  
admin.site.register(VehiculeCompagnie, VehiculeCompagnieAdmin)
admin.site.register(PhotoCompagnie)
admin.site.register(ContactVehiculeCompagnie)
