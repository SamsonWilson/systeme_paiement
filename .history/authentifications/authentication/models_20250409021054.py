
from datetime import date
from django.utils import timezone  # ✅ Import correct
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserType(models.Model):
    """
    Modèle définissant les types d’utilisateurs pré-définis.
    Exemples : Propriétaire, Locataire, Admin.
    """
    
    TYPE_CHOICES = [
        ('propriétaire', 'Propriétaire'),
        ('locataire', 'Locataire'),
        ('admin', 'Admin'),
    ]
    nom = models.CharField(max_length=50, unique=True, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom  # ✅ Correction : suppression de la double définition

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé héritant de `AbstractUser`.
    Possède des informations supplémentaires par rapport au `User` standard de Django.
    """

    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('O', 'Autre'),
    ]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    tel = models.CharField(max_length=15, blank=True, null=True)
    # 🚀 Clé étrangère pour déterminer le type d’utilisateur (ex: Propriétaire, Locataire, Admin)
    type_utilisateur = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    telephone_personne_prevenir = models.CharField(max_length=15)
    nom_personne_prevenir = models.CharField(max_length=100)
    prenom_personne_prevenir = models.CharField(max_length=100)
    # 🚀 Ajout d'une valeur par défaut pour éviter les erreurs si aucune image n'est fournie
    image = models.ImageField(upload_to='images/photo/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    def __str__(self):
        return f"{self.username} ({self.type_utilisateur.nom if self.type_utilisateur else 'Aucun type'})"

class Proprietaire(models.Model):

    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('O', 'Autre'),
    ]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='images/proprietaire/', blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Ville(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/ville/')

    def __str__(self):
        return self.nom

class Quartier(models.Model):
    nom = models.CharField(max_length=10)
    description = models.TextField()
    image = models.ImageField(upload_to='images/Quartier/')
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='quartiers')

    def __str__(self):
        return self.nom


class Maison(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    nombre_piece = models.DecimalField(max_digits=5, decimal_places=0)
    code_postal = models.CharField(max_length=10, default='Defaut')
    image = models.ImageField(upload_to='images/maison/')
    quartier = models.ForeignKey('Quartier', on_delete=models.CASCADE, related_name='maisons')
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE,related_name='maisons')  # Clé étrangère vers Maison
    def __str__(self):
        return f"{self.nom} - {self.adresse}"


class TypeChambre(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nom


class Chambre(models.Model):
    type_chambre = models.ForeignKey(TypeChambre, on_delete=models.CASCADE)  # Clé étrangère vers TypeChambre
    surface = models.FloatField()
    taux_commission = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    etat = models.CharField(max_length=20, choices=[('libre', 'Libre'), ('occupée', 'Occupée')], default='libre')
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    maison = models.ForeignKey(Maison, on_delete=models.CASCADE,related_name='chambres')  # Clé étrangère vers Maison
    def save(self, *args, **kwargs):
        # Assurez-vous que la maison est définie avant de sauvegarder
        if not self.maison:
            raise ValueError("La maison doit être définie pour enregistrer une chambre.")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Chambre {self.etat}"



class Location(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='locations'
    )
    chambre = models.ForeignKey(
        'Chambre',
        on_delete=models.CASCADE,
        related_name='locations'
    )
    
    date_debut_location = models.DateField(verbose_name="Date de début de location")
    date_fin_avance = models.DateField(null=True, blank=True, verbose_name="Date de fin d'avance")
    montant_avance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Montant d'avance"
    )
    montant_caution = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Montant de la caution"
    )
    nombre_mois_paye = models.IntegerField(default=0, verbose_name="Nombre de mois payé")
    commission = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Commission"
    )
    montant_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Montant total"
    )
    image_contrat = models.ImageField(
        upload_to='images/location/',
        blank=True,
        null=True,
        verbose_name="Image du contrat",
        help_text="Image du contrat de fin de location"
    )
    statut_paiement = models.CharField(
        max_length=30,
        choices=[
            ('payé', 'Payé'),
            ('avance payée, pas caution', 'Avance payée, pas caution')
        ],
        default='payé',
        verbose_name="Statut du paiement"
    )
    mode_paiement = models.CharField(
        max_length=50,
        choices=[
            ('espèce', 'Espèce'),
            ('mobile', 'Paiement mobile')
        ],
        default='espèce',
        verbose_name="Mode de paiement"
    )
    date_paiement = models.DateField(
        default=date.today,
        blank=True,
        null=True,
        verbose_name="Date de paiement"
    )
    Recu_pdf = models.FileField(upload_to='location/Recu/', null=True, blank=True)


    def save(self, *args, **kwargs):
        self.update_chambre_status()
        self.set_default_payment_date()
        self.calculate_commission()
        super().save(*args, **kwargs)

    def update_chambre_status(self):
        """Met à jour l'état de la chambre."""
        if self.chambre and self.chambre.etat == "libre":
            self.chambre.etat = "occupée"
            self.chambre.save()

    def set_default_payment_date(self):
        """Définit la date de paiement par défaut."""
        if self.statut_paiement == "payé" and not self.date_paiement:
            self.date_paiement = date.today()

    def calculate_commission(self):
        """Calcule la commission en fonction du taux de la chambre."""
        self.commission = (self.montant_avance * self.chambre.taux_commission / 100) if self.chambre and self.montant_avance else 0

    def __str__(self):
        utilisateur_nom = self.utilisateur.username if self.utilisateur else 'N/A'
        return f"Location {utilisateur_nom} - {self.statut_paiement} - {self.date_debut_location.strftime('%d %B %Y') if self.date_debut_location else 'N/A'}"

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class FinLocation(models.Model):
    location = models.OneToOneField(
        'Location', 
        on_delete=models.CASCADE, 
        related_name='fin_location'
    )
    date_fin_location = models.DateField()
    raison_fin = models.TextField(blank=True, null=True)  
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    montant_remboursement_caution = models.DecimalField(  
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        help_text="Montant remboursé au locataire pour la caution"
    )
    image_contrat = models.ImageField(  # Ajout du champ image
        upload_to='images/fin_location/', 
        blank=True, 
        null=True,
        help_text="Image du contrat de fin de location"
    )
    etat_chambre_final = models.CharField(
        max_length=20, 
        choices=[('libre', 'Libre'), ('occupée', 'Occupée')], 
        default='libre'
    )
    Paiement

    def save(self, *args, **kwargs):
        if self.montant_remboursement_caution > self.location.montant_caution:
            raise ValueError("Le remboursement de la caution ne peut pas dépasser la caution initiale.")

        if self.location.chambre:
            self.location.chambre.etat = 'libre'
            self.location.chambre.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Fin de location - {self.location.utilisateur.username if self.location.utilisateur else 'N/A'} - {self.date_fin_location}"


class PaiementLoyer(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='paiements')
    nombre_mois_paye = models.IntegerField(default=0)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(default=timezone.now, verbose_name="Date et heure du paiement")  # noqa: F821
    date_fin_paiement = models.DateField(null=True, blank=True)

    mode_paiement = models.CharField(
        max_length=50,
        choices=[
            ('espèce', 'Espèce'),
            ('mobile', 'Paiement mobile')
        ],
        default='espèce'
    )

    statut_paiement = models.CharField(
        max_length=30,
        choices=[
            ('confirmé', 'Confirmé'),
            ('en attente', 'En attente')
        ],
        default='confirmé'
    )

    # Commission basée sur le taux de la chambre
    commission = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Commission automatique basée sur la chambre."
    )

    commentaire = models.TextField(blank=True, null=True)
    Recu_pdf = models.FileField(upload_to='Paiement/Recu/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Vérifier que la location est bien liée
        if not self.location:
            raise ValueError("Le paiement doit être associé à une location.")

        # Vérifier que la chambre associée possède un taux de commission
        taux_commission = self.location.chambre.taux_commission if self.location.chambre else 0

        # Calcul de la commission en fonction du taux de la chambre
        self.commission = (self.montant_paye * taux_commission) / 100

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Paiement {self.montant_paye} FCFA - {self.nombre_mois_paye} mois - Statut: {self.statut_paiement}"

    class Meta:
        ordering = ['-date_paiement']
        verbose_name = "Paiement de Loyer"
        verbose_name_plural = "Paiements de Loyer"
        
# class Locataire(models.Model):
#     nom = models.CharField(max_length=100)
#     prenom = models.CharField(max_length=100)
#     adresse = models.CharField(max_length=255)
#     email = models.EmailField()
#     telephone = models.CharField(max_length=15)
#     image = models.ImageField(upload_to='images/Locataire/')


#     def __str__(self):
#         return f"{self.prenom} {self.nom}"

# class Location(models.Model):
#     locataire = models.ForeignKey(Locataire, on_delete=models.CASCADE, related_name='locations')
#     chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='locations')
#     date_debut = models.DateField()
#     date_fin = models.DateField(null=True, blank=True)
#     date_liberation = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.locataire} - {self.chambre.nom}"

# class Paiement(models.Model):
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='paiements')
#     date_paiement = models.DateField()
#     montant = models.DecimalField(max_digits=10, decimal_places=2)
#     mode_paiement = models.CharField(max_length=50, choices=[('CB', 'Carte Bancaire'), ('VIREMENT', 'Virement'), ('CHEQUE', 'Chèque')])

#     def __str__(self):
#         return f"{self.date_paiement} - {self.montant} CFA"

