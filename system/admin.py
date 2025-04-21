from django.contrib import admin
from .models import Agence, Client, TypeL, Ticket, User

# Admin pour Agence
@admin.register(Agence)
class AgenceAdmin(admin.ModelAdmin):
    list_display = ('adresse_agence',)
    search_fields = ('adresse_agence',)

# Admin pour Client
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'numero_telephone', 'agence', 'matricule','date')
    search_fields = ('nom', 'matricule')
    list_filter = ('agence',)

# Admin pour TypeL
@admin.register(TypeL)
class TypeLAdmin(admin.ModelAdmin):
    list_display = ('nom', 'montant')
    search_fields = ('nom',)

# Admin pour Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('numero', 'date', 'client', 'type_lavage', 'vendeur', 'est_utilise')
    search_fields = ('numero', 'client__nom')
    list_filter = ('date', 'est_utilise')

# Admin pour User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_admin')
    search_fields = ('email',)
    list_filter = ('is_active', 'is_admin')
