# myapp/forms.py

# from datetime import timezone
from io import BytesIO
import os
from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django import forms
from django.conf import settings
from django.db.models import Q  # ✅ Importer Q correctement
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import qrcode
from .models import Chambre, CustomUser, Location, Maison, PaiementLoyer, Proprietaire, Quartier, TypeChambre, UserType, Ville,FinLocation,Message
# from django import forms

from django.core.mail import send_mail

from django.contrib.auth import get_user_model

from django.core.mail import EmailMessage
from dateutil.relativedelta import relativedelta # type: ignore

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# from authentifications.authentication import models
User = get_user_model()  # Assurez-vous de récupérer CustomUser  # noqa: F811





from django.utils import timezone # Use django's timezone  # noqa: E402

############################################################################ La forme pour la Utilisateur  ##########################################################################################

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé pour `CustomUser`
    """

    email = forms.EmailField(
        required=True, 
        help_text="* Saisissez une adresse e-mail valide.",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre email'
        })
    )
    
    telephone_personne_prevenir = forms.CharField(
        max_length=15, 
        required=False,
        label="Téléphone d'urgence",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez un numéro de contact en cas d’urgence'
        })
    )
    
    nom_personne_prevenir = forms.CharField(
        max_length=100, 
        required=False, 
        label="Nom de la personne à prévenir",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom de la personne à prévenir'
        })
    )
    
    prenom_personne_prevenir = forms.CharField(
        max_length=100, 
        required=False, 
        label="Prénom de la personne à prévenir",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom de la personne à prévenir'
        })
    )
    
    image = forms.ImageField(
        required=False, 
        label="Photo de profil"
    )

    type_utilisateur = forms.ModelChoiceField(
        queryset=UserType.objects.all(),
        required=False, 
        help_text="Sélectionnez le type d'utilisateur.",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'nom', 'prenom', 'email', 'tel', 'type_utilisateur', 'image', 'gender', 'telephone_personne_prevenir', 'nom_personne_prevenir', 'prenom_personne_prevenir')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre numéro de téléphone'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        """
        Sauvegarde l'utilisateur et lui envoie un e-mail après son inscription
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.tel = self.cleaned_data.get('tel')
        if commit:
            user.save()
            self.send_welcome_email(user)
        return user

    def send_welcome_email(self, user):
        """
        Envoie un e-mail de bienvenue après la création du compte
        """
        subject = "Bienvenue sur notre plateforme 🎉"
        message = f"""
        Salut {user.prenom},
        Félicitations ! Votre compte a été créé avec succès. 
        Vous pouvez maintenant vous connecter et profiter de nos services.
        Merci de nous avoir rejoint ! 🚀
        -- L'équipe Support
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)


        
class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé avec Bootstrap
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Appliquer des classes Bootstrap aux champs du formulaire
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label






class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'message']

    def __init__(self, *args, **kwargs):
        """
        Limite les destinataires disponibles en fonction des permissions de l'utilisateur connecté.
        """
        self.sender = kwargs.pop('sender', None)
        super().__init__(*args, **kwargs)

        if self.sender:
            if self.sender.type_utilisateur.nom == "locataire":
                # Un locataire ne peut envoyer un message qu'à un admin
                self.fields['receiver'].queryset = CustomUser.objects.filter(type_utilisateur__nom="admin")
            elif self.sender.type_utilisateur.nom == "admin":
                # Un admin peut envoyer un message à tous les utilisateurs sauf lui-même
                self.fields['receiver'].queryset = CustomUser.objects.exclude(id=self.sender.id)
            else:
                # Si le type_utilisateur n'est pas reconnu, on peut filtrer selon d'autres critères ou lever une exception
                self.fields['receiver'].queryset = CustomUser.objects.none()
        else:
            # Si sender est None, on peut lever une erreur ou laisser la queryset vide
            self.fields['receiver'].queryset = CustomUser.objects.none()

   



class GroupMessageForm(forms.Form):
    maison = forms.ModelChoiceField(
        queryset=Maison.objects.all(),
        label="Sélectionner une maison"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Écrivez votre message ici...'}),
        label="Message"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Récupérer l'utilisateur passé en argument
        super().__init__(*args, **kwargs)
        if user:
            # Filtrer les maisons selon l'utilisateur
            self.fields['maison'].queryset = Maison.objects.filter(
                Q(proprietaire=user) | 
                Q(locataires=user)
            ).distinct()

                   
##################################################################################### La forme pour la Ville  ##########################################################################################

# class ProprietaireForm(forms.ModelForm):
#     class Meta:
#         model = Proprietaire  # noqa: F821
#         fields = ['nom', 'prenom', 'gender', 'email', 'image', 'telephone', 'adresse']
#         widgets = {
#             'nom': forms.TextInput(attrs={'class': 'form-control'}),
#             'prenom': forms.TextInput(attrs={'class': 'form-control'}),
#             'gender': forms.Select(attrs={'class': 'form-select'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
#             'telephone': forms.TextInput(attrs={'class': 'form-control'}),
#             'adresse': forms.TextInput(attrs={'class': 'form-control'}),
#         }


User = get_user_model()

class ProprietaireForm(forms.ModelForm):
    class Meta:
        model = Proprietaire
        fields = ['utilisateur']
        , 'nom', 'prenom', 'gender', 'email', 'image', 'telephone', 'adresse'
        widgets = {
            'utilisateur': forms.Select(attrs={'class': 'form-select'}),
            # 'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            # 'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            # 'gender': forms.Select(attrs={'class': 'form-select'}),
            # 'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse e-mail'}),
            # 'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            # 'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            # 'adresse': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ProprietaireForm, self).__init__(*args, **kwargs)
        self.fields['utilisateur'].queryset = User.objects.filter(type_utilisateur__nom='propriétaire')

#formulaire de recherche
class VilleSearchForm(forms.Form):
    recherche = forms.CharField(label='Rechercher une ville', max_length=100, required=False)
                
class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville  # noqa: F821
        fields = ['nom', 'description', 'image']
        widgets = {
                            'nom': forms.TextInput(attrs={
                                'class': 'form-control', 
                                'placeholder': 'Nom de la ville'
                            }),
                            'description': forms.Textarea(attrs={
                                'class': 'form-control', 
                                'rows': 5,
                                'placeholder': 'Description'
                            }),
                            'image': forms.ClearableFileInput(attrs={
                                'class': 'form-control-file'
                            }),
                        }
##################################################################################### La forme pour la Quartier ##########################################################################################
class QuartierForm(forms.ModelForm):
    class Meta:
        model = Quartier  # noqa: F821
        fields = ['nom', 'description', 'image', 'ville']
        widgets = {
                            'nom': forms.TextInput(attrs={
                                'class': 'form-control', 
                                'placeholder': 'Nom '
                            }),
                            'description': forms.Textarea(attrs={
                                'class': 'form-control', 
                                'rows': 5,
                                'placeholder': 'Description'
                            }),
                            'image': forms.ClearableFileInput(attrs={
                                'class': 'form-control-file'
                            }),
                            'ville': forms.Select(attrs={
                                'class': 'form-select',
                                'placeholder': 'Sélectionnez une ville'
                            }), 
                        }
##################################################################################### La forme pour la maison  ##########################################################################################

class MaisonForm(forms.ModelForm):
    class Meta:
        model = Maison
        fields = ['nom', 'adresse', 'code_postal', 'image', 'quartier', 'proprietaire','nombre_piece']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la maison'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code Postal'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'quartier': forms.Select(attrs={'class': 'form-control'}),
            'proprietaire': forms.Select(attrs={'class': 'form-control'}),
            'nombre_piece': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de piece '}),
        }

class TypeChambreForm(forms.ModelForm):
    class Meta:
        model = TypeChambre
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du type de chambre'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du type de chambre'
            }),
        }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     maison = cleaned_data.get('maison')

    #     if maison and maison.nombre_piece <= 0:
    #         raise forms.ValidationError(f"La maison '{maison.nom}' n'a plus de pièces disponibles.")
        
    #     return cleaned_data

class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        exclude = ['etat']  # Exclure le champ 'etat'
        """
    Formulaire pour la gestion des chambres avec une liste déroulante pour le taux de commission.
    """
    TAUX_COMMISSION_CHOICES = [
        (0, "0%"), 
        (1, "1%"), 
        (2, "2%"),
        (3, "3%"),
        (4, "4%"),
        (5, "5%"),
        (6, "6%"),
        (7, "7%"),
        (8, "8%"),
        (9, "9%"),
        (10, "10%"),
        (11, "11%"),
        (12, "12%"),
        (13, "13%"),
        (14, "14%"),
        (15, "15%"),
        (16, "16%"),
        (17, "17%"),
        (18, "18%"),
        (19, "19%"),
        (20, "20%"),
        (21, "21%"),
        (22, "22%"),
        (23, "23%"),
        (24, "24%"),
        (25, "25%"),
        (26, "26%"),
        (27, "27%"),
        (28, "28%"),
        (29, "29%"),
        (30.0, "30%"),
    ]

    taux_commission = forms.ChoiceField(
        choices=TAUX_COMMISSION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Sélectionnez le taux de commission'
        }),
        label="Taux de commission (%)"
    )
    fields = ['type_chambre', 'surface', 'prix', 'etat', 'description', 'maison', 'taux_commission']
    widgets = {
            'type_chambre': forms.Select(attrs={'class': 'form-control'}),
            'surface': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'etat': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'maison': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        maison = cleaned_data.get('maison')

        if maison and maison.nombre_piece <= maison.chambres.count():
            raise forms.ValidationError(f"La maison '{maison.nom}' n'a plus de pièces disponibles.")
        
        return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Désactive le champ maison pour empêcher sa modification
        self.fields['maison'].disabled = True
# class LocationForm(forms.ModelForm):
#     class Meta:
#         model = Location
#         exclude = ['utilisateur', 'chambre']  # Exclure les champs utilisateur et chambre
#         widgets = {
#             'date_debut_location': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'taux_commission': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'montant_avance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'date_fin_avance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'montant_caution': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'nombre_mois_paye': forms.NumberInput(attrs={'class': 'form-control'}),
#             'commission': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
#             'montant_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'description_prelevement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'montant_remboursement': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'date_fin_location': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'montant_prelever': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'statut_paiement': forms.Select(attrs={'class': 'form-control'}),
#             'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
#             'date_paiement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#         }

#     def save(self, commit=True):
#         instance = super().save(commit=False)

#         # Passer automatiquement la chambre en "occupée" si elle est libre
#         if instance.chambre and instance.chambre.etat == "libre":
#             instance.chambre.etat = "occupée"
#             instance.chambre.save()

#         # Si le statut est "payé" et qu'aucune date de paiement n'est fixée, définir la date de paiement à aujourd'hui
#         if instance.statut_paiement == "payé" and not instance.date_paiement:
#             instance.date_paiement = date.today()

#         # Calcul automatique de la commission
#         if instance.montant_avance:
#             instance.commission = instance.montant_avance * instance.taux_commission / 100
#         else:
#             instance.commission = 0

#         # Désactiver le compte de l'utilisateur si certains champs sont renseignés
#         if instance.utilisateur:
#             if (
#                 instance.description_prelevement and instance.description_prelevement != "Aucune description" or
#                 instance.montant_remboursement > 0 or
#                 instance.montant_prelever > 0
#             ):
#                 instance.utilisateur.is_active = False
#                 instance.utilisateur.save()

#         if commit:
#             instance.save()
#         return instance


# class LocationForm(forms.ModelForm):
#     """
#     Formulaire pour la gestion des locations.
#     """
#     class Meta:
#         model = Location
#         exclude = ['utilisateur', 'chambre']  # Exclure les champs utilisateur et chambre

