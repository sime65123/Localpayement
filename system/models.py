from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import random
import string
from django.db import models
import secrets
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import secrets

# Modèle pour les agences
class Agence(models.Model):
    adresse_agence = models.CharField(max_length=255)

    def __str__(self):
        return self.adresse_agence


# Gestionnaire personnalisé pour notre classe User personnalisée
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Les utilisateurs doivent avoir une adresse email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Classe User personnalisée
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='adresse email', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# Modèle Ticket mis à jour



# Modèle pour les clients
class Client(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    numero_telephone = models.CharField(max_length=15)
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=100, editable=False)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.matricule:
            # Génération du matricule
            dernier_client = Client.objects.filter(agence=self.agence).order_by('id').last()
            compteur = '00001' if not dernier_client else str(int(dernier_client.matricule.split('_')[-1]) + 1).zfill(5)
            self.matricule = f'CM_{self.agence.adresse_agence}_{compteur}'
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nom} ({self.matricule})'

# Modèle pour les types de lavage
class TypeL(models.Model):
    nom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom



# Votre modèle Ticket existant


class Ticket(models.Model):
    numero = models.CharField(max_length=100, null=True, blank=True, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type_lavage = models.ForeignKey(TypeL, on_delete=models.CASCADE)
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE)  # Mise à jour pour utiliser la classe User
    est_utilise = models.BooleanField(default=False)  # Nouveau champ pour suivre l'utilisation du pass

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.generate_unique_code()
        super(Ticket, self).save(*args, **kwargs)

    def generate_unique_code(self, length=5):
        # Générer une chaîne de caractères numériques aléatoires en utilisant secrets
        unique_code = ''.join(secrets.choice(string.digits) for _ in range(length))
        # Vérifier l'unicité du code généré
        while Ticket.objects.filter(numero=unique_code).exists():
            unique_code = ''.join(secrets.choice(string.digits) for _ in range(length))
        return unique_code

    def changer_etat_pass(self):
        self.est_utilise = not self.est_utilise
        self.save()

    def __str__(self):
        return f'Ticket {self.numero} - {self.client.nom}'