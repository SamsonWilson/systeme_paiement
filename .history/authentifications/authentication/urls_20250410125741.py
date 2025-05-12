from django.urls import path
from .views import  ChambreCreateView, ChambreDeleteView, ChambreDetailView, ChambreListView, ChambreUpdateView, CustomLoginView, GeneratePDFView, LocationCreateView, LocationDeleteView, LocationListView, LocationUpdateView, MaisonCreateView, MaisonDeleteView, MaisonDetailView, MaisonListView, MaisonUpdateView, PDFTemplateView, PaiementLoyerCreateView, PaiementLoyerDeleteView, PaiementLoyerListView, PaiementLoyerUpdateView, ProprietaireCreateView, ProprietaireDeleteView, ProprietaireDetailView, ProprietaireListView, ProprietaireUpdateView, SignUpView, TableauDeBordView, TypeChambreCreateView, TypeChambreDeleteView, TypeChambreListView, TypeChambreUpdateView, UtilisateurList_PeyementView, UtilisateurListView , VilleCreateView, VilleDeleteView, VilleListView, VilleUpdateView, QuartierCreateView, QuartierDeleteView, QuartierListView, QuartierUpdateView
# ,ChambreCreateView, ChambreDeleteView, ChambreDetailView, ChambreListView, ChambreUpdateView, LocataireCreateView, LocataireDeleteView, LocataireDetailView, LocataireListView, LocataireUpdateView, LocationCreateView, LocationDeleteView, LocationDetailView, LocationListView, LocationUpdateView, MaisonCreateView, MaisonDeleteView, MaisonListView, MaisonUpdateView, PaiementCreateView, PaiementDeleteView, PaiementDetailView, PaiementListView, PaiementUpdateView, ProprietaireCreateView, ProprietaireDeleteView, ProprietaireListView, ProprietaireUpdateView 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),  # URL pour l'inscription
    path('', CustomLoginView.as_view(), name='login'),
    path('tableau_de_bord/', TableauDeBordView.as_view(), name='tableau_de_bord'),
    # proprietaire 
    path('proprietaire/creer/', ProprietaireCreateView.as_view(), name='creer_proprietaire'),  # noqa: F821
    path('proprietaire/modifier/<int:pk>/', ProprietaireUpdateView.as_view(), name='modifier_proprietaire'),  # noqa: F821
    path('proprietaire/', ProprietaireListView.as_view(), name='liste_proprietaire'),  # noqa: F821
    path('proprietaire/supprimer/<int:pk>/', ProprietaireDeleteView.as_view(), name='supprimer_proprietaire'),  # noqa: F821
    path('proprietaire/<int:pk>/', ProprietaireDetailView.as_view(), name='detail_proprietaire'),  # noqa: F821
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

    # PaiementLoyer
    path('paiement/creer/<int:location_id>/', PaiementLoyerCreateView.as_view(), name='creer_paiement'),
    # path('paiement/creer/<int:utilisateur_id>/', PaiementLoyerCreateView.as_view(), name='creer_paiement'),
    path('paiement/modifier/<int:pk>/', PaiementLoyerUpdateView.as_view(), name='modifier_paiement'),
    path('paiement/', PaiementLoyerListView.as_view(), name='liste_paiements'),
    path('paiement/supprimer/<int:pk>/', PaiementLoyerDeleteView.as_view(), name='supprimer_paiement'),
    path('paiement/pdf/<int:pk>/', GeneratePDFView.as_view(),name='generer_recu_pdf'),









    path('utilisateur_payement/', UtilisateurList_PeyementView.as_view(), name='utilisateurpeyement_list'),  # noqa: F821
    path('utilisateurs/<int:chambre_id>/', UtilisateurListView.as_view(), name='utilisateur_list'),  # noqa: F821



    path('generate-pdf/<int:location_id>/', PDFTemplateView.as_view(), name='generate_pdf'),  # noqa: F821
    path('download-pdf/', ServePDFAndRedirectView.as_view(), name='serve_pdf_and_redirect'),
]