#         fields = [
#             'utilisateur', 'chambre', 'date_debut_location', 'montant_avance', 
#             'date_fin_avance', 'montant_caution', 'nombre_mois_paye', 'commission', 
#             'montant_total', 'image_contrat', 'statut_paiement', 'mode_paiement', 
#             'date_paiement'
#         ]
#         widgets = {
#             'utilisateur': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Sélectionnez un utilisateur'
#             }),
#             'chambre': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Sélectionnez une chambre'
#             }),
#             'date_debut_location': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control',
#                 'placeholder': 'Date de début de location'
#             }),
#             'montant_avance': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'readonly': 'readonly',
#                 'placeholder': 'Montant de l\'avance',
#                 'step': '0.01'
#             }),
#             'date_fin_avance': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control',
#                 'readonly': 'readonly',
#                 'placeholder': 'Date de fin de l\'avance'
#             }),
#             'montant_caution': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Montant de la caution',
#                 'step': '0.01'
#             }),
#             'nombre_mois_paye': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Nombre de mois payés'
#             }),
#             'commission': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'readonly': 'readonly',
#                 'placeholder': 'Commission calculée automatiquement'
#             }),
#             'montant_total': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'readonly': 'readonly',
#                 'placeholder': 'Montant total',
#                 'step': '0.01'
#             }),
#             'image_contrat': forms.ClearableFileInput(attrs={
#                 'class': 'form-control-file',
#                 'placeholder': 'Téléchargez l\'image du contrat'
#             }),
#             'statut_paiement': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Statut du paiement'
#             }),
#             'mode_paiement': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Mode de paiement'
#             }),
#             'date_paiement': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control',
#                 'placeholder': 'Date de paiement'
#             }),
#         }

