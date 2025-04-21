from django import forms
from .models import Agence, Client, TypeL, Ticket, User

# Formulaire pour Agence
class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        fields = ['adresse_agence']

# Formulaire pour Client
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'adresse', 'numero_telephone', 'agence']

# Formulaire pour TypeL
class TypeLForm(forms.ModelForm):
    class Meta:
        model = TypeL
        fields = ['nom', 'montant']

# Formulaire pour Ticket
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['client', 'type_lavage', 'vendeur']
        # Le champ 'numero' est généré automatiquement et n'est pas inclus dans le formulaire.

# Formulaire pour User
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
