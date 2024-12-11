from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    email= forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email adress"}))
    username= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ["email","username","password1","password2"]

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter firstname"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter lastname"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter email address"}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter address"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Enter bio"}))
    role = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter role"}))

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "address", "bio", "phone", "role", "profile_pic"]



from .models import Vehicule,Photo,ContactVehicule

# forms.py
class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ["nom", 'prix', 'devise', 'description', 'image_profile', 'image_galerie', 'contacté','type_bien', 'motif']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
        # Application de styles pour les autres champs comme vous l'avez déjà fait
        self.fields['nom'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez le nom du véhicule'
        })
        # (Ajoutez ici le code de style pour les autres champs)

        # Application du même style pour chaque champ, comme dans StoreImmobilierForm
        self.fields['prix'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez le prix'
        })
        self.fields['devise'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['motif'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Décrivez votre bien',
            'rows': 4
        })
        self.fields['image_profile'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['image_galerie'].widget.attrs.update({
            'class': 'hidden',  # Cacher l'élément de champ par défaut
        })
        self.fields['contacté'].widget.attrs.update({
            'class': 'hidden', 
        })
        self.fields['type_bien'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        # On ne touche pas le champ 'store' ici car il est caché.
    

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

# forms.py
# forms.py

class ContactVehiculeForm(forms.ModelForm):
    class Meta:
        model = ContactVehicule
        fields = ['nom', 'email', 'telephone', 'description', 'contacté']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre adresse e-mail'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre numéro de téléphone'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Décrivez votre demande'
            }),
            'contacté': forms.CheckboxInput(attrs={'class': 'hidden'}),  # Masquer ce champ
        }

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if len(telephone) < 10:
            raise forms.ValidationError("Le numéro de téléphone doit comporter au moins 10 chiffres.")
        return telephone


from django import forms
from .models import CompagnieVehicule,VehiculeCompagnie,PhotoCompagnie,ContactVehiculeCompagnie

class CompagnieVehiculeForm(forms.ModelForm):
    class Meta:
        model = CompagnieVehicule
        fields = ["nom", "thumbnail", "pays", "description"]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Entrez le nom de la compagnie'}),
            'pays': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Description de la compagnie'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


from .models import VehiculeCompagnie, PhotoCompagnie

class VehiculeCompagnieForm(forms.ModelForm):
    class Meta:
        model = VehiculeCompagnie
        fields = ['nom', 'prix', 'devise', 'description', 'image_profile', 'image_galerie', 'contacté', 'type_bien', 'motif', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Application du même style pour chaque champ
        self.fields['nom'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez le nom du véhicule'
        })
        self.fields['prix'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez le prix'
        })
        self.fields['devise'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['motif'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Décrivez votre véhicule',
            'rows': 4
        })
        self.fields['image_profile'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['image_galerie'].widget.attrs.update({
            'class': 'hidden',  # Cacher l'élément de champ par défaut
        })
        self.fields['contacté'].widget.attrs.update({
            'class': 'hidden', 
        })
        self.fields['type_bien'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        


class PhotoCompagnieForm(forms.ModelForm):
    class Meta:
        model = PhotoCompagnie
        fields = ['image']

class ContactVehiculeCompagnieForm(forms.ModelForm):
    class Meta:
        model = ContactVehiculeCompagnie
        fields = ['nom', 'email', 'telephone', 'description', 'contacté']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre adresse e-mail'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre numéro de téléphone'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Décrivez votre demande'
            }),
            'contacté': forms.CheckboxInput(attrs={'class': 'hidden'}),  # Masquer ce champ
        }

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if len(telephone) < 10:
            raise forms.ValidationError("Le numéro de téléphone doit comporter au moins 10 chiffres.")
        return telephone