#     def clean(self):
#         """
#         Validation personnalisée pour vérifier les champs liés à la location.
#         """
#         cleaned_data = super().clean()
#         montant_avance = cleaned_data.get('montant_avance')
#         montant_caution = cleaned_data.get('montant_caution')

#         if montant_avance and montant_avance < 0:
#             raise forms.ValidationError("Le montant de l'avance ne peut pas être négatif.")

#         if montant_caution and montant_caution < 0:
#             raise forms.ValidationError("Le montant de la caution ne peut pas être négatif.")

#         return cleaned_data

#     def __init__(self, *args, **kwargs):
#         """
#         Initialisation personnalisée pour désactiver certains champs si nécessaire.
#         """
#         super().__init__(*args, **kwargs)
#         # Désactiver certains champs si nécessaire
#         self.fields['commission'].disabled = True





# class LocationForm(forms.ModelForm):
#     """
#     Formulaire pour la gestion des locations.
#     """
#     class Meta:
#         model = Location
#         exclude = ['utilisateur', 'chambre']  # Exclure les champs utilisateur et chambre

#         fields = [
#             'utilisateur', 'chambre', 'date_debut_location', 'montant_avance', 
#             'date_fin_avance', 'montant_caution', 'nombre_mois_paye', 'commission', 
#             'montant_total', 'image_contrat', 'statut_paiement', 'mode_paiement', 
#             'date_paiement'
#         ]
#         widgets = {
#             'utilisateur': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Sélectionnez un utilisateur'
#             }),
#             'chambre': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Sélectionnez une chambre'
#             }),
#             'date_debut_location': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control',
#                 'placeholder': 'Date de début de location'
#             }),
#             'montant_avance': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'readonly': 'readonly',
#                 'placeholder': 'Montant de l\'avance',
#                 'step': '0.01'
#             }),
#             'date_fin_avance': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control',
#                 'readonly': 'readonly',
#                 'placeholder': 'Date de fin de l\'avance'
#             }),
#             'montant_caution': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Montant de la caution',
#                 'step': '0.01'
#             }),
#             'nombre_mois_paye': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Nombre de mois payés'
#             }),
#             'commission': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'readonly': 'readonly',
#                 'placeholder': 'Commission calculée automatiquement'
#             }),
#             'montant_total': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'readonly': 'readonly',
#                 'placeholder': 'Montant total',
#                 'step': '0.01'
#             }),
#             'image_contrat': forms.ClearableFileInput(attrs={
#                 'class': 'form-control-file',
#                 'placeholder': 'Téléchargez l\'image du contrat'
#             }),
#             'statut_paiement': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Statut du paiement'
#             }),
#             'mode_paiement': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Mode de paiement'
#             }),
#             'date_paiement': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control',
#                 'placeholder': 'Date de paiement'
#             }),
#         }

