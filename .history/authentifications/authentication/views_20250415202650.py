# from django.http import HttpResponseForbidden
# from django.shortcuts import render
# from email.message import EmailMessage
# from django.conf import settings
import base64
from io import BytesIO
from pyexpat.errors import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import  generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .forms import  ChambreForm, CustomUserCreationForm, CustomAuthenticationForm, LocationForm, MaisonForm, PaiementLoyerForm, ProprietaireForm, TypeChambreForm, VilleForm, VilleSearchForm,QuartierForm
from .models import Chambre, CustomUser, Location, Maison, PaiementLoyer, Proprietaire, TypeChambre, Ville, Quartier
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.contrib import messages  # noqa: F811
from datetime import  datetime
import pytz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.core.paginator import Paginator

# from django.core.files.base import ContentFile

from django.http import FileResponse, HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
import io
from datetime import date



# from django.http import HttpResponse
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

class ProprietaireCreateView(CreateView):
    model = Proprietaire
    form_class = ProprietaireForm  # noqa: F821
    template_name = 'accuiel/proprietaires/ajouter_Proprietaire.html'
    success_url = reverse_lazy('liste_proprietaire')

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
        return redirect('generate_pdf', location_id=self.object.id)

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

# class LocationListView(ListView):
#     model = Location
#     template_name = "accuiel/locations/location_list.html"  # Chemin vers votre template
#     context_object_name = "locations"  # Nom de la variable utilisée dans le template
#     paginate_by = 10  # Nombre de locations par page (facultatif)

#     def get_queryset(self):
#         """
#         Personnalisez la requête pour filtrer ou trier les données si nécessaire.
#         """
#         return Location.objects.all().order_by('-date_debut_location')  # Trier par date de début décroissante
class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'accuiel/locations/location_confirm_delete.html'
    success_url = reverse_lazy('liste_locations')
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
    template_name = 'accuiel/paiements/paiement_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Vérifie que la location existe avant toute autre action."""
        self.location = self.get_location_object()
        if not self.location:
            return redirect(reverse_lazy('liste_locations'))
        return super().dispatch(request, *args, **kwargs)

    def get_location_object(self):
        """Récupère l'objet Location à partir des paramètres de l'URL."""
        location_id = self.kwargs.get('location_id')
        if not location_id:
            messages.error(self.request, "Aucune location spécifiée.")
            return None
        return get_object_or_404(Location, id=location_id)

    def get_form_kwargs(self):
        """Passe l'objet location au formulaire."""
        kwargs = super().get_form_kwargs()
        kwargs['location'] = self.location
        return kwargs

    def get_context_data(self, **kwargs):
        """Ajoute des données utiles au contexte."""
        context = super().get_context_data(**kwargs)
        context['location'] = self.location
        context['montant_mensuel'] = self.location.montant_total
        context['date_fin_avance_iso'] = self.location.date_fin_avance.isoformat() if self.location.date_fin_avance else None
        return context

    def form_valid(self, form):
        """Si le formulaire est valide, on sauvegarde et redirige."""
        try:
            self.object = form.save()  # toute la logique métier est déjà dans le save du formulaire
            messages.success(
                self.request,
                f"Paiement #{self.object.id} enregistré avec succès. "
                f"Un reçu a été envoyé à {self.object.location.utilisateur.email}."
            )
            return redirect(self.get_success_url())
        except Exception as e:
            error_message = f"Une erreur est survenue : {e}"
            print(f"[ERREUR PaiementLoyerCreateView] {error_message}")
            messages.error(self.request, error_message)
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Affiche les erreurs du formulaire."""
        messages.error(self.request, "Le formulaire contient des erreurs.")
        return super().form_invalid(form)

    def get_success_url(self):
        """Redirige vers la vue de génération du PDF."""
        return reverse('generate_pdfpayement', kwargs={'paiementloyer_id': self.object.id})





























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
class PaiementLoyerListView(TemplateView):
    template_name = 'accuiel/paiements/paiement_list.html'
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_date_togo = datetime.now(pytz.timezone('Africa/Lome'))
        paiements_par_location = []

        locations = Location.objects.select_related('chambre', 'utilisateur')

        for location in locations:
            dernier_paiement = location.paiements.order_by('-date_paiement').first()

            if dernier_paiement:
                date_fin = dernier_paiement.date_fin_paiement
                date_expiree = date_fin < current_date_togo.date() if date_fin else False

                paiements_par_location.append({
                    'location': location,
                    'chambre': location.chambre,
                    'locataire': location.utilisateur,
                    'dernier_paiement': dernier_paiement,
                    'date_fin': date_fin,
                    'date_expiree': date_expiree
                })

        # Trier par date_fin (du plus petit au plus grand)
        paiements_par_location.sort(key=lambda x: x['date_fin'] or current_date_togo.date())

        # Pagination manuelle
        paginator = Paginator(paiements_par_location, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'paiements_par_location': page_obj,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'current_date_togo': current_date_togo,
            'total_paiements': PaiementLoyer.objects.count(),
            'paiements_confirmes': sum(1 for p in paiements_par_location if not p['date_expiree']),
            'paiements_en_attente': PaiementLoyer.objects.filter(statut_paiement="en attente").count(),
            'paiements_expires': sum(1 for p in paiements_par_location if p['date_expiree']),

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
class PDFTemplateViewLocation(View):
    def get(self, request, location_id):
        location = get_object_or_404(Location, id=location_id)
        template = get_template('recu/recu_Location.html')
        context = {'location': location}
        html = template.render(context)

        pdf_file = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('UTF-8')), dest=pdf_file)

        if pisa_status.err:
            return HttpResponse('Erreur lors de la génération du PDF')

        # Stocker en session
        request.session['pdf_data'] = pdf_file.getvalue().decode('latin1')  # nécessaire pour session

        # Rediriger vers la vue qui sert le fichier
        return redirect('serve_pdf_and_redirect') 
    
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


class PDFTemplateViewpaiyement(View):
    def get(self, request, location_id):
        PaiementLoyer = get_object_or_404(Location, id=PaiementLoyer)  # noqa: F823
        template = get_template('recu/recu_peyement.html')
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
