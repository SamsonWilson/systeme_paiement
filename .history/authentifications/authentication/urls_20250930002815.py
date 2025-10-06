from django.urls import path
from .views import  ChambreCreateView, ChambreDeleteView, ChambreDetailLocataireView, ChambreDetailView, ChambreListView, ChambreUpdateView, ChatView, ConversationDetailView, ConversationListView, CustomLoginView, DashboarProprietairedView, Download_RedirectView, FinLocationCreateView, FinLocationListView, FinLocationUpdateView, GeneratePDFView, GroupMessagesListView, ListePaiementsLocationView, LocataireDashboardView, LocationCreateView, LocationDeleteView, LocationListView, LocationUpdateView, MaisonCreateView, MaisonDeleteView, MaisonDetailView, MaisonListView, MaisonUpdateView, MessageCreateView, MessageListView, PDFTemplateViewLocation, PDFTemplateViewpaiyement, PaiementLoyer2CreateView, PaiementLoyerCreateView, PaiementLoyerDeleteView, PaiementLoyerListView, PaiementLoyerUpdateView, ProprietaireCreateView, ProprietaireDashboardView, ProprietaireDeleteView, ProprietaireDetailView, ProprietaireDetaimaisonlView, ProprietaireListView, ProprietaireListmaisonView, ProprietaireUpdateView, RedirectionParTypeUtilisateurView, ServePDFAndRedirectViewLocation, ServePDFAndRedirectViewpaiyement, SignUpView, TableauDeBordView, TypeChambreCreateView, TypeChambreDeleteView, TypeChambreListView, TypeChambreUpdateView, UserDetailView, UserListView, UserUpdateReinitialisationPasswordView, UserUpdateView, UtilisateurList_PeyementView, UtilisateurListView , VilleCreateView, VilleDeleteView, VilleListView, VilleUpdateView, QuartierCreateView, QuartierDeleteView, QuartierListView, QuartierUpdateView
# ,ChambreCreateView, ChambreDeleteView, ChambreDetailView, ChambreListView, ChambreUpdateView, LocataireCreateView, LocataireDeleteView, LocataireDetailView, LocataireListView, LocataireUpdateView, LocationCreateView, LocationDeleteView, LocationDetailView, LocationListView, LocationUpdateView, MaisonCreateView, MaisonDeleteView, MaisonListView, MaisonUpdateView, PaiementCreateView, PaiementDeleteView, PaiementDetailView, PaiementListView, PaiementUpdateView, ProprietaireCreateView, ProprietaireDeleteView, ProprietaireListView, ProprietaireUpdateView 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),  # URL pour l'inscription
    path('', CustomLoginView.as_view(), name='login'),
    path('tableau_de_bord/', TableauDeBordView.as_view(), name='tableau_de_bord'),
    path('rediriger/', RedirectionParTypeUtilisateurView.as_view(), name='rediriger_par_type'),
    path('utilisateurs/', UserListView.as_view(), name='liste_utilisateurs'),
    path('utilisateurs/<int:pk>/', UserDetailView.as_view(), name='detail_utilisateur'),
    path('utilisateurs/<int:pk>/modifier/', UserUpdateView.as_view(), name='modifier_utilisateur'),
    path('utilisateurs/<int:pk>/modifier_reset_password/', UserUpdateReinitialisationPasswordView.as_view(), name='modifier_reset_password'),
   #...existing code...
    # path('chat/', ChatView.as_view(), name='chat_page'),
    path('messagerie/messages/<int:receiver_id>/', ChatView.as_view(), name='chat_page'),
    path('messages/group/<int:maison_id>/', ChatView.as_view(), name='chat_group'),
    path('chat/messages/', MessageListView.as_view(), name='message-list'),
    # path('chat/messages/maison/<int:maison_id>/', GroupMessagesListView.as_view(), name='message-list-group'),  # Ajouté