#     def clean(self):
#         """
#         Validation personnalisée pour vérifier les champs liés à la location.
#         """
#         cleaned_data = super().clean()
#         montant_avance = cleaned_data.get('montant_avance')
#         montant_caution = cleaned_data.get('montant_caution')

#         if montant_avance and montant_avance < 0:
#             raise forms.ValidationError("Le montant de l'avance ne peut pas être négatif.")

#         if montant_caution and montant_caution < 0:
#             raise forms.ValidationError("Le montant de la caution ne peut pas être négatif.")

#         return cleaned_data

#     def save(self, commit=True):
#         """
#         Surcharge de la méthode save pour envoyer un email après la sauvegarde.
#         """
#         instance = super().save(commit=False)

#         # Envoyer un email après la sauvegarde
#         utilisateur = instance.utilisateur
#         chambre = instance.chambre

#         sujet = "Confirmation de votre location"
#         message = f"""
#         Bonjour {utilisateur.nom} {utilisateur.prenom},

#         Votre location pour la chambre "{chambre.type_chambre.nom}" a été créée avec succès.
#         Voici les détails de votre location :
#         - Chambre : {chambre.type_chambre.nom}
#         - Prix : {chambre.prix} CFA
#         - Surface : {chambre.surface} m²
#         - Taux de commission : {chambre.taux_commission}%
#         - Date de début : {instance.date_debut_location}
#         - Date de fin : {instance.date_fin_avance}
#         - Montant d'avance : {instance.montant_avance} CFA
#         - Montant de caution : {instance.montant_caution} CFA
#         - Commission : {instance.commission} CFA
#         - Montant total : {instance.montant_total} CFA
#         - Statut de paiement : {instance.statut_paiement}
#         - Mode de paiement : {instance.mode_paiement}
#         - Date de paiement : {instance.date_paiement}
#         Merci de nous faire confiance.
#         Cordialement,
#         L'équipe de gestion des locations
#         """

#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [utilisateur.email]

#         # Créer un email avec pièce jointe
#         email = EmailMessage(sujet, message, email_from, recipient_list)

#         # Vérifier si l'image du contrat existe avant de l'attacher
#         if instance.image_contrat and os.path.exists(instance.image_contrat.path):
#             email.attach_file(instance.image_contrat.path)
#         else:
#             print("Aucune image de contrat disponible ou le fichier est introuvable.")

#         # Envoyer l'email
#         email.send()

#         # Sauvegarder l'instance si nécessaire
#         if commit:
#             instance.save()

#         return instance

#     def __init__(self, *args, **kwargs):
#         """
#         Initialisation personnalisée pour désactiver certains champs si nécessaire.
#         """
#         super().__init__(*args, **kwargs)
#         # Désactiver certains champs si nécessaire
#         self.fields['commission'].disabled = True




