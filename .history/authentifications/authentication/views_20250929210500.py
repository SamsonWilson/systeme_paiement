# from django.http import HttpResponseForbidden
# from django.shortcuts import render
# from email.message import EmailMessage
# from django.conf import settings
import base64
from io import BytesIO
from pyexpat.errors import messages
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import  generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .forms import  ChambreForm, CustomUserChangeForm, CustomUserCreationForm, CustomAuthenticationForm, CustomUserReinitialisationPasswordForm, LocationForm, MaisonForm, MessageForm, PaiementLoyerForm, ProprietaireForm, TypeChambreForm, VilleForm, VilleSearchForm,QuartierForm
from .models import Chambre, CustomUser, Location, Maison, PaiementLoyer, Proprietaire, TypeChambre, Ville, Quartier
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.contrib import messages  # noqa: F811
from datetime import  datetime, timezone
import pytz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.core.paginator import Paginator
from django.db.models import Sum, Avg, Count # Fonctions d'agrégation
from decimal import Decimal #
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.template.loader import get_template
from django.views import View
# from xhtml2pdf import pisa
import io
from django.views.generic.base import RedirectView
# from django.http import JsonResponse
from .models import FinLocation
from .forms import FinLocationForm
from django.db import models  # Import de models pour les requêtes complexes
from .models import Message
# from authentifications.authentication import forms  # Import des modèles nécessaires
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Sum
# from django.http import HttpResponse

from django.views.generic import ListView
from .models import CustomUser



class UserListView(ListView):
    model = CustomUser
    template_name = 'registration/utilisateurListe.html'  # Le template que tu vas créer
    context_object_name = 'utilisateurs'    # Le nom utilisé dans le template (facultatif)
    paginate_by = 10  # (Facultatif) Pour ajouter la pagination
    # def get_queryset(self):
    #     return CustomUser.objects.filter(type_utilisateur__nom='propriétaire')

class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'registration/user_detail.html'  # Tu vas créer ce template
    context_object_name = 'utilisateur'

class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm 
    template_name = 'registration/user_formUpdate.html'  # crée ce template
    success_url = reverse_lazy('liste_utilisateurs')

# class UserUpdateReinitialisationPasswordView(UpdateView):
#     model = CustomUser
#     form_class = CustomUserReinitialisationPasswordForm
#     template_name = 'registration/ReinitialisationPasswordForm.html'  # crée ce template
#     success_url = reverse_lazy('liste_utilisateurs')
class UserUpdateReinitialisationPasswordView(UpdateView):
    model = CustomUser
    form_class = CustomUserReinitialisationPasswordForm
    template_name = 'registration/ReinitialisationPasswordForm.html' # à adapter
    success_url = reverse_lazy('liste_utilisateurs')  # redirection après modification
    def get_object(self, queryset=None):
        return CustomUser.objects.get(pk=self.kwargs['pk'])
    # facultatif : si tu veux changer l'objet à récupérer autrement que par pk
    # def get_object(self):
    #     return CustomUser.objects.get(pk=self.kwargs['pk'])
# CustomUserReinitialisationPasswordForm
class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    success_message = "Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter. 🎉"

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

@method_decorator(login_required, name='dispatch')
class TableauDeBordView(TemplateView):
    template_name = 'accuiel/Base.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 📌 Statistiques générales
        context["maisons_count"] = Maison.objects.count()
        context["quartiers_count"] = Quartier.objects.count()
        context["villes_count"] = Ville.objects.count()
        context["proprietaires_count"] = Proprietaire.objects.count()
        context["locataires_count"] = CustomUser.objects.filter(type_utilisateur__nom="locataire").count()
        context["chambres_libres_count"] = Chambre.objects.filter(etat="libre").count()
        context["chambres_occupees_count"] = Chambre.objects.filter(etat="occupée").count()
        context["paiements_count"] = PaiementLoyer.objects.count()

        # 📊 Données pour le graphique Camembert (Chambres libres vs occupées)
        context["chambres_labels"] = ["Disponibles", "Occupées"]
        context["chambres_data"] = [
            context["chambres_libres_count"],
            context["chambres_occupees_count"]
        ]

        # 📊 Données pour le graphique Barres (Locations par mois)
        locations_data = (
            Location.objects
            .values("date_debut_location__month")
            .annotate(total=models.Count("id"))
            .order_by("date_debut_location__month")
        )
        context["locations_labels"] = [f"Mois {l['date_debut_location__month']}" for l in locations_data]
        context["locations_data"] = [l["total"] for l in locations_data]

        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     # Ajoutez le type d'utilisateur au contexte s'il existe
    #     context['user_type'] = user.type_utilisateur.nom if user.type_utilisateur else None
    #     # Ajoutez d'autres données nécessaires pour le template
    #     context['user'] = user # Rendre l'objet user disponible aussi
       
    #     return context


#################################################################################  message  ######################################################"


#...existing code...
# class SendMessageView(LoginRequiredMixin, View):
#     """
#     CBV pour envoyer un message.
#     """

#     def post(self, request, *args, **kwargs):
#         sender = request.user
#         receiver_id = request.POST.get('receiver_id')
#         message_text = request.POST.get('message')
#         is_group_message = request.POST.get('is_group_message') == 'true'
#         group_receiver_ids = request.POST.getlist('group_receivers')

#         if not is_group_message:
#             # Vérifiez si le destinataire existe
#             receiver = get_object_or_404(CustomUser, id=receiver_id)

#             # Créez le message
#             message = Message.objects.create(sender=sender, receiver=receiver, message=message_text, is_group_message=False)
#         else:
#             message = Message.objects.create(sender=sender, message=message_text, is_group_message=True)
#             receivers = CustomUser.objects.filter(id__in=group_receiver_ids)
#             message.group_receivers.set(receivers)

#         return JsonResponse({
#             'status': 'ok',
#             'message': message.message,
#             'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
#         })

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['receiver', 'message', 'is_group_message', 'group_receivers']
    template_name = 'chat/message_form.html'
    success_url = reverse_lazy('conversation_list')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
