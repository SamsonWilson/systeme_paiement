
from datetime import date
from django.urls import reverse
from django.utils import timezone  # ✅ Import correct
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.db.models import Manager, OuterRef, Exists
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
    # def get_maisons_louees(self):
    #         """Retourne les maisons actuellement louées par cet utilisateur."""
    #         locations_terminees = FinLocation.objects.all().values_list('location', flat=True)
    #         return Maison.objects.filter(
    #             chambres__locations__utilisateur=self
    #         ).exclude(
    #             chambres__locations__id__in=locations_terminees
    #         ).distinct().order_by('nom')
class Proprietaire(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proprietaire'
    )
    # def __str__(self):
    #     return f"Propriétaire : {self.utilisateur.get_full_name()}" if self.utilisateur else "Propriétaire sans utilisateur"
    def __str__(self):
        if self.utilisateur:
            prenom = self.utilisateur.prenom or ""
            nom = self.utilisateur.nom or ""
            tel = self.utilisateur.tel or ""
            if nom or prenom or tel:
                return f"{prenom} {nom} ({tel})".strip()  # ✅ prénom d’abord, nom ensuite
            return self.utilisateur.username
        return "Propriétaire sans utilisateur"


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/ville/')

    def __str__(self):
        return self.nom

class Quartier(models.Model):
    nom = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/Quartier/')
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='quartiers')

    def __str__(self):
        return self.nom


class Maison(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255, default='Defaut')
    nombre_piece = models.DecimalField(max_digits=5, decimal_places=0)
    code_postal = models.CharField(max_length=10, default='Defaut')
    image = models.ImageField(upload_to='images/maison/')
    quartier = models.ForeignKey('Quartier', on_delete=models.CASCADE, related_name='maisons')
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE,related_name='maisons')  # Clé étrangère vers Maison
    def __str__(self):
        return f"{self.nom} - {self.adresse}"
    def get_locataires_actifs(self):
            """
            Retourne un QuerySet des utilisateurs (locataires) qui ont une location
            active (non terminée) dans une des chambres de cette maison.
            """
            # On ne veut que les utilisateurs qui n'ont PAS de FinLocation associée à leur location
            locations_terminées = FinLocation.objects.all().values_list('location', flat=True)

            return CustomUser.objects.filter(
                locations__chambre__maison=self,
                locations__isnull=False
            ).exclude(
                locations__id__in=locations_terminées
            ).distinct()

class TypeChambre(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nom

class Message(models.Model):
    """
    Modèle pour stocker les messages échangés entre les utilisateurs.
    """
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)
    is_group_message = models.BooleanField(default=False)
    group_receivers = models.ManyToManyField(CustomUser, related_name='group_messages', blank=True)
    maison = models.ForeignKey('Maison', on_delete=models.CASCADE, related_name='messages', null=True, blank=True)  # Nouveau champ
    image = models.ImageField(upload_to='message_images/', blank=True, null=True) # Champ pour l'image
    is_read = models.BooleanField(default=False)  # ✅ pour la notification

    class Meta:
        ordering = ['-timestamp']
    def __str__(self):
/*************  ✨ Windsurf Command ⭐  *************/
    """
    Retourne une chaîne de caractères décrivant ce message.

    Si le message est un message de groupe, la chaîne commence par "Message de groupe de ".
    Sinon, la chaîne commence par "Message de ".

    La chaîne contient ensuite le nom de l'expéditeur, le nom du destinataire (si ce n'est pas un message de groupe),
    la date et l'heure du message, ainsi que le nom de la maison (si ce n'est pas un message de groupe).

    Exemples de valeurs de retour:
        "Message de groupe de John Doe - 2022-01-01 14:30:00 (Maison: Ma maison)"

/*******  9b857c40-e91e-4111-9b5a-4968b8142e13  *******/
        if self.is_group_message:
            return f"Message de groupe de {self.sender} - {self.timestamp} (Maison: {self.maison.nom if self.maison else 'Aucune'})"
        return f"Message de {self.sender} à {self.receiver} - {self.timestamp}"  

class Chambre(models.Model):
    type_chambre = models.ForeignKey(TypeChambre, on_delete=models.CASCADE)  # Clé étrangère vers TypeChambre
    surface = models.CharField(max_length=100)
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
    Recu_pdf = models.FileField(upload_to='location_Recu/', null=True, blank=True)


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
    def get_absolute_url(self):
            return reverse('location_detail', kwargs={'pk': self.pk})  # noqa: F821
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

class FinLocation(models.Model):
    location = models.ManyToManyField(
        'Location', # Assurez-vous que 'Location' est importé ou référencé correctement
        related_name='fins_location'
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
    image_contrat = models.ImageField(
        upload_to='images/fin_location/',
        blank=True,
        null=True,
        help_text="Image du contrat de fin de location"
    )
    def __str__(self):
       
        noms = []
        try:
            # self.location.all() pourrait être vide si l'objet n'est pas encore lié ou sauvegardé
            for loc in self.location.all():
                if loc.utilisateur: # Assurez-vous que Location a un champ 'utilisateur'
                    noms.append(loc.utilisateur.username)
                else:
                    noms.append(f"Location {loc.id}") # Fallback si pas d'utilisateur lié directement
        except Exception:
            # Gérer l'exception si le Manager ManyToMany n'est pas encore disponible
            noms.append("N/A")

        return f"Fin de location(s) - {', '.join(noms)} - {self.date_fin_location}"

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
    @property
    def prix_total(self):
        return self.nombre_mois_paye * self.montant_paye
    class Meta:
        ordering = ['-date_paiement']
        verbose_name = "Paiement de Loyer"
        verbose_name_plural = "Paiements de Loyer"