# class LocationForm(forms.ModelForm):
#     """
#     Formulaire pour la gestion des locations.
#     """
#     class Meta:
#         model = Location
#         exclude = ['utilisateur', 'chambre']
#         fields = [
#             'utilisateur', 'chambre', 'date_debut_location', 'montant_avance',
#             'date_fin_avance', 'montant_caution', 'nombre_mois_paye', 'commission',
#             'montant_total', 'image_contrat', 'statut_paiement', 'mode_paiement',
#             'date_paiement'
#         ]
#         widgets = {
#             'date_debut_location': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'montant_avance': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
#             'date_fin_avance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
#             'montant_caution': forms.NumberInput(attrs={'class': 'form-control'}),
#             'nombre_mois_paye': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'min': '1',
#                 'value': '1',
#                 'required': True,
#                 'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57)',
#                 'oninput': 'this.value = Math.abs(this.value) || 1'
#             }),
#             'commission': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
#             'montant_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
#             'image_contrat': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
#             'statut_paiement': forms.Select(attrs={'class': 'form-control','readonly': 'readonly'}),
#             'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
#             'date_paiement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#         }
#     def clean_nombre_mois_paye(self):
#         nombre_mois = self.cleaned_data.get('nombre_mois_paye')
#         if nombre_mois is None or nombre_mois < 1:
#             raise forms.ValidationError("Le nombre de mois doit être supérieur ou égal à 1.")
#         return nombre_mois
#     def clean(self):
#         """
#         Validation personnalisée pour vérifier les champs liés à la location.
#         """
#         cleaned_data = super().clean()
#         montant_avance = cleaned_data.get('montant_avance')
#         montant_caution = cleaned_data.get('montant_caution')

#         if montant_avance is not None and montant_avance < 0:
#             self.add_error('montant_avance', "Le montant de l'avance ne peut pas être négatif.")

#         if montant_caution is not None and montant_caution < 0:
#             self.add_error('montant_caution', "Le montant de la caution ne peut pas être négatif.")

#         return cleaned_data

#     def save(self, commit=True):
#         """
#         Surcharge de la méthode save pour envoyer un email après la sauvegarde.
#         """
#         instance = super().save(commit=False)
        
#         # Envoyer un email après la sauvegarde
#         utilisateur = instance.utilisateur
#         chambre = instance.chambre

#         sujet = "Confirmation de votre location"
#         message = f"""
#         Bonjour {utilisateur.nom} {utilisateur.prenom},

#         Votre location pour la chambre \"{chambre.type_chambre.nom}\" a été créée avec succès.
#         Voici les détails de votre location :
#         - Chambre : {chambre.type_chambre.nom}
#         - Prix : {chambre.prix} CFA
#         - Surface : {chambre.surface} m²
#         - Taux de commission : {chambre.taux_commission}%
#         - Date de début : {instance.date_debut_location}
#         - Date de fin : {instance.date_fin_avance}
#         - Montant d'avance : {instance.montant_avance} CFA
#         - Montant de caution : {instance.montant_caution} CFA
#         - Commission : {instance.commission} CFA
#         - Montant total : {instance.montant_total} CFA
#         - Statut de paiement : {instance.statut_paiement}
#         - Mode de paiement : {instance.mode_paiement}
#         - Date de paiement : {instance.date_paiement}
#         Merci de nous faire confiance.
#         Cordialement,
#         L'équipe de gestion des locations
#         """
        
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [utilisateur.email]
#         email = EmailMessage(sujet, message, email_from, recipient_list)
        
#         # Ajouter l'image du contrat en pièce jointe si elle existe
#         if instance.image_contrat and instance.image_contrat.path:
#             try:
#                 email.attach_file(instance.image_contrat.path)
#             except Exception as e:
#                 print(f"Erreur lors de l'attachement du fichier : {e}")
        
#         email.send()
        
#         # Sauvegarder l'instance
#         if commit:
#             instance.save()
#         return instance

#     def __init__(self, *args, **kwargs):
#         """
#         Initialisation personnalisée pour désactiver certains champs si nécessaire.
#         """
#         super().__init__(*args, **kwargs)
#         self.fields['commission'].disabled = True