# class GetMessagesView(LoginRequiredMixin, View):
#     """
#     CBV pour récupérer les messages entre deux utilisateurs.
#     """
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         messages = Message.objects.filter(
#             Q(sender=user) |  # Messages envoyés par l'utilisateur
#             Q(receiver=user) |  # Messages reçus par l'utilisateur
#             (Q(is_group_message=True) & Q(group_receivers=user))  # Messages de groupe dont l'utilisateur est un destinataire
#         ).order_by('timestamp')

#         messages_data = [
#             {
#                 'sender': message.sender.username,
#                 'receiver': message.receiver.username if message.receiver else 'Groupe',
#                 'message': message.message,
#                 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
#                 'is_read': message.is_read,
#                 'is_group_message': message.is_group_message,
#                 'group_receivers': [receiver.username for receiver in message.group_receivers.all()]
#             }
#             for message in messages
#         ]
#         return JsonResponse({'messages': messages_data})

class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'accuiel/messages/message_list.html'
    context_object_name = 'message'

    def get_queryset(self):
        # Filtrer pour ne voir que les messages pertinents
        return Message.objects.filter(
            Q(sender=self.request.user) | 
            Q(receiver=self.request.user) |
            Q(group_receivers=self.request.user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter les messages de la conversation
        context['messages'] = self.get_queryset().filter(
            Q(sender=self.object.sender) | 
            Q(receiver=self.object.receiver)
        )
        return context
# class ChatView(LoginRequiredMixin, TemplateView):
#     template_name = 'accuiel/messages/message_list.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         receiver_id = self.kwargs.get('receiver_id')
#         user = self.request.user
#         all_users = CustomUser.objects.all()

#         if receiver_id:
#             receiver = get_object_or_404(CustomUser, id=receiver_id)
#             # Filtrer les messages pour afficher uniquement ceux entre l'utilisateur connecté et le locataire sélectionné
#             messages = Message.objects.filter(
#                 (Q(sender=user, receiver=receiver) |
#                  Q(sender=receiver, receiver=user))
#             ).order_by('timestamp')
#             context['chat_user'] = receiver
#         else:
#             messages = Message.objects.filter(
#                 Q(sender=user) |  # Messages envoyés par l'utilisateur
#                 Q(receiver=user) |  # Messages reçus par l'utilisateur
#                 (Q(is_group_message=True) & Q(group_receivers=user))  # Messages de groupe dont l'utilisateur est un destinataire
#             ).order_by('timestamp')

#         context['messages'] = messages
#         context['user'] = user
#         context['is_admin'] = user.type_utilisateur.nom == 'admin' if user.type_utilisateur else False
#         context['all_users'] = all_users
#         return context
#...existing code...
class ConversationListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'accuiel/messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        # Récupère les messages où l'utilisateur est soit l'expéditeur, soit le destinataire
        return Message.objects.filter(
            models.Q(sender=self.request.user) | 
            models.Q(receiver=self.request.user) |
            models.Q(group_receivers=self.request.user)
        ).distinct().order_by('-timestamp')


##########################################################################################################################################################""""""
# class ChatView(LoginRequiredMixin, View):
#     def get(self, request, receiver_id=None):
#         """
#         Gère l'affichage des messages individuels.
#         """
#         user = request.user

#         # Gérer la liste filtrée des utilisateurs
#         if hasattr(user, 'type_utilisateur') and user.type_utilisateur.nom == 'locataire':
#             # Si utilisateur est locataire => voir seulement les admins
#             all_users = CustomUser.objects.filter(type_utilisateur__nom='admin')
#         else:
#             # Sinon (admin ou propriétaire) => voir tous sauf lui-même
#             all_users = CustomUser.objects.exclude(id=user.id)

#         # Si un ID de destinataire est fourni, charger les messages individuels
#         if receiver_id:
#             chat_user = get_object_or_404(CustomUser, id=receiver_id)
#             messages = Message.objects.filter(
#                 Q(sender=user, receiver=chat_user) | Q(sender=chat_user, receiver=user)
#             ).order_by('timestamp')
            
#             return render(request, 'accuiel/messages/messages_list.html', {
#                 'messages': messages,
#                 'chat_user': chat_user,
#                 'maison': None,  # Pas de maison pour cette vue
#                 'all_users': all_users,  # Liste filtrée ici
#             })

#         # Si aucun destinataire n'est spécifié
#         raise Http404("Aucun destinataire spécifié.")

#     def post(self, request, receiver_id=None):
#         """
#         Gère l'envoi des messages privés entre un utilisateur et un administrateur.
#         """
#         user = request.user
#         message_content = request.POST.get('message')

#         # Vérification si le message n'est pas vide
#         if not message_content or not message_content.strip():
#             return JsonResponse({"message": "Le message ne peut pas être vide"}, status=400)

#         # Vérification que le destinataire est valide
#         if not receiver_id:
#             return JsonResponse({"message": "Aucun destinataire spécifié"}, status=400)

#         # Récupérer le destinataire
#         receiver = get_object_or_404(CustomUser, id=receiver_id)

#         # Vérifier que l'utilisateur ne parle pas à lui-même
#         if receiver == user:
#             return JsonResponse({"message": "Vous ne pouvez pas envoyer de messages à vous-même."}, status=400)

#         # Vérifier que l'expéditeur est un locataire et le destinataire un admin
#         if (user.type_utilisateur.nom == "locataire" and receiver.type_utilisateur.nom != "admin") or \
#            (user.type_utilisateur.nom != "locataire" and receiver.type_utilisateur.nom == "admin"):
#             return JsonResponse({"message": "La conversation doit être entre un locataire et un administrateur."}, status=400)

#         # Créer le message
#         Message.objects.create(sender=user, receiver=receiver, message=message_content)

#         # Répondre avec le succès du message
#         return JsonResponse({
#             "message": "Message individuel envoyé avec succès",
#             "message_content": message_content,
#             "timestamp": now().strftime('%H:%M'),
#         })




class ChatView(LoginRequiredMixin, View):

    def get_all_users(self, user):
        """Filtre la liste des utilisateurs disponibles selon le type."""
        if getattr(user, 'type_utilisateur', None) and user.type_utilisateur.nom == 'locataire':
            return CustomUser.objects.filter(type_utilisateur__nom='admin')
        return CustomUser.objects.exclude(id=user.id)

    def get(self, request, receiver_id=None):
        user = request.user

        if not receiver_id:
            raise Http404("Aucun destinataire spécifié.")

        receiver = get_object_or_404(CustomUser, id=receiver_id)
        messages = Message.objects.filter(
            Q(sender=user, receiver=receiver) |
            Q(sender=receiver, receiver=user)
        ).order_by('timestamp')

        return render(request, 'accuiel/messages/messages_list.html', {
            'messages': messages,
            'chat_user': receiver,
            'all_users': self.get_all_users(user),
            'maison': None,  # Tu pourras enlever maison si elle ne sert plus
        })

    def post(self, request, receiver_id=None):
        user = request.user
        message_content = request.POST.get('message', '').strip()

        if not receiver_id:
            return JsonResponse({"message": "Aucun destinataire spécifié"}, status=400)

        if not message_content:
            return JsonResponse({"message": "Le message ne peut pas être vide"}, status=400)

        receiver = get_object_or_404(CustomUser, id=receiver_id)

        if receiver == user:
            return JsonResponse({"message": "Vous ne pouvez pas envoyer de message à vous-même."}, status=400)

        if (user.type_utilisateur.nom == "locataire" and receiver.type_utilisateur.nom != "admin") or \
           (user.type_utilisateur.nom != "admin" and receiver.type_utilisateur.nom == "locataire"):
            return JsonResponse({"message": "La conversation doit être entre un locataire et un administrateur."}, status=400)

        Message.objects.create(sender=user, receiver=receiver, message=message_content)

        return JsonResponse({
            "message": "Message envoyé avec succès",
            "message_content": message_content,
            "timestamp": now().strftime('%H:%M'),
        })






    # def get(self, request, receiver_id=None):
    #     """
    #     Gère l'affichage des messages individuels.
    #     """
    #     user = request.user
    #     # Si un ID de destinataire est fourni, charger les messages individuels
    #     if receiver_id:
    #         chat_user = get_object_or_404(CustomUser, id=receiver_id)
    #         messages = Message.objects.filter(
    #             Q(sender=user, receiver=chat_user) | Q(sender=chat_user, receiver=user)
    #         ).order_by('timestamp')
    #         return render(request, 'accuiel/messages/messages_list.html', {
    #             'messages': messages,
    #             'chat_user': chat_user,
    #             'maison': None,  # Pas de maison pour cette vue
    #             'all_users': CustomUser.objects.exclude(id=user.id),  # Liste des autres utilisateurs
    #         })

    #     # Si aucun destinataire n'est spécifié
    #     raise Http404("Aucun destinataire spécifié.")

    # def post(self, request, receiver_id=None):
    #     """
    #     Gère l'envoi des messages privés.
    #     """
    #     user = request.user
    #     message_content = request.POST.get('message')

    #     # Vérification si le message n'est pas vide
    #     if not message_content or not message_content.strip():
    #         return JsonResponse({"message": "Le message ne peut pas être vide"}, status=400)

    #     # Envoi d'un message individuel
    #     if receiver_id:
    #         receiver = get_object_or_404(CustomUser, id=receiver_id)
    #         Message.objects.create(sender=user, receiver=receiver, message=message_content)
    #         return JsonResponse({
    #             "message": "Message individuel envoyé avec succès",
    #             "message_content": message_content,
    #             "timestamp": now().strftime('%H:%M'),
    #         })
    #     # Si aucun destinataire n'est spécifié
    #     return JsonResponse({"message": "Aucun destinataire spécifié"}, status=400)


class GroupMessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'accuiel/messages/messages_list.html'
    context_object_name = 'messages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupération de l'ID de la maison depuis l'URL
        maison_id = self.kwargs.get('maison_id')

        # L'utilisateur actuellement connecté
        user = self.request.user

        # Liste des maisons associées à l'utilisateur connecté
        maisons = user.maisons.all()  # Assure-toi que la relation Many-to-Many est définie dans CustomUser

        # Cas où une maison est spécifiée (message de groupe)
        if maison_id:
            maison = get_object_or_404(Maison, id=maison_id)
            # Récupérer tous les messages de la maison
            messages = Message.objects.filter(
                maison=maison,
                is_group_message=True
            ).order_by('timestamp')
            # Récupérer tous les utilisateurs associés à la maison
            utilisateurs = maison.utilisateurs.all()  # Récupère les utilisateurs associés à cette maison
            context['maison'] = maison
            context['chat_user'] = None  # Aucune conversation avec un utilisateur individuel

        else:
            # Cas où aucun groupe n'est spécifié (tous les messages de groupe de l'utilisateur)
            messages = Message.objects.filter(
                Q(is_group_message=True) & Q(group_receivers=user)
            ).order_by('timestamp')
            context['chat_user'] = None
            context['maison'] = None
            utilisateurs = []  # Aucun utilisateur spécifié dans ce cas

        # Ajouter les autres variables contextuelles
        context['messages'] = messages
        context['user'] = user
        context['maisons'] = maisons
        context['utilisateurs'] = utilisateurs

        return context


# class MessageListView(LoginRequiredMixin, ListView):
#     model = Message
#     template_name = 'accuiel/messages/messages_list.html'
#     context_object_name = 'messages'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         receiver_id = self.kwargs.get('receiver_id')
#         user = self.request.user

#         # Ici on filtre les utilisateurs selon le type de l'utilisateur connecté
#         if hasattr(user, 'type_utilisateur') and user.type_utilisateur.nom == 'locataire':
#             # Si utilisateur est locataire => voir seulement les admins
#             all_users = CustomUser.objects.filter(type_utilisateur__nom='admin')
#         else:
#             # Sinon (admin ou propriétaire) => voir tous les utilisateurs sauf lui-même
#             all_users = CustomUser.objects.exclude(id=user.id)

#         if receiver_id:
#             receiver = get_object_or_404(CustomUser, id=receiver_id)

#             messages = Message.objects.filter(
#                 Q(sender=user, receiver=receiver) |
#                 Q(sender=receiver, receiver=user)
#             ).order_by('timestamp')

#             context['chat_user'] = receiver

#         else:
#             messages = Message.objects.filter(
#                 Q(sender=user) | Q(receiver=user)
#             ).order_by('timestamp')

#             context['chat_user'] = None

#         context['messages'] = messages
#         context['user'] = user
#         context['all_users'] = all_users
#         context['is_admin'] = user.type_utilisateur.nom == 'admin' if hasattr(user, 'type_utilisateur') else False

#         return context
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'accuiel/messages/messages_list.html'
    context_object_name = 'messages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        receiver_id = self.kwargs.get('receiver_id')

        # Filtrage des utilisateurs
        if getattr(user, 'type_utilisateur', None) and user.type_utilisateur.nom == 'locataire':
            all_users = CustomUser.objects.filter(type_utilisateur__nom='admin')
        else:
            all_users = CustomUser.objects.exclude(id=user.id)

        # Chargement des messages selon qu'il y a un destinataire ou non
        if receiver_id:
            receiver = get_object_or_404(CustomUser, id=receiver_id)
            messages = Message.objects.filter(
                Q(sender=user, receiver=receiver) |
                Q(sender=receiver, receiver=user)
            ).order_by('timestamp')
            context['chat_user'] = receiver
        else:
            messages = Message.objects.filter(
                Q(sender=user) | Q(receiver=user)
            ).order_by('timestamp')
            context['chat_user'] = None

        context.update({
            'messages': messages,
            'user': user,
            'all_users': all_users,
            'is_admin': getattr(user.type_utilisateur, 'nom', '') == 'admin'
        })

        return context


# class MessageListView(LoginRequiredMixin, ListView):
#     model = Message
#     template_name = 'accuiel/messages/messages_list.html'
#     context_object_name = 'messages'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Récupération de l'ID du destinataire depuis l'URL
#         receiver_id = self.kwargs.get('receiver_id')

#         # L'utilisateur actuellement connecté
#         user = self.request.user

#         # Liste des utilisateurs à exclure (exclure l'utilisateur connecté)
#         all_users = CustomUser.objects.exclude(id=user.id)

#         # Cas où un destinataire est spécifié
#         if receiver_id:
#             receiver = get_object_or_404(CustomUser, id=receiver_id)
#             messages = Message.objects.filter(
#                 Q(sender=user, receiver=receiver) |
#                 Q(sender=receiver, receiver=user)
#             ).order_by('timestamp')
#             context['chat_user'] = receiver
#             context['maison'] = None  # Aucune maison dans ce cas

#         else:
#             # Cas où aucun destinataire n'est spécifié (tous les messages de l'utilisateur)
#             messages = Message.objects.filter(
#                 Q(sender=user) |
#                 Q(receiver=user) |
#                 (Q(is_group_message=True) & Q(group_receivers=user))
#             ).order_by('timestamp')
#             context['chat_user'] = None
#             context['maison'] = None

#         # Ajouter les autres variables contextuelles
#         context['messages'] = messages
#         context['user'] = user
#         context['is_admin'] = user.type_utilisateur.nom == 'admin' if hasattr(user, 'type_utilisateur') else False
#         context['all_users'] = all_users

#         return context



############################################################################################################################################################""""

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    receiver = forms.ModelChoiceField(queryset=CustomUser.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Seuls les utilisateurs de type admin peuvent être sélectionnés comme destinataires
            self.fields['receiver'].queryset = CustomUser.objects.filter(
                type_utilisateur__nom='admin'
            )       
#########################################################################################################################
class RedirectionParTypeUtilisateurView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        user_type = user.type_utilisateur.nom if user.type_utilisateur else None

        if user_type == 'Admin':
            return reverse('tableau_de_bord')
        elif user_type == 'Propriétaire':
            return reverse('tableau_de_bord')
        elif user_type == 'locataire':
            return reverse('tableau_de_bord')   

        return reverse('page_erreur')  # À définir si besoin
# ##################################################################### Villes #####################################################################
class VilleListView(LoginRequiredMixin,ListView):
    model = Ville
    template_name = 'accuiel/villes/ville_list.html'
    context_object_name = 'villes'
    login_url = reverse_lazy('login')  # L'URL vers laquelle rediriger en cas d'échec

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VilleSearchForm(self.request.GET)
        if form.is_valid():
            recherche = form.cleaned_data.get('recherche')
            if recherche:
                queryset = queryset.filter(nom__icontains=recherche)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VilleSearchForm(self.request.GET)
        return context

class VilleCreateView(LoginRequiredMixin,CreateView):
    model = Ville
    form_class = VilleForm
    template_name = 'accuiel/villes/ajouter_ville.html'
    success_url = reverse_lazy('ville_list')

class VilleUpdateView(LoginRequiredMixin,UpdateView):
    model = Ville
    form_class = VilleForm
    template_name = 'accuiel/villes/modifier_ville.html'
    success_url = reverse_lazy('ville_list')

class VilleDeleteView(LoginRequiredMixin,DeleteView):
    model = Ville
    template_name = 'accuiel/villes/supprimer_ville.html'
    success_url = reverse_lazy('ville_list')
# ##################################################################### Quartiers #####################################################################
class  QuartierListView(ListView):
    model = Quartier
    template_name = 'accuiel/Quartiers/Quartier_list.html'
    context_object_name = 'Quartiers'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VilleSearchForm(self.request.GET)
        if form.is_valid():
            recherche = form.cleaned_data.get('recherche')
            if recherche:
                queryset = queryset.filter(nom__icontains=recherche)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VilleSearchForm(self.request.GET)
        return context

class  QuartierCreateView(CreateView):
    model = Quartier
    form_class = QuartierForm
    template_name = 'accuiel/Quartiers/ajouter_Quartier.html'
    success_url = reverse_lazy('Quatiers_list')

class  QuartierUpdateView(UpdateView):
    model = Quartier
    form_class = QuartierForm
    template_name = 'accuiel/Quartiers/modifier_Quartier.html'
    success_url = reverse_lazy('Quatiers_list')

class  QuartierDeleteView(DeleteView):
    model = Quartier
    template_name = 'accuiel/Quartiers/supprimer_Quartier.html'
    success_url = reverse_lazy('Quatiers_list')    




# ##################################################################### Proprietaire #####################################################################
class ProprietaireListView(ListView):
    model = Proprietaire  # noqa: F821
    template_name = 'accuiel/proprietaires/Proprietaire_list.html'
    context_object_name = 'proprietaires'
    def get_queryset(self):
            """
            OPTIMISATION : On surcharge get_queryset pour pré-charger les données
            de l'utilisateur associé à chaque propriétaire.
            
            `select_related('utilisateur')` effectue une jointure SQL, ce qui réduit
            le nombre de requêtes à la base de données de N+1 à une seule.
            C'est une pratique essentielle pour les ListView.
            """
            # On récupère le queryset de base (tous les propriétaires)
            queryset = super().get_queryset()
            # On y attache les données de l'utilisateur
            return queryset.select_related('utilisateur')
class ProprietaireCreateView(CreateView):
    model = Proprietaire
    form_class = ProprietaireForm  # noqa: F821
    template_name = 'accuiel/proprietaires/ajouter_Proprietaire.html'
    success_url = reverse_lazy('liste_proprietaire')
    def form_valid(self, form):
        utilisateur = form.cleaned_data['utilisateur']
        # nom = utilisateur.nom
        # prenom = utilisateur.prenom

        # Vérification s’il existe déjà un propriétaire avec ce même utilisateur
        if Proprietaire.objects.filter(utilisateur=utilisateur).exists():
            messages.error(self.request, "Ce propriétaire existe déjà.")
            return self.form_invalid(form)

        return super().form_valid(form)

class ProprietaireUpdateView(UpdateView):
    model = Proprietaire
    form_class = ProprietaireForm
    template_name = 'accuiel/proprietaires/ajouter_Proprietaire.html'
    success_url = reverse_lazy('liste_proprietaire')

class ProprietaireDeleteView(DeleteView):
    model = Proprietaire
    template_name = 'accuiel/proprietaires/Suprimer_proprietaire.html'
    success_url = reverse_lazy('liste_proprietaire')

class ProprietaireDetailView(DetailView):  # noqa: F821
    model = Proprietaire
    template_name = 'accuiel/proprietaires/proprietaire_detail.html'
    context_object_name = 'proprietaire'

 # Assurez-vous que le chemin d'importation est correct
# gestion/views.py


# class LocationDetailView(LoginRequiredMixin, DetailView): # Example
#     model = Location
#     template_name = 'gestion/location_detail.html' # Create this template
#     context_object_name = 'location'

#     def get_queryset(self):
#         # Ensure users can only see locations related to them somehow
#         # This is just an example, adjust the logic based on your requirements
#         # (e.g., owner sees all locations in their houses, tenant sees their own)
#         queryset = super().get_queryset()
#         # Example: Allow owner to see locations in their houses
#         try:
#             prop = Proprietaire.objects.get(utilisateur=self.request.user)
#             return queryset.filter(chambre__maison__proprietaire=prop)
#         except Proprietaire.DoesNotExist:
#              # Example: Allow tenant to see their own location
#              if hasattr(self.request.user, 'locations'): # Check if user has 'locations' related_name
#                  return queryset.filter(utilisateur=self.request.user)
#              else:
#                  return queryset.none() # Or raise PermissionDenied
# --- Owner Dashboard Class-Based View ---
class DashboarProprietairedView(LoginRequiredMixin, TemplateView):
    template_name = 'accuiel/proprietaires/proprietaire_dashboard.html'
    def get_context_data(self, **kwargs):
        """
        Fetches and prepares the context data for the template.
        """
        # Get the default context from the parent class
        context = super().get_context_data(**kwargs)
        request = self.request # Access the request object via self.request
        try:
            # Get the Proprietaire profile linked to the logged-in user
            proprietaire = get_object_or_404(Proprietaire, utilisateur=request.user)
        except Http404:
            # Handle users logged in but without a Proprietaire profile
            # You might want to redirect or show a specific message.
            # For simplicity here, we re-raise Http404, which Django handles.
            # You could also set a flag in the context and show a message in the template.
            # context['error_message'] = "Vous devez être enregistré comme propriétaire..."
            # return context
            raise Http404("Vous devez être enregistré comme propriétaire pour accéder à cette page.")
        # Add the proprietaire object to the context
        context['proprietaire'] = proprietaire

        # Get all maisons owned by this proprietaire
        # Prefetch related objects for optimization
        maisons = Maison.objects.filter(proprietaire=proprietaire).prefetch_related(
            'chambres',
            'chambres__locations',
            'chambres__locations__utilisateur',
            'chambres__locations__paiements',
            'chambres__locations__fin_location', # Prefetch fin_location
            'chambres__type_chambre', # Also prefetch type_chambre if used often
        ).order_by('nom')

        # --- Data Aggregation (same logic as the FBV) ---
        maisons_details = []
        total_chambres_libres = 0
        total_chambres_occupees = 0
        grand_total_paiements = 0

        for maison in maisons:
            chambres_details = []
            maison_total_paiements = 0
            maison_chambres_libres = 0
            maison_chambres_occupees = 0

            # Use the prefetched chambres
            for chambre in maison.chambres.all():
                 # Find the *current* active location using the prefetched locations
                 # Check if a related 'fin_location' exists. The relationship name is 'fin_location'.
                 # We filter the prefetched list in Python or query again if needed.
                 # Simpler: Rely on chambre.etat and query active location if needed
                current_location = None
                total_paid_for_chambre = 0
                locataire_info = None

                if chambre.etat == 'libre':
                    maison_chambres_libres += 1
                elif chambre.etat == 'occupée':
                    maison_chambres_occupees += 1
                    # Find the active location (no FinLocation associated) among the prefetched ones
                    # This requires the OneToOne relationship 'fin_location' on Location model
                    # or checking the existence of the related FinLocation object.
                    try:
                       # Find location for this chambre that has no fin_location linked
                       active_locations = [loc for loc in chambre.locations.all() if not hasattr(loc, 'fin_location')]
                       if active_locations:
                            current_location = active_locations[0] # Assuming only one active location per room
                            # Sum payments specifically for this *current* location
                            payment_sum = current_location.paiements.aggregate(total=Sum('montant_paye'))
                            total_paid_for_chambre = payment_sum['total'] if payment_sum['total'] is not None else 0
                            locataire_info = current_location.utilisateur
                            maison_total_paiements += total_paid_for_chambre
                       else:
                           # Handle case where chambre is 'occupée' but no active location found (data inconsistency?)
                           # Log this or display a specific message
                           pass
                    except AttributeError:
                         # Handle case where fin_location relation doesn't exist or isn't prefetched correctly
                         # This might indicate a setup issue or a need to adjust prefetch/model relations
                         pass


                chambres_details.append({
                    'chambre': chambre,
                    'status': chambre.get_etat_display(),
                    'current_location': current_location,
                    'locataire': locataire_info,
                    'total_paid': total_paid_for_chambre,
                })

            maisons_details.append({
                'maison': maison,
                'chambres': chambres_details,
                'total_paiements': maison_total_paiements,
                'count_libres': maison_chambres_libres,
                'count_occupees': maison_chambres_occupees,
            })

            # Add to overall totals
            total_chambres_libres += maison_chambres_libres
            total_chambres_occupees += maison_chambres_occupees
            grand_total_paiements += maison_total_paiements

        # Add aggregated data to the context
        context['maisons_details'] = maisons_details
        context['total_chambres_libres'] = total_chambres_libres
        context['total_chambres_occupees'] = total_chambres_occupees
        context['grand_total_paiements'] = grand_total_paiements
        context['total_maisons'] = maisons.count()
        context['total_chambres'] = total_chambres_libres + total_chambres_occupees
        # Return the final context dictionary
        return context
    # def get_context_data(self, **kwargs):
    #     print(">>> Début du get_context_data")
    #     context = super().get_context_data(**kwargs)
    #     request = self.request
    #     print(">>> Utilisateur :", request.user)

    #     try:
    #         proprietaire = get_object_or_404(Proprietaire, utilisateur=request.user)
    #         print(">>> Propriétaire trouvé :", proprietaire)
    #     except Http404:
    #         print(">>> Propriétaire introuvable")
    #         raise Http404("Vous devez être enregistré comme propriétaire pour accéder à cette page.")

    #     # puis ajoute d'autres print dans la boucle maison, etc.
class ChambreDetailLocataireView(DetailView):
    model = Chambre  # Le modèle principal que cette vue va afficher
    template_name = 'accuiel/proprietaires/chambre_details.html'  # Le template à utiliser
    context_object_name = 'chambre'  # Nom de l'objet dans le template (par défaut: 'object')
    pk_url_kwarg = 'chambre_id'  # Nom du paramètre PK dans l'URL (si différent de 'pk')

    def get_context_data(self, **kwargs):
        # Appeler l'implémentation de base pour obtenir le contexte initial
        context = super().get_context_data(**kwargs)
        
        # self.object est l'instance de Chambre récupérée par DetailView
        chambre = self.object 

        # Récupérer toutes les locations pour cette chambre
        # On trie par date de début pour avoir un historique chronologique
        locations_chambre = Location.objects.filter(chambre=chambre).order_by('-date_debut_location').select_related('utilisateur')

        # Initialiser les totaux
        montant_total_recolte_global = 0
        commission_totale_globale = 0

        # Pour stocker les détails de chaque location avec ses paiements
        locations_details = []

        for loc in locations_chambre:
            # Montant initial de la location (avance)
            montant_location_initial = loc.montant_avance or 0
            commission_location_initiale = loc.commission or 0
            
            # Paiements de loyer associés à cette location
            paiements_loyer = PaiementLoyer.objects.filter(location=loc)
            
            montant_total_paiements_loyer = paiements_loyer.aggregate(total=Sum('montant_paye'))['total'] or 0
            commission_totale_paiements_loyer = paiements_loyer.aggregate(total=Sum('commission'))['total'] or 0
            
            # Totaux pour cette location spécifique
            montant_total_pour_cette_location = montant_location_initial + montant_total_paiements_loyer
            commission_totale_pour_cette_location = commission_location_initiale + commission_totale_paiements_loyer
            
            locations_details.append({
                'location': loc,
                'utilisateur': loc.utilisateur.username if loc.utilisateur else "N/A",
                'date_debut': loc.date_debut_location,
                'date_fin_avance': loc.date_fin_avance,
                'montant_avance': montant_location_initial,
                'commission_location': commission_location_initiale,
                'paiements_loyer': paiements_loyer, # Pour afficher les paiements individuels si besoin
                'total_loyers_payes_pour_location': montant_total_paiements_loyer,
                'total_commission_loyers_pour_location': commission_totale_paiements_loyer,
                'montant_total_genere_par_location': montant_total_pour_cette_location,
                'commission_totale_generee_par_location': commission_totale_pour_cette_location,
                'net_pour_location': montant_total_pour_cette_location - commission_totale_pour_cette_location
            })
            
            # Ajouter aux totaux globaux
            montant_total_recolte_global += montant_total_pour_cette_location
            commission_totale_globale += commission_totale_pour_cette_location

        net_a_payer_global = montant_total_recolte_global - commission_totale_globale

        # Ajouter les données calculées au contexte
        context['locations_details'] = locations_details
        context['montant_total_recolte_global'] = montant_total_recolte_global
        context['commission_totale_globale'] = commission_totale_globale
        context['net_a_payer_global'] = net_a_payer_global
        
        return context
    

class  ProprietaireDetaimaisonlView(DetailView):
    model = Proprietaire
    template_name = 'accuiel/proprietaires/proprietaireDetail_Maison.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proprietaire = self.object
        maisons = proprietaire.maisons.all().prefetch_related('chambres')

        stats = []
        total_paiements_global = 0
        total_commission_global = 0

        for maison in maisons:
            chambres = maison.chambres.all()
            chambres_libres = chambres.filter(etat="libre")
            chambres_occupees = chambres.filter(etat="occupée")
            chambres_stats = []

            for chambre in chambres:
                locations = chambre.locations.select_related('utilisateur').order_by('-date_debut_location')
                paiements = PaiementLoyer.objects.filter(location__chambre=chambre)
                total_paiements = paiements.aggregate(total=Sum('montant_paye'))['total'] or 0
                total_commission = paiements.aggregate(total=Sum('commission'))['total'] or 0
                total_paiements_global += total_paiements
                total_commission_global += total_commission

                # Historique détaillé des locations et paiements par location
                locations_details = []
                for loc in locations:
                    fin_location = getattr(loc, 'fin_location', None)
                    periode = {
                        "date_debut": loc.date_debut_location,
                        "date_fin": fin_location.date_fin_location if fin_location else None,
                        "en_cours": fin_location is None
                    }
                    # Paiements liés à cette location
                    paiements_loc = PaiementLoyer.objects.filter(location=loc)
                    paiements_list = [{
                        "montant": paiement.montant_paye,
                        "date": paiement.date_paiement,
                        "mode": paiement.mode_paiement,
                        "statut": paiement.statut_paiement
                    } for paiement in paiements_loc]

                    locations_details.append({
                        "utilisateur": loc.utilisateur,
                        "montant_avance": loc.montant_avance,
                        "montant_caution": loc.montant_caution,
                        "taux_commission": loc.chambre.taux_commission,
                        "periode": periode,
                        "statut_paiement": loc.statut_paiement,
                        "mode_paiement": loc.mode_paiement,
                        "montant_total": loc.montant_total,
                        "paiements": paiements_list
                    })

                # Ajout de l'historique d'état de la chambre (si tu veux ajouter un vrai log, il faudrait un modèle/tracking d'événements, ici on utilise juste locations)
                etapes = []
                for loc in locations.reverse():  # plus ancien -> plus récent
                    fin_location = getattr(loc, 'fin_location', None)
                    etat = "occupée" if loc else "libre"
                    date_liberation = fin_location.date_fin_location if fin_location else None
                    etapes.append({
                        "etat": etat,
                        "occupant": loc.utilisateur,
                        "date_debut": loc.date_debut_location,
                        "date_liberation": date_liberation
                    })

                chambres_stats.append({
                    'chambre': chambre,
                    'etat': chambre.etat,
                    'surface': chambre.surface,
                    'prix': chambre.prix,
                    'taux_commission': chambre.taux_commission,
                    'locations_details': locations_details,
                    'total_paiements': total_paiements,
                    'commission': total_commission,
                    'etapes': etapes
                })

            stats.append({
                'maison': maison,
                'chambres_libres': chambres_libres.count(),
                'chambres_occupees': chambres_occupees.count(),
                'chambres_stats': chambres_stats,
            })

        context['stats'] = stats
        context['total_paiements_global'] = total_paiements_global
        context['total_commission_global'] = total_commission_global
        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     proprietaire = self.get_object()

    #     # Relations (basées sur related_name)
    #     context['maisons_count'] = proprietaire.maisons.count()
    #     context['chambres_count'] = proprietaire.chambres.count() if hasattr(proprietaire, 'chambres') else 0

    #     # Méthodes statistiques (vérifiées pour éviter erreurs)
    #     context['total_commissions_attendues'] = proprietaire.total_commissions_attendues() if hasattr(proprietaire, 'total_commissions_attendues') else 0
    #     context['total_commissions_perçues'] = proprietaire.total_commissions_perçues() if hasattr(proprietaire, 'total_commissions_perçues') else 0
    #     context['total_loyers_attendus'] = proprietaire.total_loyers_attendus() if hasattr(proprietaire, 'total_loyers_attendus') else 0
    #     context['loyers_mensuels_moyens'] = proprietaire.loyers_mensuels_moyens() if hasattr(proprietaire, 'loyers_mensuels_moyens') else 0
    #     context['chambres_libres_count'] = proprietaire.chambres_libres_count() if hasattr(proprietaire, 'chambres_libres_count') else 0
    #     context['chambres_occupees_count'] = proprietaire.chambres_occupees_count() if hasattr(proprietaire, 'chambres_occupees_count') else 0
    #     context['taux_occupation'] = proprietaire.taux_occupation() if hasattr(proprietaire, 'taux_occupation') else 0
    #     context['derniers_paiements_loyer'] = proprietaire.derniers_paiements_loyer() if hasattr(proprietaire, 'derniers_paiements_loyer') else []
    #     context['total_montant_avance_locations'] = proprietaire.total_montant_avance_locations() if hasattr(proprietaire, 'total_montant_avance_locations') else 0
    #     context['total_montant_caution_locations'] = proprietaire.total_montant_caution_locations() if hasattr(proprietaire, 'total_montant_caution_locations') else 0
    #     context['locations_en_cours_count'] = proprietaire.locations_en_cours_count() if hasattr(proprietaire, 'locations_en_cours_count') else 0
    #     context['locations_terminees_count'] = proprietaire.locations_terminees_count() if hasattr(proprietaire, 'locations_terminees_count') else 0
    #     context['revenus_totaux'] = proprietaire.revenus_totaux() if hasattr(proprietaire, 'revenus_totaux') else 0

    #     return context


class ProprietaireListmaisonView(ListView):
    model = Proprietaire
    template_name = 'accuiel/proprietaires/proprietaire_list_maison.html' # Créez ce template
    context_object_name = 'proprietaires' # Nom de la variable dans le template pour la liste des propriétaires

    # Vous pouvez surcharger get_queryset pour optimiser les requêtes si nécessaire
    # par exemple, précharger les maisons pour éviter des requêtes supplémentaires
    # def get_queryset(self):
    #     return Proprietaire.objects.prefetch_related('maisons')   
    # 
# yourapp/views.py (remplacez 'yourapp' par le nom de votre application)



class ProprietaireDashboardView(LoginRequiredMixin, DetailView): # Hérite de DetailView
    """
    Vue basée sur les classes pour afficher le tableau de bord d'un propriétaire.
    Utilise les propriétés définies sur le modèle Proprietaire pour afficher
    les informations agrégées.
    """
    model = Proprietaire  # Spécifie le modèle à utiliser
    template_name = 'accuiel/proprietaires/proprietaire_dashboard.html'  # Chemin vers votre template
    context_object_name = 'proprietaire'  # Nom de la variable dans le template (par défaut 'object' ou 'proprietaire')

    # Optionnel : Si vous voulez restreindre qui peut voir quel dashboard
    # (par exemple, un admin voit tout, un propriétaire voit seulement le sien)
    # vous pouvez surcharger get_queryset ou get_object
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff: # ou user.type_utilisateur.nom == 'admin'
    #         return Proprietaire.objects.all()
    #     elif hasattr(user, 'proprietaire_profile'): # Si vous liez CustomUser à Proprietaire
    #          # Adaptez cette logique à comment vous liez CustomUser et Proprietaire
    #         # Peut-être que Proprietaire a un champ user = OneToOneField(CustomUser) ?
    #         # Ou l'inverse ? Ici on suppose un lien non montré dans le code initial.
    #         # Si le Proprietaire EST le CustomUser (pas un modèle séparé)
    #         # if user.type_utilisateur and user.type_utilisateur.nom == 'propriétaire':
    #         #    proprietaire_instance = ... # get related Proprietaire based on user
    #         #    return Proprietaire.objects.filter(pk=proprietaire_instance.pk)
    #          pass # Ajoutez votre logique de filtrage ici si nécessaire
    #     return Proprietaire.objects.none() # Ne rien montrer par défaut si pas autorisé

    # Si vous avez besoin d'ajouter des données *supplémentaires* au contexte
    # (qui ne sont PAS des propriétés du modèle Proprietaire), vous pouvez utiliser get_context_data
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # 'proprietaire' est déjà dans le contexte grâce à DetailView
    #     # Ajoutez d'autres éléments si nécessaire :
    #     # context['autre_info'] = AutreModele.objects.filter(...)
    #     return context  
# ##################################################################### Maison #####################################################################

class MaisonListView(ListView):
    model = Maison
    template_name = 'maisons/liste.html'
    context_object_name = 'maisons'

class MaisonCreateView(CreateView):
    model = Maison
    form_class = MaisonForm
    template_name = 'maisons/creer.html'
    success_url = reverse_lazy('maison_liste')

class MaisonUpdateView(UpdateView):
    model = Maison
    form_class = MaisonForm
    template_name = 'maisons/modifier.html'
    success_url = reverse_lazy('maison_liste')

class MaisonDeleteView(DeleteView):
    model = Maison
    template_name = 'maisons/supprimer.html'
    success_url = reverse_lazy('maison_liste')


class MaisonDetailView(DetailView):
    model = Maison
    template_name = 'maisons/detail.html'  # Chemin vers votre template
    context_object_name = 'maison'  # Nom de l'objet dans le contexte
# ##################################################################### type chambre  #####################################################################

class TypeChambreCreateView(CreateView):
    model = TypeChambre
    form_class = TypeChambreForm
    template_name = 'accuiel/type_chambre/ajouter.html'
    success_url = reverse_lazy('liste_typechambres')
    

class TypeChambreUpdateView(UpdateView):
    model = TypeChambre
    form_class = TypeChambreForm
    template_name = 'accuiel/type_chambre/ajouter.html'
    success_url = reverse_lazy('liste_typechambres')

class TypeChambreListView(ListView):
    model = TypeChambre
    template_name = 'accuiel/type_chambre/typechambre_form.html'
    context_object_name = 'liste_typechambres'
    context_object_name = 'types'

class TypeChambreDeleteView(DeleteView):
    model = TypeChambre
    template_name = 'accuiel/type_chambre/typechambre_confirm_delete.html'
    success_url = reverse_lazy('liste_typechambres')

# ##################################################################### chambres #####################################################################
class ChambreCreateView(CreateView):
    model = Chambre
    form_class = ChambreForm
    template_name = 'accuiel/chambre/ajouter.html'
    success_url = reverse_lazy('liste_chambres')
    def get_initial(self):
        initial = super().get_initial()
        maison_id = self.request.GET.get('maison_id')  # Récupère l'ID de la maison depuis l'URL
        if maison_id:
            try:
                maison = Maison.objects.get(id=maison_id)
                initial['maison'] = maison
            except Maison.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maison_id = self.request.GET.get('maison_id')
        if maison_id:
            try:
                maison = Maison.objects.get(id=maison_id)
                context['maison'] = maison
                context['nombre_total_pieces'] = maison.nombre_piece
                context['pieces_enregistrees'] = maison.chambres.count()
                context['pieces_non_enregistrees'] = maison.nombre_piece - maison.chambres.count()
            except Maison.DoesNotExist:
                context['maison'] = None
        return context
    def get_type_chambre(request, id):
        try:
            tc = TypeChambre.objects.get(pk=id)
            return JsonResponse({'piece': tc.piece})
        except TypeChambre.DoesNotExist:
            return JsonResponse({'error': 'Type non trouvé'}, status=404)
class ChambreUpdateView(UpdateView):
    model = Chambre
    form_class = ChambreForm
    template_name = 'accuiel/chambre/ajouter.html'
    success_url = reverse_lazy('liste_chambres')

class ChambreListView(ListView):
    model = Chambre
    template_name = 'accuiel/chambre/list.html'
    context_object_name = 'chambres'
    def get_queryset(self):
        maison_id = self.request.GET.get('maison_id')  # Récupérer l'ID de la maison sélectionnée
        if maison_id:
            return Chambre.objects.filter(maison_id=maison_id)
        return Chambre.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maisons'] = Maison.objects.all()  # Ajouter toutes les maisons au contexte
        context['maison_id'] = self.request.GET.get('maison_id', '')  # Conserver la sélection
        return context

class ChambreDeleteView(DeleteView):
    model = Chambre
    template_name = 'accuiel/chambre/supprimer.html'
    success_url = reverse_lazy('liste_chambres')

class ChambreDetailView(DetailView):
    model = Chambre
    template_name = 'accuiel/chambre/chambre_detail.html'
    context_object_name = 'liste_chambres'
    context_object_name = 'chambre'


# ##################################################################### locataires #####################################################################
class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'accuiel/locations/location_form.html'

    def form_valid(self, form):
        # Récupération des IDs de l'utilisateur et de la chambre
        utilisateur_id = self.kwargs.get('utilisateur_id')
        chambre_id = self.kwargs.get('chambre_id')
        # Obtention de l'utilisateur et de la chambre
        utilisateur = get_object_or_404(CustomUser, id=utilisateur_id)
        chambre = get_object_or_404(Chambre, id=chambre_id)
        # Associer les objets au formulaire
        form.instance.utilisateur = utilisateur
        form.instance.chambre = chambre
        # Enregistrement de la location
        response = super().form_valid(form)  # noqa: F841
        # Redirection vers la génération de PDF après le succès
        # return redirect('generate_pdf', location_id=self.object.id)
        return redirect('download_and_redirect', location_id=self.object.id)
    def get_context_data(self, **kwargs):
        # Mettre en contexte les informations de l'utilisateur et de la chambre
        context = super().get_context_data(**kwargs)
        utilisateur_id = self.kwargs.get('utilisateur_id')
        chambre_id = self.kwargs.get('chambre_id')
        context['utilisateur'] = get_object_or_404(CustomUser, id=utilisateur_id)
        context['chambre'] = get_object_or_404(Chambre, id=chambre_id)
        return context

    def get_success_url(self):
        # En utilisant reverse avec un pattern d'URL dynamique pour générer le PDF
        return reverse('generate_pdf', kwargs={'location_id': self.object.id})

    # model = Location
    # form_class = LocationForm
    # template_name = 'accuiel/locations/location_form.html'

    # def form_valid(self, form):
    #     utilisateur_id = self.kwargs.get('utilisateur_id')
    #     chambre_id = self.kwargs.get('chambre_id')

    #     utilisateur = get_object_or_404(CustomUser, id=utilisateur_id)
    #     chambre = get_object_or_404(Chambre, id=chambre_id)

    #     form.instance.utilisateur = utilisateur
    #     form.instance.chambre = chambre

    #     response = super().form_valid(form)  # noqa: F841

    #     # Génération du PDF
    #     template = get_template('recu/recu_location.html')
    #     context = {'location': self.object}
    #     html = template.render(context)

    #     Recu_pdf = BytesIO()
    #     pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=Recu_pdf)

    #     if not pisa_status.err:
    #         Recu_pdf.seek(0)
    #         pdf_content = Recu_pdf.getvalue()
    #         self.object.Recu_pdf.save(f'location_{self.object.id}.pdf', ContentFile(pdf_content))
    #         Recu_pdf.close()

    #     return redirect('liste_locations')


# class LocationCreateView(CreateView):
#     model = Location
#     form_class = LocationForm
#     template_name = 'accuiel/locations/location_form.html'
#     success_url = reverse_lazy('liste_locations')

#     def form_valid(self, form):
#         """
#         Associe l'utilisateur et la chambre à la location avant de valider le formulaire.
#         """
#         utilisateur_id = self.kwargs.get('utilisateur_id')
#         chambre_id = self.kwargs.get('chambre_id')

#         # Récupérer l'utilisateur et la chambre
#         utilisateur = get_object_or_404(CustomUser, id=utilisateur_id)
#         chambre = get_object_or_404(Chambre, id=chambre_id)

#         # Associer l'utilisateur et la chambre à la location
#         form.instance.utilisateur = utilisateur
#         form.instance.chambre = chambre

#         # Appeler la méthode parent pour valider le formulaire
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         """
#         Ajoute les informations de l'utilisateur et de la chambre au contexte.
#         """
#         context = super().get_context_data(**kwargs)
#         utilisateur_id = self.kwargs.get('utilisateur_id')
#         chambre_id = self.kwargs.get('chambre_id')

#         # Ajouter l'utilisateur et la chambre au contexte
#         context['utilisateur'] = get_object_or_404(CustomUser, id=utilisateur_id)
#         context['chambre'] = get_object_or_404(Chambre, id=chambre_id)
#         return context

#     def get_success_url(self):
#         """
#         Redirige vers la liste des locations après la création.
#         """
#         return reverse('liste_locations')

#     def generate_pdf(self, location):
#         """
#         Génère un fichier PDF pour la confirmation de réservation.
#         """
#         try:
#             # Configuration de la réponse HTTP pour un fichier PDF
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="reservation_{location.id}.pdf"'

#             # Création du PDF avec ReportLab
#             p = canvas.Canvas(response, pagesize=A4)
#             width, height = A4

#             # En-tête
#             p.setFont("Helvetica-Bold", 16)
#             p.drawString(100, height - 50, "Confirmation de réservation")

#             # Informations de la réservation
#             p.setFont("Helvetica", 12)
#             y = height - 100
#             p.drawString(100, y, f"Utilisateur : {location.utilisateur.nom} ({location.utilisateur.email})")
#             y -= 20
#             p.drawString(100, y, f"Chambre N° : {location.chambre.numero}")
#             y -= 20
#             p.drawString(100, y, f"Date de réservation : {location.date_debut} → {location.date_fin}")

#             # Finaliser le PDF
#             p.showPage()
#             p.save()

#             return response
#         except Exception as e:
#             print(f"Erreur lors de la génération du PDF : {e}")
#             return HttpResponse("Une erreur est survenue lors de la génération du PDF.", status=500)

# class LocationCreateView(CreateView):
#     model = Location
#     form_class = LocationForm
#     template_name = 'accuiel/locations/location_form.html'
#     success_url = reverse_lazy('liste_locations')

#     def form_valid(self, form):
#         # Récupérer l'utilisateur et la chambre depuis les paramètres de l'URL
#         utilisateur_id = self.kwargs.get('utilisateur_id')
#         chambre_id = self.kwargs.get('chambre_id')
#         utilisateur = get_object_or_404(CustomUser, id=utilisateur_id)
#         chambre = get_object_or_404(Chambre, id=chambre_id)

#         # Associer l'utilisateur et la chambre à la location
#         form.instance.utilisateur = utilisateur
#         form.instance.chambre = chambre

#         # Appeler la méthode parent pour sauvegarder la location
#         response = super().form_valid(form)

#         # Envoyer un email à l'utilisateur
#         self.envoyer_email(utilisateur, chambre, form.instance)

#         return response

#     def envoyer_email(self, utilisateur, chambre, location):
#         """
#         Envoie un email à l'utilisateur pour confirmer la création de la location,
#         avec l'image du contrat en pièce jointe.
#         """
#         sujet = "Confirmation de votre location"
#         message = f"""
#         Bonjour {utilisateur.nom} {utilisateur.prenom},

#         Votre location pour la chambre "{chambre.type_chambre.nom}" a été créée avec succès.
#         Voici les détails de votre location :
#         - Chambre : {chambre.type_chambre.nom}
#         - Prix : {chambre.prix} CFA
#         - Surface : {chambre.surface} m²
#         - Taux de commission : {chambre.taux_commission}%
#         - Date de début : {location.date_debut_location}
#         - Date de fin : {location.date_fin_avance}
#         - Montant d'avance : {location.montant_avance} CFA
#         - Montant de caution : {location.montant_caution} CFA
#         - Commission : {location.commission} CFA
#         - Montant total : {location.montant_total} CFA
#         - Statut de paiement : {location.statut_paiement}
#         - Mode de paiement : {location.mode_paiement}
#         - Date de paiement : {location.date_paiement}

#         Merci de nous faire confiance.

#         Cordialement,
#         L'équipe de gestion des locations
#         """

#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [utilisateur.email]

#         # Créer un email avec pièce jointe
#         email = EmailMessage(sujet, message, email_from, recipient_list)  # noqa: F821

#         # Ajouter l'image du contrat si elle existe
#         if location.image_contrat:  # Vérifiez que l'image du contrat existe
#             email.attach_file(location.image_contrat.path)

#         # Envoyer l'email
#         email.send()

#     def get_context_data(self, **kwargs):
#         # Ajouter les informations de l'utilisateur et de la chambre au contexte
#         context = super().get_context_data(**kwargs)
#         utilisateur_id = self.kwargs.get('utilisateur_id')
#         chambre_id = self.kwargs.get('chambre_id')
#         context['utilisateur'] = get_object_or_404(CustomUser, id=utilisateur_id)
#         context['chambre'] = get_object_or_404(Chambre, id=chambre_id)
#         return context

#     def get_success_url(self):
#         # Rediriger après la création de la location
#         return reverse('liste_locations')
class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'accuiel/locations/location_form.html'
    success_url = reverse_lazy('liste_locations')

class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'accuiel/locations/location_list.html'
    context_object_name = 'locations'
    paginate_by = 10

    def get_queryset(self):
        """
        Retourne la liste des locations filtrées et triées
        """
        queryset = Location.objects.select_related(
            'utilisateur', 
            'chambre'
        ).order_by('-date_debut_location')

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(utilisateur__nom__icontains=search) |
                Q(utilisateur__prenom__icontains=search) |
                Q(chambre__numero__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ajout de la date courante au Togo
        context['current_date_togo'] = datetime.now(pytz.timezone('Africa/Lome'))
        
        # Statistiques des locations
        locations = Location.objects.all()
        context.update({
            'total_locations': locations.count(),
            'locations_payees': locations.filter(
                statut_paiement='payé'
            ).count(),
            'avance_payee': locations.filter(
                statut_paiement='avance payée, pas caution'
            ).count(),
        })

        # Gestion de la pagination
        page = self.request.GET.get('page', 1)
        try:
            page = int(page)
        except ValueError:
            page = 1

        paginator = context['paginator']
        try:
            locations = paginator.page(page)
        except:  # noqa: E722
            locations = paginator.page(1)

        # Calcul de la plage de pages à afficher
        start_index = max(1, page - 2)
        end_index = min(paginator.num_pages, page + 2)
        page_range = range(start_index, end_index + 1)

        context.update({
            'page_range': page_range,
            'locations': locations,
            'is_paginated': paginator.num_pages > 1,
            'search': self.request.GET.get('search', ''),
        })

        return context
class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'accuiel/locations/location_confirm_delete.html'
    success_url = reverse_lazy('liste_locations')


class LocataireDashboardView(TemplateView):
    template_name = 'accuiel/locataire/locataire_dashboard.html'
    def get_context_data(self, **kwargs):
        locataire_id = self.kwargs.get('locataire_id')
        locataire = CustomUser.objects.get(id=locataire_id)
        # Transactions liées au locataire
        locations = Location.objects.filter(utilisateur=locataire)
        paiements_par_chambre = {}
        for location in locations:
            # Récupérer les paiements pour chaque location
            paiements_par_chambre[location] = PaiementLoyer.objects.filter(location=location)
        # Fin des locations
        fins_locations = FinLocation.objects.filter(location__utilisateur=locataire)
        # Calcul du montant total dû, payé et restant
        montant_total = 0
        montant_paye = 0
        for location in locations:
            montant_total += location.montant_total
            montant_paye += PaiementLoyer.objects.filter(location=location).aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0

        montant_restant = montant_total - montant_paye
# Obtenir la date/heure actuelle au Togo
        togo_timezone = pytz.timezone('Africa/Lome')
        current_time_togo = datetime.now(togo_timezone)

        # Envoi des contextes au template
        context = super().get_context_data(**kwargs)
        context['locataire'] = locataire
        context['locations'] = locations
        context['paiements_par_chambre'] = paiements_par_chambre
        context['fins_locations'] = fins_locations
        context['montant_total'] = montant_total
        context['montant_paye'] = montant_paye
        context['montant_restant'] = montant_restant
        context['current_time_togo'] = current_time_togo  # Ajout de l'heure actuelle au Togo

        # context['montant_restant'] = montant_restant
        return context

# ##################################################################### location #####################################################################

# class LocationListView(ListView):
#     model = Location
#     template_name = 'accuiel/locations/location_list.html'
#     context_object_name = 'locations'

# class LocationDetailView(DetailView):
#     model = Location
#     template_name = 'accuiel/locations/location_detail.html'
#     context_object_name = 'location'

# class LocationCreateView(CreateView):
#     model = Location
#     form_class = LocationForm
#     template_name = 'accuiel/locations/location_form.html'
#     success_url = reverse_lazy('location_list')

# class LocationUpdateView(UpdateView):
#     model = Location
#     form_class = LocationForm
#     template_name = 'accuiel/locations/location_form.html'
#     success_url = reverse_lazy('location_list')

# class LocationDeleteView(DeleteView):
#     model = Location
#     template_name = 'accuiel/locations/location_confirm_delete.html'
#     success_url = reverse_lazy('location_list')

# ##################################################################### paiement #####################################################################

class PaiementLoyerCreateView(LoginRequiredMixin, CreateView):
    model = PaiementLoyer
    form_class = PaiementLoyerForm
    template_name = 'accuiel/paiements/paiement_form.html'
    success_url = reverse_lazy("liste_paiements")

    def get_location_object(self):
        """Helper method to retrieve the Location object."""
        location_id = self.kwargs.get('location_id')
        if not location_id:
            messages.error(self.request, "Aucune location spécifiée.")
            return None
        try:
            if not hasattr(self, '_location_obj'):
                self._location_obj = get_object_or_404(Location, id=location_id)
            return self._location_obj
        except Location.DoesNotExist:
            messages.error(self.request, "La location spécifiée n'existe pas.")
            return None

    def get_form_kwargs(self):
        """Passes additional arguments to the form initialization."""
        kwargs = super().get_form_kwargs()
        location = self.get_location_object()
        if location:
            kwargs['location'] = location
        return kwargs

    def get_context_data(self, **kwargs):
        """Adds the location to the context for display in the template."""
        context = super().get_context_data(**kwargs)
        location = self.get_location_object()
        if location:
            context['location'] = location
            context['montant_mensuel'] = location.montant_total
            context['date_fin_avance_iso'] = location.date_fin_avance.isoformat() if location.date_fin_avance else None
        return context

    def form_valid(self, form):
        """Called if the form is valid. Handles saving and redirection."""
        try:
            self.object = form.save()  # Save the form and handle logic in the form's save method
            messages.success(
                self.request,
                f"Paiement #{self.object.id} pour {self.object.location} enregistré avec succès. "
                f"Un reçu a été envoyé à {self.object.location.utilisateur.email}."
            )
            return redirect(self.get_success_url())
        except Exception as e:
            error_message = f"Une erreur est survenue lors de l'enregistrement ou de l'envoi du reçu : {e}"
            print(f"ERROR in form_valid PaiementLoyerCreateView: {error_message}")
            messages.error(self.request, error_message)
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handles invalid form submissions."""
        messages.error(self.request, "Le formulaire contient des erreurs. Veuillez vérifier les champs.")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        """Check if the location exists before displaying the form."""
        location = self.get_location_object()
        if not location:
            return redirect(reverse_lazy('liste_locations'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Redirect to the PDF generation view after successful form submission."""
        return reverse('generate_pdfpayement', kwargs={'paiementloyer_id': self.object.id})


class PaiementLoyer2CreateView(LoginRequiredMixin, CreateView):
    model = PaiementLoyer
    form_class = PaiementLoyerForm
    template_name = 'accuiel/paiements/paiement_form2.html'
    success_url = reverse_lazy("liste_paiements")
    def dispatch(self, request, *args, **kwargs):
        """Vérifie que la location existe avant toute autre action."""
        self.location = self.get_location_object()
        if not self.location:
            messages.error(request, "Aucune location spécifiée.")
            return redirect(reverse_lazy('liste_locations'))
        return super().dispatch(request, *args, **kwargs)

    def get_location_object(self):
        """Récupère l'objet Location depuis les paramètres de l'URL."""
        location_id = self.kwargs.get('location_id')
        return get_object_or_404(Location, id=location_id) if location_id else None

    def get_form_kwargs(self):
        """Ajoute la location au formulaire."""
        kwargs = super().get_form_kwargs()
        kwargs['location'] = self.location
        return kwargs

    def get_context_data(self, **kwargs):
        """Ajoute des infos supplémentaires au contexte du template."""
        context = super().get_context_data(**kwargs)
        context['location'] = self.location
        context['montant_mensuel'] = self.location.montant_total
        context['date_fin_avance_iso'] = self.location.date_fin_avance.isoformat() if self.location.date_fin_avance else None

        # ✅ CORRECTION : utiliser self.location, pas Location
        dernier_paiement = PaiementLoyer.objects.filter(location=self.location).order_by('-date_paiement').first()

        context['dernier_paiement'] = dernier_paiement
        context['date_fin_paiement'] = dernier_paiement.date_fin_paiement if dernier_paiement else None

        return context

    def form_valid(self, form):
        """Sauvegarde du formulaire si valide + redirection vers PDF."""
        try:
            self.object = form.save()
            messages.success(
                self.request,
                f"Paiement #{self.object.id} enregistré avec succès. "
                f"Un reçu a été envoyé à {self.object.location.utilisateur.email}."
            )
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Une erreur est survenue : {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Affiche les erreurs si le formulaire est invalide."""
        messages.error(self.request, "Le formulaire contient des erreurs.")
        return super().form_invalid(form)

    def get_success_url(self):
        """Redirige vers la génération de reçu PDF après paiement."""
        return reverse('generate_pdfpayement', kwargs={'paiementloyer_id': self.object.id})

# Fichier : authentifications\authentication\views.py

from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.forms import ValidationError # Important pour les erreurs de validation
# Importez vos modèles Location et FinLocation
# from .models import FinLocation, Location, Chambre # Exemple, adaptez

class FinLocationCreateView(CreateView):
    model = FinLocation
    form_class = FinLocationForm
    template_name = 'accuiel/Finlocation/fin_location_form.html'
    # get_initial pour définir la valeur initiale du champ du formulaire
    def get_initial(self):
        initial = super().get_initial()
        # Assurez-vous que self.location est déjà défini par dispatch()
        if hasattr(self, 'location') and self.location:
            initial['montant_remboursement_caution'] = self.location.montant_caution
        return initial

    def dispatch(self, request, *args, **kwargs):
        # 'location_id' doit correspondre au nom dans votre urls.py
        self.location = get_object_or_404(Location, pk=self.kwargs['location_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # 1. Appelle la méthode parent pour sauvegarder l'instance FinLocation.
        #    À ce stade, l'instance (self.object) est créée dans la DB,
        #    mais la relation ManyToMany 'location' n'est PAS encore établie.
        response = super().form_valid(form)

        # 2. Établit la relation ManyToMany pour l'objet FinLocation nouvellement créé (self.object).
        #    Nous associons la 'Location' obtenue de l'URL (`self.location`).
        #    `.set()` attend un itérable (une liste), donc [self.location].
        if self.location: # Vérifie que self.location existe bien
            self.object.location.set([self.location])

        # --- Toutes les logiques dépendant des relations ManyToMany doivent venir APRES le .set() ---

        # 3. Calcule la somme des cautions des locations associées.
        #    self.object.location.all() est maintenant peuplé.
        total_caution_calculee = sum(loc.montant_caution for loc in self.object.location.all())

        # 4. Effectue la validation du remboursement de la caution.
        #    Si la validation échoue, ajoute une erreur au formulaire et retourne form_invalid.
        if form.instance.montant_remboursement_caution > total_caution_calculee:
            form.add_error(
                'montant_remboursement_caution',
                "Le remboursement de la caution ne peut pas dépasser la somme des cautions ({}).".format(total_caution_calculee)
            )
            # Important : Si l'erreur est ajoutée, nous devons retourner form_invalid
            return self.form_invalid(form) # Ceci réaffichera le formulaire avec l'erreur

        # 5. Libère les chambres associées aux locations.
        #    Note: Assurez-vous que votre modèle Location a bien un champ 'chambre' (ForeignKey vers Chambre).
        for loc_obj in self.object.location.all():
            if hasattr(loc_obj, 'chambre') and loc_obj.chambre: # Vérifie si 'chambre' existe et n'est pas None
                loc_obj.chambre.etat = 'libre' # Assurez-vous que 'etat' est un champ valide sur Chambre
                loc_obj.chambre.save()

        # Si vous aviez d'autres champs à mettre à jour sur `self.object` après ces calculs,
        # vous les mettriez ici, puis appelleriez `self.object.save()` à nouveau.
        # Par exemple:
        # self.object.champ_calcule = une_valeur_calculee
        # self.object.save(update_fields=['champ_calcule']) # Utilisez update_fields pour plus d'efficacité

        # Retourne la réponse HTTP de redirection obtenue initialement.
        return response

    def form_invalid(self, form):
        # Override form_invalid pour s'assurer que le contexte est bien passé
        # lorsque le formulaire est réaffiché après une erreur.
        # Cela est crucial si vous utilisez self.location dans votre template.
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # S'assurer que 'location' et 'montant_caution' sont toujours disponibles dans le contexte
        # pour le template, même en cas d'erreur de formulaire.
        context['location'] = self.location
        if hasattr(self.location, 'montant_caution'):
            context['montant_caution'] = self.location.montant_caution
        else:
            context['montant_caution'] = 0 # Valeur par défaut si montant_caution n'existe pas
        return context

    def get_success_url(self):
        # Assurez-vous que 'liste_paiements' existe et prend un argument 'location_id'
        return reverse('liste_paiements', args=[self.location.id])
# class FinLocationCreateView(CreateView):
#     model = FinLocation
#     form_class = FinLocationForm
#     template_name = 'accuiel/Finlocation/fin_location_form.html'
#     def get_initial(self):
#         initial = super().get_initial()
#         initial['montant_remboursement_caution'] = self.location.montant_caution
#         return initial

#     def dispatch(self, request, *args, **kwargs):
#         self.location = get_object_or_404(Location, pk=self.kwargs['location_id'])
#         return super().dispatch(request, *args, **kwargs)

#     # def form_valid(self, form):
#     #     form.instance.location = self.location  # Associer la fin à la location
#     #     return super().form_valid(form)
#     # C:\Users\hugues\Music\Projet text\authentifications\authentication\views.py

# # ... à l'intérieur de votre classe de vue ...
# def form_valid(self, form):
#     # 1. Laisser la méthode parente sauvegarder le formulaire. Cela crée l'objet
#     #    dans la base de données et retourne la réponse de redirection HTTP.
#     #    L'objet sauvegardé est stocké dans `self.object`.
#     response = super().form_valid(form)

#     # 2. Maintenant que `self.object` (qui est identique à `form.instance` après sauvegarde)
#     #    a une clé primaire, nous pouvons gérer sa relation ManyToMany.
#     #    La méthode .set() attend un itérable (comme une liste ou un queryset).
#     #    En supposant que `self.location` est un seul objet Location, nous l'enveloppons dans une liste.
#     self.object.location.set([self.location])

#     # 3. Retourner la réponse de redirection que nous avons obtenue de la méthode parente.
#     return response
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['location'] = self.location  # Passer au template
#         context['montant_caution'] = self.location.montant_caution
#         return context

#     def get_success_url(self):
#         return reverse('liste_paiements', args=[self.location.id])  
class FinLocationUpdateView(UpdateView):
    model = FinLocation
    form_class = FinLocationForm
    template_name = 'fin_location_form.html'
    success_url = reverse_lazy('fin_location_list')

    def get_object(self, queryset=None):
        return get_object_or_404(FinLocation, pk=self.kwargs['pk'])



# class FinLocationListView(ListView):
#     model = Location
#     template_name = 'accuiel/Finlocation/list_utilisateur.html'
#     context_object_name = 'locations_occupees'

#     def get_queryset(self):
#         """
#         Retourne les locations où la chambre associée est marquée 'occupée'.
#         Précharge les données liées pour l'efficacité.
#         """
#         queryset = Location.objects.filter(
#             chambre__etat='occupée', # Filtre basé sur l'état de la chambre liée
#             chambre__isnull=False # S'assure qu'une chambre est liée
#         ).select_related(
#             'chambre',                  # Jointure chambre
#             'chambre__type_chambre',    # Jointure type_chambre via chambre
#             'chambre__maison',          # Jointure maison via chambre
#             'chambre__maison__proprietaire', # Jointure proprietaire via maison
#             'utilisateur'             # Jointure utilisateur (locataire)
#         ).order_by('-date_debut_location') # Ordonne par date de début la plus récente

#         return queryset

#     def get_context_data(self, **kwargs):
#         """
#         Ajoute les statistiques calculées au contexte.
#         """
#         context = super().get_context_data(**kwargs)
#         queryset = self.get_queryset() # Récupère le queryset filtré

#         # --- Calcul des statistiques avec les agrégations Django ---
#         # C'est plus efficace que de boucler en Python si le volume de données est grand
#         stats_data = queryset.aggregate(
#             total_rooms=Count('chambre', distinct=True), # Compte les chambres uniques occupées
#             total_rent=Sum('chambre__prix'),          # Somme des prix des chambres liées
#             average_rent=Avg('chambre__prix'),        # Moyenne des prix
#             total_surface=Sum('chambre__surface'),    # Somme des surfaces
#             average_surface=Avg('chambre__surface')   # Moyenne des surfaces
#         )

#         # S'assurer que les valeurs sont présentes et ont un type correct
#         context['stats'] = {
#             'total_occupied_rooms': stats_data.get('total_rooms') or 0,
#             'total_monthly_rent': stats_data.get('total_rent') or Decimal('0.00'),
#             'average_monthly_rent': stats_data.get('average_rent') or Decimal('0.00'),
#             'total_occupied_surface': stats_data.get('total_surface') or 0.0,
#             'average_occupied_surface': stats_data.get('average_surface') or 0.0,
#         }

#         context['titre_page'] = "Liste des Chambres Occupées et Statistiques"
#         return context

class  FinLocationListView(ListView):
    model = Location
    template_name = 'accuiel/Finlocation/list_utilisateur.html'
    context_object_name = 'locations_occupees'

    def get_queryset(self):
        chambre_id = self.kwargs.get("chambre_id")  # Filtrer par ID si précisé

        queryset = Location.objects.filter(
            chambre__etat='occupée',
            chambre__isnull=False
        )

        if chambre_id:
            queryset = queryset.filter(chambre__id=chambre_id)

        queryset = queryset.select_related(
            'chambre',
            'chambre__type_chambre',
            'chambre__maison',
            'chambre__maison__proprietaire',
            'utilisateur'
        ).order_by('-date_debut_location')  # Pour avoir la plus récente en premier

        # ✅ Supprimer les doublons : garder la location la plus récente pour chaque chambre
        unique_locations = {}
        for location in queryset:
            chambre_id = location.chambre.id
            if chambre_id not in unique_locations:
                unique_locations[chambre_id] = location

        return list(unique_locations.values())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        stats_data = {
            'total_rooms': len(queryset),
            'total_rent': sum(loc.chambre.prix for loc in queryset),
            'average_rent': sum(loc.chambre.prix for loc in queryset) / len(queryset) if queryset else 0,
            # 'total_surface': ...  --> supprimé
            # 'average_surface': ...  --> supprimé
        }

        context['stats'] = {
            'total_occupied_rooms': stats_data['total_rooms'],
            'total_monthly_rent': Decimal(stats_data['total_rent']),
            'average_monthly_rent': Decimal(stats_data['average_rent']),
            # 'total_occupied_surface': ...  --> supprimé
            # 'average_occupied_surface': ...  --> supprimé
        }

        context['titre_page'] = "Liste des Chambres Occupées et Statistiques"
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     queryset = self.get_queryset()

    #     stats_data = {
    #         'total_rooms': len(queryset),
    #         'total_rent': sum(loc.chambre.prix for loc in queryset),
    #         'average_rent': sum(loc.chambre.prix for loc in queryset) / len(queryset) if queryset else 0,
    #         'total_surface': sum(loc.chambre.surface for loc in queryset),
    #         'average_surface': sum(loc.chambre.surface for loc in queryset) / len(queryset) if queryset else 0
    #     }

    #     context['stats'] = {
    #         'total_occupied_rooms': stats_data['total_rooms'],
    #         'total_monthly_rent': Decimal(stats_data['total_rent']),
    #         'average_monthly_rent': Decimal(stats_data['average_rent']),
    #         'total_occupied_surface': stats_data['total_surface'],
    #         'average_occupied_surface': stats_data['average_surface'],
    #     }

    #     context['titre_page'] = "Liste des Chambres Occupées et Statistiques"
    #     return context

class ListePaiementsLocationView(LoginRequiredMixin, ListView): # Ajout de LoginRequiredMixin (optionnel)
    model = PaiementLoyer
    template_name = 'accuiel/Finlocation/listePaiement.html'
    context_object_name = 'paiements'
    paginate_by = 10

    def get_queryset(self):
        location_id = self.kwargs.get('location_id')
        get_object_or_404(Location, pk=location_id)
        return PaiementLoyer.objects.filter(location_id=location_id).order_by('-date_paiement')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_id = self.kwargs.get('location_id')
        location = get_object_or_404(
            Location.objects.select_related(
                'utilisateur', 'chambre', 'chambre__maison', 'chambre__type_chambre'
            ),
            pk=location_id
        )
        paiements_qs = PaiementLoyer.objects.filter(location=location)
        # Statistiques 
        context['total_paid_amount'] = paiements_qs.aggregate(total=Sum('montant_paye'))['total'] or Decimal('0.0')
        context['statut_paiements'] = {
            'confirmé': paiements_qs.filter(statut_paiement='confirmé').aggregate(s=Sum('montant_paye'))['s'] or Decimal('0.0'),
            'en_attente': paiements_qs.filter(statut_paiement='en attente').aggregate(s=Sum('montant_paye'))['s'] or Decimal('0.0'),
            'rejeté': paiements_qs.filter(statut_paiement='rejeté').aggregate(s=Sum('montant_paye'))['s'] or Decimal('0.0'),
        }
        context['location'] = location
        return context








    # model = PaiementLoyer
    # form_class = PaiementLoyerForm
    # template_name = 'accuiel/paiements/paiement_form2.html'

    # def dispatch(self, request, *args, **kwargs):
    #     """Vérifie que la location existe avant toute autre action."""
    #     self.location = self.get_location_object()
    #     if not self.location:
    #         return redirect(reverse_lazy('liste_locations'))
    #     return super().dispatch(request, *args, **kwargs)

    # def get_location_object(self):
    #     """Récupère l'objet Location à partir des paramètres de l'URL."""
    #     location_id = self.kwargs.get('location_id')
    #     if not location_id:
    #         messages.error(self.request, "Aucune location spécifiée.")
    #         return None
    #     return get_object_or_404(Location, id=location_id)

    # def get_form_kwargs(self):
    #     """Passe l'objet location au formulaire."""
    #     kwargs = super().get_form_kwargs()
    #     kwargs['location'] = self.location
    #     return kwargs

    # def get_context_data(self, **kwargs):
    #     """Ajoute des données utiles au contexte."""
    #     context = super().get_context_data(**kwargs)
    #     context['location'] = self.location
    #     context['montant_mensuel'] = self.location.montant_total
    #     context['date_fin_avance_iso'] = self.location.date_fin_avance.isoformat() if self.location.date_fin_avance else None

    #     # Ajouter le dernier paiement existant s'il y en a
    #     dernier_paiement = PaiementLoyer.objects.filter(location=self.location).order_by('-date_paiement').first()
    #     if dernier_paiement:
    #         context['dernier_paiement'] = dernier_paiement
    #         context['date_fin_paiement'] = dernier_paiement.date_fin
    #     else:
    #         context['date_fin_paiement'] = None

    
    #     return context

    # def form_valid(self, form):
    #     """Si le formulaire est valide, on sauvegarde et redirige."""
    #     try:
    #         self.object = form.save()  # toute la logique métier est déjà dans le save du formulaire
    #         messages.success(
    #             self.request,
    #             f"Paiement #{self.object.id} enregistré avec succès. "
    #             f"Un reçu a été envoyé à {self.object.location.utilisateur.email}."
    #         )
    #         return redirect(self.get_success_url())
    #     except Exception as e:
    #         error_message = f"Une erreur est survenue : {e}"
    #         print(f"[ERREUR PaiementLoyerCreateView] {error_message}")
    #         messages.error(self.request, error_message)
    #         return self.form_invalid(form)

    # def form_invalid(self, form):
    #     """Affiche les erreurs du formulaire."""
    #     messages.error(self.request, "Le formulaire contient des erreurs.")
    #     return super().form_invalid(form)

    # def get_success_url(self):
    #     """Redirige vers la vue de génération du PDF."""
    #     return reverse('generate_pdfpayement', kwargs={'paiementloyer_id': self.object.id})





























    # model = PaiementLoyer
    # form_class = PaiementLoyerForm
    # template_name = 'accuiel/paiements/paiement_form2.html'
    # success_url = reverse_lazy("liste_paiements")

    # def get_paiement_object(self):
    #     """Récupère l'objet Location depuis l'URL (paiement_id)."""
    #     paiement_id = self.kwargs.get('paiement_id')
    #     if not paiement_id:
    #         messages.error(self.request, "Aucune location spécifiée.")
    #         return None
    #     try:
    #         if not hasattr(self, '_location_obj'):
    #             self._location_obj = get_object_or_404(Location, id=paiement_id)
    #         return self._location_obj
    #     except Location.DoesNotExist:
    #         messages.error(self.request, "La location spécifiée n'existe pas.")
    #         return None

    # def get_form_kwargs(self):
    #     """Ajoute l'objet Location dans les kwargs du formulaire."""
    #     kwargs = super().get_form_kwargs()
    #     paiement = self.get_paiement_object()
    #     if paiement:
    #         kwargs['location'] = paiement  # Doit être géré dans le constructeur du form
    #     return kwargs

    # def get_context_data(self, **kwargs):
    #     """Ajoute des données supplémentaires au contexte du template."""
    #     context = super().get_context_data(**kwargs)
    #     paiement = self.get_paiement_object()
    #     if paiement:
    #         context['paiement'] = paiement
    #         context['montant_mensuel'] = paiement.montant_total
    #         context['date_fin_avance_iso'] = paiement.date_fin_avance.isoformat() if paiement.date_fin_avance else None
    #     return context

    # def form_valid(self, form):
    #     """Traitement du formulaire valide : enregistrement + message."""
    #     try:
    #         self.object = form.save()
    #         messages.success(
    #             self.request,
    #             f"Paiement #{self.object.id} pour {self.object.location} enregistré avec succès. "
    #             f"Un reçu a été envoyé à {self.object.location.utilisateur.email}."
    #         )
    #         return redirect(self.get_success_url())
    #     except Exception as e:
    #         error_message = f"Erreur lors de l'enregistrement ou l'envoi du reçu : {e}"
    #         print(f"ERROR in form_valid PaiementLoyer2CreateView: {error_message}")
    #         messages.error(self.request, error_message)
    #         return self.form_invalid(form)

    # def form_invalid(self, form):
    #     """Gère les soumissions de formulaire invalides."""
    #     messages.error(self.request, "Le formulaire contient des erreurs. Veuillez vérifier les champs.")
    #     return super().form_invalid(form)

    # def dispatch(self, request, *args, **kwargs):
    #     """Vérifie l'existence de la Location avant de continuer."""
    #     if not self.get_location_object():
    #         return redirect(reverse_lazy('liste_locations'))
    #     return super().dispatch(request, *args, **kwargs)

    # def get_success_url(self):
    #     """Redirige vers la génération du PDF après le paiement."""
    #     return reverse('generate_pdfpayement', kwargs={'paiementloyer_id': self.object.id})




class PaiementLoyerUpdateView(UpdateView):
    model = PaiementLoyer
    form_class = PaiementLoyerForm
    template_name = 'paiement_loyer_form.html'
    success_url = reverse_lazy('liste_paiements')

class GeneratePDFView(DetailView):
    model = PaiementLoyer
    
    def get(self, request, *args, **kwargs):
        paiement = self.get_object()
        buffer = BytesIO()  # noqa: F821
        
        # Création du PDF
        p = canvas.Canvas(buffer, pagesize=A4)  # noqa: F821
        width, height = A4
        
        # En-tête
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, height-50, "REÇU DE PAIEMENT")
        
        # Informations du paiement
        p.setFont("Helvetica", 12)
        y = height - 100
        
        infos = [
            f"N° Reçu : {paiement.id}",
            f"Date : {paiement.date_paiement.strftime('%d/%m/%Y %H:%M')}",
            f"Locataire : {paiement.location.utilisateur.nom}",
            f"Chambre : {paiement.location.chambre.numero}",
            f"Période : {paiement.location.date_fin_avance.strftime('%d/%m/%Y')} au {paiement.date_fin_paiement.strftime('%d/%m/%Y')}",
            f"Montant : {paiement.montant_paye:,} CFA",
            f"Mode de paiement : {paiement.get_mode_paiement_display()}",
            f"Statut : {paiement.get_statut_paiement_display()}"
        ]

        for info in infos:
            p.drawString(50, y, info)
            y -= 25

        # Signatures
        y = 100
        p.line(50, y, 250, y)
        p.drawString(50, y-20, "Signature gestionnaire")
        
        p.line(300, y, 500, y)
        p.drawString(300, y-20, "Signature locataire")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return FileResponse(  # noqa: F821
            buffer, 
            as_attachment=True,
            filename=f'recu_paiement_{paiement.id}.pdf'
        )

# class PaiementLoyerListView(ListView):
#     model = PaiementLoyer
#     template_name = 'accuiel/paiements/paiement_list.html'
#     context_object_name = 'paiements'
#     paginate_by = 15

#     def get_context_data(self, **kwargs):
#         """
#         Ajoute les paiements regroupés par chambre et les informations de location au contexte.
#         """
#         context = super().get_context_data(**kwargs)
#         paiements_par_chambre = []
#         current_date_togo = datetime.now(pytz.timezone('Africa/Lome'))

#         # Parcourir toutes les chambres pour regrouper paiements et locations
#         chambres = Chambre.objects.all()
#         for chambre in chambres:
#             paiements = PaiementLoyer.objects.filter(location__chambre=chambre).order_by('-date_paiement')
#             location = Location.objects.filter(chambre=chambre).first()  # Récupérer la première location associée

#             if paiements.exists():
#                 dernier_paiement = paiements.first()
#                 date_debut = dernier_paiement.date_paiement
#                 date_fin = dernier_paiement.date_fin_paiement
#             elif location:
#                 date_debut = location.date_debut_location  # Utilisation de date_debut_location
#                 date_fin = location.date_fin_avance       # Utilisation de date_fin_avance
#             else:
#                 date_debut = None
#                 date_fin = None

#             paiements_par_chambre.append({
#                 'chambre': chambre,
#                 'paiements': paiements,
#                 'location': location,
#                 'date_debut': date_debut,
#                 'date_fin': date_fin
#             })

#         # Ajouter les données au contexte
#         context['paiements_par_chambre'] = paiements_par_chambre
#         context['current_date_togo'] = current_date_togo
#         context['total_paiements'] = PaiementLoyer.objects.count()
#         context['paiements_confirmes'] = PaiementLoyer.objects.filter(statut_paiement="confirmé").count()
#         context['paiements_en_attente'] = PaiementLoyer.objects.filter(statut_paiement="en attente").count()

        # return context


# class PaiementLoyerListView(ListView):
#     model = PaiementLoyer
#     template_name = 'accuiel/paiements/paiement_list.html'
#     context_object_name = 'paiements'
#     paginate_by = 15

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paiements_par_location = []
#         current_date_togo = datetime.now(pytz.timezone('Africa/Lome'))

#         locations = Location.objects.select_related('chambre', 'utilisateur')

#         for location in locations:
#             dernier_paiement = location.paiements.order_by('-date_paiement').first()
#             if dernier_paiement:
#                 date_fin = dernier_paiement.date_fin_paiement
#                 date_expiree = date_fin < current_date_togo.date() if date_fin else False

#                 paiements_par_location.append({
#                     'location': location,
#                     'chambre': location.chambre,
#                     'locataire': location.utilisateur,
#                     'dernier_paiement': dernier_paiement,
#                     'date_fin': date_fin,
#                     'date_expiree': date_expiree
#                 })

#         # Trier les paiements par date_fin croissante
#         paiements_par_location.sort(key=lambda x: x['date_fin'] or current_date_togo.date())

#         context.update({
#             'paiements_par_location': paiements_par_location,
#             'current_date_togo': current_date_togo,
#             'total_paiements': PaiementLoyer.objects.count(),
#             'paiements_confirmes': PaiementLoyer.objects.filter(statut_paiement="confirmé").count(),
#             'paiements_en_attente': PaiementLoyer.objects.filter(statut_paiement="en attente").count(),
#         })

#         return context
# class PaiementLoyerListView(TemplateView):
#     template_name = 'accuiel/paiements/paiement_list.html'
#     paginate_by = 15
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         current_date_togo = datetime.now(pytz.timezone('Africa/Lome'))
#         paiements_par_location = []
#         locations = Location.objects.select_related('chambre', 'utilisateur')
#         for location in locations:
#             if location.chambre.etat == 'libre':
#                 continue  # On ignore les chambres libres

#             dernier_paiement = location.paiements.order_by('-date_paiement').first()
#             if dernier_paiement:
#                 date_fin = dernier_paiement.date_fin_paiement
#                 date_expiree = date_fin < current_date_togo.date() if date_fin else False
#                 paiements_par_location.append({
#                     'location': location,
#                     'chambre': location.chambre,
#                     'locataire': location.utilisateur,
#                     'dernier_paiement': dernier_paiement,
#                     'date_fin': date_fin,
#                     'date_expiree': date_expiree
#                 })
#         # Trier par date_fin (du plus petit au plus grand)
#         paiements_par_location.sort(key=lambda x: x['date_fin'] or current_date_togo.date())
#         # Pagination manuelle
#         paginator = Paginator(paiements_par_location, self.paginate_by)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         context.update({
#             'paiements_par_location': page_obj,
#             'page_obj': page_obj,
#             'is_paginated': page_obj.has_other_pages(),
#             'current_date_togo': current_date_togo,
#             'total_paiements': PaiementLoyer.objects.count(),
#             'paiements_confirmes': sum(1 for p in paiements_par_location if not p['date_expiree']),
#             'paiements_en_attente': PaiementLoyer.objects.filter(statut_paiement="en attente").count(),
#             'paiements_expires': sum(1 for p in paiements_par_location if p['date_expiree']),
#         })
#         return context




# class PaiementLoyerListView(TemplateView):
#     template_name = 'accuiel/paiements/paiement_list.html'
#     paginate_by = 15

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         current_date_togo = datetime.now(pytz.timezone('Africa/Lome'))
#         chambre_id = self.kwargs.get('chambre_id', None)

#         paiements_par_location = []
#         chambres_deja_vues = set()  # 👈 Pour éviter les doublons

#         if chambre_id:
#             locations = Location.objects.filter(chambre__id=chambre_id).select_related('chambre', 'utilisateur')
#         else:
#             locations = Location.objects.select_related('chambre', 'utilisateur')

#         for location in locations:
#             chambre = location.chambre

#             # 💡 Ignore les chambres déjà vues ou les chambres libres
#             if chambre.id in chambres_deja_vues or chambre.etat == 'libre':
#                 continue

#             dernier_paiement = location.paiements.order_by('-date_paiement').first()
#             if dernier_paiement:
#                 date_fin = dernier_paiement.date_fin_paiement
#                 date_expiree = date_fin < current_date_togo.date() if date_fin else False
#                 paiements_par_location.append({
#                     'location': location,
#                     'chambre': chambre,
#                     'locataire': location.utilisateur,
#                     'dernier_paiement': dernier_paiement,
#                     'date_fin': date_fin,
#                     'date_expiree': date_expiree
#                 })
#                 chambres_deja_vues.add(chambre.id)  # ✅ Marquer la chambre comme vue

#         # Trier par date de fin de paiement
#         paiements_par_location.sort(key=lambda x: x['date_fin'] or current_date_togo.date())

#         # Pagination uniquement si on affiche tout
#         if not chambre_id:
#             paginator = Paginator(paiements_par_location, self.paginate_by)
#             page_number = self.request.GET.get('page')
#             page_obj = paginator.get_page(page_number)
#         else:
#             page_obj = paiements_par_location

#         context.update({
#             'paiements_par_location': page_obj,
#             'is_paginated': not chambre_id and hasattr(page_obj, 'has_other_pages') and page_obj.has_other_pages(),
#             'current_date_togo': current_date_togo,
#             'total_paiements': PaiementLoyer.objects.count(),
#             'paiements_confirmes': sum(1 for p in paiements_par_location if not p['date_expiree']),
#             'paiements_en_attente': PaiementLoyer.objects.filter(statut_paiement="en attente").count(),
#             'paiements_expires': sum(1 for p in paiements_par_location if p['date_expiree']),
#             'chambre_affichee': chambre_id,
#         })
#         return context

# ----- IMPORTS CORRECTS -----

# Pour la gestion du temps avec Django (contient .now())
from django.utils import timezone

# Pour les fuseaux horaires spécifiques comme 'Africa/Lome'
import pytz

# Si vous avez besoin de `date` du module datetime, gardez-le
from datetime import date
class PaiementLoyerListView(ListView):
    model = PaiementLoyer
    template_name = 'accuiel/paiements/paiement_list.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date_togo = timezone.now().astimezone(pytz.timezone('Africa/Lome'))
        chambre_id = self.kwargs.get('chambre_id', None)

        paiements_par_location = []

        # <<< LA CORRECTION CLÉ EST ICI >>>
        # On filtre pour ne garder que les locations qui n'ont AUCUNE FinLocation associée.
        # Cela signifie que ce sont les locations ACTIVES.
        base_locations = Location.objects.filter(
            fins_location__isnull=True
        ).select_related('chambre', 'utilisateur')

        if chambre_id:
            # Si on cherche une chambre spécifique, on filtre sur cette base
            locations = base_locations.filter(chambre__id=chambre_id)
        else:
            locations = base_locations.all()

        # Comme on ne récupère que les locations actives, on n'a plus besoin
        # de `chambres_deja_vues`. Chaque chambre n'apparaîtra qu'une seule fois.
        for location in locations:
            # On ne traite que les chambres qui sont réellement occupées
            if location.chambre.etat == 'libre':
                continue
            dernier_paiement = location.paiements.order_by('-date_paiement').first()
            if dernier_paiement:
                date_fin = dernier_paiement.date_fin_paiement
                # Comparaison correcte entre une date et un objet date
                date_expiree = date_fin < current_date_togo.date() if date_fin else False
                paiements_par_location.append({
                    'location': location,
                    'chambre': location.chambre,
                    'locataire': location.utilisateur,
                    'dernier_paiement': dernier_paiement,
                    'date_fin': date_fin,
                    'date_expiree': date_expiree
                })
            # Optionnel : que faire si une location active n'a encore aucun paiement ?
            # Vous pourriez vouloir l'afficher aussi avec un statut spécial.
            # else:
            #     paiements_par_location.append({ ... 'dernier_paiement': None, ... })


        # Trier par date de fin de paiement
        paiements_par_location.sort(key=lambda x: x['date_fin'] or current_date_togo.date())

        # Pagination (votre logique était déjà bonne)
        if not chambre_id:
            paginator = Paginator(paiements_par_location, self.paginate_by)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = paiements_par_location

        # Les statistiques peuvent maintenant utiliser la liste filtrée
        context.update({
            'paiements_par_location': page_obj,
            'is_paginated': not chambre_id and hasattr(page_obj, 'has_other_pages') and page_obj.has_other_pages(),
            'current_date_togo': current_date_togo,
            'total_paiements': PaiementLoyer.objects.count(), # Total historique
            'paiements_confirmes': sum(1 for p in paiements_par_location if not p['date_expiree']),
            'paiements_en_attente': PaiementLoyer.objects.filter(statut_paiement="en attente").count(), # Historique
            'paiements_expires': sum(1 for p in paiements_par_location if p['date_expiree']),
            'chambre_affichee': chambre_id,
        })
        return context



class PaiementLoyerDeleteView(DeleteView):
    model = PaiementLoyer
    template_name = 'paiement_loyer_confirm_delete.html'
    success_url = reverse_lazy('liste_paiements')


















class UtilisateurListView(ListView):
    model = CustomUser  # noqa: F821
    template_name = 'accuiel/locataire/locataire_list.html'  # Chemin vers le template
    context_object_name = 'utilisateurs'  # Nom de la variable utilisée dans le template
    
    def get_queryset(self):
        """
        Combine le filtrage par type 'locataire' et la recherche par nom/prénom.
        """
        query = self.request.GET.get('q')  # Récupérer la requête de recherche
        queryset = CustomUser.objects.filter(type_utilisateur__nom='locataire')  # Filtrer par type 'locataire'
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) | Q(prenom__icontains=query)  # Recherche par nom ou prénom  # noqa: F821
            )
        return queryset

    def get_context_data(self, **kwargs):
        """
        Ajoute des informations supplémentaires au contexte, comme la chambre associée.
        """
        context = super().get_context_data(**kwargs)
        chambre_id = self.kwargs.get('chambre_id')  # Récupérer l'ID de la chambre depuis l'URL
        if chambre_id:
            context['chambre'] = get_object_or_404(Chambre, id=chambre_id)
        return context
    # def get_queryset(self):
    #     # Filtrer uniquement les utilisateurs ayant un type "locataire"
    #     return CustomUser.objects.filter(type_utilisateur__nom='locataire')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Récupérer la chambre à partir de l'ID passé dans l'URL
    #     chambre_id = self.kwargs.get('chambre_id')
    #     context['chambre'] = get_object_or_404(Chambre, id=chambre_id)
    #     return context


class UtilisateurList_PeyementView(ListView):
    model = CustomUser
    template_name = 'accuiel/paiements/list_utilisateur.html'
    context_object_name = 'utilisateurs'

    def get_queryset(self):
        """
        Retourne uniquement les locataires qui ont des locations sans paiement
        """
        return CustomUser.objects.filter(
            type_utilisateur__nom='locataire',
            locations__isnull=False
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer le queryset filtré
        queryset = self.get_queryset()
        
        # Préparer les détails des locataires
        locataires_details = []
        for utilisateur in queryset:
            # Récupérer uniquement les locations sans paiement
            locations_sans_paiement = []
            
            for location in Location.objects.filter(utilisateur=utilisateur):
                # Vérifier si la location n'a pas de paiement
                if not PaiementLoyer.objects.filter(location=location).exists():
                    locations_sans_paiement.append({
                        'location': location,
                        'chambre': location.chambre,
                        'montant_total': location.montant_total,
                        'date_debut': location.date_debut_location,
                        'date_fin_avance': location.date_fin_avance
                    })
            
            # N'ajouter le locataire que s'il a des locations sans paiement
            if locations_sans_paiement:
                locataires_details.append({
                    'utilisateur': utilisateur,
                    'locations': locations_sans_paiement,
                    'nombre_locations_sans_paiement': len(locations_sans_paiement)
                })

        # Statistiques et contexte
        total_locataires = CustomUser.objects.filter(
            type_utilisateur__nom='locataire'
        ).count()
        
        locataires_avec_paiement = CustomUser.objects.filter(
            type_utilisateur__nom='locataire',
            locations__paiements__isnull=False
        ).distinct().count()

        context.update({
            'locataires_details': locataires_details,
            'total_locataires': total_locataires,
            'locataires_avec_paiement': locataires_avec_paiement,
            'locataires_sans_paiement': len(locataires_details),
            'search_query': self.request.GET.get('q', '')
        })

        # Gestion de la recherche
        query = self.request.GET.get('q')
        if query:
            filtered_details = [
                detail for detail in locataires_details
                if query.lower() in detail['utilisateur'].nom.lower() or 
                   query.lower() in detail['utilisateur'].prenom.lower() or 
                   query.lower() in detail['utilisateur'].email.lower()
            ]
            context['locataires_details'] = filtered_details
            context['search_results_count'] = len(filtered_details)

        return context
    

############################################################################ PDF pour la locatiion ########################################################################
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

class PDFTemplateViewLocation(View):
    """
    Vue pour générer et servir directement un PDF de contrat de location avec WeasyPrint.
    """
    def get(self, request, location_id, *args, **kwargs):
        try:
            location = get_object_or_404(Location, id=location_id)
            context = {'location': location}
            html_string = render_to_string('recu/recu_Location.html', context) # Assurez-vous que le chemin est correct
            base_url = request.build_absolute_uri('/')
            pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            # LA LIGNE CLÉ À CHANGER : 'attachment' au lieu de 'inline'
            filename = f"contrat_location_{location.id}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            print(f"Erreur lors de la génération du PDF pour location {location_id}: {e}")
            return HttpResponse(f"Erreur lors de la génération du PDF: {e}", status=500)
        
    # def get(self, request, location_id):
    #     location = get_object_or_404(Location, id=location_id)
    #     template = get_template('recu/recu_Location.html')
    #     context = {'location': location}
    #     html = template.render(context)

    #     pdf_file = io.BytesIO()
    #     pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('UTF-8')), dest=pdf_file)

    #     if pisa_status.err:
    #         return HttpResponse('Erreur lors de la génération du PDF')

    #     # Stocker en session
    #     request.session['pdf_data'] = pdf_file.getvalue().decode('latin1')  # nécessaire pour session

    #     # Rediriger vers la vue qui sert le fichier
    #     return redirect('serve_pdf_and_redirect') 
    

class Download_RedirectView(View):
    """
    Cette vue sert une page HTML qui déclenche le téléchargement du PDF 
    puis redirige l'utilisateur vers la page d'accueil.
    """
    def get(self, request, location_id, *args, **kwargs):
        # On prépare les URLs dont le JavaScript aura besoin
        context = {
            'pdf_url': reverse('generate_pdf', args=[location_id]),
            'home_url': reverse('liste_locations')  # Assurez-vous d'avoir une URL nommée 'accueil'
        }
        return render(request, 'messageDeSucce/succe_Location.html', context)
# c'est pour la location     
class ServePDFAndRedirectViewLocation(View):
    def get(self, request):
        pdf_data = request.session.get('pdf_data')

        if not pdf_data:
            return HttpResponse("Aucun PDF trouvé en session.", status=404)

        # Encodage en base64 pour téléchargement via le navigateur
        pdf_base64 = base64.b64encode(pdf_data.encode('latin1')).decode('utf-8')

        # Générer l'URL de redirection (ex: 'liste_locations')
        redirect_url = reverse('liste_locations')

        # Page HTML temporaire avec téléchargement + redirection
        html = f"""
        <html>
        <head>
            <title>Téléchargement...</title>
            <script>
                function downloadAndRedirect() {{
                    const link = document.createElement('a');
                    link.href = 'data:application/pdf;base64,{pdf_base64}';
                    link.download = 'recu_location.pdf';
                    document.body.appendChild(link);
                    link.click();
                    link.remove();

                    // Redirection après 2 secondes
                    setTimeout(() => {{
                        window.location.href = '{redirect_url}';
                    }}, 2000);
                }}

                window.onload = downloadAndRedirect;
            </script>
        </head>
        <body>
            <p>Téléchargement du reçu en cours... Vous allez être redirigé.</p>
        </body>
        </html>
        """

        return HttpResponse(html)

#################################################### pdf pour le payement ###################################
class PDFTemplateViewpaiyement(View):
    def get(self, request, location_id):
        PaiementLoyer = get_object_or_404(Location, id=PaiementLoyer)  # noqa: F823
        template = get_template('Recu/Recu_peyement.html')
        context = {'paiement': PaiementLoyer}
        html = template.render(context)

        pdf_file = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('UTF-8')), dest=pdf_file)

        if pisa_status.err:
            return HttpResponse('Erreur lors de la génération du PDF')

        # Stocker en session
        request.session['pdf_data'] = pdf_file.getvalue().decode('latin1')  # nécessaire pour session

        # Rediriger vers la vue qui sert le fichier
        return redirect('serve_pdf_and_redirect') 
    
class ServePDFAndRedirectViewpaiyement(View):
    def get(self, request):
        pdf_data = request.session.get('pdf_data')

        if not pdf_data:
            return HttpResponse("Aucun PDF trouvé en session.", status=404)

        # Encodage en base64 pour téléchargement via le navigateur
        pdf_base64 = base64.b64encode(pdf_data.encode('latin1')).decode('utf-8')

        # Générer l'URL de redirection (ex: 'liste_locations')
        redirect_url = reverse('liste_paiement')

        # Page HTML temporaire avec téléchargement + redirection
        html = f"""
        <html>
        <head>
            <title>Téléchargement...</title>
            <script>
                function downloadAndRedirect() {{
                    const link = document.createElement('a');
                    link.href = 'data:application/pdf;base64,{pdf_base64}';
                    link.download = 'recu_location.pdf';
                    document.body.appendChild(link);
                    link.click();
                    link.remove();

                    // Redirection après 2 secondes
                    setTimeout(() => {{
                        window.location.href = '{redirect_url}';
                    }}, 2000);
                }}

                window.onload = downloadAndRedirect;
            </script>
        </head>
        <body>
            <p>Téléchargement du reçu en cours...</p>
        </body>
        </html>
        """

        return HttpResponse(html)
