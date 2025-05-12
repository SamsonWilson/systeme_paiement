from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chambre

@receiver(post_save, sender=Chambre)
def decrement_nombre_piece(sender, instance, created, **kwargs):
    if created:  # Vérifie si une nouvelle chambre a été créée
        maison = instance.maison
        if maison.nombre_piece > 0:  # Vérifie qu'il reste des pièces disponibles
            maison.nombre_piece -= 1
            maison.save()