class LocationForm(forms.ModelForm):
    """
    Formulaire pour la gestion des locations.
    """

    class Meta:
        model = Location
        exclude = ['utilisateur', 'chambre']
        fields = [
            'utilisateur', 'chambre', 'date_debut_location', 'montant_avance',
            'date_fin_avance', 'montant_caution', 'nombre_mois_paye', 'commission',
            'montant_total', 'image_contrat', 'statut_paiement', 'mode_paiement',
            'date_paiement'
        ]
        widgets = {
            'date_debut_location': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'montant_avance': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'date_fin_avance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'montant_caution': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_mois_paye': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1',
                'required': True,
                'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57)',
                'oninput': 'this.value = Math.abs(this.value) || 1'
            }),
            'commission': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'montant_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'image_contrat': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'statut_paiement': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
            'date_paiement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_nombre_mois_paye(self):
        """
        Validation du champ `nombre_mois_paye`.
        """
        nombre_mois = self.cleaned_data.get('nombre_mois_paye')
        if nombre_mois is None or nombre_mois < 1:
            raise forms.ValidationError("Le nombre de mois doit être supérieur ou égal à 1.")
        return nombre_mois

    def clean(self):
        """
        Validation personnalisée pour vérifier les champs liés à la location.
        """
        cleaned_data = super().clean()
        montant_avance = cleaned_data.get('montant_avance')
        montant_caution = cleaned_data.get('montant_caution')

        if montant_avance is not None and montant_avance < 0:
            self.add_error('montant_avance', "Le montant de l'avance ne peut pas être négatif.")

        if montant_caution is not None and montant_caution < 0:
            self.add_error('montant_caution', "Le montant de la caution ne peut pas être négatif.")

        return cleaned_data

    def save(self, commit=True):
        """
        Surcharge de la méthode save pour envoyer un email après la sauvegarde.
        """
        instance = super().save(commit=False)

        # Vérifier si l'utilisateur et la chambre sont définis
        utilisateur = getattr(instance, 'utilisateur', None)
        chambre = getattr(instance, 'chambre', None)

        if utilisateur and chambre:
            # Préparer l'email
            sujet = "Confirmation de votre location"
            message = f"""
            Bonjour {utilisateur.nom} {utilisateur.prenom},

            Votre location pour la chambre \"{chambre.type_chambre.nom}\" a été créée avec succès.
            Voici les détails de votre location :
            - Chambre : {chambre.type_chambre.nom}
            - Prix : {chambre.prix} CFA
            - Surface : {chambre.surface} m²
            - Taux de commission : {chambre.taux_commission}%
            - Date de début : {instance.date_debut_location}
            - Date de fin : {instance.date_fin_avance}
            - Montant d'avance : {instance.montant_avance} CFA
            - Montant de caution : {instance.montant_caution} CFA
            - Commission : {instance.commission} CFA
            - Montant total : {instance.montant_total} CFA
            - Statut de paiement : {instance.statut_paiement}
            - Mode de paiement : {instance.mode_paiement}
            - Date de paiement : {instance.date_paiement}
            Merci de nous faire confiance.
            Cordialement,
            L'équipe de gestion des locations
            """

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [utilisateur.email]
            email = EmailMessage(sujet, message, email_from, recipient_list)

            # Ajouter l'image du contrat en pièce jointe si elle existe
            if instance.image_contrat and hasattr(instance.image_contrat, 'path'):
                try:
                    email.attach_file(instance.image_contrat.path)
                except Exception as e:
                    print(f"Erreur lors de l'attachement du fichier : {e}")

            # Envoyer l'email
            try:
                email.send()
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'email : {e}")

        # Sauvegarder l'instance
        if commit:
            instance.save()

        return instance

    def __init__(self, *args, **kwargs):
        """
        Initialisation personnalisée pour désactiver certains champs si nécessaire.
        """
        super().__init__(*args, **kwargs)
        self.fields['commission'].disabled = True

##################################################################################### La forme pour la PaiementLoyer  ##########################################################################################

class PaiementLoyerForm(forms.ModelForm):
    """
    Formulaire amélioré pour la gestion des paiements de loyer avec génération
    de reçu PDF et envoi d'email.
    """
    date_fin_paiement = forms.DateField(
        required=False,
        widget=forms.HiddenInput()
    )
    class Meta:
        model = PaiementLoyer
        fields = [
            'nombre_mois_paye',
            'montant_paye',
            'mode_paiement',
            'statut_paiement',
            'commentaire',
            'date_fin_paiement'
        ]
        widgets = {
            'nombre_mois_paye': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Nombre de mois',
                'required': True,
                'id': 'id_nombre_mois_paye'
            }),
            'montant_paye': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'placeholder': 'Montant calculé automatiquement'
            }),
            'mode_paiement': forms.Select(attrs={
                'class': 'form-select'
            }),
            'statut_paiement': forms.Select(attrs={
                'class': 'form-select'
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Commentaire (optionnel)'
            }),
    #         'date_fin_paiement': forms.DateInput(attrs={
    #     'class': 'form-control',
    #     'type': 'date',
    #     'readonly': True,
    #     'id': 'id_date_fin_paiement'
    # }),
            'date_fin_paiement': forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'id_date_fin_paiement'
            })
        }

    def __init__(self, *args, **kwargs):
        """
        Initialisation du formulaire avec des valeurs par défaut et gestion
        de l'objet `location`.
        """
        self.location = kwargs.pop('location', None)
        super().__init__(*args, **kwargs)

        # Valeurs par défaut
        self.fields['statut_paiement'].initial = 'confirmé'
        self.fields['mode_paiement'].initial = 'espèce'

        if self.location:
            self.instance.location = self.location

    def save(self, commit=True):
        """
        Surcharge de la méthode save pour envoyer un email après la sauvegarde.
        """
        instance = super().save(commit=False)

        # Vérifier si l'utilisateur et la chambre sont définis
        utilisateur = getattr(instance.location, 'utilisateur', None)
        chambre = getattr(instance.location, 'chambre', None)

        if utilisateur and chambre:
            # Préparer l'email
            sujet = "Confirmation de votre paiement de loyer"
            message = f"""
            Bonjour {utilisateur.nom} {utilisateur.prenom},

            Votre paiement pour la chambre \"{chambre.type_chambre.nom}\" a été enregistré avec succès.
            Voici les détails de votre paiement :
            - Chambre : {chambre.type_chambre.nom}
            - Montant payé : {instance.montant_paye} CFA
            - Nombre de mois payés : {instance.nombre_mois_paye}
            - Date de paiement : {instance.date_paiement.strftime('%d/%m/%Y')}
            - Mode de paiement : {instance.mode_paiement}
            - Statut du paiement : {instance.statut_paiement}

            Merci de nous faire confiance.
            Cordialement,
            L'équipe de gestion des locations
            """

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [utilisateur.email]

            try:
                # Créer un email
                email = EmailMessage(sujet, message, email_from, recipient_list)

                # Ajouter le reçu PDF en pièce jointe si disponible
                if instance.Recu_pdf and hasattr(instance.Recu_pdf, 'path') and os.path.exists(instance.Recu_pdf.path):
                    email.attach_file(instance.Recu_pdf.path)

                # Envoyer l'email
                email.send()
                print("Email envoyé avec succès.")
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'email : {e}")

        # Sauvegarder l'instance
        if commit:
            instance.save()

        return instance


