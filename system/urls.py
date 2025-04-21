from django.urls import path
from . import views

urlpatterns = [
    path('connexion', views.connexion, name='connexion'),
    path('deconnexion', views.logout_view, name='deconnexion'),
    path('home',views.home,name='home'),
    path('ajouter-client', views.ajout_client, name='ajout_client'),
    # path('generer-facture/', views.generer_facture, name='generer_facture'),
    # path('', views.home, name='home'),
    # path(' add_customer_view/', views.add_customer_view, name='add_customer_view'),
    path('get_client',views.get_client,name='get_client'),
    
    path('deconnexion', views.logout_view, name='deconnexion'),
    path('somme_client_du_jour', views.somme_client_du_jour, name='somme_client_du_jour'),
    path('somme_souscription_du_jour', views.somme_souscription_du_jour, name='somme_souscription_du_jour'),
    path('get_ticket', views.get_ticket, name='get_ticket'),
    path('rechercher_clients', views.rechercher_clients, name='rechercher_clients'),
    path('facture', views.invoice_preview, name='generate-invoice'),
    path('create_ticket', views.create_ticket, name='create_ticket'),
    path('analytics/', views.analytics, name='analytics'),
    
    # ... vos autres URL ...
]