#...existing code...
    # proprietaire 
    path('proprietaire/creer/', ProprietaireCreateView.as_view(), name='creer_proprietaire'),  # noqa: F821
    path('proprietaire/modifier/<int:pk>/', ProprietaireUpdateView.as_view(), name='modifier_proprietaire'),  # noqa: F821
    path('proprietaire/', ProprietaireListView.as_view(), name='liste_proprietaire'),  # noqa: F821
    path('proprietaire/supprimer/<int:pk>/', ProprietaireDeleteView.as_view(), name='supprimer_proprietaire'),  # noqa: F821
    path('proprietaire/<int:pk>/', ProprietaireDetailView.as_view(), name='detail_proprietaire'), 
     
    path('proprietaire_list_maison/', ProprietaireListmaisonView.as_view(), name='proprietaire_list_maison'), # URL pour la liste des propriétaires
    path('proprietaire_detail_list_maison/<int:pk>/', ProprietaireDetaimaisonlView.as_view(), name='proprietaire_detail'),  # noqa: F821
    path('proprietaires/<int:pk>/dashboard/', ProprietaireDashboardView.as_view(), name='proprietaire_dashboard'),


    # path('owner/dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),
    # path('owner/', OwnerDashboardView.as_view(), name='Pdashboard'),
    path('proprietairesPdashboard/', DashboarProprietairedView.as_view(), name='Pdashboard'),
     path('chambre/<int:chambre_id>/details/', ChambreDetailLocataireView.as_view(), name='chambre_details'),


    ################################################################### Villes ######################################################
    path('villes/', VilleListView.as_view(), name='ville_list'),
    path('add_ville/', VilleCreateView.as_view(), name='add_ville'),
    path('edit_ville/<int:pk>/', VilleUpdateView.as_view(), name='edit_ville'),
    path('delete_ville/<int:pk>/', VilleDeleteView.as_view(), name='delete_ville'),
    # ################################################################### Quatiers ######################################################
    path('Quatiers/',QuartierListView.as_view(), name='Quatiers_list'),
    path('add_Quatier/', QuartierCreateView.as_view(), name='add_Quatier'),
    path('edit_Quatier/<int:pk>/', QuartierUpdateView.as_view(), name='edit_Quatier'),
    path('delete_Quatier/<int:pk>/', QuartierDeleteView.as_view(), name='delete_Quatier'),
    # ################################################################### Maison ######################################################
    path('maison_liste', MaisonListView.as_view(), name='maison_liste'),
    path('creer/', MaisonCreateView.as_view(), name='maison_creer'),
    path('modifier/<int:pk>/', MaisonUpdateView.as_view(), name='maison_modifier'),
    path('supprimer/<int:pk>/', MaisonDeleteView.as_view(), name='maison_supprimer'),
    path('maisons/<int:pk>/', MaisonDetailView.as_view(), name='maison_detail'),

    # TypeChambre
    path('typechambre/creer/', TypeChambreCreateView.as_view(), name='creer_typechambre'),
    path('typechambre/modifier/<int:pk>/', TypeChambreUpdateView.as_view(), name='modifier_typechambre'),
    path('typechambre/', TypeChambreListView.as_view(), name='liste_typechambres'),
    path('typechambre/supprimer/<int:pk>/', TypeChambreDeleteView.as_view(), name='supprimer_typechambre'),

    # Chambre
    path('chambre/creer/', ChambreCreateView.as_view(), name='creer_chambre'),
    path('chambre/modifier/<int:pk>/', ChambreUpdateView.as_view(), name='modifier_chambre'),
    path('chambre/', ChambreListView.as_view(), name='liste_chambres'),
    path('chambre/supprimer/<int:pk>/', ChambreDeleteView.as_view(), name='supprimer_chambre'),
    path('chambre/<int:pk>/', ChambreDetailView.as_view(), name='chambre_detail'),  # noqa: F821
    
    # Location
    path('locations/creer/<int:chambre_id>/<int:utilisateur_id>/', LocationCreateView.as_view(), name='creer_location'),
    path('location/modifier/<int:pk>/', LocationUpdateView.as_view(), name='modifier_location'),
    path('location/', LocationListView.as_view(), name='liste_locations'),
    path('location/supprimer/<int:pk>/', LocationDeleteView.as_view(), name='supprimer_location'),
    path('locataire/<int:locataire_id>/dashboard/', LocataireDashboardView.as_view(), name='locataire_dashboard'),

    # PaiementLoyer
    path('paiement/creer/<int:location_id>/', PaiementLoyerCreateView.as_view(), name='creer_paiement'),
    path('paiement/ajouter/<int:location_id>/', PaiementLoyer2CreateView.as_view(), name='ajouter_paiement_loyer2'),

    # path('paiement/ajouter/<int:paiement_id>/', PaiementLoyer2CreateView.as_view(), name='ajouter_paiement_loyer2'),
    
    # path('paiement/creer/<int:utilisateur_id>/', PaiementLoyerCreateView.as_view(), name='creer_paiement'),
    path('paiement/modifier/<int:pk>/', PaiementLoyerUpdateView.as_view(), name='modifier_paiement'),
    path('paiement/', PaiementLoyerListView.as_view(), name='liste_paiements'),
    path('paiement/supprimer/<int:pk>/', PaiementLoyerDeleteView.as_view(), name='supprimer_paiement'),
    path('paiement/pdf/<int:pk>/', GeneratePDFView.as_view(),name='generer_recu_pdf'),

    
    path('fin-location/<int:location_id>/', FinLocationCreateView.as_view(), name='fin_location_create'),
    path('fin-location/<int:pk>/update/', FinLocationUpdateView.as_view(), name='fin_location_update'),
    path('utilisateur_Fin_Location/', FinLocationListView.as_view(), name='utilisateurs_parchambre'),
# URL pour afficher les paiements d'une location spécifique
    path('liste_paiements/<int:location_id>/', ListePaiementsLocationView.as_view(), name='liste_paiements'),


    path('utilisateur_payement/', UtilisateurList_PeyementView.as_view(), name='utilisateurpeyement_list'),  # noqa: F821
    path('utilisateurs_location/<int:chambre_id>/', UtilisateurListView.as_view(), name='utilisateur_list'),  # noqa: F821


# location
    path('generate-pdf/<int:location_id>/', PDFTemplateViewLocation.as_view(), name='generate_pdf'),  # noqa: F821
    path('download-pdf/', ServePDFAndRedirectViewLocation.as_view(), name='serve_pdf_and_redirect'),
    path('location/<int:location_id>/download/', Download_location_RedirectView.as_view(), name='download_and_redirect'),
# paiement
    path('generate-pdf/<int:paiementloyer_id>/', PDFTemplateViewpaiyement.as_view(), name='generate_pdfpayement'),  # noqa: F821
    path('download-pdf/', ServePDFAndRedirectViewpaiyement.as_view(), name='serve_pdf_and_redirect'),
]

# .venv\Scripts\activate     
# cd authentifications       
# python manage.py runserver