class FinLocationForm(forms.ModelForm):
    class Meta:
        model = FinLocation
        fields = ['location', 'date_fin_location', 'raison_fin', 'montant_restant', 'montant_remboursement_caution', 'image_contrat']
        widgets = {
            'location': forms.Select(attrs={'class': 'form-select'}), # Classe pour le select
            'date_fin_location': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # Classe pour l'input date
            'raison_fin': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), # Classe pour textarea
            'montant_restant': forms.NumberInput(attrs={'class': 'form-control'}), # Classe pour input nombre
            'montant_remboursement_caution': forms.NumberInput(attrs={'class': 'form-control'}), # Classe pour input nombre
            'image_contrat': forms.FileInput(attrs={'class': 'form-control'}), # Classe pour input file
        }

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
#     telephone_personne_prevenir = forms.CharField(max_length=15, required=False)
#     nom_personne_prevenir = forms.CharField(max_length=100, required=False)
#     prenom_personne_prevenir = forms.CharField(max_length=100, required=False)
#     image = forms.ImageField(required=False)
#     type_utilisateur = forms.ModelChoiceField(queryset=UserType.objects.all(), required=False, help_text='Select user type.')

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'nom', 'prenom', 'email', 'tel', 'type_utilisateur', 'image', 'gender', 'telephone_personne_prevenir', 'nom_personne_prevenir', 'prenom_personne_prevenir')

#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['placeholder'] = field.label

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.phone_number = self.cleaned_data.get('phone_number')
#         user.address = self.cleaned_data.get('address')
#         #  # Définir un mot de passe par défaut
#         # default_password = 'Mon_de_passe_1234'  # Remplacez par votre mot de passe par défaut choisi
#         # user.set_password(default_password)
#         if commit:
#             user.save()
#         return user


# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
#         for field_name in self.fields:
#             field = self.fields[field_name]
#             field.widget.attrs['class'] = 'form-control'  # Applique la classe de style Bootstrap
#             field.widget.attrs['placeholder'] = field.label  # Utilise le label comme placeholder
# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import CustomUser, UserType

# class CustomUserCreationForm(UserCreationForm):
#     """
#     Formulaire d'inscription personnalisé pour `CustomUser`
#     """

#     email = forms.EmailField(
#         required=True, 
#         help_text="* Saisissez une adresse e-mail valide."
#     )
    
#     telephone_personne_prevenir = forms.CharField(
#         max_length=15, 
#         required=False, 
#         label="Téléphone d'urgence"
#     )
    
#     nom_personne_prevenir = forms.CharField(
#         max_length=100, 
#         required=False, 
#         label="Nom de la personne à prévenir"
#     )
    
#     prenom_personne_prevenir = forms.CharField(
#         max_length=100, 
#         required=False, 
#         label="Prénom de la personne à prévenir"
#     )
    
#     image = forms.ImageField(
#         required=False, 
#         label="Photo de profil"
#     )

#     type_utilisateur = forms.ModelChoiceField(
#         queryset=UserType.objects.all(),  # ⚠ Configuration dans `__init__()`
#         required=False, 
#         help_text="Sélectionnez le type d'utilisateur."
#     )
#     # type_utilisateur = forms.ModelChoiceField(queryset=UserType.objects.all(), required=False, help_text='Select user type.')


#     class Meta:
#         model = CustomUser
#         fields = ('username', 'nom', 'prenom', 'email', 'tel', 'type_utilisateur', 'image', 'gender', 'telephone_personne_prevenir', 'nom_personne_prevenir', 'prenom_personne_prevenir')
#         def save(self, commit=True):
#             """
#             Sauvegarde l'utilisateur et lui envoie un e-mail après son inscription
#             """
#             user = super().save(commit=False)
#             user.email = self.cleaned_data['email']
#             user.tel = self.cleaned_data.get('tel')
#             if commit:
#                 user.save()
#             # ✅ Envoyer l'e-mail de bienvenue
#                 self.send_welcome_email(user)
#             return user
#         def send_welcome_email(self, user):
#             """
#             Envoie un e-mail de bienvenue après la création du compte
#             """
#             subject = "Bienvenue sur notre plateforme 🎉"
#             message = f"""
#             Salut {user.prenom},
#             Félicitations ! Votre compte a été créé avec succès. 
#             Vous pouvez maintenant vous connecter et profiter de nos services.
#             Merci de nous avoir rejoint ! 🚀
#             -- L'équipe Support
#             """
#             from_email = settings.DEFAULT_FROM_EMAIL
#             recipient_list = [user.email]
#             send_mail(subject, message, from_email, recipient_list, fail_silently=False)

##################################################################################### La forme pour le propriertaire  ##########################################################################################
# class ProprietaireForm(forms.ModelForm):
#     class Meta:
#         model = Proprietaire
#         fields = ['nom', 'prenom', 'sexe', 'email','image']
#         widgets = {
#             'nom': forms.TextInput(attrs={'class': 'form-control'}),
#             'prenom': forms.TextInput(attrs={'class': 'form-control'}),
#             'sexe': forms.Select(choices=[('M', 'Homme'), ('F', 'Femme')], attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
#         }
##################################################################################### La forme pour Maison  ##########################################################################################

# User = get_user_model()  # Récupère AUTH_USER_MODEL défini dans settings.py





##################################################################################### La forme pour chambre  ##########################################################################################
# from django import forms
# from .models import Chambre

# class ChambreForm(forms.ModelForm):
#     class Meta:
#         model = Chambre
#         fields = ['maison', 'nom', 'description', 'loyer_mensuel', 'image']
#         widgets = {
#             'maison': forms.Select(attrs={'class': 'form-control'}),
#             'nom': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control'}),
#             'loyer_mensuel': forms.NumberInput(attrs={'class': 'form-control'}),
#             'image': forms.FileInput(attrs={'class': 'form-control'}),
#         }
#         labels = {
#             'maison': 'Maison',
#             'nom': 'Nom de la Chambre',
#             'description': 'Description',
#             'loyer_mensuel': 'Loyer Mensuel',
#             'image': 'Image de la Chambre',
#         }
##################################################################################### La forme pour locataire  ##########################################################################################

# class LocataireForm(forms.ModelForm):
#     class Meta:
#         model = Locataire
#         fields = ['nom', 'prenom', 'adresse', 'email', 'telephone', 'image']
#         widgets = {
#             'nom': forms.TextInput(attrs={'class': 'form-control'}),
#             'prenom': forms.TextInput(attrs={'class': 'form-control'}),
#             'adresse': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'telephone': forms.TextInput(attrs={'class': 'form-control'}),
#             'image': forms.FileInput(attrs={'class': 'form-control'}),
#         }
#         labels = {
#             'nom': 'Nom',
#             'prenom': 'Prénom',
#             'adresse': 'Adresse',
#             'email': 'Email',
#             'telephone': 'Téléphone',
#             'image': 'Image de profil',
#         }

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if Locataire.objects.filter(email=email).exists():
#             raise forms.ValidationError("Cet email est déjà utilisé.")
#         return email


##################################################################################### La forme pour locations  ##########################################################################################

# class LocationForm(forms.ModelForm):
#     class Meta:
#         model = Location
#         fields = ['locataire', 'chambre', 'date_debut', 'date_fin', 'date_liberation']
#         widgets = {
#             'locataire': forms.Select(attrs={'class': 'form-control'}),
#             'chambre': forms.Select(attrs={'class': 'form-control'}),
#             'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'date_liberation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#         }
#         labels = {
#             'locataire': 'Locataire',
#             'chambre': 'Chambre',
#             'date_debut': 'Date de début',
#             'date_fin': 'Date de fin',
#             'date_liberation': 'Date de libération',
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         date_debut = cleaned_data.get('date_debut')
#         date_fin = cleaned_data.get('date_fin')
#         date_liberation = cleaned_data.get('date_liberation')

#         if date_fin and date_debut and date_fin < date_debut:
#             self.add_error('date_fin', "La date de fin ne peut pas être antérieure à la date de début.")

#         if date_liberation and date_debut and date_liberation < date_debut:
#             self.add_error('date_liberation', "La date de libération ne peut pas être antérieure à la date de début.")
        
#         return cleaned_data
    



##################################################################################### La forme pour paiyement   ##########################################################################################


# class PaiementForm(forms.ModelForm):
#     class Meta:
#         model = Paiement
#         fields = ['location', 'date_paiement', 'montant', 'mode_paiement']
#         widgets = {
#             'location': forms.Select(attrs={'class': 'form-control'}),
#             'date_paiement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'montant': forms.NumberInput(attrs={'class': 'form-control'}),
#             'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
#         }
#         labels = {
#             'location': 'Location',
#             'date_paiement': 'Date de paiement',
#             'montant': 'Montant',
#             'mode_paiement': 'Mode de paiement',
#         }

#     def clean_montant(self):
#         montant = self.cleaned_data.get('montant')
#         if montant <= 0:
#             raise forms.ValidationError("Le montant doit être supérieur à zéro.")
#         return montant    

